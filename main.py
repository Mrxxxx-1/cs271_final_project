import socket
import threading, time
from sys import exit
import json
import random

print("client")

usertable = {'A' : 10882, 'B' : 10884, 'C' : 10886, 'D' : 10888, 'E' : 10900} 
user = { ('192.168.0.167', 10882) : 'A', ('192.168.0.167', 10884) : 'B', ('192.168.0.167', 10886) : 'C', ('192.168.0.167', 10888) : 'D', ('192.168.0.167', 10900) : 'E'}
# outgoingchannel = {'A' : ['B'], 'B' : ['A', 'D'], 'C' : ['B'], 'D' : ['A', 'B', 'C', 'E'], 'E' : ['B', 'D']}
# snapshot = {'A' : {'Token' : False, 'B' : 'Empty', 'D' : 'Empty'}, 'B' : {'Token' : False, 'A' : 'Empty', 'C' : 'Empty', 'D' : 'Empty', 'E' : 'Empty'}, 'C' : {'Token' : False, 'D' : 'Empty'}, 'D' : {'Token' : False, 'B' : 'Empty','E' : 'Empty'}, 'E' : {'Token' : False, 'D' : 'Empty'}}
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
g_probability = 0
g_marker = 0

lock = threading.Lock()

def RECV():
    global g_token
    global g_probability
    global g_marker
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
                        # icount += 1
                        # print('Received snapshot from client %s' %(user[addr]))
                        # # print(rev)
                        # snapshot1[user[addr]] = rev
                        # if icount == 4 :
                        #     snapshot1[username] = lstatus
                        #     print('Snapshot finished, show all status below:')
                        #     for item in snapshot1 :
                        #         print(item, ':', snapshot1[item])
                        #     icount = 0
                        #     g_marker = 0
                        #     count = 0
                        #     # lstatus = snapshot[username]
                        #     for item in lstatus :
                        #         if item == 'Token' :
                        #             lstatus[item] = False
                        #         else :
                        #             lstatus[item] = 'Empty'
                        #     for item in incomingchannel1 :
                        #         incomingchannel1[item] = 0
                            # print(lstatus)
                            # print(incomingchannel1)
                else :
                    pass
                        # if g_marker == 0 :
                        #     print('Received the first MARKER from client %s' %(user[addr]))
                        #     incomingchannel1[user[addr]] = 1
                        #     lstatus['Token'] = g_token
                        #     g_marker = 1
                        #     count += 1
                        #     for item in channel :
                        #         print('Send MAKER to client %s' %(item))
                        #         # time.sleep(1)
                        #         s.sendto(data, (HOST, usertable[item]))
                            # print(count)
                            # if count == (len(lstatus)-1) :
                            #     lstatus1 = json.dumps(lstatus)
                            #     print('Send snapshot to initiator %s' %(rev['MAKER']))
                            #     s.sendto(lstatus1.encode('utf-8'), (HOST, usertable[rev['MAKER']]))
                        # else :
                        #     print('Received MARKER from client %s' %(user[addr]))
                        #     incomingchannel1[user[addr]] = 1
                        #     count += 1
                            # print(count)
                            # a = (count == (len(lstatus)-1))
                    # if count == channelnum and rev['MARKER'] != username :
                    #     lstatus1 = json.dumps(lstatus)
                    #     print('Send snapshot to initiator %s' %(rev['MARKER']))
                    #     # time.sleep(1)
                    #     s.sendto(lstatus1.encode('utf-8'), (HOST, usertable[rev['MARKER']]))
                    #     icount = 0
                    #     g_marker = 0
                    #     count = 0
                    #     for item in lstatus :
                    #         if item == 'Token' :
                    #             lstatus[item] = False
                    #         else :
                    #             lstatus[item] = 'Empty'
                    #     for item in incomingchannel1 :
                    #         incomingchannel1[item] = 0
                        # print(lstatus)
                        # print(incomingchannel1)
      except :
        if data.decode('utf-8') == 'Fail link':
            faillink[user[addr]] = 1
        if data.decode('utf-8') == 'Fix link' :
            faillink[user[addr]] = 0
                # if(random_unit(g_probability/100)) :
        if True :
            pass
                    # if (g_marker == 1) and (incomingchannel1[user[addr]] == 0) :
                    #     lstatus[user[addr]] = True
                    # print('received token from client %s' %(user[addr]))
                    # lock.acquire()
                    # g_token = True
                    # lock.release()
                    # time.sleep(2)
                    # t = random.randint(0, len(channel)-1)
                    # print('Send token to client %s \n' %(channel[t]))
                    # data = 'Token'
                    # lock.acquire()
                    # g_token = False
                    # lock.release()
                    # # time.sleep(1)
                    # s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))
        else :
            pass
                    # lock.acquire()
                    # g_token = False
                    # lock.release()
    #   print(faillink)
    #   if g_token == False:
    #       break

def UI():
    global g_token
    global g_probability
    global g_marker
    print("1. create [<client id>. . .]")
    print("2. put <dictionary id> <key> <value>")
    print("3. get <dictionary id> <key>")
    print("4. printDict <dictionary id>")
    print("5. printAll")
    print("6. failLink <dest>")
    print("7. fixLink <dest>")
    print("8. failProcess")
    # print("0. Exit application")
    while True :
        a = input("please insert command\n")
        if a == "0" :
            pass
            # flag = False
            # # to server
            # break
        elif a == "1" :
            pass
            # print('Issue token to local client')
            # lock.acquire()
            # g_token = True
            # lock.release()
            # time.sleep(2)
            # t = random.randint(0, len(channel)-1)
            # print('Send token to client %s \n' %(channel[t]))
            # data = 'Token'
            # lock.acquire()
            # g_token = False
            # lock.release()
            # # time.sleep(1)
            # s.sendto(data.encode('utf-8'), (HOST, usertable[channel[t]]))


        elif a == "2" :
            pass
            # print('Initiating a Snapshot')
            # snapshot1 = snapshot
            # snapshot1[username]['Token'] = g_token
            # # print(snapshot)
            # data2 = {}
            # data2['MARKER'] = username
            # data22 = json.dumps(data2)
            # g_marker = 1
            # for item in channel :
            #     print('Send MAKER to client %s' %(item))
            #     # time.sleep(1)
            #     s.sendto(data22.encode('utf-8'), (HOST, usertable[item]))


        elif a == "3" :
            pass
            # g_probability = input('Please enter token loss probability\n')
            # g_probability = float(g_probability)
            # print('Now client has a %.1f %% chance of losing the token' %(g_probability))
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
            break
        time.sleep(1)

def sendreq(data, dest) :
    if faillink[dest] == 0: 
            s.sendto(data.encode('utf-8'), (HOST, usertable[dest]))
    else :
        print("Unable to connect to process %s" %(dest))


t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()
t1.join()
t2.join()