import sys
import os

sys.path.append(os.getcwd() + '/..')
import lib.zchat as chat

print("-----")

print(dir())
print("-----+")
print(dir(chat))
import time
def JCB(x):
    for i in x:
        v = x[i]
        print(round(time.time(),0),"x",i,v)
#chat.cmd(JCB) # server listener

if 0:
    s = chat.Server(port=30002)
    #print("-----")
    print(dir(s))
    import time
    while 1:
        x = s.poll()
        a = s.get_clients()
        print(a)
        #if x:
        #    pass#
        #
        #print(time.time(),x)
        time.sleep(0.1)
#chat.cmd(port=30002) # SERVER
chat.cmd(JCB,port=30002) # SERVER
#jclient = s
#
#jclient = chat.tcp_sender()#port=50001)

import json

#jtxt = {"hi":1}
#jtxt = json.dumps(jtxt)
#jtxt = bytes(jtxt,"ascii")
#jclient.send( jtxt ) #b"\00 ")

