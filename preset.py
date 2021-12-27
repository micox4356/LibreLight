


import lib.chat as chat
import time

import lib.motion as motion 

def inp():
    c = chat.tcp_sender()
    while 1:
        x = input(":: ")
        c.send(x)


fx = []
#for i in range(10):
def loop():
    c = chat.tcp_sender()
    x = 0

    fx1 = motion.Effect(size=30,speed=2500)
    fx2 = motion.Effect(TYPE="cosinus",size=30,speed=2500)
    fd1 = motion.FadeFast(start=10,target=10,fadetime=4)
    
    while 1:
        xfd1= int(fd1.next())
        #print("fd",xfd1)
        if xfd1 == 10:
            fd1 = motion.FadeFast(start=xfd1,target=200,fadetime=4)
        if xfd1 == 200:
            fd1 = motion.FadeFast(start=xfd1,target=10,fadetime=4)

        x1 = int(fx1.next(50))
        x2 = int(fx2.next(127))
        x += 3
        if x >= 255:
            x=0
        c.send("d201:{},d241:{},d243:{}".format(xfd1,x2,x1))
        time.sleep(0.051)

loop()
#inp()
