from nodescan_v6_2  import *

import time
import _thread as thread

import socket, struct
print(socket.AF_INET)

sock.close()
print("start")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6454))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

except socket.error as e:
    print("Socket 6454 ", "ERR: {0} ".format(e.args))
    sys.exit()

def recive():
    print("-- NODE READ LOOP START ---")
    print()
    while 1:
        data, addr = sock.recvfrom(500)
        print("\e[1;33;4;44m",end="")
        print(">>",addr,data,end="")
        print("\e[0m")
        time.sleep(0.001)

    print("-- NODE READ LOOP END ---")
    print()

#thread.start_new_thread(recive, () )
import random
x=random.randint(0,99)
sn = "ShortName"+str(x)
ln = "LongName"+str(x)

print(sn,ln)

#rx = ArtNetNodes()
#rx.loop()
#time.sleep(4)
univ = random.randint(0,16)

x=ArtAddress(ip="2.0.0.99" ,ShortName=sn, LongName=ln,Port="",Universes=univ,raw=1)
sock.sendto(x[0] ,x[1])
x=ArtAddress(ip="2.0.0.4"  ,ShortName=sn, LongName=ln,Port="",Universes=univ,raw=1)
sock.sendto(x[0] ,x[1])
x=ArtAddress(ip="2.0.0.15" ,ShortName=sn, LongName=ln,Port="",Universes=univ,raw=1)
sock.sendto(x[0] ,x[1])

time.sleep(1)
#poll()
#while 1:
#    input("ende")
