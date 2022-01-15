#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is part of LibreLight.

LibreLight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

LibreLight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LibreLight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""
import sys
if "__file__" in dir():
    sys.stdout.write("\x1b]2;"+str(__file__)+"\x07") # terminal title
else:
    sys.stdout.write("\x1b]2;"+str("__file__")+"\x07") # terminal title

import time
import socket
import struct
import sys
import random
import math

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
                    if int(xx[i]*100) != int( v*100):
                        #print("----v",x[i],v,t)
                        pass
                        #print("i:{:0.2f} xx:{:0.2f} v:{:0.2f} {:0.2f}----v {}".format(i,xx[i],v,t+100,dmxch))
                        #print("i:{:0.2f} xx:{:0.2f} v:{:0.2f} {:0.2f}----v {}".format(i,xx[i],v,t+100,dmxch))
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
    def __init__(self,start,target,time,clock,delay=0):
        #print("init Fade ",start,target,time,clock)
        if delay < 0:
            delay = 0.0001
        if time <= 0:
            time = 0.0001
        clock += delay
        self.__delay = delay
        self.__clock = clock 
        self.__clock_curr = clock 
        self.__time = time
        self.__start = start
        self.__last = start
        self.__target = target
        self.run = 1
        #print("INIT", str(self) )
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<Fade Next:{:0.2f} Start:{:0.2f} Target:{:0.2f} T{:0.2f} Clock:{:0.2f} run:{} delay:{:0.2f}>".format( 
                    self.__last, self.__start,self.__target,self.__time,self.__clock_curr,self.run,self.__delay )
    def next(self,clock=None):
        if self.__time <= 0 and self.__delay <= 0:
            self.__last = self.__target
            self.run = 0
        
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock

        if self.__target > self.__start:
            if self.__last >= self.__target:
                self.run = 0
                return self.__target
        else:
            if self.__last <= self.__target:
                self.run = 0
                return self.__target
            
        current = (self.__clock - self.__clock_curr) / self.__time
        length = self.__start - self.__target
        self.__last = self.__start+ length*current 
        #if self.__last < 0:
        #    self.__last = 0
        #if self.__last > 255:
        #    self.__last = 255
        self.run = 1
        return self.__last

    def ctl(self,cmd="",value=None): # if x-fade cmd="%" value=50
        # start,stop,fwd,bwd,revers
        pass

class FX():
    def __init__(self,xtype="sinus",size=10,speed=10,start=0,offset=0,base="",clock=0):
        self.__xtype=xtype
        self.__size  = size
        self.__start = start
        self.__base = base
        self.__speed = speed
        self.__offset = offset
        self.__clock = clock
        self.__clock_curr = clock
        self.run = 1
        self.__angel = self.__clock_curr*360%360
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<FX Next:{:0.2f} xtype:{} Size:{:0.2f} Speed:{:0.2f} ang:{:0.2f} base:{} Clock:{:0.2f} run:{}>".format( 
                    self.next(),self.__xtype, self.__size,self.__speed,self.__angel, self.__base,self.__clock_curr,self.run )
    def next(self,clock=None):
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock
        t = self.__clock_curr  * self.__speed / 255
        t += self.__offset / 1024 #255
        t += self.__start / 1024 #255
        self.__angel = t%1*360 #self.__clock_curr%1 #*360%360
        t = t%1
        rad = math.radians(self.__angel)

        base = 0
        if self.__base == "+": # add
            base = self.__size
        elif self.__base == "-": # sub
            base = self.__size*-1

        # todo start angle 20°
        # todo width angle 90°

        #print("{:0.2f} {:0.2f} {:0.2f} {:0.2f}".format(self.__angel ,self.__clock_curr,self.__angel ,math.sin(rad) ) )
        if self.__xtype == "sinus":
            return math.sin( rad ) * self.__size/2 + base/2
        elif self.__xtype == "cosinus":
            return math.cos( rad ) * self.__size/2 + base/2
        elif self.__xtype == "on2":
            out = self.__size/2
            if self.__angel > 90 and self.__angel <=270:
                out *=-1
            out += base/2
            print("ON {:0.2f} {:0.2f} {:0.2f} {:0.2f}".format(out,t,0,self.__angel, base))
            return out 
        elif self.__xtype == "on":
            out = self.__size/2
            if self.__angel > 90 and self.__angel <=270:
                pass
            else:
                out *=-1
            out += base/2
            return out 
        elif self.__xtype == "bump":
            out = 0 
            if self.__base == "-": # sub
                out = (t%1-1) * self.__size 
            elif self.__base == "+": # sub
                out = (t%1) * self.__size 
            else:
                out = (t%1-0.5) * self.__size 
            #print("bump",out)
            return out
        elif self.__xtype == "bump2":
            out = 0 
            if self.__base == "+": # sub
                out = (t%1-1) * (self.__size *-1) 
            elif self.__base == "-": # sub
                out = (t%1) * (self.__size *-1)
            else:
                out = (t%1-0.5) * (self.__size *-1)
            #print("bump",out)
            return out
        elif self.__xtype == "fade":
            x = t * 2 
            if x > 1:
                x = 2-x 
            x -= 0.5
            out = x * self.__size + base/2
            #print("FADE {:0.2f} {:0.2f} {:0.2f} {:0.2f}".format(out,t,x,self.__angel, base))
            return out
        else:
            return 0

class DMXCH(object):
    def __init__(self):
        self._base_value = 0
        self._fade  = None
        self._fx    = None
        self._fx_value = 0

        self._flush    = None
        self._flush_fx = None
        self._flush_fx_value = 0
        self._last_val = None
    def fade(self,target,time=0,clock=0,delay=0):
        if target != self._base_value:
            try:
                target = float(target)
                self._fade = Fade(self._base_value,target,time=time,clock=clock,delay=delay)
                #self._fade.next()
                #self._fade.next()
            except Exception as e:
                print( "Except:fade",e,target,time,clock)
    def fx(self,xtype="sinus",size=40,speed=40,start=0,offset=0,base="", clock=0):
        if str(xtype).lower() == "off":
            #self._fx = Fade(self._fx_value,target=0,time=2,clock=clock) 
            self._fx = None
            self._fx_value = 0 
        else:
            self._fx = FX(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=clock)
    def flush(self,target,time=0,clock=0,delay=0):
        if str(target).lower() == "off":
            self._flush = None
        else:#elif target != self._base_value:
            try:
                target = float(target)
                self._flush = Fade(self._last_val,target,time=time,clock=clock,delay=delay)
            except Exception as e:
                print( "Except:flush",target,time,clock,__name__,e,)
    def flush_fx(self,xtype="sinus",size=40,speed=40,start=0,offset=0,base="",clock=0):
        if str(xtype).lower() == "off":
            #self._fx = Fade(self._fx_value,target=0,time=2,clock=clock) 
            self._flush_fx = None
            self._flush_fx_value = 0 
        else:
            self._flush_fx = FX(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=clock)

    def fx_ctl(self,cmd=""):#start,stop,off
        pass
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "< DMXCH {:0.2f} > \n{}\n {}".format( self._last_val,self._fx,self._fade)
    def fade_ctl(self,cmd=""):#start,stop,backw,fwd,bounce
        pass
    def next(self,clock=0):
        value = self._base_value
        if self._last_val is None:
            self._last_val = value
        fx_value = self._fx_value

        if self._flush is not None:
            value = self._flush.next(clock)
            #flicker bug ?!
            value = self._flush.next(clock)
            fx_value = 0
        elif self._fade is not None:#is Fade:# is Fade:
            self._base_value = self._fade.next(clock)
            #flicker bug ?!
            self._base_value = self._fade.next(clock)
            value = self._base_value

        
        if self._flush_fx is not None:# is FX:
            fx_value = self._flush_fx.next(clock)
        elif self._fx is not None and self._flush is None:# is FX:
            self._fx_value = self._fx.next(clock)
            fx_value = self._fx_value

        self._last_val = value+fx_value
        return self._last_val
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
    #print("CB",data)

    cmds = split_cmd(data)
    c = clock.time() 
    c = float(c)
    time = 0
    delay = 0

    for xcmd in cmds:
        if xcmd.startswith("df"):
            xxcmd=xcmd[2:].split(":")
            #print("DMX:",xxcmd)
            if len(xxcmd) < 2:
                print("cmd err df",xcmd)
                continue
            if "alloff" == xxcmd[1].lower():
                for i in Bdmx:
                    if i is not None:
                        i.flush(target="off",clock=c)
                continue
            l = xxcmd
            try:
                k=int(l[0])-1
                v=l[1]
                
                if len(l) >= 3:
                    time=float(l[2])
                #if v > 255:
                #    v = 255
                if len(l) >= 3:
                    try:time=float(l[2])
                    except:print("ERR","time",xcmd)
                if len(l) >= 4:
                    try:delay=float(l[3])
                    except:print("ERR","delay",xcmd)

                if len(Bdmx) > k:
                    Bdmx[k].flush(target=v,time=time, clock=c,delay=delay)
            except Exception as e:
                print("EXCEPTION IN FADE",e)
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        elif xcmd.startswith("d"):
            xxcmd=xcmd[1:].split(":")
            #print("DMX:",xxcmd)
            l = xxcmd
            try:
                k=int(l[0])-1
                v=l[1]
                if len(l) >= 3:
                    time=float(l[2])
                #if v > 255:
                #    v = 255
                if len(l) >= 3:
                    try:time=float(l[2])
                    except:pass
                if len(l) >= 4:
                    try:delay=float(l[3])
                    except:pass

                if len(Bdmx) > k:
                    Bdmx[k].fade(target=v,time=time, clock=c,delay=delay)
            except Exception as e:
                print("EXCEPTION IN FADE",e)
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        elif xcmd.startswith("fxf"):
            #print("fxf:",xxcmd)
            if "alloff" == xxcmd[1].lower():
                for i in Bdmx:
                    if i is not None:
                        i.flush_fx(xtype="off",clock=c)
            l = xxcmd
            try:
                xtype=""
                size=40
                speed=100
                start=0
                offset=0
                base=""
                k=int(l[0])-1
                xtype=l[1]
                if len(l) >= 3:
                    try:size=int(l[2])
                    except:pass
                if len(l) >= 4:
                    try:speed=int(l[3])
                    except:pass
                if len(l) >= 5:
                    try:start=int(l[4])
                    except:pass
                if len(l) >= 6:
                    try:offset=int(l[5])
                    except:pass
                if len(l) >= 7:
                    try:base=l[6]
                    except:pass
                
                if len(Bdmx) > k:
                    #Bdmx[k].fade(target=v,time=t, clock=c)
                    Bdmx[k].flush_fx(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=c)
            except Exception as e:
                print("EXCEPTION IN FX",e)
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        elif xcmd.startswith("fx"):
            xxcmd=xcmd[2:].split(":")
            print("DMX:",xxcmd)
            if len(xxcmd) < 2:
                print("xxcmd err",xxcmd,xcmd)
                continue  
            if "alloff" == xxcmd[1].lower():
                for i in Bdmx:
                    i.fx(xtype="off",clock=c)
            l = xxcmd
            try:
                xtype=""
                size=40
                speed=100
                start=0
                offset=0
                base=""

                k=int(l[0])-1
                xtype=l[1]
                if len(l) >= 3:
                    try:size=int(l[2])
                    except:pass
                if len(l) >= 4:
                    try:speed=int(l[3])
                    except:pass
                if len(l) >= 5:
                    try:start=int(l[4])
                    except:pass
                if len(l) >= 6:
                    try:offset=int(l[5])
                    except:pass
                if len(l) >= 7:
                    try:base=l[6]
                    except:pass
                
                if len(Bdmx) > k:
                    #Bdmx[k].fade(target=v,time=t, clock=c)
                    Bdmx[k].fx(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=c)
            except Exception as e:
                print("EXCEPTION IN FX",xcmd,e)
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))


chat.cmd(CB) # server listener

input("END")
