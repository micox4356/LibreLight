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

(c) 2012 micha@librelight.de
"""
import sys
import time
import json
import zlib
    
rnd_id = ""
rnd_id += " Beta 22.02 "
import subprocess

import tool.git as git
rnd_id += git.get_all()


if "__file__" in dir():
    sys.stdout.write("\x1b]2;"+str(__file__)+" "+rnd_id+"\x07") # terminal title
else:
    sys.stdout.write("\x1b]2;"+str("__file__")+" "+rnd_if+"\x07") # terminal title

__run_main = 0
if __name__ == "__main__":
    __run_main = 1
else:
    import __main__ 
    print(dir())
    if "unittest" not in dir(__main__):
        __run_main = 1

import time
import socket
import struct
import sys
import random
import math

from collections import OrderedDict
 
import lib.zchat as chat
import lib.ArtNetNode as ANN
import _thread as thread  
#thread.start_new_thread
import lib.motion as motion

#idmx = [0]*512 # incremental dmx
dmx  = [0]*512 # absolute dmx data

gcolor = 1
def cprint(*text,color="blue",space=" ",end="\n"):
    color = color.lower()
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
        time.sleep(0.001)


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
        self.__tick = 0.001 # incremental timer drift's on highe cpu load ?
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
if __run_main:
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
        self.abs = 0
        self.run = 1
        self.end = 0
        self.off = 0
        #print("INIT", str(self) )
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return "<FADE Next:{:0.2f} from:{:0.2f} to:{:0.2f} ft:{:0.2f} Clock:{:0.2f} run:{} delay:{:0.2f}>".format( 
                    self.__last, self.__start,self.__target,self.__ftime,self.__clock_curr,self.run,self.__delay )
    def next(self,clock=None):
        if self.__ftime <= 0 and self.__delay <= 0:
            self.__last = self.__target
            self.end = 1
            self.run = 0
        
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock

        if self.__target > self.__start:
            if self.__last >= self.__target:
                self.run = 0
                self.end = 1
                return self.__target
        else:
            if self.__last <= self.__target:
                self.run = 0
                self.end = 1
                return self.__target
            
        current = (self.__clock - self.__clock_curr) / self.__ftime
        length = self.__start - self.__target
        self.__last = self.__start+ length*current 
        self.run = 1
        return self.__last

    def ctl(self,cmd="",value=None): # if x-fade cmd="%" value=50
        pass

class _MASTER():
    def __init__(self,name="None"):
        self.__data = {}
        self.name = name
    def val(self,name,value=None):
        _value = 100 #% 
        name = str(name)

        if name not in self.__data:
            self.__data[name] = 100


        _value = self.__data[name] 
        if value is not None:
            if _value != value:
                print(self.name,"CHANGE MASTER:",name,"from:",_value,"to:",value)
            self.__data[name] = value

        _value = self.__data[name] 

        return _value /100.
        

exec_size_master  = _MASTER("EXEC-SIZE")
exec_speed_master = _MASTER("EXEC-SPEED")
exec_offset_master = _MASTER("EXEC-OFFSET")


size_master  = _MASTER("SIZE")
speed_master = _MASTER("SPEED")

exe_master = []
exe_master.append({"SIZE":100,"SPEED":100,"id":12,"link-ids":[2]})



class MASTER_FX():
    def __init__(self):
        self.__data = []
        self.__ok = []
        self.i=0
        self.old_offsets = []
        self.offsets = []
        self.count = -1
        self.init = 10

    def add(self,fx):
        if fx not in self.__data:
            self.__data.append(fx)
            info = fx._get_info()
            offset = 0
            if "offset" in info:
                offset = info["offset"]
            self.old_offsets.append(offset)
            self.offsets.append(offset)
            if "xtype" in info:
                if info["xtype"] == "rnd":
                    self._shuffle()
            
    def _shuffle(self):
        random.seed(1000)
        random.shuffle(self.old_offsets)

    def _init(self):
        self._shuffle()
        for i,v in enumerate(self.old_offsets):
            offset = self.old_offsets[i]
            self.offsets[i] =  offset
        self.init = 0
    def next(self,child):
        i = self.__data.index(child)
        offset = self.old_offsets[i]
        self.offsets[i] =  offset
        return offset

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
            self.count=count
            
        idx = self.__data.index(child) 
        offset = self.offsets[idx]

        return offset
        

class FX():
    def __init__(self,xtype="sinus",size=10,speed=10,invert=0,width=100,start=0,offset=0,base="",clock=0,master=None,master_id=0):
        self.__xtype=xtype
        self.__size  = size
        self.__start = start
        self.__master_id = master_id
        if width > 200:
            width = 200
        if width <= 0:
            width = 1
        self.__fade_in_master = 0
        self.__width = width
        self.__invert = invert
        self.__base = base
        self.__speed = speed
        self.__offset = offset
        self.__clock = clock
        self.__clock_curr = clock
        self.__clock_delta = 0
        self.__clock_old = self.__clock_curr
        self.out = 0
        self.old_v = -1
        self.run = 1
        self.count = -1
        self.abs = 0 # ABSOLUT
        self.__angel = self.__clock_curr*360%360
        if master is None:
            cprint(master, "MASTER_FX ERR",master,color="red")
            self.__master = MASTER_FX()
            self.__master.add(self)
        else:
            self.__master = master
            self.__master.add(self)
        if self.__xtype == "rnd":
            self.__offset = self.__master.get(self,-2)
            self.__offset = self.__master.next(self)#,count)
        
        self._exec_id = None

        self.next()

    def exec_id(self,_id=None):
        if type(_id) is not type(None):
            self._exec_id = str(_id)
        return self._exec_id

    def _get_info(self):
        return {"offset":self.__offset,"xtype":self.__xtype}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        ABS = "INC"
        if self.abs:
            ABS = "ABS"
        return "<FX Next:{:0.2f} xtype:{} Size:{:0.2f} Speed:{:0.2f} ang:{:0.2f} base:{} Clock:{:0.2f} run:{} EXEC:{} :{}>".format( 
                    self.next(), self.__xtype, self.__size, self.__speed, self.__angel
                    , self.__base, self.__clock_curr, self.run, self._exec_id,ABS )

    def _calc_fx(self,v,t,size,base):
        base = 0
        if self.__base == "-": # sub
            if self.__invert:
                v = 1-v
                size *=-1
            v *=-1
        elif self.__base == "+": # sub
            if self.__invert:
                v = v-1
        else:
            v = (t%1-0.5)
        return v

    def next(self,clock=None):
        if type(clock) is float or type(clock) is int:#not None:
            self.__clock_curr = clock
        
        d  = (self.__clock_curr - self.__clock_old) 
        
        m1 = ( speed_master.val(self.__master_id)) # global speed-master
        m2 = ( exec_speed_master.val(self._exec_id)) # exec start by 0

        shift  = 0
        m = (m1 * m2)  -1
        shift += d * m

        self.__clock_delta += shift
        self.__clock_old = self.__clock_curr
        
        t = self.__clock_curr
        t += self.__clock_delta
        t *= self.__speed / 60 

        offset2 = self.__offset 
        offset2 *= exec_offset_master.val(self._exec_id) 

        t += offset2 / 100 
        t += self.__start  / 1024 #255

        tw = t%1
        count = t//1
        t = t * (100/self.__width)
        if tw > self.__width/100:
            t = 1 
        
        self.__angel = t%1*360 
        t = t%1
        rad = math.radians(self.__angel)

        self.abs = 0
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
            if self.__angel > 90 and self.__angel <=270:
                v=1
            else:
                v=0
            
            if count != self.count and v == 0: # and v: # % 2 == 0:#!= self.count:
                 self.__master.next(self)#,count)
            self.__offset = self.__master.get(self,count)
                
            v = self._calc_fx(v,t,size,base)

        elif self.__xtype == "on":
            if self.__angel > 90 and self.__angel <=270:
                v=1
            else:
                v=0
            v = self._calc_fx(v,t,size,base)

        elif self.__xtype == "ramp" or self.__xtype == "bump":
            v = (t%1) 
            v = self._calc_fx(v,t,size,base)
            
        elif self.__xtype == "ramp2" or self.__xtype == "bump2":
            v = (t%1) 
            v = 1-v  
            if v == 1:
                v=0
            v = self._calc_fx(v,t,size,base)

        elif self.__xtype == "static":
            self.abs = 1
            base = size #100
            v=0
            size=0

        elif self.__xtype == "fade":
            x = t * 2 
            if x > 1:
                x = 2-x 
            x -= 0.5
            v = x*2
            if self.__base == "+": # add
                pass
            else:
                v *= -1

            v/=2

        if self.__invert:
            v *=-1
    
        out = v *size +base 
        self.out = out
        self.count = count

        out = out * size_master.val(self.__master_id)  # master 
        out = out * exec_size_master.val(self._exec_id)  # master 
        return out 

class DMXCH(object):
    def __init__(self,dmx=-1):
        self._base_value = 0
        self._fade  = None
        self._fx    = [None,None] # None
        self._fx_value = 0

        self._dmx = dmx
        self._dmx_fine = 0

        self._fix_id = 0 
        self._v_master_id=0
        self._last_val_raw=0

        self._flash    = None
        self._flash_fx = None
        self._flash_fx_value = 0
        self._last_val = None
        self._exec_ids = [None,None,None,None] # go, go-fx, flash, flash-fx
    
    def fade(self,target,ftime=0,clock=0,delay=0):
        if target != self._base_value:
            try:
                target = float(target)
                self._fade = Fade(self._base_value,target,ftime=ftime,clock=clock,delay=delay)
            except Exception as e:
                print( "Except:fade",e,target,ftime,clock)
        self.next(clock)

    def fx(self,xtype="sinus",size=40,speed=40,invert=0,width=100,start=0,offset=0,base="", clock=0,master=None):
        self._fx[0] = self._fx[1]
        if str(xtype).lower() == "off":
            fx_value = self._fx_value
            if fx_value != 0:
                cprint("???????______ FX OFF AS FADE",fx_value,0,255)
                if self._fx[1].abs:
                    self._fx[1] = Fade(self._last_val_raw,0,ftime=0.5,clock=clock) 
                else:
                    self._fx[1] = Fade(fx_value,0,ftime=0.5,clock=clock) 
            else:
                self._fx[1] = None
                self._fx_value = 0 
        else:
            self._fx[1] = FX(xtype=xtype,size=size,speed=speed,invert=invert
                                ,width=width,start=start,offset=offset,base=base
                                ,clock=clock,master=master,master_id=1) 
            self._fx[1].exec_id(self._exec_ids[1])

        self.next(clock)

    def flash(self,target,ftime=0,clock=0,delay=0):
        if str(target).lower() == "off":
            if self._flash:
                cur_val = self._flash.next()
                cur_tar = self._base_value
                self._flash = Fade(cur_val,cur_tar,ftime=ftime,clock=clock) 
                self._flash.off = 1
        else:
            try:
                target = float(target)
                self._flash = Fade(self._last_val,target,ftime=ftime,clock=clock,delay=delay)
                self._flash = Fade(self._last_val,target,ftime=0,clock=clock,delay=delay)
            except Exception as e:
                print( "Except:flash",target,ftime,clock,__name__,e,)
        self.next(clock)

    def flash_fx(self,xtype="sinus",size=40,speed=40,invert=0,width=100,start=0,offset=0,base="",clock=0,master=None):
        if str(xtype).lower() == "off":
            fx_value = self._fx_value
            self._flash_fx = None 
            self._flash_fx_value = 0 
        else:
            self._flash_fx = FX(xtype=xtype,size=size,speed=speed,invert=invert
                                ,width=width,start=start,offset=offset,base=base
                                ,clock=clock,master=master,master_id=0)
            self._flash_fx.exec_id(self._exec_ids[3])
        self.next(clock)
        #print("init flash_fx",self)

    def fx_ctl(self,cmd=""): #start,stop,off
        pass
    
    def __str__(self):
        return self.__repr__()

    def exec_ids(self,_id=None):
        #if type(_id) is not type(None):
        #    #self._exec_id = _id
        #    #print("set exec_id",_id)
        return self._exec_ids

    def __repr__(self):
        v = self._last_val
        if type(self._last_val) in [int,float]:
            v = round(self._last_val,2)

        return "<BUFFER DMX:{} FINE:{} VAL:{} EXEC:{}\n  fd:{}\n  fx:{}\n  fx_flash:{}\n".format(
                    self._dmx,self._dmx_fine
                    ,v,str(self._exec_ids)
                    ,self._fade
                    ,self._fx
                    ,self._flash_fx)
    
    def fade_ctl(self,cmd=""): #start,stop,backw,fwd,bounce
        pass
    
    def next(self,clock=0):
        try:
            self._next(clock)
        except Exception as e:
            cprint("Exception DMXCH.next()" ,e)
        out = self._last_val
        return out

    def _next(self,clock=0):
        value = self._base_value
        
        if self._last_val is None:
            self._last_val = value
        fx_value = self._fx_value
        fx_abs = 0

        if self._flash is not None:
            value = self._flash.next(clock)
            value = self._flash.next(clock) #flicker bug ?!

            if self._flash.end == 1 and self._flash.off == 1:
                self._flash = None
            fx_value = 0

        elif self._fade is not None: # is Fade: # is Fade:
            self._base_value = self._fade.next(clock)
            self._base_value = self._fade.next(clock) #flicker bug ?!
            value = self._base_value

        
        if self._flash_fx is not None:# is FX:
            fx_value = self._flash_fx.next(clock)
            fx_abs = self._flash_fx.abs
        else:
            self._fx_value = 0
            if self._fx[-1] is not None and self._flash is None:# is FX:
                self._fx_value += self._fx[-1].next(clock)
                fx_abs = self._fx[-1].abs
            fx_value = self._fx_value

        if fx_abs == 1:
            self._last_val = fx_value
        else:
            self._last_val = value + fx_value
        
        self._last_val_raw = self._last_val 


        if self._v_master_id in V_MASTER:
            vm = V_MASTER[self._v_master_id].next(clock)
            vm = vm/256
            self._last_val *= vm 

        out = self._last_val
        return out


V_MASTER = {} #DMXCH
Bdmx = []
for i in range(512*7+1):
    Bdmx.append( DMXCH(i) )
    #print(type(dmx[i]))

_id = 1



def split_cmd(data):
    if "cmd" in data:
        cmd = data["cmd"]
        #print("cmd",cmd)
        if "," in cmd:
            cmds = cmd.split(",")
        else:
            cmds = [cmd]
    return cmds


class VDMX():
    """functional implementation as class for namespace encapsulation

    """
    def __init__(self):
        self.data = OrderedDict() 
        self.data[4] = {"DMX":[21,22,23],"VALUE":255, "LIMIT":255} #,"DMXCH":DMXCH("V4")}
        for k,v in self.data.items():
            pass
            #dmxch = v["DMXCH"]
            #dmxch.fade(10,0)
            #dmxch.fx(size=200,speed=200,base="-") #self,xtype="sinus",size=40,speed=40,invert=0,width=100,start=0,offset=0,base="", clock=0,master=None):

    def _list_by_dmx(self,_dmx=0):
        data = OrderedDict()
        for i,link in self.data.items(): # enumerate(self.data):
            if _dmx in link["DMX"]:
                #print( "_list_by_dmx",i,link)
                data[i] = link
        return data


    def dmx_by_id(self,_id=0):
        #print("dmx by master-id:",_id)

        if _id in self.data:
            for i,link in self.data[_id].items():
                #print("dmx_by_id", i,link)
                return (i,link)

        return 0,{}

    def by_dmx(self,clock,dmx):
        #print("master of dmx:",dmx)
        val=0
        flag = 0
        data = self._list_by_dmx(dmx)
        for i,row in data.items():
            if "DMXCH" not in row:
                row["DMXCH"] = DMXCH("V{}".format(i))
                row["DMXCH"].fade(255,0)

            v = row["DMXCH"].next(clock)
            #row["DMXCH"].fade(200,20)
            if v >= val:
                val = v
            flag = 1
        out = 1.
        if val > 255:
            val = 255
        
        if flag:
            out = val/255.
        else: 
            out = 1.
        return out

vdmx = VDMX()


class HTP_MASTER():
    """functional implementation as class for namespace encapsulation

    """
    def __init__(self):
        self.data = OrderedDict() 
        #self.data[1] = {"DMX":[1,2,3],"VALUE":80, "LIMIT":255}
        #self.data[2] = {"DMX":[12,13,22],"VALUE":70, "LIMIT":255}
        #self.data[3] = {"DMX":[22,23,24],"VALUE":99, "LIMIT":255}
        self.data[4] = {"DMX":[22,23,24],"VALUE":99, "LIMIT":255,"DMXCH":DMXCH(4)}

    def _list_by_dmx(self,_dmx=0):
        data = OrderedDict()
        for i,link in self.data.items(): # enumerate(self.data):
            if _dmx in link["DMX"]:
                #print( "_list_by_dmx",i,link)
                data[i] = link
        return data


    def dmx_by_id(self,_id=0):
        #print("dmx by master-id:",_id)

        if _id in self.data:
            for i,link in self.data[_id].items():
                #print("dmx_by_id", i,link)
                return (i,link)

        return 0,{}

    def val_by_dmx(self,dmx=0):
        #print("master of dmx:",dmx)
        val=0
        flag = 0
        data = self._list_by_dmx(dmx)
        for i,link in data.items():

            #print("master_by_dmx", i,link)
            if link["VALUE"] > val:
                #print("master_by_dmx", i,link)
                val = link["VALUE"]
                flag=1
        out = 1.
        if flag:
            out = val/255.
        
        return out
htp_master = HTP_MASTER()

#htp_master.data[_id] = {"DMX":[1,2,3],"VALUE":80, "LIMIT":255,"DMXCH":DMXCH()}



class Main():
    def __init__(self):
        self.artnet = {}
        self.fx = {} # key is dmx address
        self.lock = thread.allocate_lock()
    def loop(self):
        xx = [0]*512
        ii = 0
        old_univ = -1
        xx = [0]*512
        for ii,dmxch in enumerate(Bdmx):
            i = ii%512
            univ = ii//512
            if str(univ) not in self.artnet:
                print("add uiv",univ)
                self.artnet[str(univ)] = ANN.ArtNetNode(to="10.10.10.255",univ=univ)

            if univ != old_univ:
                old_univ = univ
                try:
                    artnet.next()
                except:pass
                artnet = self.artnet[str(univ)]
                artnet.dmx = [0]*512

        fps_start = time.time()
        fps = 0
        dbg= 0#1
        while 1:
            self.lock.acquire_lock()

            start = time.time()
            _t=0
            t = clock.time()
            ii = 0
            old_univ = -1
            xx = [0]*512
            for ii,dmxch in enumerate(Bdmx):
                i = ii%512
                univ = ii//512
                s_univ = str(univ)
                if s_univ not in self.artnet:
                    print("add uiv",univ)
                    self.artnet[s_univ] = ANN.ArtNetNode(to="10.10.10.255",univ=univ)


            if dbg:
                end = time.time()
                print(" t",_t,ii,round(end-start,4))
            start = time.time()
            _t+=1

            old_univ = -1
            xx = [0]*512
            for ii,dmxch in enumerate(Bdmx):
                i = ii%512
                univ = ii//512

                if univ != old_univ:
                    old_univ = univ
                    artnet = self.artnet[str(univ)]
                    xx = artnet.dmx 

                v = dmxch.next(t)
                xx[i] = int(v)

            if dbg:
                end = time.time()
                print(" t",_t,ii,round(end-start,4))
            start = time.time()
            _t+=1

            old_univ = -1
            xx = [0]*512
            for ii,dmxch in enumerate(Bdmx): #fine loop
                dmx_fine =  dmxch._dmx_fine
                if dmx_fine > 0:
                    i = ii%512
                    univ = ii//512

                    if univ != old_univ:
                        artnet = self.artnet[str(univ)]
                        xx = artnet.dmx# = xx
                    
                    v = dmxch.next(t)
                    vv = vdmx.by_dmx(clock=i,dmx=ii+1)
                    try:
                        v = v*vv # disable v-master
                    except Exception as e:
                        cprint("Exception v*vv",[v,vv],e)
                        continue

                    vf = int(v%1*255)
                    dmx_fine = dmx_fine%512
                    try:
                        if v >= 255:
                            xx[dmx_fine-1] = 255
                        elif v < 0:
                            xx[dmx_fine-1] = 0
                        else:
                            xx[dmx_fine-1] = int(v%1*255)
                    except Exception as e:
                        print("E dmx_fine",e,dmx_fine)
            if dbg:
                end = time.time()
                print(" t",_t,ii,round(end-start,4))
                print()
            start = time.time()
            _t+=1


            self.lock.release_lock()

            for k,artnet in self.artnet.items():
                artnet.next()

            fps += 1
            stop_fps = 50
            time.sleep(1/30)
            if fps >= stop_fps:
                fps_t = time.time()
                print(round(stop_fps/(fps_t-fps_start),2),"core/fps") 
                fps = 0
                fps_start = time.time()

main = Main()
if __run_main:
    thread.start_new_thread(main.loop,())


def _init_action(row):#Bdmx,out,DMX):
    Admx = row["DMXCH"]
    line_sub_count = 0
    if row["fx"]:
        x = row["fx"]
        Admx.fx(xtype=x["xtype"]
                ,size=x["size"]
                ,speed=x["speed"]
                ,invert=x["invert"]
                ,width=x["width"]
                ,start=x["start"]
                ,offset=x["offset"]
                ,base=x["base"]
                ,clock=x["clock"]
                ,master=x["master"])
        
        line_sub_count += 1
    if row["flash_fx"]:
        x = row["flash_fx"]
        Admx.flash_fx(xtype=x["xtype"]
                ,size=x["size"]
                ,speed=x["speed"]
                ,invert=x["invert"]
                ,width=x["width"]
                ,start=x["start"]
                ,offset=x["offset"]
                ,base=x["base"]
                ,clock=x["clock"]
                ,master=x["master"])
        line_sub_count += 1

    if row["flash"]:
        x = row["flash"]
        Admx.flash(target=x["target"]
                ,ftime=x["ftime"]
                ,clock=x["clock"]
                ,delay=x["delay"])
        line_sub_count += 1
    if row["fade"]:
        x = row["fade"]
        Admx.fade(target=x["target"]
                ,ftime=x["ftime"]
                ,clock=x["clock"]
                ,delay=x["delay"])
        line_sub_count += 1

    return line_sub_count


def set_dmx_fine_ch(Admx,dmx_fine_nr):
    try:
        if int(dmx_fine_nr) > 0:
            Admx._dmx_fine = int(dmx_fine_nr)
    except Exception as e:
        cprint(x,color="red")
        cprint("except 3455",e,color="red")

def _parse_cmds(cmds,clock=0,master_fx=None):
    c=clock
    out = {}
    for x in cmds:
        Admx = DMXCH() #dummy

        _fix_id=0
        _attr = ""
        if "CMD" in x:
            print("CMD:",x)

            if "EXEC-SPEED-MASTER" == x["CMD"]:
                exec_speed_master.val(x["NR"],x["VALUE"])
            if "EXEC-SIZE-MASTER" == x["CMD"]:
                exec_size_master.val(x["NR"],x["VALUE"])
            if "EXEC-OFFSET-MASTER" == x["CMD"]:
                exec_offset_master.val(x["NR"],x["VALUE"])

            if "SPEED-MASTER" == x["CMD"]:
                speed_master.val(x["NR"],x["VALUE"])
            if "SIZE-MASTER" == x["CMD"]:
                size_master.val(x["NR"],x["VALUE"])

        else:
            #print("x",x)
            
            if "DMX" in x:
                DMX = int(x["DMX"])
            else:
                continue

            if "VALUE" in x:
                v = x["VALUE"]
            else:
                continue

            _inc = 0
            _fix_id = 0
            _val = -1
            _clock = 0
            exec_id = None

            if "VALUE" in x:
                _val = x["VALUE"]
            if "INC" in x:
                _inc = x["INC"]
            if "FIX" in x:
                _fix_id = x["FIX"]
            if "clock" in x:
                _clock=x["clock"]
            if "ATTR" in x:
                _attr = x["ATTR"]

            if DMX <= 0: # VIRTUAL
                DMX = "FIX"+str(_fix_id)
                ok = 0
                if "ATTR" in x:
                    _attr = x["ATTR"]
                    if "DIM" == x["ATTR"]:
                        if _fix_id not in V_MASTER:
                            V_MASTER[_fix_id] = DMXCH()
                        #print("_val",_val)
                        #V_MASTER[_fix_id].fade(_val,ftime=0,clock=0,delay=0)
                        #print("  V-MASTER",_fix_id,_val,_inc)
                        ok = 1
                

                if _fix_id in V_MASTER:
                    Admx = V_MASTER[_fix_id]

                if not ok:
                    continue
            else:
                if DMX < len(Bdmx):
                    Admx = Bdmx[DMX-1]
                else:
                    print("DMX ADDRESS too BIG",DMX)
                    continue 

            
            if "DMX-FINE" in x and DMX > 0:
                set_dmx_fine_ch(Admx, x["DMX-FINE"])

            #print("-")
            if "EXEC" in x:
                exec_id = x["EXEC"]

            if "ATTR" in x:
                _attr = x["ATTR"]
            if "FIX" in x:
                _fix_id = x["FIX"]


            fx=""
            fx2={}
            ftime=0
            delay=0
            if "FX" in x:
                fx = x["FX"]
            if "FX2" in x:
                fx2 = x["FX2"]
            if "FADE" in x:
                ftime = x["FADE"]
            if "DELAY" in x:
                delay = x["DELAY"]


            #print("DO",[exec_id],x)
            # ids = [401,402,304,103] 
            # exec-id, exec-fx-id, flush-id, flush-fx-id
            if v != "off":
                if "FLASH" in x:
                    ids = Admx.exec_ids()
                    if type(v) is int:
                        ids[2] = exec_id
                    if fx2:
                        ids[3] = exec_id
                    #print(" ",[ids, exec_id],"FL")
                else: # GO or ON
                    ids = Admx.exec_ids()
                    if type(v) is int:
                        ids[0] = exec_id
                    if fx2:
                        ids[1] = exec_id
                    #print(" ",[ids, exec_id],"GO")

            if v == "off":
                if "FLASH" in x:
                    ids = Admx.exec_ids()
                    stop = 0
                    #print(" ",[ids, exec_id])
                    if ids[2] != exec_id:
                        stop = 1
                    else:
                        ids[2] = None

                    if fx2:
                        if ids[3] != exec_id:
                            stop = 1
                        else:
                            ids[3] = None
                            stop = 0
                    if stop:
                        # this FLASH cmd OFF/RELEASE is not valid anymore
                        continue


            #aprint("OK")        
            #ids = Admx.exec_ids()
            #print("OK ",[ids, exec_id])

            #Bdmx[DMX].exec_id(exec_id)
            out[DMX] = {"flash":{},"fade":{},"fx":{},"flash_fx":{},"fix_id":_fix_id,"attr":_attr,"DMXCH":Admx}
            if v is not None:
                if "FLASH" in x:
                    out[DMX]["flash"] = {"target":v,"ftime":ftime, "clock":c,"delay":delay,"DMXCH":Admx}
                else:
                    out[DMX]["fade"] = {"target":v,"ftime":ftime, "clock":c,"delay":delay,"DMXCH":Admx}
            
            if type(fx2) is dict and fx2:
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
                    for dmxch in Bdmx:
                        if dmxch is not None:
                            dmxch.flash_fx(xtype="off",clock=c)
                            dmxch.fx(xtype="off",clock=c)
                    for j in V_MASTER:
                        dmxch = V_MASTER[j]
                        if j is not None:
                            dmxch.flash_fx(xtype="off",clock=c)
                            dmxch.fx(xtype="off",clock=c)

                if "FLASH" in x:
                    out[DMX]["flash_fx"] = {"xtype":xtype,"size":size,"speed":speed,
                                "invert":invert,"width":width,"start":start
                                ,"offset":offset,"base":base,"clock":c,"master":master_fx}
                else:
                    out[DMX]["fx"] = {"xtype":xtype,"size":size,"speed":speed
                            ,"invert":invert,"width":width,"start":start
                            ,"offset":offset,"base":base,"clock":c,"master":master_fx}

            elif type(fx) is str and fx:  
                # old fx like sinus:200:12:244 
                ccm = str(DMX+1)+":"+fx
                print("fx",ccm)
                if "FLASH" in x:
                    pass#CB({"cmd":"fxf"+ccm})
                else:
                    pass#CB({"cmd":"fx"+ccm})
    return out



import hashlib
JCB_GLOB_BUF = {}

def JCB(data,sock=None): #json client input
    t_start = time.time()
    s = time.time()

    e  = time.time()
    ct = int(e*100)/100
    print()
    msg = "{} JCB START: {:0.02f} sizeof:{}"
    msg = msg.format(ct,e-s,sys.getsizeof(data) ) 
    print(msg)

    jdatas = []
    l2 = 0
    for line in data:
        
        data2 = json.loads(line)
        l2 += len(data2)
        #print("line:",line)
        jdatas.append(data2) #["CMD"])

    print("INPUT JCB =>",len(data),":",l2)
    c = clock.time() 
    c = float(c)
    ftime = 0
    delay = 0
    out = {}
    line=""
    for cmds in jdatas:
        for line in cmds: # run first
            #print(line)
            if "FLASH" in line:
                cprint("FLUSH",end=" ",color="CYAN")
                if "VALUE" in line:
                    if line["VALUE"] == "off":
                        cprint("OFF",end=" ",color="red")
                    else:
                        cprint("ON",end=" ",color="green")
                print("")
            else:
                cprint("FADE",color="CYAN")
            break

    for cmds in jdatas:
        for line in cmds:
            if "time" in line:
                jt_start = line["time"]
                latenz = round(t_start-jt_start,4)
                if latenz > 0.5:
                    cprint("latenz 0.5 >",latenz,color="red")
                    break
    for cmds in jdatas:
        #line = json.dumps(cmds)
        #md5 = hashlib.md5.hexdigest(line)
        
        master_fx = MASTER_FX()
        if not cmds:
            continue

        try:
            out = _parse_cmds(cmds,clock=c,master_fx=master_fx)


            #cprint("-","{:0.04} sec.".format(time.time()-t_start),color="yellow")
            # ------- ---------------------------------------------------- 

        except Exception as e:
            cprint("EXCEPTION JCB",e,color="red")
            cprint("----",str(cmds)[:150],"...",color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            raise e

    line_count = 0
    line_count_sub = 0
    line_size = 0
    attr_count = {}
    attr_count2 = 0


    if out:
        try:
            try: # second loop to sync-start all dmxch's
                main.lock.acquire_lock()
                for _id in out:
                    row = out[_id]
                    #print(row)
                    line_size += sys.getsizeof(row)

                    #print("_id",_id)
                    Admx = row["DMXCH"]
                    #print("Admx",Admx)

                    if "attr" in row:
                        if row["attr"] not in attr_count:
                            attr_count[row["attr"]] = 0
                    attr_count[row["attr"]] += 1
                    attr_count2 +=1

                    if row["fix_id"]:
                        _fix_id = row["fix_id"]
                        Admx._fix_id = _fix_id
                        if "attr" in row:
                            if row["attr"] in ["RED","GREEN","BLUE","WHITE","AMBER"]: #CYAN,MAGENTA,YELLOW
                                Admx._v_master_id = _fix_id
                                #print("SET V_MASTER",row)
                            
                    line_count_sub += _init_action(row)
                    line_count += 1
                e = time.time()
                print(" sub-JCB TIME:","{:0.02f}".format(e-s),int(e*100)/100)

            finally:
                main.lock.release_lock()
            #time.sleep(1/30)

        except Exception as e:
            cprint("EXCEPTION JCB",e,color="red")
            cprint("----",str(cmds)[:150],"...",color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            raise e

        #cprint(" ","{:0.04} sec.".format(time.time()-t_start),color="yellow")
        print("attr_count:",attr_count)
        #print(line_count,line_size)

        e  = time.time()
        ct = int(e*100)/100
        msg = "{} JCB: END  {:0.02f} sizeof:{} fix-count:{} attr-count:{}"
        msg = msg.format(ct,e-s,line_size,line_count,line_count_sub ) 
        print(msg)
        time.sleep(1/60)
            

if __run_main:
        
    s = chat.Server(cb=JCB)
    while 1:
        s.poll()
        time.sleep(0.001)





