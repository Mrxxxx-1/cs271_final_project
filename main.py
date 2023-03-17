import socket
import threading, time
from sys import exit
import json
import random

print("client")

usertable = {'A' : 10882, 'B' : 10884, 'C' : 10886, 'D' : 10888, 'E' : 10900} 
user = { ('192.168.0.167', 10882) : 'A', ('192.168.0.167', 10884) : 'B', ('192.168.0.167', 10886) : 'C', ('192.168.0.167', 10888) : 'D', ('192.168.0.167', 10900) : 'E'}
faillink = {'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    username = input("Please input your username : ")
    if usertable.get(username) == None :
        print("wrong username!")
        continue
    break

PORT = usertable[username]
HOST = '192.168.0.167'
s.bind((HOST, PORT))


g_token = True

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
                # if(random_unit(g_probability/100)) :
        if True :
            pass
        else :
            pass


def UI():
    global g_token
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
            pass
        elif a == "2" :
            pass
        elif a == "3" :
            pass
        elif a == '4' :
            pass
        elif a == '5' :
            pass
        elif a == '6' :
            dest = input('Please enter the dest process\n')
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