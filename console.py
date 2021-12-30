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
from collections import OrderedDict
 
import lib.chat as chat
import lib.ArtNetNode as ANN
import _thread as thread  
#thread.start_new_thread
import lib.motion as motion

#idmx = [0]*512 # incremental dmx
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
        self.artnet.send()
        xx = [0]*512
        self.artnet.dmx = xx# [:] #dmx #[0]*512
        while 1:
            t = clock.time()
            for i,dmxch in enumerate(Bdmx):
                v = dmxch.next(t)
                if i == 0:
                    if xx[i]+1 < v or xx[i]-1 > v :
                        #print("----v",x[i],v,t)
                        print("i:{:0.2f} xx:{:0.2f} v:{:0.2f} {:0.2f}----v {}".format(i,xx[i],v,t+100,dmxch))
                xx[i] = int(v)
            #artnet._test_frame()
            self.artnet.next()
            #self.artnet.send()
            time.sleep(0.01)

main = Main()
#thread.start_new_thread(artnet_loop,())
thread.start_new_thread(main.loop,())

class CLOCK():
    def __init__(self):
        self.__time = 0
        self.__start = time.time() # only for debugging
        self.__tick = 0.01 # incremental timer drift's on highe cpu load ?
    def time(self):
        return self.__time
    def get_drift(self):
        run_time = time.time() - self.__start
        tick_time = self.__time # * self.__tick
        print( "runtime:{:0.2f} tick_timer:{:0.2f} drift:{:0.2f}".format(run_time,tick_time,run_time-tick_time))
    def loop(self):
        while 1:
            self.__time +=self.__tick
            #if int(self.__time*100)/10. % 10 == 0:# self.__time % 2 == 0:
            #    print( self.get_drift())
            #print(self.__time)
            #for i in range(10):
            time.sleep(self.__tick)
clock = CLOCK()
thread.start_new_thread(clock.loop,())

class Fade():
    def __init__(self,start,target,time,clock):
        #print("init Fade ",start,target,time,clock)
        self.__clock = clock
        self.__clock_curr = clock
        self.__time = time
        self.__start = start
        self.__last = start
        self.__target = target
        print("INIT", str(self) )
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<Fade Next:{:0.2f} Start:{:0.2f} Target:{:0.2f} Clock:{:0.2f}>".format( 
                    self.next(), self.__start,self.__target,self.__clock_curr )
    def next(self,clock=None):
        if self.__time <= 0:
            self.__last = self.__target
        
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock

        if self.__target > self.__start:
            if self.__last >= self.__target:
                return self.__target
        else:
            if self.__last <= self.__target:
                return self.__target
            
        current = (self.__clock - self.__clock_curr) / self.__time
        length = self.__start - self.__target
        self.__last = self.__start+ length*current 
        return self.__last

    def ctl(self,cmd="",value=None): # if x-fade cmd="%" value=50
        # start,stop,fwd,bwd,revers
        pass

class FX():
    def __init__(self,type="sinus",size=10,speed=10,offset=0):
        pass
    def next(self):
        pass

class DMXCH(object):
    def __init__(self):
        self._value = 1
        self._fade  = None
        self._fx    = None

    def fade(self,target,time=0,clock=0):
        if target != self._value:
            self._fade = Fade(self._value,target,time=time,clock=clock)
    def fx(self,type="sinus",size=20,speed=20,offset=0):
        pass
    def fx_ctl(self,cmd=""):#start,stop,off
        pass
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        try:
            return " DMXCH {:0.2f} {:0.2f}".format( self._value,self._fade)
        except:
            return " DMXCH {:0.2f} {}".format( self._value,self._fade)
    def fade_ctl(self,cmd=""):#start,stop,backw,fwd,bounce
        pass
    def next(self,clock=0):
        if type(self._fade) is Fade:# is Fade:
            self._value = self._fade.next(clock)
        return self._value
Bdmx = []
for i in range(512):
    Bdmx.append( DMXCH() )
    #print(type(dmx[i]))

def split_cmd(data):
    if "cmd" in data:
        cmd = data["cmd"]
        #print("cmd",cmd)
        if "," in cmd:
            cmds = cmd.split(",")
        else:
            cmds = [cmd]
    return cmds



def CB(data):
    print("CB",data)

    cmds = split_cmd(data)
    c = clock.time() 
    for xcmd in cmds:
        if xcmd.startswith("d"):
            xxcmd=xcmd[1:].split(":")
            #print("DMX:",xxcmd)
            l = xxcmd
            t = 2
            try:
                k=int(l[0])-1
                v=float(l[1])
                if len(l) >= 3:
                    t=float(l[2])
                if v > 255:
                    v = 255

                if len(Bdmx) > k:
                    Bdmx[k].fade(target=v,time=t, clock=c)
            except Exception as e:
                print("EXCEPTION IN DMX",e)

chat.cmd(CB) # server listener

input("END")
