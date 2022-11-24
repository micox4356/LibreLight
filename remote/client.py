import sys
import os

sys.path.append(os.getcwd() + '/..')
import lib.zchat as chat

#print("-----")

#print(dir())
#print("-----")
#print(dir(chat))

#def JCB(x):
#    for i in x:
#        print(i)
#chat.cmd(JCB) # server listener
#s = chat.Server(port=30001)
#print("-----")
#print(dir(s))
#chat.cmd(port=30002)
#jclient = s
#
#jclient = chat.tcp_sender()#port=50001)

#import json

#jtxt = {"hi":1}
#jtxt = json.dumps(jtxt)
#jtxt = bytes(jtxt,"ascii")
#jclient.send( jtxt ) #b"\00 ")



#sys.path.append(os.getcwd() + '/..')
import time
data = "hi"
data = data.encode("utf-8")
c = chat.Client(port=30002)
client = c
time.sleep(0.05)
client.send(data)
import time
while 1:
    try:
        data = input("<")
        data = bytes(data,"utf-8")
        client.send(data)
    except Exception as e:
        print("Exc",e)
    time.sleep(0.1)
