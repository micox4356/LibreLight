import sys
import os

sys.path.append(os.getcwd() + '/..')
import lib.zchat as chat

print("-----")

print(dir())
print("-----")
print(dir(chat))

def JCB(x):
    for i in x:
        print(i)
#chat.cmd(JCB) # server listener
#s = chat.Server(port=30001)
#print("-----")
#print(dir(s))
chat.cmd(port=30002) # SERVER
#jclient = s
#
#jclient = chat.tcp_sender()#port=50001)

import json

#jtxt = {"hi":1}
#jtxt = json.dumps(jtxt)
#jtxt = bytes(jtxt,"ascii")
#jclient.send( jtxt ) #b"\00 ")

