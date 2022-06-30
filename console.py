#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is part of LibreLight.

LibreLight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

LibreLight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LibreLight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha@uxsrv.de
"""
import sys
rnd_id = ""
rnd_id += " Beta 22.02 "
import subprocess
rnd_id += subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

if "__file__" in dir():
    sys.stdout.write("\x1b]2;"+str(__file__)+" "+rnd_id+"\x07") # terminal title
else:
    sys.stdout.write("\x1b]2;"+str("__file__")+" "+rnd_if+"\x07") # terminal title

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

gcolor = 1
def cprint(*text,color="blue",space=" ",end="\n"):
    #return 0 #disable print dbg
    if not gcolor:
        print(text)
        return 0

    if color == "green":
        txt = '\033[92m'
    elif color == "red":
        txt = '\033[0;31m\033[1m'
    elif color == "yellow":
        txt = '\033[93m\033[1m'
    elif color == "cyan":
        txt = '\033[96m'
    else:
        txt = '\033[94m'
    for t in text:
        txt += str(t ) +" "
    #HEADER = '\033[95m'
    #OKBLUE = '\033[94m'
    #OKCYAN = '\033[96m'
    #OKGREEN = '\033[92m'
    #WARNING = '\033[93m'
    #FAIL = '\033[91m'
    #ENDC = '\033[0m'
    #BOLD = '\033[1m'
    #UNDERLINE = '\033[4m'
    txt += '\033[0m'
    print(txt,end=end)
    #return txt

def artnet_loop():
    #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=12)
    #artnet = ANN.ArtNetNode(to="127.0.0.1",port=6555,univ=0)
    artnet = ANN.ArtNetNode(to="10.10.10.255",univ=0)
    #artnet = ANN.ArtNetNode(to="2.0.0.255",univ=0)
    #artnet = ANN.ArtNetNode(to="10.10.10.255",univ=1)
    #dmx[205] = 255 #205 BLUE
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
        self.artnet = {}
        #self.artnet["0"] = ANN.ArtNetNode(to="10.10.10.255",univ=0)
        #self.artnet["0"].dmx[512-1] = 10
        #self.artnet["1"] = ANN.ArtNetNode(to="10.10.10.255",univ=1)
        #self.artnet["1"].dmx[512-1] = 11
        self.fx = {} # key is dmx address
    def loop(self):
        #dmx[205] = 255 #205 BLUE
        #self.artnet.send()
        xx = [0]*512
        #artnet = self.artnet["0"]
        #artnet.dmx = xx# [:] #dmx #[0]*512
        old_univ = -1
        while 1:
            t = clock.time()
            ii = 0
            for ii,dmxch in enumerate(Bdmx):
                i = ii%512
                univ = ii//512
                if str(univ) not in self.artnet:
                    print("add uiv",univ)
                    self.artnet[str(univ)] = ANN.ArtNetNode(to="10.10.10.255",univ=univ)
                    self.artnet[str(univ)].dmx[512-1] = 100+univ

                if univ != old_univ:
                    old_univ = univ
                    #print("UNIV",ii/512)
                    try:
                        artnet.next()
                    except:pass
                    artnet = self.artnet[str(univ)]
                    artnet.dmx = xx
                
                v = dmxch.next(t)
                if i == 0:
                    #print(dmxch)
                    if int(xx[i]*100) != int( v*100):
                        #print("----v",x[i],v,t)
                        pass
                        #print("i:{:0.2f} xx:{:0.2f} v:{:0.2f} {:0.2f}----v {}".format(i,xx[i],v,t+100,dmxch))
                        #print("i:{:0.2f} xx:{:0.2f} v:{:0.2f} {:0.2f}----v {}".format(i,xx[i],v,t+100,dmxch))
                xx[i] = int(v)
            try:    
                artnet.next()
            except:pass
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
class CLOCK_REAL():
    def __init__(self):
        self.__time = 0
        self.__start = time.time() # only for debugging
        self.__tick = 0.01 # incremental timer drift's on highe cpu load ?
    def time(self):
        self.__time = time.time()
        return self.__time
    def get_drift(self):
        run_time = time.time() - self.__start
        tick_time = self.__time # * self.__tick
        print( "runtime:{:0.2f} tick_timer:{:0.2f} drift:{:0.2f}".format(run_time,tick_time,run_time-tick_time))
    def loop(self):
        pass
#clock = CLOCK()
clock = CLOCK_REAL()
thread.start_new_thread(clock.loop,())

class Fade():
    def __init__(self,start,target,ftime,clock,delay=0):
        #print("init Fade ",start,target,ftime,clock)
        if delay < 0:
            delay = 0.0001
        if ftime <= 0:
            ftime = 0.0001
        clock += delay
        self.__delay = delay
        self.__clock = clock 
        self.__clock_curr = clock 
        self.__ftime = ftime
        self.__start = start
        self.__last = start
        self.__target = target
        self.run = 1
        #print("INIT", str(self) )
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<Fade Next:{:0.2f} Start:{:0.2f} Target:{:0.2f} T{:0.2f} Clock:{:0.2f} run:{} delay:{:0.2f}>".format( 
                    self.__last, self.__start,self.__target,self.__ftime,self.__clock_curr,self.run,self.__delay )
    def next(self,clock=None):
        if self.__ftime <= 0 and self.__delay <= 0:
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
            
        current = (self.__clock - self.__clock_curr) / self.__ftime
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

class MASTER_FX():
    def __init__(self):
        cprint(self,"MASTER_FX INIT !",color="green")

        self.__data = []
        self.__ok = []
        self.i=0
        self.old_offsets = []
        self.offsets = []
        self.count = -1
        self.init = 10
    def add(self,fx):
        if fx not in self.__data:
            #cprint(self,"ADD TO MASTER !",color="green")
            self.__data.append(fx)
            info = fx._get_info()
            cprint(self,"ADD" ,info,color="green")
            offset = 0
            if "offset" in info:
                offset = info["offset"]
            self.old_offsets.append(offset)
            self.offsets.append(offset)
            if "xtype" in info:
                if info["xtype"] == "rnd":
                    self._shuffle()
                    #self.init += 1
            
    def _shuffle(self):
        #cprint(self,"REORDER RANDOM !",color="green")
        #self.init = 0

        #cprint(self.old_offsets)
        random.shuffle(self.old_offsets)
        #cprint(self.old_offsets)
    def _init(self):
        self._shuffle()
        #self.offsets = []
        for i,v in enumerate(self.old_offsets):
            offset = self.old_offsets[i]
            self.offsets[i] =  offset
        self.init = 0
    def next(self,child):
        i = self.__data.index(child)
        offset = self.old_offsets[i]
        self.offsets[i] =  offset
        return offset
        #for i,v in enumerate(self.old_offsets):
        #    offset = self.old_offsets[i]
        #    self.offsets[i] =  offset


    def get(self,child,count):

        offset = 0

        if child not in self.__data:
            return offset

        if self.init:
            self._init()

        idx = self.__data.index(child) 
        if (self.count != count and idx == 0 ) or  self.init == 0:
            self.init = 1
            self._shuffle()
            #print( count)
            self.count=count
            

        idx = self.__data.index(child) 
        offset = self.offsets[idx]

        return offset
        

class FX():
    def __init__(self,xtype="sinus",size=10,speed=10,invert=0,width=100,start=0,offset=0,base="",clock=0,master=None):
        self.__xtype=xtype
        self.__size  = size
        self.__start = start
        if width > 200:
            width = 200
        if width <= 0:
            width = 1
        self.__width = width
        self.__invert = invert
        self.__base = base
        self.__speed = speed
        self.__offset = offset
        self.__clock = clock
        self.__clock_curr = clock
        self.out = 0
        self.old_v = -1
        self.run = 1
        self.count = -1
        self.__angel = self.__clock_curr*360%360
        if master is None:
            cprint(master, "MASTER_FX ERR",master,color="red")
            self.__master = MASTER_FX()
            self.__master.add(self)
        else:
            cprint( "MASTER_FX OK",master,color="red")
            self.__master = master
            self.__master.add(self)
        if self.__xtype == "rnd":
            self.__offset = self.__master.get(self,-2)
            self.__offset = self.__master.next(self)#,count)
        print("init FX",self)
    def _get_info(self):
        print(self.__offset)
        return {"offset":self.__offset,"xtype":self.__xtype}
        #return self.next(),self.__xtype, self.__size,self.__speed,self.__angel, self.__base,self.__clock_curr,self.run 
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<FX Next:{:0.2f} xtype:{} Size:{:0.2f} Speed:{:0.2f} ang:{:0.2f} base:{} Clock:{:0.2f} run:{}>".format( 
                    self.next(),self.__xtype, self.__size,self.__speed,self.__angel, self.__base,self.__clock_curr,self.run )
    def next(self,clock=None):
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock
        t = self.__clock_curr  * self.__speed / 60
        t += self.__offset / 100 #255 #1024 #255
        t += self.__start  / 1024 #255
        tw = t%1
        count = t//1
        t = t * (100/self.__width)
        if tw > self.__width/100:
            t = 1 
        
        self.__angel = t%1*360 
        t = t%1
        rad = math.radians(self.__angel)

        v=0
        out = 0
        base = 0
        size = self.__size

        if self.__base == "+": # add
            base = size/2
        elif self.__base == "-": # sub
            base = size/2*-1

        if self.__xtype == "sinus":
            v = math.sin( rad )
            v/=2
        elif self.__xtype == "cosinus":
            v = math.cos( rad )
            if self.__base == "+": # add
                size *= -1

            v/=2
        elif self.__xtype == "rnd":
            #base = 0
            if self.__angel > 90 and self.__angel <=270:
                v=1
            else:
                v=0
            #if count != self.count and v: # % 2 == 0:#!= self.count:
            #    #self.__offset = random.randint(0,1024)# /1024
            #    self.__master._shuffle()
            
            if count != self.count and v == 0: # and v: # % 2 == 0:#!= self.count:
                 self.__master.next(self)#,count)
            #self.__master.next(self)#,count)
            self.__offset = self.__master.get(self,count)
                
            base = 0
            if self.__base == "-": # sub
                if self.__invert:
                    v = 1-v
                    #base = -size
                    size *=-1
                v *=-1
            elif self.__base == "+": # sub
                if self.__invert:
                    v = v-1
            else:
                v = (t%1-0.5)
        elif self.__xtype == "on":
            #base = 0
            if self.__angel > 90 and self.__angel <=270:
                v=1
            else:
                v=0
            base = 0
            if self.__base == "-": # sub
                if self.__invert:
                    v = 1-v
                    #base = -size
                    size *=-1
                v *=-1
            elif self.__base == "+": # sub
                if self.__invert:
                    v = v-1
            else:
                v = (t%1-0.5)
        elif self.__xtype == "ramp" or self.__xtype == "ramp":
            v = (t%1) 
            base = 0
            if self.__base == "-": # sub
                if self.__invert:
                    v = 1-v
                    #base = -size
                    size *=-1
                v *=-1
            elif self.__base == "+": # sub
                if self.__invert:
                    v = v-1
            else:
                v = (t%1-0.5)


        elif self.__xtype == "ramp2" or self.__xtype == "bump2":
            v = (t%1) 
            v = 1-v  
            if v == 1:
                v=0
            base = 0
            if self.__base == "-": # sub
                if self.__invert:
                    v = 1-v
                    #base = -size
                    size *=-1
                v *=-1
            elif self.__base == "+": # sub
                if self.__invert:
                    v = v-1
            else:
                v = (t%1-0.5)

        elif self.__xtype == "fade":
            x = t * 2 
            if x > 1:
                x = 2-x 
            x -= 0.5
            v = x*2
            #base /= 2
            #base *=2 
            if self.__base == "+": # add
                pass#base /= 2
            else:
                v *= -1

            v/=2

        if self.__invert:
            v *=-1

        out = v *size +base
        self.out = out
        self.count = count
        return out

class DMXCH(object):
    def __init__(self):
        self._base_value = 0
        self._fade  = None
        self._fx    = None
        self._fx_value = 0

        self._flash    = None
        self._flash_fx = None
        self._flash_fx_value = 0
        self._last_val = None
    def fade(self,target,ftime=0,clock=0,delay=0):
        if target != self._base_value:
            try:
                target = float(target)
                self._fade = Fade(self._base_value,target,ftime=ftime,clock=clock,delay=delay)
                #self._fade.next()
                #self._fade.next()
            except Exception as e:
                print( "Except:fade",e,target,ftime,clock)
    def fx(self,xtype="sinus",size=40,speed=40,invert=0,width=100,start=0,offset=0,base="", clock=0,master=None):
        print([self,xtype,size,speed,start,offset,base, clock])
        if str(xtype).lower() == "off":
            fx_value = self._fx_value
            if fx_value != 0:
                cprint("???????______ FX OFF AS FADE",fx_value,0,255)
                self._fx = Fade(fx_value,0,ftime=0.5,clock=clock)#,delay=delay)
            else:
                #self._fx = Fade(self._fx_value,target=0,ftime=2,clock=clock) 
                self._fx = None
                self._fx_value = 0 
        else:
            self._fx = FX(xtype=xtype,size=size,speed=speed,invert=invert,width=width,start=start,offset=offset,base=base,clock=clock,master=master)
    def flash(self,target,ftime=0,clock=0,delay=0):
        if str(target).lower() == "off":
            self._flash = None
        else:#elif target != self._base_value:
            try:
                target = float(target)
                self._flash = Fade(self._last_val,target,ftime=ftime,clock=clock,delay=delay)
            except Exception as e:
                print( "Except:flash",target,ftime,clock,__name__,e,)
    def flash_fx(self,xtype="sinus",size=40,speed=40,invert=0,width=100,start=0,offset=0,base="",clock=0,master=None):

        #if self._flash_fx is not None :
        #    cprint("flash_fx",xtype)

        if str(xtype).lower() == "off":
            fx_value = self._fx_value
            #if fx_value != 0:
            #    cprint("???????______ FX OFF AS FADE",fx_value,0,255)
            #    self._flash_fx = Fade(fx_value,0,ftime=0.5,clock=clock)#,delay=delay)
            #    self._flash_fx = None 
            #else:
            #    self._flash_fx = None 
            #    self._flash_fx_value = 0 
            self._flash_fx = None 
            self._flash_fx_value = 0 
        else:
            self._flash_fx = FX(xtype=xtype,size=size,speed=speed,invert=invert,width=width,start=start,offset=offset,base=base,clock=clock,master=master)

    def fx_ctl(self,cmd=""):#start,stop,off
        pass
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "< DMXCH {:0.2f} > {} {}".format( self._last_val,self._fx,self._fade)
    def fade_ctl(self,cmd=""):#start,stop,backw,fwd,bounce
        pass
    def next(self,clock=0):
        value = self._base_value
        if self._last_val is None:
            self._last_val = value
        fx_value = self._fx_value

        if self._flash is not None:
            value = self._flash.next(clock)
            #flicker bug ?!
            value = self._flash.next(clock)
            fx_value = 0
        elif self._fade is not None:#is Fade:# is Fade:
            self._base_value = self._fade.next(clock)
            #flicker bug ?!
            self._base_value = self._fade.next(clock)
            value = self._base_value

        
        if self._flash_fx is not None:# is FX:
            fx_value = self._flash_fx.next(clock)
        elif self._fx is not None and self._flash is None:# is FX:
            self._fx_value = self._fx.next(clock)
            fx_value = self._fx_value

        self._last_val = value+fx_value
        return self._last_val

Bdmx = []
for i in range(512*3):
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

import time
import json
import zlib
    
def JCB(data): #json client input
    t_start = time.time()
    #jdatas = data["cmd"].split("\x00")
    jdatas = [data["cmd"]]

    c = clock.time() 
    c = float(c)
    print("JCB",round(c,2))
    ftime = 0
    delay = 0
    for j in jdatas:
        master_fx = MASTER_FX()
        if not j:
            continue
        try:
            cprint("JCB",j)
            jdata = j #jdatas[j]
            jtxt = jdata
            #jtxt = zlib.decompress(jtxt) #jtxt.decode())
            jtxt = str(jtxt,"UTF-8")
            cmds = json.loads(jtxt)
            for x in cmds:
                #cprint(int(clock.time()*1000)/1000,end=" ",color="yellow")#time.time())
                #cprint("json", x,type(x),color="yellow")#,cmds[x])

                if "DMX" in x:
                    DMX = int(x["DMX"])
                else:continue
                if DMX > 0:
                    DMX -=1
                else:continue

                if "VALUE" in x:# and x["VALUE"] is not None:
                    v = x["VALUE"]
                else:continue
                if "FX" in x:# and x["VALUE"] is not None:
                    fx = x["FX"]
                else:fx=""
                if "FX2" in x:# and x["VALUE"] is not None:
                    fx2 = x["FX2"]
                else:fx2={}
                if "FADE" in x:
                    ftime = x["FADE"]
                else:ftime=0
                if "DELAY" in x:
                    delay = x["DELAY"]
                else:delay=0

                if len(Bdmx) < DMX:
                    continue
                
                if v is not None:
                    if "FLASH" in x:
                        #print("FLASH")
                        Bdmx[DMX].flash(target=v,ftime=ftime, clock=c,delay=delay)
                    else:
                        #print("FADE")
                        Bdmx[DMX].fade(target=v,ftime=ftime, clock=c,delay=delay)
                
                if type(fx2) is dict and fx2:

                    #cprint("FX2",DMX,fx2,color="green")
                    xtype="fade"
                    size  = 10
                    speed = 10
                    start = 0
                    offset= 0
                    width=100
                    invert=0
                    base = "-"
                    if "TYPE" in fx2:
                        xtype = fx2["TYPE"]
                    if "SIZE" in fx2:
                        size = fx2["SIZE"]
                    if "SPEED" in fx2:
                        speed = fx2["SPEED"]
                    if "OFFSET" in fx2:
                        offset = fx2["OFFSET"]
                    if "BASE" in fx2:
                        base = fx2["BASE"]
                    if "INVERT" in fx2:
                        invert = fx2["INVERT"]
                    if "WIDTH" in fx2:
                        width = fx2["WIDTH"]
                    
                    if "off" == x["VALUE"]: #fix fx flash off
                        xtype= "off"

                    if "alloff" == xtype.lower():
                        for i in Bdmx:
                            if i is not None:
                                i.flash_fx(xtype="off",clock=c)
                                i.fx(xtype="off",clock=c)

                    if "FLASH" in x:
                        Bdmx[DMX].flash_fx(xtype=xtype,size=size,speed=speed,invert=invert,width=width,start=start,offset=offset,base=base,clock=c,master=master_fx)
                    else:
                        Bdmx[DMX].fx(xtype=xtype,size=size,speed=speed,invert=invert,width=width,start=start,offset=offset,base=base,clock=c,master=master_fx)

                elif type(fx) is str and fx:  # old fx like sinus:200:12:244 
                    ccm = str(DMX+1)+":"+fx
                    print("fx",ccm)
                    if "FLASH" in x:
                        CB({"cmd":"fxf"+ccm})
                    else:
                        CB({"cmd":"fx"+ccm})

            print(time.time()-t_start)
            print(time.time())
            return
        except Exception as e:
            cprint("EXCEPTION JCB",e,color="red")
            cprint("----",jdata,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            
def CB(data): # raw/text client input 
    #print("CB",data)

    cmds = split_cmd(data)
    c = clock.time() 
    c = float(c)
    ftime = 0
    delay = 0

    for xcmd in cmds:
        if xcmd:
            cprint("CB",xcmd,end=" ")
            pass
        else:
            continue

        if xcmd.startswith("fxf"):
            xxcmd=xcmd[3:].split(":")
            #print("fxf:",xxcmd)
            if "alloff" == xxcmd[1].lower():
                for i in Bdmx:
                    if i is not None:
                        i.flash_fx(xtype="off",clock=c)
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
                    #Bdmx[k].fade(target=v,ftime=t, clock=c)
                    Bdmx[k].flash_fx(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=c)
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
                    #Bdmx[k].fade(target=v,ftime=t, clock=c)
                    Bdmx[k].fx(xtype=xtype,size=size,speed=speed,start=start,offset=offset,base=base,clock=c)
            except Exception as e:
                print("EXCEPTION IN FX",xcmd,e)
                print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))


#jchat = chat.CMD(CB,port=50001) # server listener
#thread.start_new_thread(jchat.poll,())
chat.cmd(JCB) # server listener
#chat.cmd(JCB,port=50001) # server listener

#input("END")
