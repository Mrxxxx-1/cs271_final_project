import socket
import threading, time
from sys import exit
import json
from dictionary import *

print("client")

usertable = {1 : 10882, 2 : 10884, 3 : 10886, 4 : 10888, 5 : 10900} 
user = { ('192.168.0.167', 10882) : 1, ('192.168.0.167', 10884) : 2, ('192.168.0.167', 10886) : 3, ('192.168.0.167', 10888) : 4, ('192.168.0.167', 10900) : 5}
faillink = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
usertable2 = {1 : 10782, 2 : 10784, 3 : 10786, 4 : 10788, 5 : 10700}

while True :
    username = input("Please input your username : ")
    username = int(username)
    if usertable.get(username) == None :
        print("wrong username!")
        continue
    break

PORT = usertable[username]
HOST = '192.168.0.167'
s.bind((HOST, PORT))


def read_dic_id():
    with open("keys/"+ str(username) +"/my_dic.txt", "r") as file:
        dic_list = [line.strip() for line in file.readlines()]
    return dic_list
    

def write_dic_id():
    with open("keys/"+ str(username) +"/my_dic.txt", "w") as file:
        for item in g_dictionary:
            file.write(item + "\n")
    pass

g_token = True
g_dictionary = []
g_dictionary = read_dic_id()


lock = threading.Lock()

def RECV():
    global g_token
    count = 0
    icount = 0 
    while g_token:
      try:
        (data, addr) = s.recvfrom(1024)
      except ConnectionResetError:
        print("Unable to connect to process")
        continue
      time.sleep(3)
      try :
            if isinstance(json.loads(data.decode('utf-8')), dict) :
                rev = {}
                rev = json.loads(data.decode('utf-8'))
                if 'Token' in rev :
                    pass
                else :
                    pass
      except :
        if data.decode('utf-8') == 'Fail link':
            faillink[user[addr]] = 1
        if data.decode('utf-8') == 'Fix link' :
            faillink[user[addr]] = 0
        if True :
            pass
        else :
            pass


def UI():
    global g_token
    global g_dictionary
    counter = 11
    print("1. create [<client id>. . .]")
    print("2. put <dictionary id> <key> <value>")
    print("3. get <dictionary id> <key>")
    print("4. printDict <dictionary id>")
    print("5. printAll")
    print("6. failLink <dest>")
    print("7. fixLink <dest>")
    print("8. failProcess")
    while True :
        a = input("please insert command\n")
        if a == "0" :
            pass
        elif a == "1" :
            input_str = input("Enter a list of dictionary members separated by commas: ")
            clientlist = input_str.split(",")
            print("Your list of values is:", clientlist)
            dic = Dictionary(clientlist, counter, username)
            dic.commit_log_entry()
            log = dic.log_entry
            dic_file = {
                'id' : log['dic_id'],
                'members' : log['members']
            }
            counter += 1
            # write dictionary to the file
            # public_key = load_public_key(username, log['dic_id'])
            # dic_file = json.dumps(dic_file)
            # encrypt_dic = encrypt_message(dic_file, public_key)
            dic_write(dic_file, log['dic_id'], str(username))
            g_dictionary.append(str(log['dic_id']))
            write_dic_id()
            # with open("keys/"+ str(username) +"/my_dic.txt", "w") as file:
            #     for item in g_dictionary:
            #         file.write(item + "\n")
            # print(type(encrypt_dic))
            # print(encrypt_dic)
            pass
        elif a == "2" :
            input_str = input('Enter <dictionary id> <key> <value>:')
            parameter = input_str.split(' ')
            print(parameter)
            data = {}
            data[parameter[1]] = parameter[2]
            public_key = load_public_key(username, parameter[0])
            data = json.dumps(data)
            encrypt_data = encrypt_message(data, public_key)
            message = {
                'from': username,
                'type': 'put',
                'dic_id': parameter[0],
                'data': encrypt_data,
            }
            dic = {}
            dic = dic_read(message['dic_id'], str(username))
            dic[parameter[1]] = parameter[2]
            dic_write(dic, parameter[0], str(username))
            pass
        elif a == "3" :
            input_str = input('Enter <dictionary id> <key>:')
            parameter = input_str.split(' ')
            print(parameter)
            data = parameter[1]
            public_key = load_public_key(username, parameter[0])
            encrypt_data = encrypt_message(data, public_key)
            message = {
                'from': username,
                'type': 'get',
                'dic_id': parameter[0],
                'data': encrypt_data,
            }
            data = {}
            data = dic_read(message['dic_id'], str(username))
            key = data[parameter[1]]
            print('%s : %s read from dictionary %s' %(parameter[1], key, parameter[0]))           
            pass
        elif a == '4' :
            dic_id = input('Enter <dictionary id>')
            print(dic_read(dic_id, str(username)))
            pass
        elif a == '5' :
            print('all dictionaries local client is a member of:')
            print(g_dictionary)
            pass
        elif a == '6' :
            dest = input('Please enter the dest process\n')
            dest = int(dest)
            if usertable.get(dest) == None or dest == username :
                print("wrong dest process!")
                continue
            data = 'Fail link'
            sendreq(data, dest)
            faillink[dest] = 1
            # s.sendto(data.encode('utf-8'), (HOST, usertable[dest]))
            print('Fail link %s\n' %(dest))
            # print(faillink)
            pass
        elif a =='7' :
            dest = input('Please enter the dest process\n')
            dest = int(dest)
            if usertable.get(dest) == None or dest == username :
                print("wrong dest process!")
                continue
            data = 'Fix link'
            faillink[dest] = 0
            sendreq(data, dest)
            # s.sendto(data.encode('utf-8'), (HOST, usertable[dest]))
            print('Fix link %s' %(dest))
            pass
        elif a == '8' :
            g_token = False
            print('Fail process %s' %(username))
            data = 'Stop'
            s.sendto(data.encode('utf-8'), (HOST, usertable[username]))
            break
        time.sleep(1)

def sendreq(data, dest) :
    if faillink[dest] == 0: 
            s.sendto(data.encode('utf-8'), (HOST, usertable[dest]))
    else :
        print("Unable to connect to process %s" %(dest))




n = 0

t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()

t2.join()
n = n + 1
t1.join()
n = n + 1

while True:
    if n == 2:
        while True :
            command = input("Please input Y to restart the process : ")
            if command != 'Y' :
                print("wrong command!")
                continue
            n = 0
            t1 = threading.Thread(target=RECV)
            t2 = threading.Thread(target=UI)
            t1.start()
            t2.start()

            t2.join()
            n = n + 1
            t1.join()
            n = n + 1
            break 
    time.sleep(1)