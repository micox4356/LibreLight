#! /usr/bin/python
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
import random
rnd_id = str(random.randint(1000,9000))
rnd_id += " beta 22.10 "
import subprocess
import string
_gcmd=['git', 'rev-parse', '--short', 'HEAD']
try:
    r = subprocess.check_output(_gcmd)
    rnd_id += r.decode('ascii').strip()
except Exception as e:
    rnd_id += " no git" 
    #rnd_id += " ".join(_gcmd) +str(e)

try:
    xtitle = __file__
except:
    xtitle = "__file__"

if "/" in xtitle:
    xtitle = xtitle.split("/")[-1]
import sys

sys.stdout.write("\x1b]2;"+str(xtitle)+" "+str(rnd_id)+"\x07") # terminal title

import json
import time
import sys
import os 

import _thread as thread
import traceback

import tkinter
import tkinter as tk
from tkinter import font

space_font = None
import tkinter.simpledialog
from idlelib.tooltip import Hovertip


_global_short_key = 1






import lib.zchat as chat
import lib.motion as motion

from collections import OrderedDict

_POS_LEFT = 0
_POS_TOP  = 15
_config = []
try: 
    h = os.environ["HOME"]
    lines = [{}]
    try: 
        f = open(h +"/LibreLight/config.json")
        lines = f.readlines()

    except FileNotFoundError as e: #Exception as e:
        f = open(h +"/LibreLight/config.json","w")
        f.write('{"POS_TOP":0}\n{"POS_LEFT":0}')
        f.close()
        print("Exception:",e)

    for line in lines:
        line=line.strip()
        print("config read",line)
        row = json.loads(line) 
        _config.append(row)

except Exception as e:
    print("Exception:",e)

try: 
    for row in _config:
        print("config:",row)
        if "POS_LEFT" in row:
           _POS_LEFT = int(row["POS_LEFT"]) 
        if "POS_TOP" in row:
           _POS_TOP = int(row["POS_TOP"]) 
except Exception as e:
    print("Exception:",e)


def showwarning(msg="<ERROR>",title="<TITLE>"):
    _main = tkinter.Tk()
    defaultFont = tkinter.font.nametofont("TkDefaultFont")
    print("showwarning",defaultFont)
    defaultFont.configure(family="FreeSans",
                           size=10,
                           weight="normal")
    
    geo ="{}x{}".format(20,20)
    _main.geometry(geo)
    def _quit():
        time.sleep(.02)
        _main.quit()
    thread.start_new_thread(_main.mainloop,())
    #_main.quit()

    #msg="'{}'\n Show Does Not Exist\n\n".format(show_name)
    #msg += "please check\n"
    #msg += "-{}init.txt\n".format(self.show_path0)
    #msg += "-{}".format(self.show_path1)

    r=tkinter.messagebox.showwarning(message=msg,title=title,parent=None)


CUES    = OrderedDict()
groups  = OrderedDict()

class Modes():
    def __init__(self):
        self.modes = {}
        self.__cfg = {}
        self.__cb = None
    def val(self,mode,value=None): #like jquery
        if value is not None:
            return self.set(mode,value)
        elif mode in self.modes:
            return self.modes[mode]
    def get(self,mode,value=None):
        return self.val(mode,value)
    def __check(self,mode):
        if mode not in self.modes:
            self.modes[mode] = 0
            self.__cfg[mode] = 0
    def cfg(self,mode,data={}):
        self.__check(mode)
        if type(data) is dict:
            for k in data:
                v = data[k]
                if v not in self.__cfg:
                    self.__cfg[k] = v
            return 1
        elif type(data) is str:
            if data in self.__cfg:
                return self.__cfg[data]

    def set(self,mode,value):
        protected = ["BLIND","CLEAR","REC-FX"]
        self.__check(mode)
        if mode == "CLEAR":
            return 1
        elif mode == "ESC":
            for m in self.modes:
                print("ESC",m)
                if m == "COPY":
                    PRESETS.clear_copy()
                if m == "MOVE":
                    PRESETS.clear_move()
                if m != "BLIND":
                    self.modes[m] = 0
                    self.callback(m)
            return 1

        if value:
            for m in self.modes:
                if m not in protected and mode not in protected and m != mode:
                    #cprint("-#-# clear mode",mode,m,value,color="red")
                    if self.modes[m]:
                        self.modes[m]= 0
                        self.callback(m)
            if self.modes[mode] and value == 1:
                if modes == "MOVE":
                    PRESETS.clear_move()
                if modes == "COPY":
                    PRESETS.clear_copy()
                self.modes[mode] = 0 # value
            else:
                self.modes[mode] = value #1 #value
        else:
            self.modes[mode] = 0 #value
            if modes == "COPY":
                PRESETS.clear_copy()
            if modes == "MOVE":
                PRESETS.clear_move()
        self.callback(mode)
        return value
    def set_cb(self,cb):
        if cb:
            self.__cb = cb
    def callback(self,mode):
        if self.__cb is not None and mode in self.modes:
            value = self.modes[mode]
            self.__cb(mode=mode,value=value)


modes = Modes()

#modes.val("BLIND", 0)
#modes.modes["BLIND"] = 0
modes.modes["ESC"] = 0
modes.modes["REC"] = 0
modes.modes["EDIT"] = 0
modes.modes["MOVE"] = 0
modes.modes["FLASH"] = 0
modes.modes["GO"] = 0
modes.modes["DEL"] = 0
modes.modes["REC-FX"] = 0
modes.modes["SELECT"] = 0
modes.modes["CFG-BTN"] = 0
modes.modes["LABEL"] = 0

def xcb(mode,value=None):
    print("xcb","MODE CALLBACK",mode,value)
    if mode == "REC-FX":
        print("xcb",modes.val("REC-FX"))
#modes.set_cb(xcb)

POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]
#client = chat.tcp_sender(port=50001)
    

def set_exec_fader(nr,val,color=""):
    exec_wing = window_manager.get_obj(name="EXEC-WING") #= WindowManager()
    if not exec_wing: 
        return

    #print(exec_wing)
    try:
        exec_wing.set_fader(nr,val,color=color)
    except Exception as e:
        print("exception",e)
    #print("remote in:",round(time.time(),0),"x",i,v)

# remote input - start (memcached)
def JCB(x):
    for i in x:
        jv = x[i]

        try:
            jv = json.loads(jv)
            jv = jv[0]
            #print(jv)
            v = jv["iVAL"]
            #exec_wing.set_fader(0,v)
            set_exec_fader(0,v)
            set_exec_fader(1,200-v)
            set_exec_fader(2,int(v/2+10))
        except Exception as e:
            print("exception",e)
        #print("remote in:",round(time.time(),0),"x",i,v)

#chat.cmd(JCB,port=30002) # SERVER
thread.start_new_thread(chat.cmd,(JCB,30002)) # SERVER
# remote input - end

# read memcachd
memcache = None
try:
    import memcache
except Exception as e:
    print("Exception IMPORT ERROR",e)

class MC():
    def __init__(self,server="127.0.0.1",port=11211):
        print("----------- MC")
        try:
            self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            #self.init()
        except Exception as e:
            print("Exception",e)

        # def init(self):
        data = {}
        start = time.time()
        delta = start
        index = self.mc.get("index")
        if index:
            for i in index:
                print("key",i)

        self.fader_map = []
        for i in range(30+1):
            self.fader_map.append({"UNIV":0,"DMX":0})

        try:
            f = open("/home/user/LibreLight/fader.json")
            lines = f.readlines()
            for i,line in enumerate(lines):
                jdata = json.loads(line)
                print("fader_map ->>",i,jdata)
                self.fader_map[i] = jdata

        except Exception as e:
            print("Except Fader_map",e)
        #exit()

    def ok(self):
        if self.mc: 
            return 1
        return 0

    def test(self):
        if not self.ok():
            return 
        self.mc.set("some_key", "Some value")
        self.value = mc.get("some_key")

        self.mc.set("another_key", 3)
        self.mc.delete("another_key")

    def loop(self):
        thread.start_new_thread(self._loop,())
        if not self.ok():
            return 

    def _loop(self):
        print("++++++++++ start.memcachd read loop",self )
        while 1:
            send = 0
            #print("+")
            try:
                ip="10.10.10.13:0"
                #ip="ltp-out:0"
                #print(ip)
                x=self.mc.get(ip)
                
                if x:
                    #print(ip,x)
                    #val = x[501-1]
                    #val = x[141-1]
                    for i, line in enumerate(self.fader_map):
                        try:
                            #print(i,line)
                            dmx = int(line["DMX"])
                            if dmx > 0:
                                val = x[dmx-1]
                                #print("mc val",val)
                                set_exec_fader(i,val,color="#aaa")
                        except:pass

                time.sleep(0.01)
            except Exception as e:
                print("exc", e)
                time.sleep(1)

_mc=MC()
_mc.loop()
#time.sleep(1)
#exit()

jclient = chat.tcp_sender()#port=50001)
import zlib
def jclient_send(data):
    t_start = time.time()
    jtxt = data
    jdatas = []
    for jdata in data:
        if "CMD" in jdata:
            try:
                jdatas.append(jdata)
            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint("-----",color="red")
        elif "DMX" in jdata:
            try:
                dmx = int(jdata["DMX"])
                if int(dmx) >= 1: # ignore DMX lower one
                    if "FIX" in jdata and "ATTR" in jdata:    
                        fix = jdata["FIX"]
                        attr = jdata["ATTR"]
                        # find dmx-fine channel
                        jdata["DMX-FINE"] = FIXTURES.get_dmx(fix,attr+"-FINE")
                    jdatas.append(jdata)
                else:
                    cprint("jclient_send, ignore DMX ",jdata["DMX"],color="red")
            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint(e,color="red")
                cprint("-----",color="red")
            
    jtxt = jdatas
    jtxt = json.dumps(jtxt)
    jtxt = jtxt.encode()
    #jtxt = zlib.compress(jtxt)
    jclient.send( jtxt ) #b"\00 ")
    #print(round((time.time()-t_start)*1000,4),"milis")
    cprint("{:0.04} sec.".format(time.time()-t_start),color="yellow")
    cprint("{:0.04} tick".format(time.time()),color="yellow")


def _highlight(fix,_attr="DIM"): 
    " patch test button "
    print("highlight",fix,"1")

    if fix not in FIXTURES.fixtures:
        return None

    d = FIXTURES.fixtures[fix]

    #for k,v in d.items():
    #    print("-",k,v)
    DMX = d["DMX"] + d["UNIVERS"]*512
    if "ATTRIBUT" in d:
        ATTR= d["ATTRIBUT"]
        data = {"VALUE":200,"DMX":1}
        attr = ""

        if _attr in ATTR:
            attr = _attr
        else:
            return #stop
        
    
        print(attr,ATTR[attr])
        old_val = ATTR[attr]["VALUE"]
        data["DMX"] = DMX + ATTR[attr]["NR"]-1
        print(attr,ATTR[attr])
        print(data)
        for i in range(3):
            print("highlight",fix,"0")
            data["VALUE"] = 100
            jclient_send([data])
            time.sleep(0.1)

            print("highlight",fix,"1")
            data["VALUE"] = 234
            jclient_send([data])
            time.sleep(0.3)

        
        print("highlight",fix,"0")
        data["VALUE"] = old_val 
        jclient_send([data])

def highlight2(fix,attr="DIM"):
    def x():
        highlight(fix,attr=attr)
    return x

def highlight(fix):
    print("highlight",fix)
    thread.start_new_thread(_highlight,(fix,"DIM"))
    thread.start_new_thread(_highlight,(fix,"RED"))
    thread.start_new_thread(_highlight,(fix,"GREEN"))
    thread.start_new_thread(_highlight,(fix,"BLUE"))

class ValueBuffer():
    def __init__(self,_min=0,_max=255):
        self._value = 2
        self._on = 1
        self._min=_min
        self._max=_max
    def check(self):
        if self._value < self._min:
            self._value = self._min
        elif self._value > self._max:
            self._value = self._max

    def inc(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value += round(value,4)
            else:
                self._value += value
        self.check()
        return self._value
    def val(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value = round(value,4)
            else:
                self._value = value
        self.check()
        return self._value
    def on(self):
        self._on = 1
    def off(self):
        self._on = 0
    def _is(self):
        if self._on:
            return 1
        return 0

FADE = ValueBuffer()  #2 #0.1 #1.13
FADE.val(2.0)
FADE_move = ValueBuffer()  #2 #0.1 #1.13
FADE_move.val(4.0)

DELAY = ValueBuffer()  #2 #0.1 #1.13
DELAY.off()
DELAY.val(0.2)

fx_prm_move = {"SIZE":40,"SPEED":8,"OFFSET":100,"BASE":"0","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":100}

fx_prm      = {"SIZE":255,"SPEED":10,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":1,"SHUFFLE":0,"WING":2,"WIDTH":25,"FX-X":1,"FX:MODE":0}
fx_x_modes    = ["spiral","left","right","up","down","left_right","up_down"]

fx_modes    = ["RED","GREEN","BLUE","MAG","YELLOW","CYAN"]
fx_mo       = ["fade","on","rnd","ramp","ramp2","cosinus","sinus"]

class FX_handler():
    def __init__():
        pass



def reshape_preset(data ,value=None,xfade=0,flash=0,ptfade=0):

    f=0 #fade

    out = []
    delay=0
    for row in data:
        #cprint("reshape_preset in:",row)
        line = {}
        line["DELAY"]=delay
        if type(value) is float:
            line["VALUE"] = value #round(value,3)
        else:
            line["VALUE"] = value

        if value is not None: 
            line["FX"] = row["FX"].split(":",1)[-1]
        else:
            line["FX"] = row["FX"]

        if row["FX2"]:
            line["FX2"] = row["FX2"]

        if row["FIX"]:
            line["FIX"] = row["FIX"]
        if row["ATTR"]:
            line["ATTR"] = row["ATTR"]


        if row["VALUE"] is not None:
            if value is None: 
                v=row["VALUE"]
                if type(v) is float:
                    line["VALUE"]  = v #round(v,3)
                else:
                    line["VALUE"]  = v

        if row["ATTR"] in ["PAN","TILT"]:
            f = ptfade 

        for a in ["DIM","ZOOM","FOCUS","RED","GREEN","BLUE","WHITE","AMBER","IRIS","BLADE"]: 
            #FADE ATTRIBUTES
            if a in row["ATTR"]:
                f = xfade 
                break

        if flash:
            xfade = 0
        if type( f ) is float:
            line["FADE"] = round(f,4)
        else:
            line["FADE"] = f
        
        if 0:
            cprint("reshape_preset j",line,color="red") 
        #cprint("reshape_preset out:",line)
        out.append(line)
        if DELAY._is():
            delay+=DELAY.val()/100 #0.02
    return out

class dummy_event():
    def __init__(self):
        self.num =0
        self.type = 4 #press 5 release
        self.set_value=-1


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

cprint("________________________________")
 
def process_wings(xfixtures):
    """process the wing's of selected fixtures
    input: [1,2,3,4,10,12,13,14]
    if WING = 2 return: [[1,2,3,4][14,13,12,10]]
    """
    wing_buffer = []
    fix_count = len(xfixtures)
    prm = fx_prm # ToDo:  global WING for PAN/TILE !? ATTRIBUT is not availible in this moment 

    if prm["WING"] > 1 and fix_count > 1:
        wing_count = fix_count // prm["WING"]
        number_of_fix_in_wing = fix_count // wing_count

        if number_of_fix_in_wing < 2:
            number_of_fix_in_wing = 2

        for i in range(number_of_fix_in_wing):
            j = i*wing_count
            wing = xfixtures[j:j+wing_count]
            if i%2!=0:
                wing = wing[::-1]
            print("wing",i,"j",j,"wing_count:",wing_count,"wing",wing)
            wing_buffer.append(wing)

        if fix_count > j+wing_count: # append Fixtures Left over
            wing = xfixtures[j+wing_count:]
            wing_buffer.append(wing)
    else:
        wing_buffer.append(xfixtures)

    if prm["SHUFFLE"]:
        _wing_buffer = []
        for wing in wing_buffer:
            wing = wing[:]
            random.shuffle(wing)
            _wing_buffer.append(wing)
        wing_buffer = _wing_buffer
    return wing_buffer

def process_effect(wing_buffer,fx_name=""):
    jdatas = []
    offset = 0
    offset_move = 0
    start = fx_prm["START"]
    base  = fx_prm["BASE"]

    for wing in wing_buffer:
        count_of_fix_in_wing = len(wing)
        coffset= 0 # 1024/count_of_fix_in_wing * (offset/255)
        coffset_move=0
    
        for fix in wing:
            if fix not in FIXTURES.fixtures:
                continue
            data = FIXTURES.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                jdata = {"MODE":"FX"}
                jdata["VALUE"] = None
                jdata["FIX"] = fix
                jdata["DMX"] = FIXTURES.get_dmx(fix,attr)
                jdata["DMX-FINE"] = FIXTURES.get_dmx(fix,attr+"-FINE")
                jdata["ATTR"] =attr
                if attr.endswith("-FINE"):
                    continue
                if attr in ["PAN","TILT"]:
                    csize  = fx_prm_move["SIZE"]
                    cspeed = fx_prm_move["SPEED"]
                    cstart = fx_prm_move["START"]
                    cbase  = fx_prm_move["BASE"]
                    width  = fx_prm_move["WIDTH"]
                    invert = fx_prm_move["INVERT"]
                    coffset_move= round(offset_move,1)
                else:
                    csize  = fx_prm["SIZE"]
                    cspeed = fx_prm["SPEED"]
                    cstart = fx_prm["START"]
                    cbase  = fx_prm["BASE"]
                    width  = fx_prm["WIDTH"]
                    invert = fx_prm["INVERT"]
                    coffset= round(offset,1)

                fx=""
                if "SIN" in fx_name:
                    fx = "sinus"
                elif "FD" in fx_name:
                    fx = "fade"
                elif "RND" in fx_name:
                    fx = "rnd"
                elif "ON" in fx_name:
                    fx = "on"
                elif "RAMP2" in fx_name:
                    fx = "bump2"
                    fx = "ramp2"
                elif "RAMP" in fx_name:
                    fx = "ramp"
                elif "COS" in fx_name:
                    fx = "cosinus"

                if fx:
                    if attr in ["PAN","TILT"]:
                        cprint("SKIP FX attr:{} fix:{} " .format(attr,fix) )
                        continue

                if fx:
                    if fx_prm["SPEED"] < 0:
                        fx = "off"
                else:
                    if ":DIM" in fx_name:
                        base=""
                        ffxb=fx_mo[fx_prm["MO"]] 
                        #ffxb= "cosinus" 
                        if attr == "DIM":
                            if fx_prm["SPEED"] < 0:
                                fx = "off"
                            else:
                                fx = ffxb #"fade"
                    elif ":TILT" in fx_name:
                        base=""
                        if attr == "PAN":
                            fx = "off"
                        if attr == "TILT":
                            if fx_prm["SPEED"] < 0:
                                fx = "off"
                            else:
                                fx = "sinus"
                    elif ":PAN" in fx_name:
                        base=""
                        if attr == "PAN":
                            if fx_prm_move["SPEED"] < 0:
                                fx = "off"
                            else:
                                fx = "cosinus" 
                        if attr == "TILT":
                           fx = "off"
                    elif ":CIR" in fx_name:
                        base=""
                        if attr == "PAN":
                            if fx_prm_move["SPEED"] < 0:
                                fx = "off"
                            else:

                                fx = "cosinus" 
                        if attr == "TILT":
                            if fx_prm["SPEED"] < 0:
                                fx = "off"
                            else:
                                fx = "sinus"
                    elif ":RED" in fx_name:

                        ffxb= fx_mo[fx_prm["MO"]] 
                        ffx= "off" #fx_mo[fx_prm["MO"]] 
                        if "RED" in fx_modes[fx_prm["MODE"]]:#
                            base="-"
                            if attr == "RED":
                                fx=ffx
                            if attr == "GREEN":
                                fx = ffxb# "off"
                            if attr == "BLUE":
                                fx =  ffxb#"off"
                        elif "GREEN" in fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#in fx_name:
                            base="-"
                            if attr == "RED":
                                fx =  ffxb#"off" 
                        elif "GREEN" in fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#in fx_name:
                            if attr == "GREEN":
                                fx = ffxb# "off"
                                fx=ffx
                            if attr == "BLUE":
                                fx =  ffxb#"off"
                        elif "BLUE" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#fx_name:
                            base="-"
                            if attr == "RED":
                                fx = ffxb# "off" 
                            if attr == "GREEN":
                                fx = ffxb# "off"
                            if attr == "BLUE":
                                fx = ffxb# "off"
                                fx=ffx
                        elif "YELLOW" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#fx_name:
                            base="-"
                            if attr == "RED":
                                fx = ffxb# "off" 
                                fx=ffx
                            if attr == "GREEN":
                                fx = ffxb# "off"
                                fx=ffx
                            if attr == "BLUE":
                                fx = "off"
                        elif "CYAN" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#fx_name:
                            base="-"
                            if attr == "RED":
                                fx = ffxb# "off" 
                            if attr == "GREEN":
                                fx = ffxb# "off"
                                fx=ffx
                            if attr == "BLUE":
                                fx = ffxb# "off"
                                fx=ffx
                        elif "MAG" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#fx_name:
                            base="-"
                            if attr == "RED":
                                fx = ffxb# "off" 
                                fx=ffx
                            if attr == "GREEN":
                                fx = ffxb# "off"
                            if attr == "BLUE":
                                fx = ffxb# "off"
                                fx=ffx
                        else:
                            cprint("FX: unbekant",fx_modes[fx_prm["MODE"]],color="red")

                    fxtype = fx

                fxtype = fx

                if "FX" not in data["ATTRIBUT"][attr]:
                    data["ATTRIBUT"][attr]["FX"] =""
                if "FX2" not in data["ATTRIBUT"][attr]:
                    data["ATTRIBUT"][attr]["FX2"] ={}

                if data["ATTRIBUT"][attr]["ACTIVE"] and fxtype:
                    #print("++ADD FX",fix,attr,fx)
                    #data["ATTRIBUT"][attr]["FX"] = fx #"sinus:40:100:10"
                    fjdata = {}
                    if cspeed < 0.1:
                        fjdata["TYPE"]  = "off"
                    else:
                        fjdata["TYPE"]  = fxtype
                    fjdata["SIZE"] = round(csize,2)
                    fjdata["SPEED"] = round(cspeed,2)
                    fjdata["WIDTH"] = int(width)
                    fjdata["START"] = cstart
                    if attr in ["PAN","TILT"]:
                        fjdata["OFFSET"]= round(coffset_move,2)
                    else:
                        fjdata["OFFSET"]= round(coffset,2)
                    fjdata["INVERT"]= int(invert)
                    fjdata["BASE"]  = cbase
                    jdata["FX2"] = fjdata
                    data["ATTRIBUT"][attr]["FX2"] = fjdata
                    jdatas.append(jdata)

            
            if fx_prm_move["OFFSET"] > 0.5: # and 
                aoffset_move = (100/count_of_fix_in_wing) * (fx_prm_move["OFFSET"]/100) 
                if fx_prm_move["DIR"] <= 0:
                    offset_move -= aoffset_move 
                else:
                    offset_move += aoffset_move 
                offset_move = round(offset_move,2)

            if fx_prm["OFFSET"] > 0.5: # and 
                aoffset = (100/count_of_fix_in_wing) * (fx_prm["OFFSET"]/100) 
                if fx_prm["DIR"] <= 0:
                    offset -= aoffset 
                else:
                    offset += aoffset 
                offset = round(offset,2)

    if jdatas and not modes.val("BLIND"):
        jclient_send(jdatas)
    master.refresh_fix()

    return jdatas

def process_matrix(xfixtures):
    fix_count = len(xfixtures)
    fx_x = fx_prm["FX-X"]
    fx_mod = fx_x_modes[fx_prm["FX:MODE"]]
    print("----",fx_x,fx_mod)
    if fx_x > 1 and fix_count > fx_x:
        try: 
            from lib import matrix
            w=fx_x
            h=int(fix_count/fx_x)

            if fx_mod == "spiral":
                _map = matrix.spiral(w,h)
            elif fx_mod == "up_down":
                _map = matrix.up_down(w,h)
            elif fx_mod == "left_right":
                _map = matrix.left_right(w,h)
            elif fx_mod == "left":
                _map = matrix.left(w,h)
            elif fx_mod == "right":
                _map = matrix.right(w,h)
            elif fx_mod == "up":
                _map = matrix.up(w,h)
            elif fx_mod == "down":
                _map = matrix.down(w,h)
            else:
                return xfixtures # do nothing

            matrix.mprint(xfixtures,w,h)
            out = ["0"]*(w*h)
            for i,f in enumerate(xfixtures):
                if i < w*h:
                    j = int(_map[i])
                    print([i,f,j])
                    out[j] = f

            matrix.mprint(out,w,h)
            xfixtures = out
        except Exception as e:
            print("matrix exception",e)

    return xfixtures

class Xevent_fx():
    """ global input event Handeler for short cut's ... etc
    """
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data = data
        self.attr = attr
        self.elem = elem
        self.mode = mode

    def fx(self,event):
        cprint("Xevent.fx",self.attr,self.fix,event)
        fx2 = {}
        if event.num == 4:
            cprint("FX:COLOR CHANGE",fx_prm,color="red")
            txt = "FX:RED" 
            fx_prm["MODE"] += 1
            if fx_prm["MODE"] >= len(fx_modes):
                fx_prm["MODE"]=0
            txt = "FX:\n"+fx_modes[fx_prm["MODE"]]

            master.fx.elem["FX:RED"]["text"] = txt
        elif event.num == 5:
            cprint("FX:COLOR CHANGE",fx_prm,color="red")
            txt = "FX:RED" 
            fx_prm["MODE"] -= 1
            if fx_prm["MODE"] < 0:
                fx_prm["MODE"]= len(fx_modes)-1
            txt = "FX:\n"+fx_modes[fx_prm["MODE"]]
            master.fx.elem["FX:RED"]["text"] = txt

        if event.num == 4:
            cprint("FX-X: CHANGE",fx_prm,color="red")
            txt = "FX-X:" 
            fx_prm["FX:MODE"] += 1
            if fx_prm["FX:MODE"] >= len(fx_x_modes):
                fx_prm["FX:MODE"]=0
            txt = "FX:MODE\n"+fx_x_modes[fx_prm["FX:MODE"]]

            master.fx.elem["FX:MODE"]["text"] = txt
        elif event.num == 5:
            cprint("FX-X: CHANGE",fx_prm,color="red")
            txt = "FX-X:" 
            fx_prm["FX:MODE"] -= 1
            if fx_prm["FX:MODE"] < 0:
                fx_prm["FX:MODE"]= len(fx_x_modes)-1
            txt = "FX:MODE\n"+fx_x_modes[fx_prm["FX:MODE"]]
            master.fx.elem["FX:MODE"]["text"] = txt

        elif event.num == 1:
            xfixtures = []
            fix_active =FIXTURES.get_active() 
            for fix in fix_active:
                if fix == "CFG":
                    continue
                xfixtures.append(fix)

            if not xfixtures:
                cprint("470 fx() ... init no fixture selected",color="red")
                return 0
            
            
            xfixtures = process_matrix(xfixtures)
            wing_buffer = process_wings(xfixtures)
            process_effect(wing_buffer,fx_name=self.attr)


    def command(self,event,mode=""):       
        cprint("fx_command",self.mode)
        if self.mode == "FX":
            prm = fx_prm
            ct = self.data.fx 
        if self.mode == "FX-MOVE":
            prm = fx_prm_move
            ct = self.data.fx_moves 

        if 1:
            if self.attr.startswith("SIZE:"):#SIN":
                #global fx_prm
                k = "SIZE"
                if event.num == 1:
                    prm[k] =30
                elif event.num == 3:
                    prm[k] =100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] +=5
                elif event.num == 5:
                    prm[k] -=5
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 0:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5
                ct.elem[self.attr]["text"] = "SIZE:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("SPEED:"):#SIN":
                #global prm
                k = "SPEED"
                if event.num == 1:
                    prm[k] = 6
                elif event.num == 3:
                    prm[k] = 60
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 0.06
                    elif prm[k] < 5:
                        prm[k] *=1.2
                    else:
                        prm[k] +=5 #1.1
                elif event.num == 5:
                    if prm[k] <= 5:
                        prm[k] *=0.8
                    else:
                        prm[k] -= 5 #1.1
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 0.05:
                    prm[k] =0
                if prm[k] > 5 and prm[k] < 10: #bug
                    prm[k] =5

                if prm[k] < 0:
                    ct.elem[self.attr]["text"] = "SPEED:\noff".format(prm[k])
                else:
                    ct.elem[self.attr]["text"] = "SPEED:\n{:0.02f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("START:"):#SIN":
                #global prm
                k = "START"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] += 5 #1.1
                elif event.num == 5:
                    prm[k] -= 5 #1.1
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 5:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5

                ct.elem[self.attr]["text"] = "START:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("WIDTH:"):#SIN":
                #global prm
                k = "WIDTH"
                if event.num == 1:
                    prm[k] = 25
                elif event.num == 2:
                    prm[k] = 50
                elif event.num == 3:
                    prm[k] = 100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    elif prm[k] == 50:
                        prm[k] = 100
                    elif prm[k] == 5:
                        prm[k] = 25
                    elif prm[k] == 25:
                        prm[k] = 50
                    else:
                        prm[k] += 5 #*=1.1
                elif event.num == 5:
                    if prm[k] == 10:
                        prm[k] = 5
                    elif prm[k] == 25:
                        prm[k] = 10
                    elif prm[k] == 50:
                        prm[k] = 25
                    elif prm[k] == 100:
                        prm[k] = 50
                    #else:
                    #    prm[k] -=5 #/=1.1
                    
                #prm[k] =int(prm[k])
                
                if prm[k] < 0:
                    prm[k] = 0
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] == 6: #bug
                    prm[k] =5
                if prm[k] > 25 and prm[k] < 50: #bug
                    prm[k] =50
                if prm[k] > 50 and prm[k] < 100: #bug
                    prm[k] =100

                ct.elem[self.attr]["text"] = "WIDTH:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("DIR:"):#SIN":
                #global prm
                k = "DIR"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = -1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =-1
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "DIR:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("SHUFFLE:"):#SIN":
                #global prm
                k = "SHUFFLE"
                if event.num == 1:
                    prm[k] = 0
                elif event.num == 3:
                    prm[k] = 1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =0
                if prm[k] == 6: #bug ?
                    prm[k] =5
                ct.elem[self.attr]["text"] = k+":\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("INVERT:"):#SIN":
                #global prm
                k = "INVERT"
                if event.num == 1:
                    prm[k] = 0
                elif event.num == 3:
                    prm[k] = 1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =0
                if prm[k] == 6: #bug ?
                    prm[k] =5
                ct.elem[self.attr]["text"] = k+":\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("FX-X:"):#SIN":
                #global prm
                k = "FX-X"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = 2
                elif event.num == 4:
                    prm[k] += 1
                elif event.num == 5:
                    prm[k] -=1
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] < 1:
                    prm[k] =1
                    
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "FX-X:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("WING:"):#SIN":
                #global prm
                k = "WING"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = 2
                elif event.num == 4:
                    prm[k] += 1
                elif event.num == 5:
                    prm[k] -=1
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] < 1:
                    prm[k] =1
                    
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "WING:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("OFFSET:"):#SIN":
                #global prm
                k = "OFFSET"
                if event.num == 1:
                    prm[k] = 50
                elif event.num == 2:
                    prm[k] *= 2
                elif event.num == 3:
                    prm[k] = 100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] +=5 #*=1.1
                elif event.num == 5:
                    prm[k] -=5 #/=1.1
                #prm[k] =int(prm[k])
                
                #if prm[k] > 512:
                #    prm[k] = 512
                if prm[k] < 5:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5

                ct.elem[self.attr]["text"] = "OFFSET:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("BASE:"):
                k = "BASE"
                if event.num == 1:
                    prm[k] = "-"
                elif event.num == 3:
                    prm[k] = "0"
                elif event.num == 4:
                    prm[k] = "+"
                elif event.num == 5:
                    prm[k] = "0"
                ct.elem[self.attr]["text"] = "BASE:\n{}".format(prm[k])
            elif self.attr.startswith("FX:"):#SIN":
                self.fx(event)

            elif self.attr == "FX OFF":
                if event.num == 1:
                    FIXTURES.fx_off("all")
                    CONSOLE.fx_off("all")
                    CONSOLE.flash_off("all")
                    master.refresh_fix()
                    return 0

                #if event.num == 1:
            elif self.attr == "REC-FX":
                print("ELSE",self.attr)
                modes.val(self.attr,1)

            return 0
            
    def cb(self,event):
        cprint("EVENT_fx cb",self.attr,self.mode,event,color='yellow')
        print(["type",event.type,"num",event.num])
        try:
            change = 0

            if self.mode.startswith("FX"):
                self.command(event)
                return 0

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        return 1 
        
def save_window_position(save_as=""):
    try:
        base = Base()
        fname = "/home/user/LibreLight"
        fname = base.show_path1 +base.show_name 
        if save_as:
            fname = save_as 
        fname +=  "/gui.txt"
        print("save_window_position",fname)
        f = open(fname,"w")
        for k,win in window_manager.windows.items():
            print("save:win:pos",win,k)
            if not win:
                continue
            #print("d",dir(win))
            #print("winfo",k,win.tk.geometry())
            line="{} {}\n".format(k,win.tk.geometry())
            #print("> ",[line])
            f.write( line )
            f.flush()
        f.close()
    except Exception as e:
        cprint("save_window_position Exception:",e,color="red")
        return 

def save_window_position_loop(): # like autosave
    def loop():
        time.sleep(20)
        try:
            while 1:
                save_window_position()
                time.sleep(60)
        except Exception as e:
            print("save_loop",e)
    thread.start_new_thread(loop,())

def load_window_position():
    try:
        base = Base()
        fname = "/home/user/LibreLight"
        fname = base.show_path1 +base.show_name 
        fname +=  "/gui.txt"
        print("load_window_position",fname)
        f = open(fname,"r")
        data = {}
        for line in f.readlines():
            line = line.strip()
            if " " in line:
                k,geo = line.split(" ",1)
                data[k] = geo

        for k,win in window_manager.windows.items():
            if not win:
                continue
            if k in data:
                try:
                    #print("> ",[k,data[k]])
                    win.tk.geometry(data[k])
                except Exception as e:
                    cprint("load_window_position Exception:",e,color="red")
            #print("winfo",k,win.tk.geometry())
        f.close()
    except Exception as e:
        cprint("load_window_position Exception:",e,color="red")
        return 
 
class Xevent():
    """ global input event Handeler for short cut's ... etc
    """
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode


    def setup(self,event):       
        cprint("xevent.SETUP",[self.mode,self.attr],color="red")
        if self.mode == "SETUP":
            if self.attr == "SAVE\nSHOW":
                self.elem["bg"] = "orange"
                self.elem["text"] = "SAVING..."
                self.elem["bg"] = "red"
                tkinter.Tk.update_idletasks(gui_menu_gui.tk)
                #self.elem["fg"] = "orange"
                self.elem.config(activebackground="orange")
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()
                save_window_position()
                #time.sleep(1)
                #modes.val(self.attr,0)
                self.elem["bg"] = "lightgrey"
                #self.elem["fg"] = "lightgrey"
                self.elem.config(activebackground="lightgrey")
            elif self.attr == "LOAD\nSHOW":
                name = "LOAD-SHOW"
                base = Base()
                line1 = "PATH: "+base.show_path1 +base.show_name
                line2 = "DATE: "+ time.strftime("%Y-%m-%d %X",  time.localtime(time.time()))
                class cb():
                    def __init__(self,name=""):
                        self.name=name
                        print("cb",name)
                    def cb(self,event=None,**args):
                        print("cdb",self.name,event,args)
                        if self.name != "<exit>":
                            print("-----------------------:")
                            LOAD_SHOW_AND_RESTAT(self.name).cb()
                        #self.elem["bg"] = "lightgrey"
                        #self.elem.config(activebackground="lightgrey")

                pw = PopupList(name,cb=cb)
                frame = pw.sframe(line1=line1,line2=line2)
                r = _load_show_list(frame,cb=cb)

    
                #self.elem["bg"] = "red"# "lightgrey"
                #self.elem.config(activebackground="red")
                #self.elem.config(activebackground="lightgrey")
                #w.tk.attributes('-topmost',False)
            elif self.attr == "SAVE\nSHOW AS":
                base = Base()

                #def _cb(fname):
                def _cb(data):
                    fname = data["Value"]
                    print(self,"save_show._cb()",fname)
                    fpath,fname = base.build_path(fname)
                    cprint("SAVE AS",fpath,fname)
                    if base._create_path(fpath):
                        a=PRESETS.backup_presets(save_as=fpath)
                        b=FIXTURES.backup_patch(save_as=fpath)
                        #base._set(fname)
                        
                        save_window_position(save_as=fpath)
                        LOAD_SHOW_AND_RESTAT(fname).cb() 
                dialog._cb = _cb
                dialog.askstring("SAVE SHOW AS","SAVE SHOW AS:")
            elif self.attr == "SAVE &\nRESTART":
                self.elem["bg"] = "orange"
                self.elem["text"] = "SAVING..."
                self.elem["bg"] = "red"
                tkinter.Tk.update_idletasks(gui_menu_gui.tk)
                #self.elem["fg"] = "orange"
                self.elem.config(activebackground="orange")
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()

                save_window_position()
                self.elem["text"] = "RESTARTING..."
                #time.sleep(1)
                #modes.val(self.attr,0)
                self.elem["bg"] = "lightgrey"
                #self.elem["fg"] = "lightgrey"
                self.elem.config(activebackground="lightgrey")
                LOAD_SHOW_AND_RESTAT("").cb(force=1)
            elif self.attr == "DRAW\nGUI":
                #self.elem["bg"] = "orange"
                old_text = self.elem["text"]
                self.elem["text"] = "DRAWING..."
                #self.elem["bg"] = "red"
                #time.sleep(0.05)
                #print("redraw",name)
                #if name == "PATCH":
                #    gui_patch.draw()
                #if name == "DIMMER":
                #    gui_fix.draw()
                self.elem["text"] = "PATCH..."
                window_manager.top("PATCH")
                gui_patch.draw(FIXTURES)
                self.elem["text"] = "FIX..."
                gui_fix.draw(FIXTURES)
                window_manager.top("FIXTURES")
                master._refresh_exec()
                self.elem["text"] = old_text  
            else:
                r=tkinter.messagebox.showwarning(message="{}\nnot implemented".format(self.attr.replace("\n"," ")),parent=None)
        return 1

    def live(self,event):       
        if self.mode == "LIVE":
                    
            if "FADE" in self.attr or "DELAY" in self.attr:
               
                if self.attr == "FADE":
                    ct = FADE
                if self.attr == "DELAY":
                    ct = DELAY
                if "PAN/TILT\nFADE" in self.attr:
                    ct = FADE_move

                value = ct.val()
                #print("EVENT CHANGE ",[self.attr])
                print("EVENT CHANGE:",self.mode,value,self.attr)
                if value < 0.01:
                    ct.val(0.01)
                elif value > 100.0:
                    pass #value = 100
                if event.num == 4:
                    value *= 1.1
                elif event.num == 5:
                    value /= 1.1
                elif event.num == 1:
                    if ct._is():
                        ct.off()# = 0
                        self.data.commands.elem[self.attr]["bg"] = "grey"
                        self.elem.config(activebackground="grey")
                    else:
                        ct.on()# = 1
                        self.data.commands.elem[self.attr]["bg"] = "green"
                        self.elem.config(activebackground="lightgreen")
                elif event.num == 2:
                    if value > 1 and value < 4:
                        value = 4
                    elif value > 3 and value < 6:
                        value = 6
                    elif value > 5 and value < 7:
                        value = 8
                    elif value > 7 and value < 9:
                        value = 10
                    elif value > 9:
                        value = 0.01
                    elif value < 1:
                        value = 1.1
                value = round(value,3)
                value = ct.val(value)

                if self.attr == "FADE":
                    self.data.commands.elem[self.attr]["text"] = "FADE:\n{:0.2f}".format(value)
                if self.attr == "DELAY":
                    self.data.commands.elem[self.attr]["text"] = "DELAY:\n{:0.3f}".format(value)
                if "PAN/TILT\nFADE" in self.attr:
                    self.data.commands.elem[self.attr]["text"] = "PAN/TILT\nFADE:{:0.2f}".format(value)



    def command(self,event):       
        if self.mode == "COMMAND":
            
            if self.attr == "CLEAR":
                if event.num == 1:
                    ok = FIXTURES.clear()
                    if ok:
                        master.refresh_fix()
                    modes.val(self.attr,0)


            elif self.attr == "SAVE":
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()
                #time.sleep(1)
                modes.val(self.attr,0)
            elif self.attr == "S-KEY":
                global _global_short_key
                if _global_short_key:
                    _global_short_key = 0
                    master.commands.elem["S-KEY"]["bg"] = "red"
                    master.commands.elem["S-KEY"]["activebackground"] = "red"
                else:
                    _global_short_key = 1
                    master.commands.elem["S-KEY"]["bg"] = "green"
                    master.commands.elem["S-KEY"]["activebackground"] = "green"
                print("s-key",_global_short_key)
            else:
                if event.num == 1:
                    print("ELSE",self.attr)
                    modes.val(self.attr,1)

            return 0


    def encoder(self,event):
        global _shift_key
        cprint("Xevent","ENC",self.fix,self.attr,self.mode)
        cprint("SHIFT_KEY",_shift_key,"??????????")

        if self.mode == "ENCODER":
            if self._encoder(event):
                #master._refresh_fix() # now
                master.refresh_fix() # delayed
                #master._refresh_fix() # now

        if self.mode == "ENCODER2":
            if self._encoder(event):
                master.refresh_fix() # delayed

    def _encoder(self,event):
        global _shift_key
        if 1: #self.mode == "ENCODER" or self.mode == "ENCODER2":
            cprint("-- Xevent","_ENC",self.fix,self.attr,self.mode)
            cprint("-- SHIFT_KEY",_shift_key,"??????????")
            #cprint(self.data)
            val=""
            if event.num == 1:
                val ="click"
            elif event.num == 4:
                val ="++"
                if _shift_key:
                    val = "+"
            elif event.num == 5:
                val ="--"
                if _shift_key:
                    val = "-"
            print("SHIFT",val,_shift_key)
            if val:
                #if self.attr == "DIM" and self.fix == 0 and val == "click":
                #if self.fix == 0 and val == "click":
                #if self.attr == "DIM" and self.fix == 0 and val == "click":
                #if self.attr == "DIM" and self.fix == 0 and val == "click":
                #    pass    
                #else:

                FIXTURES.encoder(fix=self.fix,attr=self.attr,xval=val)
                return 1       

            #if self.mode == "ENCODER": # fast refresh
            #     master._refresh_fix()
            #else: #"ENCODER2" slow refresh
            #     master.refresh_fix()
            #     #master._refresh_fix()

            
    def cb(self,event):
        cprint("EVENT cb",self.attr,self.mode,event,color='yellow')
        print(["type",event.type,"num",event.num])
        try:
            change = 0
            if "keysym" in dir(event):
                if "Escape" == event.keysym:
                    ok = FIXTURES.clear()
                    master.refresh_fix()
                    return 0

            if self.mode == "SETUP":
                self.setup(event)
            elif self.mode == "COMMAND":
                self.command(event)
            elif self.mode == "LIVE":
                self.live(event)
            elif self.mode == "ENCODER":
                self.encoder(event)
            elif self.mode == "ENCODER2":
                self.encoder(event)
            elif self.mode == "FX":
                cprint("Xevent CALLING FX WRONG EVENT OBJECT !!",color="red")
            elif self.mode == "ROOT":
                if event.keysym=="Escape":
                    pass

            elif self.mode == "INPUT":
                print("INP",self.data.entry.get())
                if event.keycode == 36:
                    x=self.data.entry.get()
                    #client.send(x)

            elif self.mode == "INPUT2":
                print("INP2",self.data.entry2.get())
                if event.keycode == 36:
                    x=self.data.entry2.get()
                    #client.send(x)

            elif self.mode == "INPUT3":
                print("INP3",self.data.entry3.get())
                if event.keycode == 36:
                    x=self.data.entry3.get()
                    #client.send(x)

            elif self.mode == "PRESET":
                nr = self.attr #int(self.attr.split(":")[1])-1

                if event.num == 3: # right click for testing
                    if str(event.type) == '4': #4 ButtonPress
                        if modes.val("CFG-BTN"):
                            master.btn_cfg(nr,testing=1)

                if event.num == 1:
                    if str(event.type) == '4': #4 ButtonPress
                        if modes.val("REC"):
                            self.data.preset_rec(nr)
                            modes.val("REC",0)
                        elif modes.val("DEL"):
                            ok=PRESETS.delete(nr)
                            if ok:
                                modes.val("DEL",0)
                                master.refresh_exec()
                        elif modes.val("COPY"):
                            ok=PRESETS.copy(nr)
                            if ok:
                                modes.val("COPY",0)
                                master.refresh_exec()
                        elif modes.val("MOVE"):
                            ok=PRESETS.move(nr)
                            if ok:
                                #modes.val("MOVE",0) # keep MOVE on
                                master.refresh_exec()
                        elif modes.val("CFG-BTN"):
                            master.btn_cfg(nr)

                        elif modes.val("LABEL"):#else:
                            master.label(nr)

                        elif modes.val("EDIT"):
                            FIXTURES.clear()
                            self.data.preset_select(nr)
                            self.data.preset_go(nr,xfade=0,event=event,val=255,button="go")
                            modes.val("EDIT", 0)
                            master.refresh_fix()

                        elif modes.val("SELECT"):
                            self.data.preset_select(nr)
                        else:
                            self.data.preset_go(nr,event=event,val=255)
                    else:
                        self.data.preset_go(nr,xfade=0,event=event,val=0)

                        
                if event.num == 3:
                    if not modes.val("REC"):
                        self.data.preset_go(nr,xfade=0,ptfade=0,event=event,val=255)
                        
                return 0
            elif self.mode == "INPUT":
                return 0

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        return 1 
        
def wheel(event,d=None):
    print("wheel",event,d)
    
import copy



class Element():
    def __init__(self):
        self.__data = {}
    def set(self,key,val):
        self.__data[key] = val

        
class Base():
    def __init__(self):
        cprint("Base.init()",color="red")
        self._init()

    def _init(self):
        show_name = "DemoShow"
        self.home = os.environ['HOME'] 
        self.show_path0 = self.home +"/LibreLight/"
        self.show_path  = self.show_path0 
        self.show_path1 = self.show_path0 + "show/"
        try:
            f = open(self.show_path+"init.txt","r")
            for line in f.readlines():
                #cprint(line)
                if not line.startswith("#"):
                    show_name = line.strip()
                    show_name = show_name.replace(".","")
                    show_name = show_name.replace("\\","")
                    show_name = show_name.replace("/","")
            self.show_name = show_name
        except Exception as e:
            cprint("show name exception",color="red")
            msg="Error Exception:{}".format(e)
            r=tkinter.messagebox.showwarning(message=msg,parent=None)
        finally:
            f.close()
        
        fpath = self.show_path1 +show_name 
        if not os.path.isdir(fpath):
            cprint(fpath)
            print( os.path.isdir(fpath))

            msg="'{}'\n Show Does Not Exist\n\n".format(show_name)
            msg += "please check\n"
            msg += "-{}init.txt\n".format(self.show_path0)
            msg += "-{}".format(self.show_path1)

            showwarning(msg=msg,title="Show Error")
            exit()

        self._check()
    def _set(self,fname):
        ok= os.path.isdir(self.show_path1+"/"+fname)
        ini = self.show_path0+"init.txt"
        print("SET SHOW NAME",fname,ok,ini)
        try:
            f = open( ini ,"r")
            lines = f.readlines()
            f.close()
            if len(lines) >= 10: # cut show history
                print("_set",ini,len(lines))
                lines = lines[-10:]
                f = open( ini ,"w")
                f.writelines(lines)
                f.close()
                exit()

        except:pass
        if ok:
            #self.show_name = fname
            f = open( ini ,"a")
            f.write(fname+"\n")
            f.close()
            return 1
        
    def _check(self):
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/show/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/" +self.show_name +"/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        pass
    def _list(self):
        #self._check()
        show_list =  list(os.listdir( self.show_path1 ))
        out = []
        for fname in show_list:
            #print(fname)
            ctime = os.path.getmtime(self.show_path1+fname)
            ctime = time.strftime("%Y-%m-%d %X",  time.localtime(ctime)) #1650748726.6604707))
            try:
                mtime = os.path.getmtime(self.show_path1+fname+"/patch.sav")
                mtime = time.strftime("%Y-%m-%d %X",  time.localtime(mtime)) #1650748726.6604707))
            except:
                mtime = 0

            if mtime:
                out.append([fname,mtime])#,ctime])

        from operator import itemgetter
        out=sorted(out, key=itemgetter(1))
        out.reverse()
        return out

    def _load(self,filename):
        xfname = self.show_path+"/"+str(filename)+".sav"
        print("load",xfname)

        try:
            f = open(xfname,"r")
            lines = f.readlines()
            f.close()    
        except Exception as e:
            msg = "Exception: {}".format(e)
            msg += "\n\ncheck\n-init.txt"
            cprint(msg,color="red")
            showwarning(msg=msg,title="load Error")

        data   = OrderedDict()
        labels = OrderedDict()
        i=0
        for line in lines:
            if line.count("\t") < 2:
                cprint("Error line.count('\\t') < 2  (is:{})".format(line.count("\t")),color="red",end=" ")
                cprint("file:{}".format(xfname),color="red")
                continue
            key,label,rdata = line.split("\t",2)
            key = int(key)

            jdata = json.loads(rdata,object_pairs_hook=OrderedDict)
            nrnull = 0

            if "ATTRIBUT" in jdata:  # translate old FIXTURES.fixtures start with 0 to 1          

                if nrnull:
                    print("DMX NR IS NULL",attr,"CHANGE +1")
                    for attr in jdata["ATTRIBUT"]:
                        if "NR" in jdata["ATTRIBUT"][attr]:
                            nr = jdata["ATTRIBUT"][attr]["NR"]
                            if nr >= 0:
                                jdata["ATTRIBUT"][attr]["NR"] +=1

            data[key] = jdata
            labels[key] = label
            
        return data,labels

    def _clean_path(self,fpath):
        _path=[]
        for i in fpath:
            fpath = fpath.replace(" ","_")
            if i in string.ascii_letters+string.digits+"äöüßÖÄÜ_-":
                _path.append(i)
        path = "".join(_path)
        return path

    def build_path(self,save_as):
        save_as = self._clean_path(save_as)
        path = self.show_path.split("/")
        path = "/".join(path[:-2])
        fpath = path+"/"+save_as
        return fpath,save_as

    def _create_path(self,fpath):
        if os.path.isdir(fpath):
            cprint("STOP SHOW EXIST !",color="red")
            return 0
        else:
            cprint("CREATE DIR ",fpath,color="green")
            os.mkdir(fpath)
        #self._set(save_as)
        return fpath

    def _backup(self,filename,data,labels,save_as):

        if save_as:
            xfname = save_as +"/"+str(filename)+".sav"
        else:
            xfname = self.show_path+"/"+str(filename)+".sav"

        print("backup",xfname)
        f = open(xfname,"w")
        for key in data:
            line = data[key]
            #print(line)
            label = "label" 
            if key in labels:
                label = labels[key]
            if label == "Name-"+str(key):
                label = ""
            #print(xfname,"load",key,label,len(line))

            f.write( "{}\t{}\t{}\n".format( key,label,json.dumps(line) ) )
        f.close()

        return 1


def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) 

class cb():
    def __init__(self,win):
        self.win = win
    def _callback(self,event):
        clobj=event.widget
        ## undermouse=find_withtag(master.CURRENT)
        undermouse=self.win.find_closest(self.win.CURRENT)
        print( repr(undermouse))
    def callback(self,event):
        print(__file__,self,"callback",event)
        cnv = self.win
        item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
        tags = cnv.gettags(item)
        #cnv.itemconfigure(self.tag, text=tags[0])
        print(tags,item)
        color = cnv.itemcget(item, "fill")
        cnv.itemconfig("all", width=1)#filla="green")
        cnv.itemconfig(item, width=3)#filla="green")
        print(color)
        print( hex_to_rgb(color[1:]))


class Elem_Container():
    def __init__(self):
        self.commands = []
        self.val = {}
        self.elem = {}

class MASTER():
    def __init__(self):
        #super().__init__() 
        self.base = Base ()
        self.load()
        self._XX = 0

        self.all_attr =["DIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.fx_moves = Elem_Container()
        self.fx_moves.commands =["REC-FX","FX OFF","\n"
                ,"FX:CIR","FX:PAN","FX:TILT", "WIDTH:\n100","DIR:\n0","INVERT:\n0","\n",
                "SHUFFLE:\n0","SIZE:\n","SPEED:\n","START:\n","OFFSET:\n","\n"
                ]
                #, "FX:SIN","FX:COS","FX:RAMP","FX:RAMP2","FX:FD","FX:ON","BASE:\n-"] #,"FX:RND" ]

        self.fx = Elem_Container()
        self.fx.commands =[
                "FX:DIM","FX:RED", "WIDTH:\n25","WING:\n2","DIR:\n1","INVERT:\n1","\n","SHUFFLE:\n0"
                ,"SIZE:\n","SPEED:\n","START:\n","OFFSET:\n","BASE:\n-","FX-X:\n-","FX:MODE"
                ]
        self.fx_generic = Elem_Container()
        self.fx_generic.commands =["FX:SIN","FX:COS","FX:RAMP","FX:RAMP2","FX:FD","FX:ON"] 

        self.commands = Elem_Container()
        self.commands.commands =["\n","ESC","CFG-BTN","LABEL","-","DEL","-","\n"
                ,"SELECT","FLASH","GO","-","MOVE","S-KEY","\n"
                ,"BLIND","CLEAR","REC","EDIT","COPY","-","\n" 
                ]
        self.elem_presets = {}
        
        for i in range(8*8*8):
            if i not in PRESETS.val_presets:
                name = "Preset:"+str(i+1)+":\nXYZ"
                #self.presets[i] = [i]
                PRESETS.val_presets[i] = OrderedDict() # FIX 
                PRESETS.val_presets[i]["CFG"] =  OrderedDict() # CONFIG 
                PRESETS.label_presets[i] = "-"

        modes.set_cb(self.xcb)
    def button_refresh(self,name,color,color2=None,text="",fg=None):
        cprint("button_refresh",name,color)
        #if color == "gold":
        #    color2 = "yellow"
        if color2 is None:
            color2 = color
        if text:
            text = "\n"+str(text)
        if name in self.commands.elem:
            self.commands.elem[name]["bg"] = color
            self.commands.elem[name]["text"] = name+ text
            self.commands.elem[name].config(activebackground=color2)
            if fg:
                self.commands.elem[name]["fg"] = fg
        elif name in self.fx.elem:
            #todo
            self.fx.elem[name]["bg"] = color
            self.fx.elem[name].config(activebackground=color2)
            if fg:
                self.fx.elem[name]["fg"] = fg

        # new version
        for elems in [self.fx_moves]:
            if name in elems.elem:
                elem = elems.elem[name]
                cprint("elem",elem)
                elem.config(bg = color)
                elem.config(text = name+text)
                elem.config(activebackground=color2)

                if fg and "fg" in elem:
                    elem["fg"] = fg

    def btn_cfg(self,nr,testing=0):
        cfg    = PRESETS._btn_cfg(nr) 
        button = PRESETS.btn_cfg(nr) 
        label  = PRESETS.label(nr) 

        def _cb(data):
            print(self,"btn_cfg._cb()",data)
            if data:

                if "Button" in  data and type(data["Button"]) is str:
                    txt = data["Button"]
                    PRESETS.btn_cfg(nr,txt)
                    self.elem_presets[nr].configure(text= PRESETS.get_btn_txt(nr))

                if "Label" in  data and type(data["Label"]) is str:
                    txt = data["Label"]
                    PRESETS.label(nr,txt) 
                    self.elem_presets[nr].configure(text= PRESETS.get_btn_txt(nr))

            modes.val("CFG-BTN",0)
            master._refresh_exec()
        dialog._cb = _cb

        if 1: # testing:
            dialog.ask_exec_config(str(nr+1),button=button,label=label,cfg=cfg)
        else:
            dialog.askstring("CFG-BTN","GO=GO FL=FLASH\nSEL=SELECT EXE:"+str(nr+1),initialvalue=txt)

    def label(self,nr):
        txt = PRESETS.label(nr) 
        def _cb(data):
            txt = data["Value"]
            print(self,"label._cb()",nr,txt)
            if txt:
                PRESETS.label(nr,txt) 
                self.elem_presets[nr].configure(text = PRESETS.get_btn_txt(nr))
            modes.val("LABEL", 0)

            master._refresh_exec()

        dialog._cb= _cb #_x(nr)
        dialog.askstring("LABEL","EXE:"+str(nr+1),initialvalue=txt)

    def xcb(self,mode,value=None):
        cprint("MODE CALLBACK",mode,value,color="green",end="")
        #cprint(self,"xcb","MODE CALLBACK",mode,value,color="green")
        if value:
            cprint("===== ON  ======",color="red")
            txt = ""
            if mode == "REC-FX":
                modes.val("REC",0)
                modes.val("REC",1)
            if value == 2:
                if mode in ["MOVE","COPY"]:
                    txt="to"
                self.button_refresh(mode,color="orange",text=txt)#,fg="blue")
            else:
                if mode in ["MOVE","COPY"]:
                    txt="from"
                self.button_refresh(mode,color="red",text=txt)#,fg="blue",text="from")
        else:
            cprint("===== OFF ======",color="red")
            if mode == "REC-FX":
                modes.val("REC",0)
            self.button_refresh(mode,color="lightgrey")#,fg="black")

    def load(self,fname=""):
        pass
    def exit(self):
        print("__del__",self)
        PRESETS.backup_presets()
        #print("********************************************************")
        FIXTURES.backup_patch()
        #print("*********del",self,"***********************************************")
    def refresh_exec(self):
        refresher.reset() # = Refresher()

    def _refresh_exec(self):
        cprint("PRESET.refresh_exec()")
        
        self._XX +=1
        for k in PRESETS.val_presets: 
            label = ""

            if k not in self.elem_presets:
                cprint("ERROR",k ,"not in elem_presets continue")
                continue
            if k in PRESETS.label_presets:
                label = PRESETS.label_presets[k]
                #print([label])
            b = self.elem_presets[k]
            
            ifval = 0
            fx_only = 0
            if k in PRESETS.val_presets and len(PRESETS.val_presets[k]) :
                sdata = PRESETS.val_presets[k]
                #print("sdata7654",sdata)
                BTN="go"
                if "CFG" in sdata:#["BUTTON"] = "GO"
                    if "BUTTON" in sdata["CFG"]:
                        BTN = sdata["CFG"]["BUTTON"]
                #txt=str(k+1)+" "+str(BTN)+" "+str(len(sdata)-1)+"\n"+label
                txt="{} {} {}\n{}".format(k+1,BTN,len(sdata)-1,label)
                #txt+=str(self._XX)
                b.configure(text= txt)
                b.configure(bg="yellow")
                b.config(activebackground="yellow")
                if len(sdata) > 1:
                    ifval = 1
                    fx_color = 0
                    val_color = 0
                    for fix in sdata:
                        if fix == "CFG":
                            continue
                        #print( "$$$$",fix,sdata[fix])
                        for attr in sdata[fix]:
                            if "FX2" in sdata[fix][attr]:
                                if sdata[fix][attr]["FX2"]:
                                    fx_color = 1
                            if "FX" in sdata[fix][attr]:
                                if sdata[fix][attr]["FX"]:
                                    fx_color = 1
                            if "VALUE" in sdata[fix][attr]:
                                if sdata[fix][attr]["VALUE"] is not None:
                                    val_color = 1

                    b.configure(fg= "black")
                    if val_color:
                        b.configure(bg="gold")
                        b.config(activebackground="#ffaa55")
                        if fx_color:
                            b.configure(fg = "blue")
                    else:   
                        if fx_color:
                            fx_only = 1
                else:
                    b.configure(bg="grey")
                    b.config(activebackground="#aaa")


            if "\n" in txt:
                txt1 = txt.split("\n")[0]

            b.configure(fg="black")
            if ifval:
                if fx_only:
                    b.configure(bg = "cyan")
                    b.config(activebackground="#55d4ff")

                if "SEL" in txt1:
                    b.configure(bg="#77f")
            else: 
                b.configure(bg="grey")
                b.configure(fg="darkgrey") #black")

                if "SEL" in txt1:
                    b.configure(fg="blue")
                elif "ON" in txt1:
                    b.configure(fg="#040")
                elif "GO" in txt1:
                    b.configure(fg="#555")

            if "FL" in txt1:
                b.configure(fg="#00e")

    def refresh_fix(self):
        refresher.reset() # = Refresher()
    def _refresh_fix(self):
        c_d =0
        c_f =0
        c_a =0
        for fix in FIXTURES.fixtures:                            
            sdata = FIXTURES.fixtures[fix]                            
            _c_a = 0
            for attr in sdata["ATTRIBUT"]:
                if "FINE" in attr:
                    continue
                v2 = sdata["ATTRIBUT"][attr]["VALUE"]
                if fix in self.elem_attr:
                    
                    elem = self.elem_attr[fix][attr]
                    #print( attr,v2)
                    elem["text"] = "{} {:0.2f}".format(attr,v2)
                    if sdata["ATTRIBUT"][attr]["ACTIVE"]:
                        elem["bg"] = "yellow"
                        elem.config(activebackground="yellow")
                        if "DIM" in sdata["ATTRIBUT"] and len(sdata["ATTRIBUT"]) == 1:
                            c_d+=1
                        else:
                            _c_a += 1
                    else:
                        elem["bg"] = "grey"
                        elem.config(activebackground="grey")

                    if "FX2" not in sdata["ATTRIBUT"][attr]: # insert FX2 excetption
                        sdata["ATTRIBUT"][attr]["FX2"] = OrderedDict()
                        
                    if sdata["ATTRIBUT"][attr]["FX"]:
                        elem["fg"] = "blue"
                    elif sdata["ATTRIBUT"][attr]["FX2"]:
                        elem["fg"] = "red"
                    else:
                        elem["fg"] = "black"
            c_a += _c_a
            if _c_a>0:
                c_f +=1

        c_a2=0

        if c_f > 0:
            c_a2 = round(c_a/c_f,2)
            if c_a2 % 1 > 0:
                gui_menu.config("FIXTURES","bg","orange")
                gui_menu.config("FIXTURES","activebackground","orange")
            else:
                gui_menu.config("FIXTURES","bg","yellow")
                gui_menu.config("FIXTURES","activebackground","yellow")
        else:
            gui_menu.config("FIXTURES","bg","")
            gui_menu.config("FIXTURES","activebackground","")
        gui_menu.update("FIXTURES","{} : {}".format(c_f,c_a2))

        if c_d > 0:
            gui_menu.config("DIMMER","bg","yellow")
            gui_menu.config("DIMMER","activebackground","yellow")
        else:
            gui_menu.config("DIMMER","bg","")
            gui_menu.config("DIMMER","activebackground","")
        gui_menu.update("DIMMER","{}".format(c_d))

    def preset_rec(self,nr):
        print("------- STORE PRESET")
        data = FIXTURES.get_active()
        if modes.val("REC-FX"):
            PRESETS.rec(nr,data,"REC-FX")
            modes.val("REC-FX",0)
        else:
            PRESETS.rec(nr,data)
            
        sdata=data
        PRESETS.val_presets[nr] = sdata
        
        master._refresh_exec()
        return 1


    def preset_select(self,nr):
        print("SELECT PRESET")
        sdata = PRESETS.val_presets[nr]
        cmd = ""
        for fix in sdata:
            if fix == "CFG":
                continue
            for attr in sdata[fix]:
                v2 = sdata[fix][attr]["VALUE"]
                v2_fx = sdata[fix][attr]["FX"]
                #print( self.data.elem_attr)
                if fix in self.elem_attr:
                    if attr in self.elem_attr[fix]:
                        elem = self.elem_attr[fix][attr]
                        FIXTURES.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                        elem["bg"] = "yellow"

    def preset_go(self,nr,val=None,xfade=None,event=None,button="",ptfade=None):
        t_start = time.time()
        if xfade is None and FADE._is():
            xfade = FADE.val()
        
        if ptfade is None and FADE_move._is():
            ptfade = FADE_move.val()

        print("GO PRESET FADE",nr,val)

        rdata = PRESETS.get_raw_map(nr)
        if not rdata:
            return 0
        print("???????")
        cfg   = PRESETS.get_cfg(nr)
        print("''''''''")
        #virtcmd  = FIXTURES.get_virtual(rdata)
        if not cfg:
            cprint("NO CFG",cfg,nr)
            return 0

        xFLASH = 0
        value=None
        cprint("preset_go",nr,cfg)
        if modes.val("SELECT") or ( "BUTTON" in cfg and cfg["BUTTON"] == "SEL") and val and not button: #FLASH
            self.preset_select(nr)
        elif modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL") and not button: #FLASH
            xFLASH = 1
            xfade = 0
            if type(val) is not type(None) and val == 0 :
                value = "off"
            if event:
                if str(event.type) == "ButtonRelease" or event.type == '5' :
                    value = "off"

            cprint("preset_go() FLUSH",value,color="red")
            
            fcmd  = FIXTURES.update_raw(rdata,update=0)
            self._preset_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH,nr=nr)
                
        elif not val:
            cprint("preset_go() STOP",value,color="red")
        elif button == "on" or ( modes.val("ON") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["on","ON"])):
            fcmd  = FIXTURES.update_raw(rdata)
            self._preset_go(rdata,cfg,fcmd,value,xfade=0,xFLASH=xFLASH)
        elif button == "go" or ( modes.val("GO") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["go","GO"])): 
            fcmd  = FIXTURES.update_raw(rdata)
            self._preset_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH,ptfade=ptfade,nr=nr)



        if not (modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL")): #FLASH
            self.refresh_exec()
            self.refresh_fix()
        cprint("preset_go",time.time()-t_start)

    def _preset_go(self,rdata,cfg,fcmd,value=None,xfade=None,event=None,xFLASH=0,ptfade=0,nr=None):
        if xfade is None and FADE._is():
            xfade = FADE.val()

        if ptfade is None and FADE_move._is():
            ptfade = FADE_move.val()
        cprint("PRESETS._preset_go() len=",len(rdata),cfg)
        if xfade is None:
            xfade = cfg["FADE"]
        if ptfade is None:
            ptfade = cfg["FADE"]
        #vcmd = reshape_preset( rdata ,value,[],xfade=xfade,fx=1) 
        #cprint(rdata,color="red")
        vcmd = reshape_preset( rdata ,value,xfade=xfade,ptfade=ptfade) 

        cmd = []
        delay=0
        for i,v in enumerate(fcmd):
            #print("go",i,v)
            if xFLASH:
                vcmd[i]["FLASH"] = 1

            DMX = fcmd[i]["DMX"]
            if "VALUE" in vcmd[i] and type(vcmd[i]["VALUE"]) is type(float):
                vcmd[i]["VALUE"] = round(vcmd[i]["VALUE"],3)
            if value is not None:
                vcmd[i]["VALUE"] = value 
            if value == "off":
                if "FX2" in vcmd:
                    vcmd[i]["FX2"]["TYPE"] = value
            if "FIX" in fcmd:
                vcmd[i]["FIX"] = fcmd["FIX"]
            if DMX and vcmd[i]:
                vcmd[i]["DMX"] = DMX

            if "VIRTUAL" in fcmd[i]:
                for a in fcmd[i]["VIRTUAL"]:
                    DMX = fcmd[i]["VIRTUAL"][a]
                    if DMX and vcmd[i]:
                        vcmd[i]["DMX"] = DMX
            if type(nr) is not type(None):
                vcmd[i]["EXEC"] = str(int(nr)+1)
            #cprint(vcmd[i],color="red")
            cmd.append(vcmd[i])

        if cmd and not modes.val("BLIND"):
            jclient_send(cmd)

    def render(self):
        #Xroot.bind("<Key>",Xevent(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        #self.draw_input()
        pass
        


##draw_sub_dim



class InputEventBlocker():
    def __init__(self):
        self.__init = 0
        self.cursor = "88888"

    def set(self,el,txt):
        self.e = el
        self.e_txt = txt
        self.cursor = "88888"

    def init(self):
        if self.__init == 0:
            try:
                self.el = tk.Button()
                self.e_txt = tk.StringVar()
                self.__init = 1
            except Exception as e:
                pirnt("init() exception",e)
    def _lock(self):
        global _global_short_key
        _global_short_key = 0
        master.commands.elem["S-KEY"]["bg"] = "red"

    def _unlock(self):
        global _global_short_key
        _global_short_key = 1
        master.commands.elem["S-KEY"]["bg"] = "green"

    def lock(self):
        self._lock()
        #self.e["bg"] = "red"
        #self.el.config({"background": "grey"})
        #self.e.focus()

    def unlock(self):
        self._unlock()
        #self.e["bg"] = "blue"
        #self.el.config({"background": "yellow"})
        #self.el.focus_set()

    def event(self,event,**args):
        self.init()
        #print()
        print(self,event,args)
        #print("###-",self.e_txt,dir(self.e_txt))
        if "S-KEY" not in master.commands.elem:
            return 
        if "num" in dir(event):
            self.lock()
        if "keysym" in dir(event):
            t=self.e_txt.get()
            if t and t[-1] == "<":
                t = t[:-1]
            if event.keysym == "Return" or event.keysym == "Tab" or event.keysym == "ISO_Left_Tab":
                self.unlock() 
                #self.e_txt.set(t)
            print("filter: get()",_global_short_key,t)
            t2 = t
            if _global_short_key == 0:
                if event.keysym == "BackSpace":
                    if len(t) > 1:
                        t2 = t[:-1]
                    else:
                        t2=""
                elif event.keysym == "Escape":
                    t2=""
                elif event.keysym == "space":
                    t2=t+" "
                elif event.char in "äöüÄÖÜ-_,.;:#'*+~":
                    t2=t+event.char
                elif len(event.keysym) == 1:
                    t2=t+event.keysym
            
                #self.e_txt.set(t2+"<")
        #time.sleep(0.2)
        #_global_short_key = 1

input_event_blocker = InputEventBlocker()

from tkgui.dialog import *
dialog = Dialog()

from tkgui.draw import *
            

           
from tkgui.GUI import *

#draw_enc

class LOAD_FIXTURE():
    def __init__(self,name="",master=None):
        self.name=name
        self.master=master

    def cb(self,event=None):
        print("LOAD_FIXTURE",self.name,event)
        if self.master is not None:
            #for i in dir(self.master): #.load_MH2()
            #    print(i)
            if "SPARX" in self.name:
                self.master.load_MH2()
            else:
                self.master.load_DIM()
            print(dir(self.master))

class LOAD_SHOW_AND_RESTAT():
    def __init__(self,fname=""):
        self.fname=fname
        self.base = Base()

    def cb(self,event=None,force=0):
        print("LOAD_SHOW_AND_RESTART.cb force={} name={}".format(force,self.fname) )
        if not self.fname and not force:
            return 0
        if self.base.show_name == self.fname and not force:
            cprint("filename is the same",self.fname)
            return 0
        if not force:
            self.base._set(self.fname)

        print("LOAD SHOW:",event,self.fname)

        print(sys.executable, os.path.abspath(__file__), *sys.argv)
        os.execl("/usr/bin/python3", "/opt/LibreLight/Xdesk/_LibreLightDesk.py", "_LibreLightDesk.py")
        sys.exit()
                
class PopupList():
    def __init__(self,name="<NAME>",master=0,width=400,height=450,exit=1,left=_POS_LEFT+400,top=_POS_TOP+100,cb=None,bg="black"):
        self.name = name
        self.frame = None
        self.bg=bg
        self.cb = cb
        if cb is None: 
            cb = DummyCallback #("load_show_list.cb")
        w = Window(self.name,master=master,width=width,height=height,exit=exit,left=left,top=top,cb=cb)
        self.w = w
        w.show()
    def sframe(self,line1="<line1>",line2="<line2>",data=[]):

        xframe=self.w.tk
        if self.bg:
            xframe.configure(bg=self.bg)
            self.w.tk.configure(bg=self.bg)
        c=0
        r=0

        b = tk.Label(xframe,bg="grey",text=line1,anchor="w")
        b.pack(side="top",expand=0,fill="x" ) 


        b = tk.Label(xframe,bg="grey",text=line2,anchor="w")
        b.pack(side="top",expand=0,fill="x" ) 

        b = tk.Label(xframe,bg="black",fg="black",text="")
        if self.bg:
            b.configure(fg=self.bg)
            b.configure(bg=self.bg)
        b.pack(side="top") 

        b = tk.Entry(xframe,width=10,text="")#,anchor="w")
        b.pack(side="top",expand=0,fill="x") 
        b.focus()


        #frame = tk.Frame(xframe,heigh=2800)
        #frame.pack(fill=tk.BOTH,expand=1, side=tk.TOP)

        frame = ScrollFrame(xframe,width=300,height=500,bd=1,bg=self.bg)
        #frame.pack(side="left") #fill=tk.BOTH,expand=1, side=tk.TOP) 
        #self.frame = frame
        self.w.tk.state(newstate='normal')
        self.w.tk.attributes('-topmost',True)
        return frame


class DummyCallback():
    def __init__(self,name="name"):
        self.name = name
    def cb(self,event=None):
        print("DummyCallback.cb",[self.name,event])


def _load_show_list(frame,cb=None):
    c=0
    r=0
    base = Base()
    for i in ["name","stamp"]: #,"create"]:
        b = tk.Label(frame,bg="grey",text=i)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
    r+=1
    blist = base._list()
    for i in range(10):
        blist.append(["",""])

    if cb is None: 
        cb = DummyCallback #("load_show_list.cb")

    for i in blist:
        #print(i)
        c=0
        for j in i:
            bg="lightgrey"
            dbg="lightgrey"
            if i[1] > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*4)):
                dbg = "lightgreen"
            elif i[1] > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*24*7)):
                dbg = "green"


            if c > 0:
                b = tk.Button(frame,text=j,anchor="w",bg=dbg,relief="sunken")
                b.config(activebackground=dbg)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            else:
                if base.show_name == i[0]:
                    bg="green"
                _cb = cb(j)
                b = tk.Button(frame,text=j,anchor="w",height=1,bg=bg,command=_cb.cb)

                if base.show_name == i[0]:
                    b.config(activebackground=bg)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
        r+=1


def _load_fixture_list(frame,cb=None,master=None,bg="black"):
    frame.configure(bg=bg)
    c=0
    r=0
    base = Base()
    for i in ["name","stamp"]: #,"create"]:
        b = tk.Label(frame,bg="grey",text=i)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
    r+=1
    blist = [] #base._list()
    blist.append(["MAC-500","martin","z"])
    blist.append(["MAC-2000","martin","z"])
    blist.append(["MAC-VIPER","martin","z"])
    blist.append(["SPARX-7","JB","z"])
    blist.append(["SPARX-11","JB","z"])
    blist.append(["JB-P6","JB","z"])
    blist.append(["JB-P7","JB","z"])
    blist.append(["JB-A7","JB","z"])
    blist.append(["TMH-12","Eurolight","z"])
    for i in range(10):
        blist.append(["",""])


    if cb is None: 
        cb = DummyCallback #("load_show_list.cb")

    for i in blist:
        #print(i)
        c=0
        for j in i:
            bg="lightgrey"
            dbg="lightgrey"
            if i[1] > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*4)):
                dbg = "lightgreen"
            elif i[1] > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*24*7)):
                dbg = "green"


            if c > 0:
                b = tk.Button(frame,text=j,anchor="w",bg=dbg,relief="sunken")
                b.config(activebackground=dbg)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            else:
                if base.show_name == i[0]:
                    bg="green"

                _cb=cb(j)
                _cb.master=master
                b = tk.Button(frame,text=j,anchor="w",height=1,bg=bg,command=_cb.cb)

                if base.show_name == i[0]:
                    b.config(activebackground=bg)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
        r+=1






class Fixtures():
    def __init__(self):
        #super().__init__() 
        self.base=Base()
        #self.load()
        self.fixtures = OrderedDict()
        self.gui = GUIHandler()

        
    def load_patch(self):
        filename="patch"
        #self.base._init()
        d,l = self.base._load(filename)
        self.fixtures = OrderedDict()
        for i in l:
            sdata = d[i]
            new_f = OrderedDict()
            #print("++++")
            for k,j in sdata.items():
                overide=0 # only for repair
                if overide:
                    if k in ["TYPE","VENDOR"]: #ignor
                        continue
                new_f[k] = j
                if k =="NAME":
                    #print("AAAADDDDDD")
                    if "TYPE" not in sdata and not overide:
                        if len( sdata["ATTRIBUT"]) == 1:
                            new_f["TYPE"] = "DIMMER"
                        elif "PAN" in sdata["ATTRIBUT"]:
                            new_f["TYPE"] = "MOVER"
                        elif "RED" in sdata["ATTRIBUT"] and len(sdata["ATTRIBUT"]) == 3:
                            new_f["TYPE"] = "RGB"
                        elif "RED" in sdata["ATTRIBUT"]:
                            new_f["TYPE"] = "LED"
                        elif "CYAN" in sdata["ATTRIBUT"]:
                            new_f["TYPE"] = "COLOR"
                        else:
                            new_f["TYPE"] = ""
                    if "VENDOR" not in sdata and not overide:
                        new_f["VENDOR"] = ""

                #print(k,j)#,sdata)
            sdata = new_f
            if "ACTIVE" not in sdata:
                sdata["ACTIVE"] = 0
            for attr in sdata["ATTRIBUT"]:
                sdata["ATTRIBUT"][attr]["ACTIVE"] = 0
            #print("load",filename,sdata)
            #if "CFG" not in sdata:
            #    sdata["CFG"] = OrderedDict()
            self.fixtures[str(i)] = sdata
        #PRESETS.label_presets = l
        self.fx_off("all")

    def backup_patch(self,save_as=""):
        filename = "patch"
        #self.fx_off("all")
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        #self.base._init()
        self.base._backup(filename,data,labels,save_as)

    def fx_get(self,fix=None):
        out={}
        if not fix or fix == "all":
            #self.data.fx.elem[self.attr]["bg"] = "magenta"
            for fix in self.fixtures:
                data = self.fixtures[fix]
                for attr in data["ATTRIBUT"]:
                    out[str(fix)+"."+str(attr)+".fx"] =  data["ATTRIBUT"][attr]["FX"] 
                    out[str(fix)+"."+str(attr)+".fx"] =  data["ATTRIBUT"][attr]["FX2"]

        return out
    def fx_off(self,fix=None):
        if not fix or fix == "all":
            #self.data.fx.elem[self.attr]["bg"] = "magenta"
            for fix in self.fixtures:
                data = self.fixtures[fix]
                for attr in data["ATTRIBUT"]:
                    data["ATTRIBUT"][attr]["FX"] = ""
                    data["ATTRIBUT"][attr]["FX2"] = OrderedDict()

    def get_attr(self,fix,attr):
        if fix in self.fixtures:
            data = self.fixtures[fix]
            if "ATTRIBUT" in data:
                if attr in data["ATTRIBUT"]:
                    return data["ATTRIBUT"][attr]

    def get_max_dmx_nr(self,fix):
        max_dmx = 0
        used_dmx = 0
        if fix not in self.fixtures:
            return (used_dmx,max_dmx)

        data = self.fixtures[fix]
        used_dmx = len(data["ATTRIBUT"])
        for a in data["ATTRIBUT"]:
            attr = data["ATTRIBUT"][a]
            if "NR" in attr:
                try:
                    _n = int(attr["NR"])
                    if _n > max_dmx:
                        max_dmx=_n
                except ValueError:pass
        return (used_dmx,max_dmx)

    def get_dmx(self,fix,attr):
        #cprint("get_dmx",[fix,attr])
        if fix in self.fixtures:
            data = self.fixtures[fix]
            DMX = -99
            if "DMX" in data:
                DMX = int(data["DMX"])
                if DMX < 1: # ignore attribute with DMX lower 1
                    return -22
            else:
                return -1


            if "UNIVERS" in data:
                if int(data["UNIVERS"]) >= 0:
                    DMX += (int(data["UNIVERS"])*512)
                else:
                    return -33
            adata = self.get_attr(fix,attr)
            #-hier ende 8.2.22
            #cprint("adata",adata,DMX)

            if adata:
                if "NR" in adata:
                    NR = adata["NR"] 
                    if NR >= 1:
                        DMX+=NR-1
                    else:
                        return -44
                return DMX
            return -4
        return -3
    def update_raw(self,rdata,update=1):
        cprint("update_raw",len(rdata))
        cmd = []
        for i,d in enumerate(rdata):
            xcmd = {"DMX":""}
            #print("fix:",i,d)
            fix   = d["FIX"]
            attr  = d["ATTR"]
            v2    = d["VALUE"]
            v2_fx = d["FX"]

            if fix not in self.fixtures:
                continue 
            sdata = self.fixtures[fix] #shortcat
            ATTR  = sdata["ATTRIBUT"] 

            sDMX = 0
            if  sdata["DMX"] > 0:
                #print( sdata)
                sDMX = (sdata["UNIVERS"]*512)+sdata["DMX"]  
                #sDMX =sdata["DMX"]  
            #else:
            #    continue

            if attr not in ATTR:
                continue
            #DMX = FIXTURES.get_dmx(fix) 
            if ATTR[attr]["NR"] >= 0:
                DMX = sDMX+ATTR[attr]["NR"]-1
                xcmd["DMX"] = str(DMX)
            else:
                if attr == "DIM" and ATTR[attr]["NR"] < 0:
                    xcmd["VIRTUAL"] = {}
                    for a in ATTR:
                        if ATTR[a]["MASTER"]:
                            xcmd["VIRTUAL"][a] = sDMX+ATTR[a]["NR"]-1
                    #print( "VIRTUAL",xcmd)


            cmd.append(xcmd)

            v=ATTR[attr]["VALUE"]
            if v2 is not None and update:
                ATTR[attr]["VALUE"] = v2
            
            if d["FX2"] and update:
                ATTR[attr]["FX2"] = d["FX2"] 

            #self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
            text = str(attr)+' '+str(round(v,2))
            #self.gui.update(fix,attr,args={"text":text})
            #print("END 5454 _=_=_=_=_==_")
        #cprint("update_raw",cmd,color="red")
        return cmd


    def encoder(self,fix,attr,xval="",xfade=0,xdelay=0,blind=0):

        _blind = 0
        if modes.val("BLIND"):
            _blind = 1 
        if blind:
            _blind = 1
        
        if not _blind:
            cprint("FIXTURES.encoder",fix,attr,xval,xfade,color="yellow")

        if attr == "CLEAR":
            self.clear()
            return 0

        if attr == "ALL":
            x=self.select(fix,attr,mode="toggle")
            return x

        out = []
        if fix not in self.fixtures: 
            print(" activate Fixture in fixture list on encoder click ")

            #jdata=[{"MODE":"---"}]
            ii =0
            #jclient_send(jdata)
            delay=0
            print("-->A HIER <--")
            sub_data = []
            for fix in self.fixtures:
                ii+=1
                #cprint(fix,attr,xval)
                data = self.fixtures[fix]
                if "-FINE" in attr.upper():
                    continue

                elif (attr in data["ATTRIBUT"] ) and "-FINE" not in attr.upper()   :
                    if xval == "click":
                        self.select(fix,attr,mode="on")
                    elif data["ATTRIBUT"][attr]["ACTIVE"]:
                        if fix: # prevent endless recursion
                            #print("------",end="")
                            #self.encoder(fix,attr,xval,xfade,delay)
                            sub_data.append([fix,attr,xval,xfade,delay])
                if DELAY._is():
                    delay += DELAY.val()/100

            sub_jdata = []
            for dd in sub_data:
                #print("---",len(sub_data),end="")
                #self.encoder(fix,attr,xval,xfade,delay)
                _x123 = self.encoder(dd[0],dd[1],dd[2],dd[3],dd[4],blind=1)
                sub_jdata.append(_x123)

            if sub_jdata:
                print("--- SEND MASTER ENCODER:",len(sub_data),sub_data[0],"... _blind:",_blind)#,end="")
                jclient_send(sub_jdata) 

            jdata=[{"MODE":ii}]
            print("-->B HIER <--")
            jclient_send(jdata)
            return 0

        data = self.fixtures[fix]

        if xval == "click":
            #cprint(data)
            return self.select(fix,attr,mode="toggle")

    
        v2=data["ATTRIBUT"][attr]["VALUE"]
        change=0
        increment = 4.11
        jdata = {"MODE":"ENC"}
        if xval == "++":
            v2+= increment
            jdata["INC"] = increment
            change=1
        elif xval == "--":
            jdata["INC"] = increment*-1
            v2-= increment
            change=1
        elif xval == "+":
            increment = 0.5
            v2+= increment
            jdata["INC"] = increment
            change=1
        elif xval == "-":
            increment = 0.5
            jdata["INC"] = increment*-1
            v2-= increment
            change=1
        elif type(xval) is int or type(xval) is float:
            v2 = xval 
            change=1

            
        if v2 < 0:
            v2=0
        elif v2 > 256:
            v2=256
        jdata["VALUE"] = round(v2,4)
        jdata["FIX"] = fix
        jdata["ATTR"] = attr
        jdata["DMX"] = FIXTURES.get_dmx(fix,attr)
        jdata["DMX-FINE"] = FIXTURES.get_dmx(fix,attr+"-FINE")
        out = {} 
        if change:
            data["ATTRIBUT"][attr]["ACTIVE"] = 1
            data["ATTRIBUT"][attr]["VALUE"] = round(v2,4)

            jdata["FADE"] = 0
            if xfade:
                jdata["FADE"] = xfade
            if xdelay:
                #if attr not in ["PAN","TILT"] and 1:
                jdata["DELAY"] = xdelay


            if not _blind:
                jdata = [jdata]
                #print("ENC",jdata)
                jclient_send(jdata)
                time.sleep(0.001)
        return jdata
        return v2

    def get_active(self):
        cprint("get_active",self)
        CFG = OrderedDict()
        sdata = OrderedDict()
        sdata["CFG"] = CFG # OrderedDict()
        sdata["CFG"]["FADE"] = FADE.val()
        sdata["CFG"]["DEALY"] = 0
        #sdata["CFG"]["BUTTON"] = "GO"
        for fix in self.fixtures:                            
            data = self.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    if fix not in sdata:
                        sdata[fix] = {}
                    if attr not in sdata[fix]:
                        sdata[fix][attr] = OrderedDict()
                        if not modes.val("REC-FX"):
                            sdata[fix][attr]["VALUE"] = data["ATTRIBUT"][attr]["VALUE"]
                            #sdata[fix][attr]["FADE"] = FADE.val() #fade
                        else:
                            sdata[fix][attr]["VALUE"] = None #data["ATTRIBUT"][attr]["VALUE"]

                        if "FX" not in data["ATTRIBUT"][attr]: 
                             data["ATTRIBUT"][attr]["FX"] =""
                        if "FX2" not in data["ATTRIBUT"][attr]: 
                             data["ATTRIBUT"][attr]["FX2"] ={}
                        
                        sdata[fix][attr]["FX"] = data["ATTRIBUT"][attr]["FX"] 
                        sdata[fix][attr]["FX2"] = data["ATTRIBUT"][attr]["FX2"] 
    
        return sdata

    def _deselect_all(self,fix=None):
        cprint("FIXTURES._deselect_all()",fix,"ALL",color="yellow")
        c=0
        if fix in self.fixtures:
            data = self.fixtures[fix]

            for attr in data["ATTRIBUT"]:
                #print("SELECT ALL",fix,attr)
                if "-FINE" in attr.upper():
                    pass
                else:
                    c+=self.select(fix,attr,mode="off",mute=1)
        
        return c

    def _select_all(self,fix=None,mode="toggle"):
        cprint("FIXTURES._select_all()",fix,"ALL",mode,color="yellow")
        c=0
        if fix in self.fixtures:
            data = self.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                #print("SELECT ALL",fix,attr)
                if "-FINE" in attr.upper():
                    pass
                else:
                    c+=self.select(fix,attr,mode="on",mute=1)

            if not c and mode == "toggle": # unselect all
                c= self._deselect_all(fix=fix)
        return c 

    def select(self,fix=None,attr=None,mode="on",mute=0):
        if not mute:
            cprint("FIXTURES.select()",fix,attr,mode,color="yellow")
        out = 0

        if fix in self.fixtures:
            data = self.fixtures[fix]
            if attr.upper() == "ALL":
                x=self._select_all(fix=fix,mode=mode)
                return x
            elif attr in data["ATTRIBUT"]:
                if mode == "on":
                    if not data["ATTRIBUT"][attr]["ACTIVE"]:
                        data["ATTRIBUT"][attr]["ACTIVE"] = 1
                        out = 1
                elif mode == "off":
                    if data["ATTRIBUT"][attr]["ACTIVE"]:
                        data["ATTRIBUT"][attr]["ACTIVE"] = 0
                        out = 1
                elif mode == "toggle":
                    if data["ATTRIBUT"][attr]["ACTIVE"]:
                        data["ATTRIBUT"][attr]["ACTIVE"] = 0
                    else:
                        data["ATTRIBUT"][attr]["ACTIVE"] = 1
                    out = 1
        return out

    def clear(self):
        out = 0
        for fix in self.fixtures:
            data = self.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                #if attr.endswith("-FINE"):
                #    continue
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    out +=1
                data["ATTRIBUT"][attr]["ACTIVE"] = 0
        return out



def CFG_CHECKER(sdata):
    "repair CFG  "
    ok = 0
    if "CFG" not in sdata:
        sdata["CFG"] = OrderedDict()
        ok += 1
    if "FADE" not in sdata["CFG"]:
        sdata["CFG"]["FADE"] = 4
        ok += 1
    if "DELAY" not in sdata["CFG"]:
        sdata["CFG"]["DELAY"] = 0
        ok += 1
    if "BUTTON" not in sdata["CFG"]:
        sdata["CFG"]["BUTTON"] = "GO"
        ok += 1
    if "HTP-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["HTP-MASTER"] = 100 #%
        ok += 1
    if "SIZE-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["SIZE-MASTER"] = 100 #%
        ok += 1
    if "SPEED-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["SPEED-MASTER"] = 100 #%
        ok += 1
    if "OFFSET-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["OFFSET-MASTER"] = 100 #%
        ok += 1

    #try:del sdata["CFG"]["SPEED-MASTER"] #= 100 #%
    #except:pass

    return ok


class Presets():
    def __init__(self):
        #super().__init__() 
        self.base = Base()
        #self.load()
        self._last_copy = None
        self._last_move = None
        self.fx_buffer = {}

    def load_presets(self): 
        #self._load()
        filename="presets"
        #self.base._init()
        d,l = self.base._load(filename)
        for i in d:
            sdata = d[i]
            ok = CFG_CHECKER(sdata)

        self.val_presets = d
        self.label_presets = l

    def check_cfg(self,nr=None):
        cprint("PRESETS.check_cfg()",nr)#,color="red")
        ok = 0
        if nr is not None:
            if nr in self.val_presets:
                sdata = self.val_presets[nr]
                ok += self._check_cfg(sdata)
            else:
                cprint("nr not in data ",nr,color="red")
        else:
            for nr in self.val_presets:
                sdata = self.val_presets[nr]
                ok += self._check_cfg(sdata)
        return ok

    def _check_cfg(self,sdata):
        cprint("PRESETS._check_cfg()")#,color="red")

        ok = CFG_CHECKER(sdata)

        if ok:
            cprint("REPAIR CFG's",ok,sdata["CFG"],color="red")
        return ok
        
    def backup_presets(self,save_as=""):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        #self.base._init()
        self.base._backup(filename,data,labels,save_as)
        

    def get_cfg(self,nr):
        cprint("PRESETS.get_cfg()",nr)
        self.check_cfg(nr)
        if nr not in self.val_presets:
            cprint("get_cfg",self,"error get_cfg no nr:",nr,color="red")
            return {}
        if "CFG" in self.val_presets[nr]:
            return self.val_presets[nr]["CFG"]

    def clean(self,nr):
        
        if nr not in self.val_presets:
            self.val_presets[nr] = OrderedDict()
            #self.val_presets[nr]["VALUE"] = 0
            #self.val_presets[nr]["FX"] = ""


        sdata = self.val_presets[nr]
        for fix in sdata:
            #print("exec.clear()",nr,fix,sdata[fix])
            for attr in sdata[fix]:
                row = sdata[fix][attr]
                if fix == "CFG":
                    continue

                if "VALUE" not in row:
                    row["VALUE"] = None
                if "FX" not in row:
                    row["FX"] = "" 
                if "FX2" not in row:
                    row["FX2"] = OrderedDict()
                elif row["FX2"]:
                    for k in ["SIZE","SPEED","START","OFFSET"]:
                        row["FX2"][k] = int( row["FX2"][k] )
                    row["FX"] = "" 


                if "FX" in row and row["FX"] and not row["FX2"]: # rebuild old FX to Dict-FX2
                    #"off:0:0:0:16909:-:"
                    x = row["FX"].split(":")
                    print("-fx",x,len(x))
                    #'FX2': {'TYPE': 'sinus', 'SIZE': 200, 'SPEED': 30, 'START': 0, 'OFFSET': 2805, 'BASE': '-'}}
                    if len(x) >= 6:
                        row["FX2"]["TYPE"] = x[0] 
                        row["FX2"]["SIZE"] =  int(x[1])
                        row["FX2"]["SPEED"] = int(x[2]) 
                        row["FX2"]["START"] = int(x[3]) 
                        row["FX2"]["OFFSET"] = int(x[4]) 
                        row["FX2"]["BASE"] = x[5] 
                    row["FXOLD"] = row["FX"]
                    row["FX"] = ""
                #cprint("exec.clear()",nr,fix,row)

            
    def get_raw_map(self,nr):
        self.clean(nr)

        print("get_raw_map",nr)
        sdata = self.val_presets[nr]
        cmd = ""
        out = []
        dmx=-1
        for fix in sdata:
            if fix == "CFG":
                #print("CFG",nr,sdata[fix])
                continue

            for attr in sdata[fix]:
                x = {}
                #print("RAW",attr)
                x["FIX"]   = fix
                x["ATTR"]  = attr

                x["VALUE"] = sdata[fix][attr]["VALUE"]
                x["FX"]    = sdata[fix][attr]["FX"]
                x["FX2"]    = sdata[fix][attr]["FX2"]
                #x["DMX"]  = sdata[fix][attr]["NR"] 

                out.append(x)
        return out

    def get_btn_txt(self,nr):
        sdata=self.val_presets[nr]
        BTN="go"
        if "CFG" in sdata:
            if "BUTTON" in sdata["CFG"]:
                BTN = sdata["CFG"]["BUTTON"]
        _label = self.label_presets[nr] # = label
        txt=str(nr+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+_label
        print("get_btn_txt",nr,[txt])
        return txt

    def _btn_cfg(self,nr,txt=None):
        if nr not in self.val_presets:
            return ""
        if "CFG" not in self.val_presets[nr]:
            self.val_presets[nr]["CFG"] = OrderedDict()
        return self.val_presets[nr]["CFG"]

    def btn_cfg(self,nr,txt=None):
        if nr not in self.val_presets:
            return ""
        if "CFG" not in self.val_presets[nr]:
            self.val_presets[nr]["CFG"] = OrderedDict()
        if "BUTTON" not in self.val_presets[nr]["CFG"]:
            self.val_presets[nr]["CFG"]["BUTTON"] = ""
        if type(txt) is str:
            self.val_presets[nr]["CFG"]["BUTTON"] = txt
        if self.val_presets[nr]["CFG"]["BUTTON"] is None:
            self.val_presets[nr]["CFG"]["BUTTON"] = ""

        print("EEE", self.val_presets[nr]["CFG"]["BUTTON"] )
        return self.val_presets[nr]["CFG"]["BUTTON"] 

    def label(self,nr,txt=None):
        if nr not in self.label_presets:
            return ""
        if type(txt) is str:
            self.label_presets[nr] = txt
            print("set label",nr,[txt])
        print("??? ?? set label",nr,[txt])
        return self.label_presets[nr] 

    def clear_move(self):
        cprint("PRESETS.clear_move()",end=" ")
        self.clear_copy()
        
    def clear_copy(self):
        cprint("PRESETS.clear_copy()",end=" ")
        if self._last_copy is not None:
            cprint("=OK=",color="red")
            self._last_copy = None
        else:
            cprint("=NONE=",color="green")

    def copy(self,nr,overwrite=1):
        cprint("PRESETS._copy",nr,"last",self._last_copy)
        if nr >= 0:
            if self._last_copy is not None:
                if modes.val("COPY"):
                    modes.val("COPY",3)
                ok = self._copy(self._last_copy,nr,overwrite=overwrite)
                return ok #ok
            else:
                if modes.val("COPY"):
                    modes.val("COPY",2)
                self._last_copy = nr
                cprint("PRESETS.copy START ",color="red")
                return 0
        return 1 # on error reset move
    def _copy(self,nr_from,nr_to,overwrite=1):
        cprint("PRESETS._copy",nr_from,"to",nr_to)
        self.check_cfg(nr_from)
        if type(self._last_copy) is None:
            cprint("PRESETS._copy last nr is None",color="red")
            return 0
        cprint("------ PRESETS._copy", nr_from in self.val_presets , nr_to in self.val_presets)
        if nr_from in self.val_presets and nr_to in self.val_presets:
            fdata = self.val_presets[nr_from]
            tdata = self.val_presets[nr_to]
            #cprint(fdata)
            flabel = self.label_presets[nr_from]
            tlabel = self.label_presets[nr_to]
            self.val_presets[nr_to] = copy.deepcopy(fdata)
            self.label_presets[nr_to] = flabel
            if not overwrite: #default
                cprint("overwrite",overwrite)
                self.val_presets[nr_from] = copy.deepcopy(tdata)
                self.label_presets[nr_from] = tlabel
            #self.label_presets[nr_from] = "MOVE"
            self.clear_copy()
            cprint("PRESETS.copy OK",color="green")
            return 1

    def move(self,nr):
        cprint("PRESETS.move",self._last_copy,"to",nr)
        if nr >= 0: 
            last = self._last_copy
            if modes.val("MOVE"):
                modes.val("MOVE",2)
            ok= self.copy(nr,overwrite=0)
            if ok and last:
                if modes.val("MOVE"):
                    modes.val("MOVE",3)
                cprint("PRESETS.move OK",color="red")
                #self.delete(last)
                return ok #ok
            
        return 0 # on error reset move
    def delete(self,nr):
        cprint("PRESETS.delete",nr)
        ok=0
        if nr in self.val_presets:
            self.val_presets[nr] = OrderedDict()
            self.label_presets[nr] = ""
            ok = 1
        self.check_cfg(nr)
        return ok

    def rec(self,nr,data,arg=""):
        cprint("rec",self,"rec()",len(data),arg)
        self.check_cfg(nr)
        self._check_cfg(data) #by ref

        odata=self.val_presets[nr]
        #print("odata",odata)
        if "CFG" in odata:
            if "BUTTON" in odata["CFG"]:
                data["CFG"]["BUTTON"] = odata["CFG"]["BUTTON"]  
        self.val_presets[nr] = data
        return 1
           

class FixtureEditor():
    def __init__(self,dmx=1):
        pass
        self.elem=[]
        self.dmx=dmx
        print("init FixtureEditor",dmx)
    def event(self,a1="",a2=""):
        print([self.dmx,a1,a2])
        j=[]
        jdata = {'VALUE': int(a1), 'args': [] , 'FADE': 0,'DMX': str(self.dmx)}
        j.append(jdata)

        jclient_send(j)

class MasterWing():
    def __init__(self,dmx=1):
        pass
        self.elem=[]
        self.dmx=dmx
        print("init MasterWing",dmx)
    def event(self,a1="",a2=""):
        print([self.dmx,a1,a2])
        jdata = {'CMD': "MASTER", 'NAME': str(a1),'VALUE':str(a2) }

        j=[]
        j.append(jdata)
        jclient_send(j)

class BufferVar():
    def __init__(self,elem):
        self.elem = elem
    def change_dmx(self,event=""):
        nr=1
        txt=""
        def cb(data):
            txt = data["Value"]
        dialog._cb = _cb
        dialog.askstring("FADER-DMX-START",""+str(nr+1),initialvalue=txt)
        print("change_dmx",[event,self])


            

# GUI_FaderLayout():









lf_nr = 0


        
from tkinter import PhotoImage 

_shift_key = 0

class Window():
    def __init__(self,title="tilte",master=0,width=100,height=100,left=None,top=None,exit=0,cb=None,resize=1):
        global lf_nr
        #ico_path="/opt/LibreLight/Xdesk/icon/"
        ico_path="./icon/"
        self.cb = cb

        if master: 
            self.tk = tkinter.Tk()
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.withdraw() # do not draw
            self.tk.resizable(resize,resize)
            defaultFont = tkinter.font.nametofont("TkDefaultFont")
            print(defaultFont)
            defaultFont.configure(family="FreeSans",
                                   size=10,
                                   weight="bold")
            #self.tk.option_add("*Font", FontBold)
            # MAIN MENUE
            try:
                self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"main.png"))
            except Exception as e:
                print("Exception GUIWindow.__init__",e)
        else:
            # addtional WINDOW
            self.tk = tkinter.Toplevel()
            self.tk.iconify()
            #self.tk.withdraw() # do not draw
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.resizable(resize,resize)
            
            try:
                if "COLORPICKER" in title:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"picker.png"))
                elif "ENCODER" in title:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"enc.png"))
                elif "EXEC" in title:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"exec.png"))
                elif "FX" in title:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"fx.png"))
                else:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"scribble.png"))
            except Exception as e:
                print("Exception on load window icon",title)
                print("Exception:",e)
            #time.sleep(3)
            self.tk.deiconify()



        self.tk["bg"] = "black"
        self.tk.bind("<Button>",self.callback)
        self.tk.bind("<Key>",self.callback)
        self.tk.bind("<KeyRelease>",self.callback)
        self.tk.title(""+str(title)+" "+str(lf_nr)+":"+str(rnd_id))
        lf_nr+=1
        #self.tk.geometry("270x600+0+65")
        geo ="{}x{}".format(width,height)
        if left is not None:
            geo += "+{}".format(left)
            if top is not None:
                geo += "+{}".format(top)

        #self._event_clear = Xevent(fix=0,elem=None,attr="CLEAR",data=self,mode="ROOT").cb
        self.tk.geometry(geo)
        self.show()
    def update_idle_task(self):
        tkinter.Tk.update_idletasks(gui_menu_gui.tk)
        pass
    def close_app_win(self,event=None):
        print("close_app_win",self,event)
        if exit:
            save_window_position()
            self.tk.destroy()
        try:
            self.cb("<exit>").cb()
        except Exception as e:
            print("EXCETPION close_app",e)

    def title(self,title=None):
        if title is None:
            return self.tk.title()
        else:
            #return self.tk.title(title)
            return self.tk.title(""+str(title)+" "+str(lf_nr)+":"+str(rnd_id))
    def show(self):
        self.tk.deiconify()
        pass
    def mainloop(self):
        #save_window_position_loop() #like autosave
        try:
            self.tk.mainloop()
        finally:
            self.tk.quit()

    def callback(self,event,data={}):#value=255):
        global _global_short_key
        #time.sleep(0.1)
        if not _global_short_key:
            #cprint("<GLOBAL-GUI-EVENT-DISABLED>",event,color="red")
            return 1

        global _shift_key
        #cprint("<GUI>",event,color="yellow")
        #cprint("<GUI>",event.state,data,[event.type],color="yellow")
        value = 255
        if "Release" in str(event.type) or str(event.type) == '5' or str(event.type) == '3':
            value = 0
        if "keysym" in dir(event):
            if "Escape" == event.keysym:
                FIXTURES.clear()
                modes.val("ESC",1)
                master.refresh_fix()
            elif event.keysym in ["Shift_L","Shift_R"]:
                #cprint(event.type)
                if "KeyRelease" in str(event.type) or str(event.type) in ["3"]:
                    _shift_key = 0
                else:
                    _shift_key = 1
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                global _ENCODER_WINDOW
                if _shift_key:
                    _ENCODER_WINDOW.title("SHIFT/FINE ")
                else:
                    _ENCODER_WINDOW.title("ENCODER") 

            elif event.keysym in "ebfclrms" and value: 
                if "e" == event.keysym:
                    modes.val("EDIT",1)
                elif "b" == event.keysym:
                    modes.val("BLIND",1)
                elif "f" == event.keysym:
                    modes.val("FLASH",1)
                elif "c" == event.keysym:
                    modes.val("CFG-BTN",1)
                elif "l" == event.keysym:
                    modes.val("LABEL",1)
                elif "r" == event.keysym:
                    modes.val("REC",1)
                elif "m" == event.keysym:
                    x=modes.val("MOVE",1)
                    if not x:
                        PRESETS.clear_move()
                elif "s" == event.keysym:
                    modes.val("SELECT",1)
            elif event.keysym in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
                nr = int( event.keysym[1:]) # F:1-12
                nr = nr-1+81  
                cprint("F-KEY",value,nr,event.keysym)
                #print(event)
                master.preset_go(nr-1,xfade=None,val=value)
            elif event.keysym in ["1","2","3","4","5","6","7","8","9","0"]:
                nr = int( event.keysym)
                if nr == 0:
                    nr = 10
                nr = nr-1+161  
                cprint("NUM-KEY",value,nr)
                master.preset_go(nr-1,xfade=None,val=value)
            elif "End" == event.keysym:
                FIXTURES.fx_off("all")
                CONSOLE.fx_off("all")
                CONSOLE.flash_off("all")
            elif "Delete" == event.keysym:
                #PRESETS.delete(nr)
                if value:
                    modes.val("DEL",1)



class WindowManager():
    def __init__(self):
        self.windows = {}
        self.obj = {}
        self.nr= 0
        self.first=""
    def new(self,w,name="",obj=None):
        if not self.first:
            if name:
                self.first = name
            else:
                self.first = str(self.nr)
            w.tk.state(newstate='normal')
            w.tk.attributes('-topmost',True)


        if name:
            self.windows[str(name)] = w
            self.obj[str(name)] = obj
        else:
            self.windows[str(self.nr)] = w
            self.obj[str(self.nr)] = obj
            self.nr+=1
        #w.show()
    def mainloop(self):
        self.windows[self.first].mainloop()

    def get(self,name):
        print(self,".get(name) =",name)
        name = str(name)
        if name in self.windows:
            out = self.windows[name]
            print(out)
            return out
    def get_obj(self,name):
        #print(self,".get(name) =",name)
        name = str(name)
        if name in self.windows:
            out = self.obj[name]
            #print(out)
            return out

    def top(self,name):
        name = str(name)
        if name in self.windows:
            self.windows[name].tk.state(newstate='normal')
            self.windows[name].tk.attributes('-topmost',True)
            self.windows[name].tk.attributes('-topmost',False)
            self.windows[name].tk.update_idletasks()# gui_menu_gui.tk)
            #print("redraw",name)
            #if name == "PATCH":
            #    gui_patch.draw()
            #if name == "DIMMER":
            #    gui_fix.draw()
            if name == "EXEC":
                master._refresh_exec()
                self.windows[name].tk.update_idletasks()# gui_menu_gui.tk)
                #tkinter.Tk.update_idletasks(gui_menu_gui.tk)
        else:
            print(name,"not in self.windows",self.windows.keys())


class Console():
    def __init__(self):
        pass

    def flash_off(self,fix):
        pass#client.send("df0:alloff:::,")
    def fx_off(self,fix):
        cprint("Console.fx_off()",fix)
        if not fix or fix == "all":
            #client.send("fx0:alloff:,fxf:alloff:,")
            #client.send("df0:alloff:::,")
            j = []
            if 0:
                jdata = {'VALUE': None, 'args': [], 'FX': 'alloff::::', 'FADE': 2, 'DMX': '0'}
                j.append(jdata)
                jdata = {'VALUE': None, 'args': [], 'FX': 'alloff::::', 'FADE': 2,'FLASH':1, 'DMX': '0'}
                j.append(jdata)
            else:
                jdata = {'VALUE': None, 'args': [], 'FX2': {"TYPE":"alloff"}, 'FADE': 2,'FLASH':1, 'DMX': '1'}
                j.append(jdata)

            jclient_send(j)
            return 0

def test_1():
    #LibreLight --no-gui --show=unitest --dmx-out=on --exec="sel fix 1-10; go preset 2; encoder DIM sel; encoder DIM ++"
    pass



window_manager = WindowManager()

CONSOLE = Console()
PRESETS = Presets()

FIXTURES = Fixtures()

def LOAD_SHOW():
    PRESETS.load_presets()
    FIXTURES.load_patch()
    #draw_enc(gui,root2)
    #master._refresh_fix()
    #master._refresh_exec()
LOAD_SHOW()

master = MASTER()


class Refresher():
    def __init__(self):
        self.time = time.time()+1
    def reset(self):
        self.time = time.time()+.1
    def refresh(self):
        if time.time() > self.time:
            if time.time() < self.time+2:
                #self.time = time.time()+1
                self._refresh()
    def _refresh(self):
        print(self,"refresh()")
        master._refresh_fix()
        master._refresh_exec()
    def loop(self,args={}):
        while 1:

            try:
                self.refresh()
                tkinter.Tk.update_idletasks(gui_menu_gui.tk)
            except Exception as e:print("loop exc",e)
            time.sleep(0.2)


print("main",__name__)


__run_main = 0
if __name__ == "__main__":
    __run_main = 1
else:
    import __main__ 
    if "unittest" not in dir(__main__):
        __run_main = 1




refresher = Refresher()

if __run_main:
    print("main")
    thread.start_new_thread(refresher.loop,())
    

    TOP = _POS_TOP + 15
    L0 = _POS_LEFT 
    L1 = _POS_LEFT + 95
    L2 = _POS_LEFT + 920 
    W1 = 810
    H1 = 550
    HTB = 23 # hight of the titlebar from window manager

    w = Window("MAIN",master=1,width=85,height=H1//2,left=L0,top=TOP,resize=0)
    gui_menu_gui = w
    data = []
    #data.append({"text":"COMMAND"})
    #data.append({"text":"CONFIG"})
    data.append({"text":"PATCH"})
    data.append({"text":"DIMMER"})
    data.append({"text":"FIXTURES"})
    data.append({"text":"EXEC"})
    data.append({"text":"EXEC-WING"})
    gui_menu = GUI_menu(w.tk,data)

    window_manager = gui_menu.window_manager #= window_manager
    
    window_manager.new(w)


    name="EXEC"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w1 = ScrollFrame(w.tk,width=W1,height=H1)
    #frame_exe = w.tk
    #draw_preset(master,w1)#w.tk)
    draw_exec(master,w1,PRESETS)#w.tk)
    window_manager.new(w,name)

    name="CONFIG"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w1 = ScrollFrame(w.tk,width=W1,height=H1)
    #frame_exe = w.tk
    #draw_preset(master,w1)#w.tk)
    window_manager.new(w,name)

    name="DIMMER"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w2 = ScrollFrame(w.tk,width=W1,height=H1)
    #frame_dim = w1 # w.tk
    #master.draw_dim(w1.tk)
    window_manager.new(w,name)

    name="FIXTURES"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w1 = ScrollFrame(w.tk,width=W1,height=H1)
    #frame_fix = w1 #w.tk
    #draw_fix(master,w1,w2)#.tk)
    gui_fix = GUI_FIX(master,w1,w2)
    gui_fix.draw(FIXTURES)
    window_manager.new(w,name)


    name="FIXTURE-EDITOR"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w1 = ScrollFrame(w.tk,width=W1,height=H1)
    data=[]
    for i in range((24+12)*15):
        data.append({"text"+str(i):"test"})
    GUI_FaderLayout(w1,data)
    window_manager.new(w,name)

    name="MASTER-WING"
    #w = Window(name,master=0,width=730,height=205,left=L1-80,top=TOP+H1-200)
    w = Window(name,master=0,width=75,height=405,left=L0,top=TOP+H1-220)
    #w1 = ScrollFrame(w.tk,width=W1,height=H1)
    w1 = tk.Frame(w.tk,width=W1,height=H1)
    w1.pack()
    data=[]
    for i in range(2):
        data.append({"MASTER"+str(i):"MASTER"})
    GUI_MasterWingLayout(w1,data)
    window_manager.new(w,name)

    name="EXEC-WING"
    #w = Window(name,master=0,width=730,height=205,left=L1-80,top=TOP+H1-200)
    w = Window(name,master=0,width=600,height=415,left=L1,top=TOP+H1+HTB*2)
    #w1 = ScrollFrame(w.tk,width=W1,height=H1)
    w1 = tk.Frame(w.tk,width=W1,height=H1)
    w1.pack()
    data=[]
    for i in range(10*3):
        data.append({"EXEC"+str(i):"EXEC"})
    obj=GUI_ExecWingLayout(w1,data)
    window_manager.new(w,name,obj)


    name="ENCODER"
    w = Window(name,master=0,width=620,height=113,left=L0+710,top=TOP+H1+15+HTB*2)
    _ENCODER_WINDOW = w
    draw_enc(master,w.tk)#Xroot)
    window_manager.new(w,name)

    #name="REMOTE-CONTROL"
    #w = Window(name,master=0,width=220,height=113,left=L0+710,top=TOP+H1+HTB*2+123)
    #_ENCODER_WINDOW = w
    #draw_enc(master,w.tk)#Xroot)

    name = "SETUP"
    w = Window(name,master=0,width=415,height=42,left=L1+10+W1,top=TOP,resize=0)
    w.tk.title("SETUP   SHOW:"+master.base.show_name)
    draw_setup(master,w.tk)
    window_manager.new(w,name)

    name = "COMMAND"
    w = Window(name,master=0,width=415,height=130,left=L1+10+W1,top=TOP+81,resize=0)#+96)
    draw_command(master,w.tk)
    window_manager.new(w,name)

    name = "LIVE"
    w = Window(name,master=0,width=415,height=42,left=L1+10+W1,top=TOP+235,resize=0)#250)
    draw_live(master,w.tk)
    window_manager.new(w,name)

    name = "CLOCK"
    w = Window(name,master=0,width=335,height=102,left=L1+10+W1+80,top=TOP+H1+HTB+160,resize=0)#250)
    draw_clock(master,w.tk)
    window_manager.new(w,name)

    name="FX"
    w = Window(name,master=0,width=415,height=297,left=L1+10+W1,top=TOP+302,resize=0)#317)
    #frame_fx = w.tk
    draw_fx(master,w.tk)
    window_manager.new(w,name)


    name="PATCH"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    w1 = ScrollFrame(w.tk,width=W1,height=H1)
    main_preset_frame = w1
    gui_patch = GUI_PATCH(master,main_preset_frame)
    gui_patch.draw(FIXTURES)
    window_manager.new(w,name)

    #LibreLightDesk
    name="COLORPICKER"
    w = Window(name,master=0,width=600,height=113,left=L1+5,top=TOP+5+HTB*2+H1)
    draw_colorpicker(master,w.tk,FIXTURES,master)
    window_manager.new(w,name)

    name="TableA"
    w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    space_font = tk.font.Font(family="FreeSans", size=1 ) #, weight="bold")
    x=TableFrame(root=w.tk)#,left=80,top=620)
    w.show()
    data =[]
    for a in range(40):
        data.append(["E","E{}".format(a+1)])

    x.draw(data=data,head=["E","C"],config=[12,5,5])
    w=x.bframe

    #window_manager.new(w,name)



    #Xroot = tk.Tk()
    #Xroot["bg"] = "black" #white
    #Xroot.title( xtitle+" "+str(rnd_id) )
    #Xroot.geometry("1024x800+130+65")


    master.render()
    window_manager.top("Table")
    #w = frame_fix #Window("OLD",master=0,width=W1,height=500,left=130,top=TOP)
    window_manager.new(w,name)


    #Set EXEC-FADER SIZE TO 0 on Startup
    for nr in range(10):
        set_exec_fader(nr,0) #,color="#fff")

    load_window_position()
    try:
        #root.mainloop()
        #tk.mainloop()
        window_manager.mainloop()
        
    finally:
        master.exit()

