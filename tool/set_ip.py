import nodescan_v6_2 as n
import socket

import time
import socket, struct
import sys
import _thread as thread
import copy
import random

sys.stdout.write("\x1b]2;Nodescan\x07")
if 0:
    print(socket.AF_INET)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 6454))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error as e:
        print("Socket 6454 ", "ERR: {0} ".format(e.args))
        sys.exit()
        
        
        
    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock2.bind(('', 6455))
        sock2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error as e:
        print("Socket2 6454 ", "ERR: {0} ".format(e.args))
        sys.exit()


    print(socket.AF_INET)
    sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 


print(dir(n))

def loop():
    print("-- NODE SCAN START ---")
    print()
    while 1:
        data, addr = sock.recvfrom(500)
        new_node = ArtNet_decode_pollreplay( data )            
        print("rvc loop",addr)
        if new_node:
            print("rcv",new_node)
            #self.add(new_node)
        time.sleep(0.001)
    print("-- NODE SCAN STOP ---")
    print()
#192.168.0.91

import time
import _thread as thread

#thread.start_new_thread(loop, () )

time.sleep(2)

n.set_ip4(cur_ip=(192,168,0,91),new_ip=(2,0,0,201),new_netmask=(255,0,0,0) )




