#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is part of grandPA.

grandPA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

grandPA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with grandPA.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""

import time
import socket
import struct
import random
 
import lib.chat as chat
import lib.ArtNetNode as ANN
import _thread as thread  
#thread.start_new_thread

idmx = [0]*512 # incremental dmx
dmx  = [0]*512 # absolute dmx data

def artnet_loop():
    #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=12)
    #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=0)
    artnet = ANN.ArtNetNode(to="10.10.10.255",univ=0)
    #artnet = ANN.ArtNetNode(to="2.0.0.255",univ=0)
    #artnet = ANN.ArtNetNode(to="10.10.10.255",univ=1)
    dmx[205] = 255 #205 BLUE
    artnet.dmx= dmx #[0]*512
    artnet.send()
    while 1:
        #artnet._test_frame()
        artnet.next()
        time.sleep(0.01)

class Main():
    def __init__(self):
        #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=12)
        #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=0)
        #artnet = ANN.ArtNetNode(to="2.0.0.255",univ=0)
        #artnet = ANN.ArtNetNode(to="10.10.10.255",univ=1)
        self.artnet = ANN.ArtNetNode(to="10.10.10.255",univ=0)
        self.fx = {} # key is dmx address
    def loop(self):
        #dmx[205] = 255 #205 BLUE
        self.artnet.dmx= dmx #[0]*512
        self.artnet.send()
        while 1:
            #artnet._test_frame()
            self.artnet.next()
            time.sleep(0.01)

main = Main()
#thread.start_new_thread(artnet_loop,())
thread.start_new_thread(main.loop,())

def split_cmd(data):
    if "cmd" in data:
        cmd = data["cmd"]
        print("cmd",cmd)
        if "," in cmd:
            cmds = cmd.split(",")
        else:
            cmds = [cmd]
    return cmds



def CB(data):
    print("CB",data)

    cmds = split_cmd(data)
    
    for xcmd in cmds:
        if xcmd.startswith("d"):
            xxcmd=xcmd[1:].split(":")
            print("DMX:",xxcmd)
            l = xxcmd
            try:
                k=int(l[0])-1
                v=int(l[1])
                if v > 255:
                    v = 255

                if len(dmx) > k:
                    dmx[k] = v
            except Exception as e:
                print("EXCEPTION IN DMX",e)

chat.cmd(CB) # server listener

input("END")
