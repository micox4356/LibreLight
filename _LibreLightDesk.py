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
import subprocess
import string
import copy
import traceback
import tool.movewin as movewin

rnd_id  = str(random.randint(100,900))
rnd_id += " beta"
rnd_id2 = ""
rnd_id3 = ""
_ENCODER_WINDOW = None


import tool.git as git
rnd_id += git.get_all()


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

HOME = os.getenv('HOME')

import _thread as thread
import traceback

import tkinter
import tkinter as tk
from tkinter import font

space_font = None
import tkinter.simpledialog
from idlelib.tooltip import Hovertip

INIT_OK = 0
_global_short_key = 1


path = "/home/user/LibreLight/"
#os.chdir(path)
f = open(path+"init.txt","r")
lines=f.readlines()
f.close()
out = []
for line in lines:
    if line != "EASY\n":
        out.append(line)
f = open(path+"init.txt","w")
f.writelines(out)
f.close()
if "--easy" in sys.argv:
    f = open(path+"init.txt","a")
    f.write("EASY\n")
    f.close()
    if not os.path.isdir(path+"show/EASY"):
        cmd = "cp -vrf '/opt/LibreLight/Xdesk/home/LibreLight/show/EASY' '{}/show/EASY' ".format(path)
        print(cmd)
        #input()
        os.system(cmd)
    # check if EASY show exist !


icolor = 1
def cprint(*text,color="blue",space=" ",end="\n"):
    #return 0 #disable print dbg
    if not color:
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
    sys.stdout.flush() # to grep output

cprint("________________________________")
 



import lib.zchat as chat
import lib.motion as motion

from collections import OrderedDict

_FIX_FADE_ATTR = ["PAN","TILT","DIM","RED","GREEN","BLUE","WHITE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]


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
        cprint("Exception:",e)

    cprint("config read")
    for line in lines:
        line=line.strip()
        print("   config:",line)
        row = json.loads(line) 
        _config.append(row)

except Exception as e:
    cprint("Exception:",e)

try: 
    for row in _config:
        #print("   config:",row)
        if "POS_LEFT" in row:
           _POS_LEFT = int(row["POS_LEFT"]) 
        if "POS_TOP" in row:
           _POS_TOP = int(row["POS_TOP"]) 
except Exception as e:
    cprint("Exception:",e)


def showwarning(msg="<ERROR>",title="<TITLE>"):
    _main = tkinter.Tk()
    defaultFont = tkinter.font.nametofont("TkDefaultFont")
    cprint("showwarning",defaultFont)
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
                cprint("ESC",m)
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
    cprint("xcb","MODE CALLBACK",mode,value)
    if mode == "REC-FX":
        cprint("xcb",modes.val("REC-FX"))
#modes.set_cb(xcb)

POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]
#client = chat.tcp_sender(port=50001)


def set_exec_fader_cfg(nr,val,label="",color=""):
    exec_wing = window_manager.get_obj(name="EXEC-WING") 
    if not exec_wing: 
        return
    try:
        if len(exec_wing.fader_elem) > nr:
            exec_wing.fader_elem[nr].attr["text"] =  label
            cfg = get_exec_btn_cfg(nr+80)
            if cfg:
                exec_wing.fader_elem[nr].attr["bg"] = cfg["bg"]
                exec_wing.fader_elem[nr].attr["fg"] = cfg["fg"]
    except Exception as e:
        cprint("- exception:",e)
        print(nr,val,label)

def set_exec_fader(nr,val,label="",color="",info="info",change=0):
    exec_wing = window_manager.get_obj(name="EXEC-WING") 
    if not exec_wing: 
        return
    try:
        exec_wing.set_fader(nr,val,color=color,info=info,change=change)
    except Exception as e:
        pass
        cprint("- exception:",e)
        print(nr,val,label)
        raise e
   

def set_exec_fader_all():
    print()
    cprint( "set_exec_fader_all()",color="green")
    for nr in range(10):
        _label = PRESETS.label_presets[nr+80] # = label
        print("  _label",_label)
        set_exec_fader(nr,0,label=_label) 
        set_exec_fader_cfg(nr,0,label=_label)

def refresh_exec_fader_cfg():
    cprint( "set_exec_fader_all()",color="green")
    for nr in range(10):
        _label = PRESETS.label_presets[nr+80] # = label
        #print("_label",_label)
        set_exec_fader_cfg(nr,0,label=_label)

# remote input - start (memcached)
def JCB(x,sock=None):
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
            cprint("exception",e)
            print(sys.exc_info()[2])
        #print("remote in:",round(time.time(),0),"x",i,v)

r1_server = chat.Server(port=30002)
def server1_loop():
    while 1:
        r1_server.poll(cb=JCB)
        time.sleep(0.01)
thread.start_new_thread(server1_loop,()) # SERVER
# remote input - end
chat.dbg=1

class DEVENT():
    def __init__(self):
        #if "keysym" in dir(event):
        #if "Escape" == 
        #event.keysym:
        #event.num == 1:
        self.keysym = ""
        self.num = 1
        self.type = ""

def JSCB(x,sock=None):
    i = ""
    msg = ""
    msgs = []
    try:
        #print("JSCB",sock)
        for i in x:
            #print("i",[i])
            msgs = json.loads(i)
            print(" JSCB",msgs) #,sock)
            if type(msgs) is list:
                for msg in msgs:
                    print("  ",msg)
                    # FIXTURES.encoder
                    if "event" in msg:
                        if "FIXTURES" == msg["event"]:
                            FIX=0
                            VAL=""
                            ATTR=""
                            if "FIX" in msg:
                                FIX=msg["FIX"]
                            if "VAL" in msg:
                                VAL=msg["VAL"]
                            if "ATTR" in msg:
                                ATTR=msg["ATTR"]
                            print("  Xevent",FIX,VAL,ATTR)
                            #cb = Xevent(fix=FIX,elem=None,attr=ATTR,mode="ENCODER",data=[]) #data)
                            #FIXTURES.encoder(str(FIX),ATTR,xval="click",xfade=0,xdelay=0)#,blind=0)
                            FIXTURES.encoder(str(FIX),ATTR,xval=VAL,xfade=0,xdelay=0)#,blind=0)

                            #print(dir(cb))
                            #event =  DEVENT()
                            #event.num = enum

                            #master.refresh_fix() # delayed
                            #refresher_fix.reset() # = Refresher()
                            #cb.cb(event)
                        if "CLEAR" == msg["event"]:
                            FIXTURES.clear()
            #bounce msg
            #if sock:
            #    msg = json.dumps(msg)
            #    msg = bytes(msg,"utf8")
            #    chat._send(sock,msg)
            
    except Exception as e:
        cprint("exception JSCB:",e)
        cprint("- i:",i)
        cprint("- msg:",msgs)
        cprint(traceback.format_exc(),color="red")
        if sock:
            msg = ["Notice: Exception on JSCB-SERVER: ",str(e)]
            msg = json.dumps(msg)
            msg = bytes(msg,"utf8")
            chat._send(sock,msg)



# external GUI
r_server = chat.Server(port=30003,cb=JSCB)
def server_loop():
    while 1:
        r_server.poll(cb=JSCB)
        time.sleep(0.001)
thread.start_new_thread(server_loop,()) # SERVER

# read memcachd
memcache = None
try:
    import memcache
except Exception as e:
    cprint("Exception IMPORT ERROR",e)
        
class MC_FIX():
    def __init__(self,server="127.0.0.1",port=11211):
        cprint("MC.init() ----------" ,server,port,color="red")
        try:
            #self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            self.mc = memcache.Client(['{}:{}'.format(server,port)], debug=0)
            #self.init()
        except Exception as e:
            cprint("-- Exception",e)

    def set(self,index="fix",data=[]):
        #time.sleep(5)

        if 1: #while 1:
            #print("MC.send",index) #,data) 
            index = self.mc.get("index")
            #if index:
            #    for i in index:
            #        print("  key",i)

            self.mc.set("fix", data)

        #examles
        #self.mc.set("some_key", "Some value")
        #self.value = mc.get("some_key")
        #self.mc.set("another_key", 3)
        #self.mc.delete("another_key")


class MC():
    def __init__(self,server="127.0.0.1",port=11211):
        cprint("MC.init() ----------" ,server,port,color="red")
        try:
            #self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            self.mc = memcache.Client(['{}:{}'.format(server,port)], debug=0)
            #self.init()
        except Exception as e:
            cprint("-- Exception",e)

        # def init(self):
        data = {}
        start = time.time()
        delta = start
        index = self.mc.get("index")
        if index:
            for i in index:
                print("  key",i)
        self.last_fader_val = [-1]*512
        self.fader_map = []
        for i in range(30+1):
            self.fader_map.append({"UNIV":0,"DMX":0})

        try:
            fname = HOME + "/LibreLight/fader.json"
            f = open(fname)
            lines = f.readlines()
            cprint("FADER MAP",fname)

            for i,line in enumerate(lines):
                jdata = json.loads(line)
                print("  fader_map ->>",i,jdata)
                self.fader_map[i] = jdata

        except Exception as e:
            cprint("-- Except Fader_map",e)
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
        cprint("++++++++++ start.memcachd read loop",self )
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
                                #print("dmx_in change:",[i,val])
                                change = 0
                                if i < len(self.last_fader_val):
                                    if self.last_fader_val[i] != val:
                                        self.last_fader_val[i] = val
                                        print("dmx_in change:",[i,val])
                                        change = 1
                                set_exec_fader(nr=i,val=val,color="#aaa",info="dmx_in",change=change)
                        except Exception as e:
                            cprint("MC exc:",e,color="red")
                            traceback.print_exc()
                            pass

                time.sleep(0.01)
            except Exception as e:
                cprint("exc", e)
                time.sleep(1)

_mc=MC()
_mc.loop()

console = chat.Client() #port=50001)

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
                jdata["DMX"] = int(jdata["DMX"])
                dmx = jdata["DMX"]

                if "ATTR" not in jdata:
                    # for fx off
                    jdatas.append(jdata)

                else: 
                    fix = "00000"
                    attr = "00000"
                    if "FIX" in jdata:    
                        fix  = jdata["FIX"]
                    if "ATTR" in jdata:    
                        attr = jdata["ATTR"]

                    dmx_fine = FIXTURES.get_dmx(fix,attr+"-FINE")
                    if jdata["DMX"] != dmx_fine and dmx > 0 and dmx_fine > 0:
                        jdata["DMX-FINE"] = dmx_fine
                    if "DMX-FINE" in jdata:
                        if jdata["DMX-FINE"] <= 0:
                            del jdata["DMX-FINE"] 
                       
                        

                    if jdata["ATTR"].startswith("_"):
                        pass # ignore attr._ACTIVE 
                    else:
                        jdatas.append(jdata)
                
                #cprint("-- ",jdata,color="red")

            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint(e,color="red")
                cprint("-----",color="red")
            
    jtxt = jdatas
    jtxt = json.dumps(jtxt)
    jtxt = jtxt.encode()
    console.send( jtxt ) #b"\00 ")
    cprint("{:0.04} sec.".format(time.time()-t_start),color="yellow")
    cprint("{:0.04} tick".format(time.time()),color="yellow")


def _highlight(fix,_attr="DIM"): 
    " patch test button "
    cprint("highlight",fix,"1")

    if fix not in FIXTURES.fixtures:
        return None

    d = FIXTURES.fixtures[fix]

    #for k,v in d.items():
    #    cprint("-",k,v)
    DMX = d["DMX"] + d["UNIVERS"]*512
    if "ATTRIBUT" in d:
        ATTR= d["ATTRIBUT"]
        data = {"VALUE":200,"DMX":1}
        attr = ""

        if _attr in ATTR:
            attr = _attr
        else:
            return #stop
        
    
        cprint(attr,ATTR[attr])
        old_val = ATTR[attr]["VALUE"]
        data["DMX"] = DMX + ATTR[attr]["NR"]-1
        cprint(attr,ATTR[attr])
        cprint(data)
        for i in range(3):
            cprint("highlight",fix,"0")
            data["VALUE"] = 100
            jclient_send([data])
            time.sleep(0.1)

            cprint("highlight",fix,"1")
            data["VALUE"] = 234
            jclient_send([data])
            time.sleep(0.3)

        
        cprint("highlight",fix,"0")
        data["VALUE"] = old_val 
        jclient_send([data])

def highlight2(fix,attr="DIM"):
    def x():
        highlight(fix,attr=attr)
    return x

def highlight(fix):
    cprint("highlight",fix)
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

        if "FX" not in row:
            cprint("698 FX not in row...",row,color="red")
            row["FX"] = ""
        else:
            if type(row["FX"]) is not str:
                cprint("702 FX is not str...",row,color="red")
                row["FX"] = ""

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
            cprint("wing",i,"j",j,"wing_count:",wing_count,"wing",wing)
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

                if attr.startswith("_"):
                    continue
                if attr.endswith("-FINE"):
                    continue

                jdata = {"MODE":"FX"}
                jdata["VALUE"]    = None
                jdata["FIX"]      = fix
                dmx               = FIXTURES.get_dmx(fix,attr)
                jdata["DMX"]      = dmx

                dmx_fine = FIXTURES.get_dmx(fix,attr+"-FINE")
                if dmx_fine != jdata["DMX"] and dmx > 0:
                    jdata["DMX-FINE"] = dmx_fine

                jdata["ATTR"]     = attr

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
    master._refresh_fix()

    return jdatas

def process_matrix(xfixtures):
    fix_count = len(xfixtures)
    fx_x = fx_prm["FX-X"]
    fx_mod = fx_x_modes[fx_prm["FX:MODE"]]
    cprint("----",fx_x,fx_mod)
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
                    cprint([i,f,j])
                    out[j] = f

            matrix.mprint(out,w,h)
            xfixtures = out
        except Exception as e:
            cprint("matrix exception",e)

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
                    master._refresh_fix()
                    return 0

                #if event.num == 1:
            elif self.attr == "REC-FX":
                cprint("ELSE",self.attr)
                modes.val(self.attr,1)

            return 0
            
    def cb(self,event):
        cprint("EVENT_fx cb",self.attr,self.mode,event,color='yellow')
        cprint(["type",event.type,"num",event.num])
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
        

window_list_buffer = {}

def save_window_position(save_as=""):
    global window_list_buffer
    cprint()
    cprint("save_window_position",[save_as])

    base = Base()
    fname = HOME+"/LibreLight"
    fname = base.show_path1 +base.show_name 
    if save_as:
        fname = save_as 
    fname +=  "/gui.txt"
    cprint("- fname",fname)

    for k in window_list_buffer:
        window_list_buffer[k][0] = 0   

    for k,win in window_manager.windows.items():
        try:
            geo = win.tk.geometry()
            data = [1,k,geo]
            if k not in  window_list_buffer:
                cprint("-- new:win:pos",k.ljust(15," "),data)
            elif window_list_buffer[k][2] != geo:
                cprint("-- update:win:pos",k.ljust(15," "),data)
            window_list_buffer[k] = data

            if k in ["PATCH","FIXTURES","DIMMER","FIXTURE-EDITOR","CONFIG"]:
                window_list_buffer[k][0] = 0   

        except Exception as e:
            cprint("-A save_window_position Exception:",k,e,color="red")

    lines = ""
    for k,data in window_list_buffer.items():
        try:
            #print("-- save:win:pos",k.ljust(15," "),data)
            if not data[2]:
                continue
            line ="{} {} {}\n"
            line = line.format(data[0],k,data[2])
            lines += line
        except Exception as e:
            cprint("-A save_window_position Exception:",e,color="red")

    try:
        f = open(fname,"w")
        f.write( lines )
    except Exception as e:
        cprint("-B save_window_position Exception:",e,color="red")
    finally:
        f.close() #f.flush()



def save_window_position_loop(): # like autosave
    def loop():
        time.sleep(20)
        try:
            while 1:
                save_window_position()
                time.sleep(60)
        except Exception as e:
            cprint("save_loop",e)
    thread.start_new_thread(loop,())

def get_window_position(_filter="",win=None):
    global window_list_buffer
    cprint()
    show = None
    k = _filter
    geo = ""

    cprint("get_window_position",[_filter])
    if _filter in window_list_buffer:
        show,k,geo  = window_list_buffer[_filter]
        if win:
            win.tk.geometry(geo)
    return show,k,geo


def read_window_position():
    try:
        base = Base()
        fname = HOME+"/LibreLight"
        fname = base.show_path1 +base.show_name 
        fname +=  "/gui.txt"
        cprint("- fname:",fname)
        f = open(fname,"r")
        lines = f.readlines()
        f.close()
        out = []
        for line in lines:
            line = line.strip()
            #print(line)
            if " " in line:
                if line.count(" ") >= 2:
                    show,name,geo = line.split(" ",2)
                elif line.count(" ") == 1:
                    name,geo = line.split(" ",1)
                    show = 1

                if "--easy" in sys.argv:
                    if name not in ["MAIN","EXEC","SETUP"]:
                        show=0
            out.append([show,name,geo])

        return out
    except Exception as e:
        cprint("- load_window_position 345 Exception:",e,color="red")
        return 
    return []

def split_window_show(lines,_filter=""):
    try:
        for show,name,geo in lines:
            #print( "wwWww "*10,[show,name,geo] )
            if _filter in name:
                return int(show)
    except Exception as e:
        cprint("- split_window_show 345 Exception:",e,color="red")

def split_window_position(lines,_filter=""):
    try:
        for show,name,geo in lines:
            #print( "wwWww "*10,[show,name,geo] )
            if _filter in name:
                geo = geo.replace("+"," ")
                geo = geo.replace("x"," ")
                geo = geo.split()
                #print( "wwWww "*10,[show,name,geo] )
                if len(geo) == 4:
                    #print( [show,name,geo] )
                    args = {}
                    args["width"]  = int(geo[0])
                    args["height"] = int(geo[1])
                    args["left"]   = int(geo[2])
                    args["top"]    = int(geo[3])
                    return args
    except Exception as e:
        cprint("- split_window_position 345 Exception:",e,color="red")



def load_window_position(_filter=""):
    print()
    global window_list_buffer
    cprint()
    cprint("load_window_position",[_filter])
    try:
        lines = read_window_position()

        data = {}
        for show,name,geo in lines:
            data[name] = [show,name,geo]
            window_list_buffer[name] = [show,name,geo]

        for name,win in window_manager.windows.items():
            if not win:
                continue

            if name not in data:
                continue

            if _filter:
                if _filter != name:
                    continue

            w = data[name][2] 

            print("  set_win_pos","filter:",[_filter],"Name: {:<20}".format(name),w,win)
            try:
                win.tk.geometry(w)
            except Exception as e:
                cprint("- load_window_position 544 Exception:",e,color="red")

    except Exception as e:
        cprint("- load_window_position 345 Exception:",e,color="red")
        return 
 
class BLINKI():
    def __init__(self,e):
        self.e = e
    def blink(self):
        e = self.e
        e.config(bg='green')
        duration = 150
        for i in range(8):
            d = i * duration
            if i % 2 == 0:
                e.after(d, lambda: e.config(bg='white')) # after 1000ms
                e.after(d, lambda: e.config(activebackground='white')) # after 1000ms
            else:
                e.after(d, lambda: e.config(bg='orange')) # after 1000ms
                e.after(d, lambda: e.config(activebackground='orange')) # after 1000ms
        i+=1
        duration = 150
        e.after(d, lambda: e.config(bg='white')) # after 1000ms
        e.after(d, lambda: e.config(activebackground='white')) # after 1000ms

class Xevent():
    """ global input event Handeler for short cut's ... etc
    """
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode

    def _save_show(self):
        self.elem["bg"] = "orange"
        self.elem["text"] = "SAVING..."
        self.elem["bg"] = "red"
        self.elem.config(activebackground="orange")
        modes.val(self.attr,1)
        PRESETS.backup_presets()
        FIXTURES.backup_patch()
        save_window_position()
        self.elem["bg"] = "lightgrey"
        self.elem.config(activebackground="lightgrey")
        b = BLINKI(self.elem)
        b.blink()
        self.elem["text"] = "SAVE\nSHOW"

    def setup(self,event):       
        cprint("xevent.SETUP",[self.mode,self.attr],color="red")
        if self.mode == "SETUP":
            if self.attr == "SAVE\nSHOW":
                self._save_show()
            elif self.attr == "LOAD\nSHOW":
                name = "LOAD-SHOW"
                base = Base()
                line1 = "PATH: "+base.show_path1 +base.show_name
                line2 = "DATE: "+ time.strftime("%Y-%m-%d %X",  time.localtime(time.time()))
                class cb():
                    def __init__(self,name=""):
                        self.name=name
                        cprint("   LOAD-SHOW.init",name)
                    def cb(self,event=None,**args):
                        cprint("   LOAD-SHOW.cdb",self.name,event,args)
                        if self.name != "<exit>":
                            cprint("-----------------------:")
                            LOAD_SHOW_AND_RESTAT(self.name).cb()

                pw = PopupList(name,cb=cb)
                print(line1,line2)
                frame = pw.sframe(line1=line1,line2=line2)
                r = frame_of_show_list(frame,cb=cb)
            elif self.attr == "NEW\nSHOW":
                base = Base()

                #def _cb(fname):
                def _cb(data):
                    if not data:
                        cprint("err443",self,"_cb",data)
                        return None
                    fname = data["Value"]
                    cprint(self,"save_show._cb()",fname)
                    fpath,fname = base.build_path(fname)
                    cprint("SAVE NEW SHOW",fpath,fname)
                    if base._create_path(fpath):
                        a=PRESETS.backup_presets(save_as=fpath,new=1)
                        b=FIXTURES.backup_patch(save_as=fpath,new=1)
                        #base._set(fname)
                        
                        save_window_position(save_as=fpath)
                        LOAD_SHOW_AND_RESTAT(fname).cb() 
                dialog._cb = _cb
                dialog.askstring("CREATE NEW SHOW","CREATE NEW SHOW:")
            elif self.attr == "SAVE\nSHOW AS":
                base = Base()

                #def _cb(fname):
                def _cb(data):
                    if not data:
                        cprint("err443",self,"_cb",data)
                        return None
                    fname = data["Value"]
                    cprint(self,"save_show._cb()",fname)
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
                self.elem.config(activebackground="orange")
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()

                save_window_position()
                self.elem["text"] = "RESTARTING..."
                self.elem["bg"] = "lightgrey"
                self.elem.config(activebackground="lightgrey")
                LOAD_SHOW_AND_RESTAT("").cb(force=1)
            elif self.attr == "DRAW\nGUI":
                old_text = self.elem["text"]
                window_manager.top("PATCH")
                gui_patch.draw(FIXTURES)
                gui_fix.draw(FIXTURES)
                window_manager.top("FIXTURES")
                master._refresh_exec()
                self.elem["text"] = old_text  
            elif self.attr == "PRO\nMODE":
                self._save_show()
                import lib.restart as restart
                restart.pro()
            elif self.attr == "EASY\nMODE":
                self._save_show()
                import lib.restart as restart
                restart.easy()
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
                cprint("EVENT CHANGE:",self.mode,value,self.attr)
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
                        master._refresh_fix()
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
                cprint("s-key",_global_short_key)
            else:
                if event.num == 1:
                    cprint("ELSE",self.attr)
                    modes.val(self.attr,1)

            return 0


    def encoder(self,event):
        global _shift_key
        cprint("Xevent","ENC",self.fix,self.attr,self.mode)
        cprint("SHIFT_KEY",_shift_key,"??????????")

        if self.mode == "ENCODER":
            if self._encoder(event):
                master.refresh_fix() # delayed
                refresher_fix.reset() # = Refresher()

        if self.mode == "ENCODER2":
            if self._encoder(event):
                master.refresh_fix() # delayed
                refresher_fix.reset() # = Refresher()

        if self.mode == "INVERT":
            cprint("INVERT",event)
            if self._encoder(event):
                master.refresh_fix() # delayed
                refresher_fix.reset() # = Refresher()

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
            #print("SHIFT",val,_shift_key)
            if val:
                FIXTURES.encoder(fix=self.fix,attr=self.attr,xval=val)
                return 1       


            
    def cb(self,event):
        cprint("EVENT cb",self.attr,self.mode,event,color='yellow')
        cprint(["type",event.type,"num",event.num])

        global INIT_OK
        INIT_OK = 1
        try:
            change = 0
            if "keysym" in dir(event):
                if "Escape" == event.keysym:
                    ok = FIXTURES.clear()
                    master._refresh_fix()
                    cprint()
                    return 0

            if self.mode == "SETUP":
                self.setup(event)
            elif self.mode == "COMMAND":
                self.command(event)
            elif self.mode == "LIVE":
                self.live(event)
            elif self.mode == "ENCODER":
                self.encoder(event)
                master.refresh_fix()

            elif self.mode == "ENCODER2":
                self.encoder(event)
            elif self.mode == "INVERT":
                self.encoder(event)
            elif self.mode == "FX":
                cprint("Xevent CALLING FX WRONG EVENT OBJECT !!",color="red")
            elif self.mode == "ROOT":
                if event.keysym=="Escape":
                    pass

            elif self.mode == "INPUT":
                cprint("INP",self.data.entry.get())
                if event.keycode == 36:
                    x=self.data.entry.get()
                    #client.send(x)

            elif self.mode == "INPUT2":
                cprint("INP2",self.data.entry2.get())
                if event.keycode == 36:
                    x=self.data.entry2.get()
                    #client.send(x)

            elif self.mode == "INPUT3":
                cprint("INP3",self.data.entry3.get())
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
                            time.sleep(0.05)
                            master._refresh_exec(nr=nr)
                        elif modes.val("DEL"):
                            ok=PRESETS.delete(nr)
                            if ok:
                                modes.val("DEL",0)
                                #master.refresh_exec()
                                master._refresh_exec(nr=nr)
                        elif modes.val("COPY"):
                            ok=PRESETS.copy(nr)
                            if ok:
                                modes.val("COPY",0)
                                master._refresh_exec(nr=nr)
                        elif modes.val("MOVE"):
                            ok,cnr,bnr=PRESETS.move(nr)
                            if ok:
                                #modes.val("MOVE",0) # keep MOVE on
                                master._refresh_exec(nr=nr)
                                master._refresh_exec(nr=bnr)
                        elif modes.val("CFG-BTN"):
                            master.btn_cfg(nr)
                            #master._refresh_exec(nr=nr)
                        elif modes.val("LABEL"):#else:
                            master.label(nr)
                            #master._refresh_exec(nr=nr)

                        elif modes.val("EDIT"):
                            FIXTURES.clear()
                            self.data.preset_select(nr)
                            self.data.preset_go(nr,xfade=0,event=event,val=255,button="go")
                            modes.val("EDIT", 0)
                            master.refresh_fix()
                            refresher_fix.reset() # = Refresher()

                        elif modes.val("SELECT"):
                            self.data.preset_select(nr)
                        else:
                            self.data.preset_go(nr,event=event,val=255)
                    else:
                        self.data.preset_go(nr,xfade=0,event=event,val=0)
                        cprint(" == "*10)
                        master.refresh_fix()
                        refresher_fix.reset() # = Refresher()

                        
                if event.num == 3:
                    if not modes.val("REC"):
                        if str(event.type) == '4': #4 ButtonPress
                            self.data.preset_go(nr,xfade=0,ptfade=0,event=event,val=255)
                        else:
                            self.data.preset_go(nr,xfade=0,ptfade=0,event=event,val=0)
                        
                cprint()
                return 0
            elif self.mode == "INPUT":
                cprint()
                return 0

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        cprint()
        return 1 
        
def wheel(event,d=None):
    cprint("wheel",event,d)
    



class Element():
    def __init__(self):
        self.__data = {}
    def set(self,key,val):
        self.__data[key] = val

def _fixture_decode_sav_line(line):
    out = None
    out = [0,"none",{}]

    if line.count("\t") < 2:
        cprint("Error line.count('\\t') < 2  (is:{})".format(line.count("\t")),color="red",end=" ")
        cprint("file:{}".format(line),color="red")
    else:
        key,label,rdata = line.split("\t",2)
        jdata = json.loads(rdata,object_pairs_hook=OrderedDict)
        key = int(key)
        #label += " dsav"
        #label = label.replace(" dsav","")
        out = [key,label,jdata]

    #if not out:
    #print(line)
    #sys.exit()
    return out

def _fixture_repair_nr0(jdata):
    nrnull = 0
    if "ATTRIBUT" in jdata:  # translate old FIXTURES.fixtures start with 0 to 1          
        if nrnull:
            cprint("DMX NR IS NULL",attr,"CHANGE +1")
            for attr in jdata["ATTRIBUT"]:
                if "NR" in jdata["ATTRIBUT"][attr]:
                    nr = jdata["ATTRIBUT"][attr]["NR"]
                    if nr >= 0:
                        jdata["ATTRIBUT"][attr]["NR"] +=1
    #return jdata
        
def _clean_path(fpath):
    _path=[]
    for i in fpath:
        fpath = fpath.replace(" ","_")
        if i in string.ascii_letters+string.digits+"äöüßÖÄÜ_-":
            _path.append(i)
    path = "".join(_path)
    return path

def _read_init_txt(show_path):
    fname = show_path+"init.txt"
    show_name = None
    msg = ""

    if not os.path.isfile( fname ):
        msg = "_read_init_txt Errror: " +fname +"\n NOT FOUND !"
        return [None,msg]

    try:
        f = open(fname,"r")
        for line in f.readlines():
            line = line.strip()
            print("  init.txt:",[line])
            if line.startswith("#"):
                continue
            if not line:
                continue

            show_name = line
            show_name = show_name.replace(".","")
            show_name = show_name.replace("\\","")
            show_name = show_name.replace("/","")
    except Exception as e:
        cprint("show name exception",color="red")
        msg="read_init_txt Error:{}".format(e)
    finally:
        f.close()

    return [show_name,msg]


def _listdir(show_path):
    #self._check()
    show_list =  list(os.listdir( show_path ))
    out = []
    for fname in show_list:
        if fname == "EASY": #hidde EASY show in list !
            continue
        #print(fname)
        ctime = os.path.getmtime(show_path+fname)
        ctime = time.strftime("%Y-%m-%d %X",  time.localtime(ctime)) #1650748726.6604707))
        try:
            mtime = os.path.getmtime(show_path+fname+"/patch.sav")
            mtime = time.strftime("%Y-%m-%d %X",  time.localtime(mtime)) #1650748726.6604707))
        except:
            mtime = 0

        if mtime:
            out.append([fname,mtime])#,ctime])

    from operator import itemgetter
    out=sorted(out, key=itemgetter(1))
    out.reverse()
    return out



def _read_sav_file(xfname):
    cprint("load",xfname)
    lines = []
    if not os.path.isfile(xfname):
        return []

    f = open(xfname,"r")
    lines = f.readlines()
    f.close()    

    data   = OrderedDict()
    labels = OrderedDict()
    i=0
    for line in lines:
        r = _fixture_decode_sav_line(line)
        if r:
            key,label,jdata = r
            _fixture_repair_nr0(jdata)
            data[key]   = jdata
            labels[key] = label
        
    return data,labels


class Base():
    def __init__(self):
        cprint("Base.init()",color="red")
        self._init()

    def _init(self):
        show_name = "" #DemoShow #"ErrorRead-init.txt"
        self.show_path0 = HOME +"/LibreLight/"
        self.show_path  = self.show_path0 
        self.show_path1 = self.show_path0 + "show/"
        
        msg = " X "
        self.show_name,msg = _read_init_txt(self.show_path)
        if not self.show_name:
            r=tkinter.messagebox.showwarning(message=msg,parent=None)
            sys.exit()
        
        fpath = self.show_path1 +show_name 
        if not os.path.isdir(fpath):
            cprint(fpath)
            cprint( os.path.isdir(fpath))

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
        cprint("SET SHOW NAME",fname,ok,ini)
        try:
            f = open( ini ,"r")
            lines = f.readlines()
            f.close()
            if len(lines) >= 10: # cut show history
                cprint("_set",ini,len(lines))
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
        cprint("BASE._list()")
        out = _listdir(self.show_path1)
        return out

    def _load(self,filename):
        xpath = self.show_path+"/"+str(filename)+".sav"
        if not os.path.isfile(xpath):
            msg = ""#"Exception: {}".format(e)
            msg += "\n\ncheck\n-init.txt"
            cprint(msg,color="red")
            showwarning(msg=msg,title="load Error")
            return
        return _read_sav_file(xpath)



    def build_path(self,save_as):
        save_as = _clean_path(save_as)
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

        cprint("backup",xfname)
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
        cprint( repr(undermouse))
    def callback(self,event):
        cprint(__file__,self,"callback",event)
        cnv = self.win
        item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
        tags = cnv.gettags(item)
        #cnv.itemconfigure(self.tag, text=tags[0])
        cprint(tags,item)
        color = cnv.itemcget(item, "fill")
        cnv.itemconfig("all", width=1)#filla="green")
        cnv.itemconfig(item, width=3)#filla="green")
        cprint(color)
        cprint( hex_to_rgb(color[1:]))

def get_exec_btn_cfg(nr):
    #b.configure(fg=_fg,bg=_bg,activebackground=_ba,text=_text)
    #for k in PRESETS.val_presets: 
    k = nr
    if 1:
        _bg = "grey"
        _ba = "grey"
        _fg = "lightgrey"
        _text = "N/V"

        if nr >= 0:
            #if self._nr_ok:
            #    return #pass#abreak
            if nr != k:
                return #continue
            #else:
            #    self._nr_ok = 1


        label = ""

        #if k not in self.elem_presets:
        #    cprint("ERROR",k ,"not in elem_presets continue")
        #    return #continue
        if k in PRESETS.label_presets:
            label = PRESETS.label_presets[k]
            #print([label])
        #b = self.elem_presets[k]
        
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
            _text = txt
            #if b.text != txt: # TODO
            #    #txt+=str(self._XX)
            #    #b.configure(text= txt)
            #    _text = txt
            #    _bg="yellow"
            #    _ba="yellow"

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

                #try:b.configure(fg= "black")
                #except:pass
                if val_color:
                    _bg = "gold"
                    _ba = "#ffaa55"
                    if fx_color:
                        _fg = "blue"
                else:   
                    if fx_color:
                        fx_only = 1
            else:
                _bg = "grey"
                _ba = "#aaa"


        if "\n" in txt:
            txt1 = txt.split("\n")[0]

        _fg = "black"
        if ifval:
            if fx_only:
                _bg = "cyan"
                _ba = "#55d4ff"

            if "SEL" in txt1:
                #b.configure(bg="#77f")
                _bg = "#77f"
        else: 
            _bg = "grey"
            _fg = "darkgrey"

            if "SEL" in txt1:
                _fg = "blue"
            elif "ON" in txt1:
                _fg = "#040"
            elif "GO" in txt1:
                _fg = "#555"

        if "FL" in txt1:
            _fg = "#00e"
        
        out = {}
        out["bg"] = _bg
        out["ba"] = _ba
        out["fg"] = _fg
        out["text"] = _text
        
        return out
        #b.configure(fg=_fg,bg=_bg,activebackground=_ba,text=_text)

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
        
        self.setup_elem = {} # Elem_Container()
        self.setup_cmd  = ["SAVE\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS","SAVE &\nRESTART","DRAW\nGUI","PRO\nMODE"]

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
                ,"BLIND","CLEAR","REC","EDIT","COPY",".","\n" 
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
        try:
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
        except Exception as e:cprint("exc",self,e)

    def btn_cfg(self,nr,testing=0):
        cfg    = PRESETS._btn_cfg(nr) 
        button = PRESETS.btn_cfg(nr) 
        label  = PRESETS.label(nr) 

        def _cb(data):
            if not data:
                cprint("err443",self,"_cb",data)
                return None
            cprint(self,"btn_cfg._cb()",data)
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
            master._refresh_exec(nr=nr)
        dialog._cb = _cb

        if 1: # testing:
            dialog.ask_exec_config(str(nr+1),button=button,label=label,cfg=cfg)
        else:
            dialog.askstring("CFG-BTN","GO=GO FL=FLASH\nSEL=SELECT EXE:"+str(nr+1),initialvalue=txt)

    def label(self,nr):
        txt = PRESETS.label(nr) 
        def _cb(data):
            if not data:
                cprint("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            cprint(self,"label._cb()",nr,txt)
            if txt:
                PRESETS.label(nr,txt) 
                self.elem_presets[nr].configure(text = PRESETS.get_btn_txt(nr))
            modes.val("LABEL", 0)

            master._refresh_exec(nr=nr)

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
        cprint("__del__",self)
        PRESETS.backup_presets()
        #print("********************************************************")
        FIXTURES.backup_patch()
        #print("*********del",self,"***********************************************")
    def refresh_exec(self):
        refresher_exec.reset() # = Refresher()

    def _refresh_exec(self,nr=-1):
        s = time.time()
        cprint("PRESET.refresh_exec()")
        refresher_exec.reset() # = Refresher()
        
        self._XX +=1
        self._nr_ok = 0

        for nr in PRESETS.val_presets: 
            cfg = get_exec_btn_cfg(nr)
            if not cfg:
                out = {}
                out["bg"] = "lightgrey"
                out["ba"] = "grey"
                out["fg"] = "grey"
                out["text"] = "?"
                cfg = out

            b = self.elem_presets[nr]
            b.configure(fg=cfg["fg"],bg=cfg["bg"],activebackground=cfg["ba"],text=cfg["text"])


        time.sleep(0.01)
    def refresh_fix(self):
        refresher_fix.reset() # = Refresher()
    def _refresh_fix(self):
        cprint(self,"_refresh_fix")
        s=time.time(); _XXX=0

        menu_buff = {"DIM":0,"DIM-SUB":0,"FIX":0,"FIX-SUB":0}

        elem_buffer = []

        for fix in FIXTURES.fixtures:                            
            sdata = FIXTURES.fixtures[fix]                            

            elem_attr_fix = None
            if fix in self.elem_attr:
                elem_attr_fix = self.elem_attr[fix]

            if "DIM" in sdata["ATTRIBUT"] and "_ACTIVE" in sdata["ATTRIBUT"] and len(sdata["ATTRIBUT"]) == 2:
                KEY = "DIM-SUB"
            else:
                KEY = "FIX-SUB"
            FIX = 0
            DIM = 0
            for attr in sdata["ATTRIBUT"]:
                _buff = {}
                row = sdata["ATTRIBUT"][attr]

                if attr.endswith("-FINE"):
                    continue

                b_attr = attr
                if b_attr == "_ACTIVE":
                    b_attr = "S"

                elem = None
                if elem_attr_fix:
                    if b_attr not in elem_attr_fix:
                        continue

                    elem = elem_attr_fix[b_attr]
                    if not elem:
                        continue
                

                
                if "elem" not in _buff:
                    _buff["elem"] = elem

                if not attr.startswith("_"):
                    v2 = row["VALUE"]
                    #_text  = "{} {}".format(str(attr).rjust(4,"0"),str(v2).rjust(4,"0")) # ~0.2 sec
                    _text  = "{} {}".format(attr,v2) 
                    _buff["text"] = _text

                if row["ACTIVE"]:
                    _buff["bg"] = "yellow"
                    _buff["abg"] = "yellow"

                    menu_buff[KEY] += 1
                    if b_attr == "S":
                        if KEY == "DIM-SUB":
                            DIM =1
                        else:
                            FIX =1
                else:
                    _buff["bg"] = "grey"
                    _buff["abg"] = "grey"

                if "FX" not in row: # insert FX2 excetption
                    row["FX"] = "" #OrderedDict()
                if "FX2" not in row: # insert FX2 excetption
                    row["FX2"] = {} #OrderedDict()
                #print("row",fix,row)    
                if row["FX"]:
                    _buff["fg"] = "blue"
                elif row["FX2"]:
                    _buff["fg"] = "red"
                else:
                    _buff["fg"] = "black"

                elem_buffer.append(_buff)

            menu_buff["FIX"] += FIX
            menu_buff["DIM"] += DIM

        cprint(" =+= "*10,"refresh_fix")
        try:
            for row in elem_buffer:
                elem = row["elem"]
                if not elem:
                     continue
                #print("<elem>",elem)
                for e in row:
                    if e == "elem":
                        continue
                    v = row[e]
                    #print("confg:",["key:",e,"val:",v])

                    if e == "abg":
                        elem.config(activebackground=v)
                    else:
                        elem[e] = v
            w = window_manager.get_win("FIXTURES")
            #print(dir(w))
            w.update_idle_task()
            #tkinter.Tk.update_idletasks(w)
        except Exception as e:
            cprint("exc434",e)

        cprint("fix:",_XXX,round(time.time()-s,2),color="red");_XXX += 1
        cprint(gui_menu)

        menu_buff["FIX-SUB"] -= menu_buff["FIX"]
        if menu_buff["FIX-SUB"]:
            gui_menu.config("FIXTURES","bg","yellow")
            gui_menu.config("FIXTURES","activebackground","yellow")
        elif menu_buff["FIX"]:
            gui_menu.config("FIXTURES","bg","orange")
            gui_menu.config("FIXTURES","activebackground","orange")
        else:
            gui_menu.config("FIXTURES","bg","")
            gui_menu.config("FIXTURES","activebackground","")

        gui_menu.update("FIXTURES","{} : {}".format(menu_buff["FIX"],menu_buff["FIX-SUB"]))

        menu_buff["DIM-SUB"] -= menu_buff["DIM"]
        if menu_buff["DIM-SUB"]:
            gui_menu.config("DIMMER","bg","yellow")
            gui_menu.config("DIMMER","activebackground","yellow")
        elif menu_buff["DIM"]:
            gui_menu.config("DIMMER","bg","orange")
            gui_menu.config("DIMMER","activebackground","orange")
        else:
            gui_menu.config("DIMMER","bg","")
            gui_menu.config("DIMMER","activebackground","")


        gui_menu.update("DIMMER","{} : {}".format(menu_buff["DIM"],menu_buff["DIM-SUB"]))

        cprint("fix:",_XXX,round(time.time()-s),color="red"); _XXX += 1

    def preset_rec(self,nr):
        cprint("------- STORE PRESET")
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
        cprint("SELECT PRESET")
        sdata = PRESETS.val_presets[nr]
        cmd = ""
        for fix in sdata:
            if fix == "CFG":
                continue
            for attr in sdata[fix]:
                #v2 = sdata[fix][attr]["VALUE"]
                #v2_fx = sdata[fix][attr]["FX"]
                #print( self.data.elem_attr)
                #if fix in self.elem_attr:
                #    if attr in self.elem_attr[fix]:
                #        elem = self.elem_attr[fix][attr]
                FIXTURES.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                FIXTURES.fixtures[fix]["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
                #elem["bg"] = "yellow"

    def preset_go(self,nr,val=None,xfade=None,event=None,button="",ptfade=None):
        t_start = time.time()
        if xfade is None and FADE._is():
            xfade = FADE.val()
        
        if ptfade is None and FADE_move._is():
            ptfade = FADE_move.val()

        cprint("GO PRESET FADE",nr,val)

        rdata = PRESETS.get_raw_map(nr)
        if not rdata:
            return 0
        cprint("???????")
        cfg   = PRESETS.get_cfg(nr)
        cprint("''''''''")
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
        
        #print("IIIIIIIIIIIiiiiiiiiiiiiiiiiiii",nr,val)
        #print(len(self.elem_presets) )
        if len(self.elem_presets) > nr: # RED BUTTON IF PRESSED
            #print("IIIIIIIIIIIiiiiiiiiiiiiiiiiiii",nr,val)
            if val:# or value:
                #self.elem_presets[nr].config(borderwidth=1)
                self.elem_presets[nr].config(bg="red")
            else:
                self._refresh_exec()
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

            if type(nr) is not type(None):
                vcmd[i]["EXEC"] = str(int(nr)+1)

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
        try:master.commands.elem["S-KEY"]["bg"] = "red"
        except Exception as e:cprint("exc",self,e)
        cmd="xset -display :0.0 r rate 240 15"
        print(cmd)
        os.system(cmd)

    def _unlock(self):
        global _global_short_key
        _global_short_key = 1
        try:master.commands.elem["S-KEY"]["bg"] = "green"
        except Exception as e:cprint("exc",self,e)
        cmd = "xset -display :0.0 r off"
        print(cmd)
        os.system(cmd)


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

        cprint(self,event,args)
        #print("###-",self.e_txt,dir(self.e_txt))
        if "S-KEY" not in master.commands.elem:
            #cprint("<GLOBAL-GUI-EVENT-DISABLED>",event,color="red")
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
            cprint("filter: get()",_global_short_key,t)
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



class LOAD_SHOW_AND_RESTAT():
    def __init__(self,fname=""):
        self.fname=fname
        self.base = Base()

    def cb(self,event=None,force=0):
        cprint("LOAD_SHOW_AND_RESTART.cb force={} name={}".format(force,self.fname) )
        if not self.fname and not force:
            return 0
        if self.base.show_name == self.fname and not force:
            cprint("filename is the same",self.fname)
            return 0
        if not force:
            self.base._set(self.fname)

        cprint("LOAD SHOW:",event,self.fname)

        BASE_PATH = "/opt/LibreLight/Xdesk/"
        cmd="_LibreLightDesk.py"
        arg = ""
        print("fork",[BASE_PATH,cmd,arg])
        if "--easy" in sys.argv:
            arg = "--easy"
        
        movewin.process_kill(BASE_PATH+"tksdl/")
        os.execl("/usr/bin/python3", BASE_PATH, cmd,arg)
        sys.exit()
                
class PopupList():
    def __init__(self,name="<NAME>",master=0,width=400,height=450,exit=1,left=_POS_LEFT+400,top=_POS_TOP+100,cb=None,bg="black"):
        self.name = name
        self.frame = None
        self.bg=bg
        self.cb = cb
        if cb is None: 
            cb = DummyCallback #("load_show_list.cb")
        #w = Window(self.name,master=master,width=width,height=height,exit=exit,left=left,top=top,cb=cb)
        args = {"title":self.name,"master":master,"width":width,"height":height,"exit":exit,"left":left,"top":top,"cb":cb}
        w = Window(args)
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
        b["state"] = "readonly"
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
        cprint("DummyCallback.cb",[self.name,event])

class BaseCallback():
    def __init__(self,cb=None,args={}):
        self._cb=cb
        self.args = args

    def cb(self,**args):
        print("BaseCallback.cb()")
        print("  ",self.args)
        print("  ",self._cb)
        if self._cb:
            if self.args:
                self._cb(args=self.args) 
            else:
                self._cb() 

def frame_of_show_list(frame,cb=None):
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

def _parse_fixture_name(name):
    out = []
    #{"FIX","MAN","CH","PATH":""}
    if name.count(".") == 2:
        m,n,e = name.split(".")
        #out = [n,m,"0",name]
        out = {"name":n,"manufactor":m,"fname":name}
    elif name.count("_") == 2:
        name,e = name.split(".")
        m,n,c = name.split("_")
        out = {"name":n,"ch":c,"manufactor":m,"name":name}
        #out = [n,m,c,name]
    else:
        out = {"name":name}
    return out

def online_help(page):
    print("INIT:online_help",page)

    try:
        page = page.replace("&","")
        page = page.replace("=","")
        page = page.replace("/","")
        import webbrowser
        def _cb():
            print("online_help",page)
            webbrowser.open("http://librelight.de/wiki/doku.php?id="+page )
        return _cb
    except Exception as e:
        print("online_help Exception",e)
        raise e

    def _cb():
        print("error online_help",page)
    return _cb 



def index_fixtures():
    p="/opt/LibreLight/Xdesk/fixtures/"
    ls = os.listdir(p )
    ls.sort()
    blist = []
    
    for l in ls:
        b = _parse_fixture_name(l)
        b.append(p)
        b.insert(0,"base")
        blist.append(b)
    return blist



#def _fixture_create_import_list(path=None):
def _fixture_load_import_list(path=None):
    if not path:
        path = "/home/user/LibreLight/show"

    blist = []
    lsd = os.listdir(path)
    lsd.sort()
    fname_buffer = []
    for sname in lsd:
        #print("   ",sname)
        ok = 0
        try:
            fname = path+"/"+sname+"/patch.sav"
            if os.path.isfile(fname):
                ok = 1
            else:
                fname = path+"/"+sname
                if os.path.isfile(fname):
                    ok = 1
            #fname_buffer = []
            if not ok:
                continue

            f = open(fname)
            lines = f.readlines()
            f.close()

            for line in lines:
                ok2 = 0
                _key = ""
                line = line.split("\t")
                if len(line) < 2:
                    continue
                jdata = json.loads(line[2])

                fixture = jdata
                _len = str(fixture_get_ch_count(fixture))
                if "ATTRIBUT" in jdata:
                    #_len = len(jdata["ATTRIBUT"])
                    #if "_ACTIVE" in jdata["ATTRIBUT"]:
                    #    _len -= 1
                    _key = list(jdata["ATTRIBUT"].keys()) 
                    _key.sort()
                    _key = str(_key)
                    if _key not in fname_buffer:
                        fname_buffer.append(_key) # group same fixtures by ATTR
                        ok2 = 1
                if ok2:
                    name = jdata["NAME"]
                    #row = [name,fname+":"+name,path])
                    xfname = fname.replace(path,"")
                    row = {"xfname":xfname ,"name":name,"ch":_len, "xpath":path,"d":_key} #,"b":jdata}
                    blist.append(row)
        except Exception as e:
            print("exception",e)
            raise e
    return blist


def fixture_get_ch_count(fixture):
    _len = [0,0]
    if "ATTRIBUT" not in fixture:
        return [-1,-1]

    for at in fixture["ATTRIBUT"]:
        #print(at,_len)
        #print(" ",fixture["ATTRIBUT"][at])
        if not at.startswith("_") and not at.startswith("EMPTY"):
            _len[1] += 1

        if "NR" in fixture["ATTRIBUT"][at]:
            NR = fixture["ATTRIBUT"][at]["NR"]
            if NR > _len[0]:
                _len[0] = NR
        #print("-",at,_len)

    return _len

def fixture_get_attr_data(fixture,attr):
    if "ATTRIBUT" in fixture:
        if attr in fixture["ATTRIBUT"]:
            return fixture["ATTRIBUT"][attr]

    if "NAME" in fixture:
        print("  NO fixture_get_attr_data A",fixture["NAME"],attr)
    else:
        print("  NO fixture_get_attr_data B",fixture,attr)

def fixture_order_attr_by_nr(fixture):
    out1 = []
    max_nr = 0
    if "ATTRIBUT" not in fixture:
        return []

    nrs = {}
    for at in fixture["ATTRIBUT"]:
        #print("+   ",at)
        atd = fixture_get_attr_data(fixture,at)
        #print("+   ",atd)
        if not atd:
            continue

        k = atd["NR"]
        v = at
        nrs[k] = v
        if k > max_nr:
            max_nr = k

    for i in range(1,max_nr+1):
        if i not in nrs:
            v = "EMPTY" #-{}".format(i)
            nrs[i] = v
            #print("-: ",v)


    nrs_key = list(nrs.keys())
    nrs_key.sort()
    #print(nrs_key)

    for k in nrs_key:
        v = nrs[k]
        #print("-: ",k,v)
        out1.append(v)

    #print()
    return out1 

def _load_fixture_list(mode="None"):
    blist = []

    if mode == "USER":
        path = HOME+"/LibreLight/fixtures/"

    elif mode == "GLOBAL":
        path="/opt/LibreLight/Xdesk/fixtures/"

    elif mode == "IMPORT":
        path=None 

    _r =  _fixture_load_import_list(path=path)
    blist.extend( _r )
    return blist




def FIXTURE_CHECK_SDATA(ID,sdata):
    print("FIXTURE_CHECK_SDATA",ID)
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

    sdata["ATTRIBUT"]["_ACTIVE"] = OrderedDict()
    sdata["ATTRIBUT"]["_ACTIVE"]["NR"] = 0
    sdata["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
    sdata["ATTRIBUT"]["_ACTIVE"]["VALUE"] = 0
    sdata["ATTRIBUT"]["_ACTIVE"]["FX2"] = {}
    sdata["ATTRIBUT"]["_ACTIVE"]["FX"] = ""

    if "DIM" not in sdata["ATTRIBUT"]:
        _tmp = None
        #print(sdata)
        vdim_count = 0
        for a in ["RED","GREEN","BLUE"]:#,"WHITE","AMBER"]:
            if a in sdata["ATTRIBUT"]:
                vdim_count +=1

        if vdim_count == 3:
            _tmp =  {"NR": 0, "MASTER": "0", "MODE": "F", "VALUE": 255, "ACTIVE": 0, "FX": "", "FX2": {}}
            _tmp = OrderedDict(_tmp)
            sdata["ATTRIBUT"]["DIM"] =_tmp 
        print("ADD ---- VDIM",vdim_count,_tmp)
        #input("STOP")

    for attr in sdata["ATTRIBUT"]:
        row = sdata["ATTRIBUT"][attr]
        row["ACTIVE"] = 0

        if "FX" not in row:
            row["FX"] =""
        if "FX2" not in row:
            row["FX2"] = {}
        if "MASTER" not in row:
            row["MASTER"] = 0


    if "ID" not in sdata:
        sdata["ID"] = str(ID)
    return sdata


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
            #sdata = self._repair_sdata(sdata)
            sdata = FIXTURE_CHECK_SDATA(i,sdata)

            self.fixtures[str(i)] = sdata
        #PRESETS.label_presets = l
        self._re_sort()
        self.fx_off("all")

    def _re_sort(self):
        keys = list(self.fixtures.keys())
        keys2=[]
        for k in keys:
            #k = "{:0>5}".format(k)
            k = int(k)
            keys2.append(k)
        keys2.sort()
        fixtures2 = OrderedDict()
        for k in keys2:
            k = str(k)
            fixtures2[k] = self.fixtures[k]


        self.fixtures = fixtures2

    def backup_patch(self,save_as="",new=0):
        filename = "patch"
        #self.fx_off("all")
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        if new:
            data = []
            labels = {}
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
        #cprint("get_dmx",[fix,attr], fix in self.fixtures)
        DMX = -99
        if attr.startswith("_"):
            return -88

        if fix in self.fixtures:
            data = self.fixtures[fix]
            if "DMX" in data:
                DMX = int(data["DMX"])
            
            if DMX <= 0:
                return DMX # VIRTUAL FIX

            if "UNIVERS" in data:
                DMX += int(data["UNIVERS"])*512

            adata = self.get_attr(fix,attr)

            if adata:
                if "NR" in adata:
                    NR = adata["NR"] 
                    if NR <= 0:
                        return -12 # not a VIRTUAL ATTR
                    else:
                        DMX+=NR-1
                    return DMX
        return -199

    def update_raw(self,rdata,update=1):
        #cprint("update_raw",len(rdata))
        cmd = []
        for i,d in enumerate(rdata):
            xcmd = {"DMX":""}
            fix   = d["FIX"]
            attr  = d["ATTR"]
            v2    = d["VALUE"]
            v2_fx = d["FX"]

            if fix not in self.fixtures:
                continue 

            sdata = self.fixtures[fix] #shortcat

            ATTR  = sdata["ATTRIBUT"] 
            if attr not in ATTR:
                continue

            #print(sdata)
            #print("FIX",fix,attr)
            sDMX = FIXTURES.get_dmx(fix,attr)
            #print(sDMX)
            xcmd["DMX"] = str(sDMX)

            cmd.append(xcmd)

            v=ATTR[attr]["VALUE"]
            if v2 is not None and update:
                ATTR[attr]["VALUE"] = v2
            
            if d["FX2"] and update:
                ATTR[attr]["FX2"] = d["FX2"] 

            text = str(attr)+' '+str(round(v,2))
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

        if attr == "INV-ATTR":
            cprint("-x-x-x-x-x-x-x-X-")
            x=self.select(fix,attr,mode="swap")
            #x=self.select(fix,"ALL",mode="swap")
            master.refresh_fix()
            return x
        if attr == "INV-FIX":
            cprint("-x-x-x-x-x-x-x-x-")
            x=self.select(fix,attr,mode="swap")
            #x=self.select(fix,"ALL",mode="swap")
            return x
        out = []
        if fix not in self.fixtures: 
            cprint(" activate Fixture in fixture list on encoder click ")

            ii =0
            delay=0
            sstart = time.time()
            cprint("-->A HIER <--")
            sub_data = []
            for _fix in self.fixtures:
                ii+=1
                data = self.fixtures[_fix]
                if "-FINE" in attr.upper():
                    continue

                elif (attr in data["ATTRIBUT"] ) and "-FINE" not in attr.upper()   :
                    if xval == "click":
                        self.select(_fix,attr,mode="on")
                    elif data["ATTRIBUT"][attr]["ACTIVE"]:
                        if _fix:
                            sub_data.append([_fix,attr,xval,xfade,delay])
                if DELAY._is():
                    delay += DELAY.val()/100

            sub_jdata = []
            for dd in sub_data:
                #print("---",len(sub_data),end="")
                #self.encoder(fix,attr,xval,xfade,delay)
                _x123 = self.encoder(dd[0],dd[1],dd[2],dd[3],dd[4],blind=1)
                sub_jdata.append(_x123)

            if sub_jdata:
                cprint("--- SEND MASTER ENCODER:",len(sub_data),sub_data[0],"... _blind:",_blind)#,end="")
                jclient_send(sub_jdata) 

            jdata=[{"MODE":ii}]
            cprint("-->B HIER <--")
            jclient_send(jdata)
            return 0

        data = self.fixtures[fix]

        if xval == "click":
            #cprint(data)
            return self.select(fix,attr,mode="toggle")

    
        v2=data["ATTRIBUT"][attr]["VALUE"]
        change=0
        increment = 5 #4.11
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
            increment = 0.25 #.5
            v2+= increment
            jdata["INC"] = increment
            change=1
        elif xval == "-":
            increment = 0.25 #.5
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

        jdata["VALUE"]    = round(v2,4)
        jdata["FIX"]      = fix
        jdata["FADE"]     = 0
        jdata["DELAY"]    = 0
        jdata["ATTR"]     = attr
        dmx               = FIXTURES.get_dmx(fix,attr)
        jdata["DMX"]      = dmx

        dmx_fine = FIXTURES.get_dmx(fix,attr+"-FINE")
        if dmx_fine != jdata["DMX"] and dmx > 0:
            jdata["DMX-FINE"] = dmx_fine

        out = {} 
        if change:
            data["ATTRIBUT"][attr]["ACTIVE"] = 1
            data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
            data["ATTRIBUT"][attr]["VALUE"] = round(v2,4)

            if xfade:
                jdata["FADE"] = xfade

            if xdelay:
                #if attr not in ["PAN","TILT"] and 1:
                jdata["DELAY"] = xdelay

            if not _blind:
                jdata = [jdata]
                jclient_send(jdata)
                time.sleep(0.001)

        return jdata

    def get_active(self):
        cprint("get_active",self)
        CFG = OrderedDict()

        sdata = OrderedDict()
        sdata["CFG"] = CFG # OrderedDict()
        sdata["CFG"]["FADE"] = FADE.val()
        sdata["CFG"]["DEALY"] = 0

        for fix in self.fixtures:                            
            data = self.fixtures[fix]

            for attr in data["ATTRIBUT"]:
                if not data["ATTRIBUT"][attr]["ACTIVE"]:
                    continue

                if fix not in sdata:
                    sdata[fix] = {}

                if attr not in sdata[fix]:
                    sdata[fix][attr] = OrderedDict()

                    if not modes.val("REC-FX"):
                        sdata[fix][attr]["VALUE"] = data["ATTRIBUT"][attr]["VALUE"]
                    else:
                        sdata[fix][attr]["VALUE"] = None 

                    if "FX" not in data["ATTRIBUT"][attr]: 
                         data["ATTRIBUT"][attr]["FX"] = ""

                    if "FX2" not in data["ATTRIBUT"][attr]: 
                         data["ATTRIBUT"][attr]["FX2"] = {}
                    
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

    def _select_all(self,fix=None,mode="toggle",mute=0):
        if not mute:
            cprint("FIXTURES._select_all()",fix,"ALL",mode,color="yellow")
        c=0
        if fix in self.fixtures:
            data = self.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                #print("SELECT ALL",fix,attr)
                if "-FINE" in attr.upper():
                    continue
                
                if mode == "toggle":
                    c+=self.select(fix,attr,mode="on",mute=mute)
                elif mode == "swap":
                    if not attr.startswith("_"):
                        c+=self.select(fix,attr,mode="toggle",mute=mute)

            if not c and mode == "toggle": # unselect all
                c= self._deselect_all(fix=fix)
        return c 

    def select(self,fix=None,attr=None,mode="on",mute=0):
        if not mute:
            cprint("FIXTURES.select() >>",fix,attr,mode,color="yellow")
        out = 0
    
        if fix == "SEL":
            if attr.upper() == "INV-ATTR":
                fixs = self.get_active()
                cprint("selected:",len(fixs))
                for fix in fixs:
                    x=self._select_all(fix=fix,mode=mode,mute=1)
                return None 

        if fix in self.fixtures:
            if attr.upper() == "ALL":
                x=self._select_all(fix=fix,mode=mode)
                return x

            data = self.fixtures[fix]
            if attr in data["ATTRIBUT"]:
                if mode == "on":
                    if not data["ATTRIBUT"][attr]["ACTIVE"]:
                        data["ATTRIBUT"][attr]["ACTIVE"] = 1
                        data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
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
                        data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
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



def PRESET_CFG_CHECKER(sdata):
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
            ok = PRESET_CFG_CHECKER(sdata)

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

        ok = PRESET_CFG_CHECKER(sdata)

        if ok:
            cprint("REPAIR CFG's",ok,sdata["CFG"],color="red")
        return ok
        
    def backup_presets(self,save_as="",new=0):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        if new:
            #a = []
            #for i in range(512):
            #    e = PRESET_CFG_CHECKER({})
            #    e["NAME"] = str(i)
            #    a.append(e)
            #data = a 
            data = []#*512
            labls = [""]*512
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
                    cprint("-fx",x,len(x))
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

        cprint("get_raw_map",nr)
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
        #txt=str(nr+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+_label
        #txt=str(nr+1)+" "+str(BTN)+" "+str(len(sdata)-1)+"\n"+_label
        txt="{} {} {}\n{}".format(nr+1,BTN,len(sdata)-1,_label)
        cprint("get_btn_txt",nr,[txt])
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

        master._refresh_exec(nr=nr)
        cprint("EEE", self.val_presets[nr]["CFG"]["BUTTON"] )
        return self.val_presets[nr]["CFG"]["BUTTON"] 

    def label(self,nr,txt=None):
        if nr not in self.label_presets:
            return ""
        if type(txt) is str:
            self.label_presets[nr] = txt
            cprint("set label",nr,[txt])
        cprint("??? ?? set label",nr,[txt])
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
            if ok and last >= 0:
                if modes.val("MOVE"):
                    modes.val("MOVE",3)
                cprint("PRESETS.move OK",color="red")
                #self.delete(last)
                return ok,nr,last #ok
            
        return 0,nr,last # on error reset move
    def delete(self,nr):
        cprint("PRESETS.delete",nr)
        ok=0
        if nr in self.val_presets:
            self.val_presets[nr] = OrderedDict()
            self.label_presets[nr] = "-"
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
        cprint("init FixtureEditor",dmx)
    def event(self,a1="",a2=""):
        cprint([self.dmx,a1,a2])
        j=[]
        jdata = {'VALUE': int(a1), 'args': [] , 'FADE': 0,'DMX': str(self.dmx)}
        j.append(jdata)

        jclient_send(j)

class MasterWing():
    def __init__(self,dmx=1):
        pass
        self.elem=[]
        self.dmx=dmx
        cprint("init MasterWing",dmx)
    def event(self,a1="",a2=""):
        cprint([self.dmx,a1,a2])
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
        cprint("change_dmx",[event,self])


            



lf_nr = 0


        
from tkinter import PhotoImage 

_shift_key = 0

class on_focus():
    def __init__(self,name,mode):
        self.name = name
        self.mode = mode
    def cb(self,event=None):
        print("on_focus",event,self.name,self.mode)
        try:
            e = master.commands.elem["."]
        except:pass

        if self.mode == "Out":
            cmd="xset -display :0.0 r rate 240 20"
            print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#aaa"
                e["activebackground"] = "#aaa"
            except:pass
        if self.mode == "In":
            cmd = "xset -display :0.0 r off"
            print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#fff"
                e["activebackground"] = "#fff"
            except:pass

class Window():
    def __init__(self,args): #title="title",master=0,width=100,height=100,left=None,top=None,exit=0,cb=None,resize=1):
        global lf_nr
        self.args = {"title":"title","master":0,"width":100,"height":100,"left":None,"top":None,"exit":0,"cb":None,"resize":1}
        self.args.update(args)
        
        cprint("Window.init()",id(self.args),color="yellow")
        cprint("  ",self.args,color="yellow")

        ico_path="./icon/"
        self.cb = cb

        if self.args["master"]: 
            self.tk = tkinter.Tk()
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.withdraw() # do not draw
            self.tk.resizable(self.args["resize"],self.args["resize"])
            defaultFont = tkinter.font.nametofont("TkDefaultFont")
            cprint(defaultFont)
            defaultFont.configure(family="FreeSans",
                                   size=10,
                                   weight="bold")
            # MAIN MENUE
            try:
                self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"main.png"))
            except Exception as e:
                cprint("Exception GUIWindow.__init__",e)
        else:
            # addtional WINDOW
            self.tk = tkinter.Toplevel()
            self.tk.iconify()
            #self.tk.withdraw() # do not draw
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.resizable(self.args["resize"],self.args["resize"])
            
            try:
                if "COLORPICKER" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"picker.png"))
                elif "ENCODER" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"enc.png"))
                elif "EXEC" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"exec.png"))
                elif "FX" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"fx.png"))
                else:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"scribble.png"))
            except Exception as e:
                cprint("Exception on load window icon",self.args["title"])
                cprint("Exception:",e)
            #time.sleep(3)
            self.tk.deiconify()



        self.tk["bg"] = "black"
        self.tk.bind("<Button>",self.callback)
        self.tk.bind("<Key>",self.callback)
        self.tk.bind("<KeyRelease>",self.callback)
        self.tk.bind("<FocusIn>", on_focus(self.args["title"],"In").cb)
        self.tk.bind("<FocusOut>", on_focus(self.args["title"],"Out").cb)

        self.tk.title(""+str(self.args["title"])+" "+str(lf_nr)+":"+str(rnd_id))
        lf_nr+=1
        #self.tk.geometry("270x600+0+65")
        geo ="{}x{}".format(self.args["width"],self.args["height"])
        if self.args["left"] is not None:
            geo += "+{}".format(self.args["left"])
            if self.args["top"] is not None:
                geo += "+{}".format(self.args["top"])

        #self._event_clear = Xevent(fix=0,elem=None,attr="CLEAR",data=self,mode="ROOT").cb
        self.tk.geometry(geo)
        self.show()
    def update_idle_task(self):
        if INIT_OK:
            tkinter.Tk.update_idletasks(gui_menu_gui.tk)
        pass
    def close_app_win(self,event=None):
        cprint("close_app_win",self,event,self.args["title"],color="red")
        if exit:
            if self.title == "MAIN":
               save_window_position()
            save_window_position()
            
            self.tk.destroy()
        try:
            self.cb("<exit>").cb()
        except Exception as e:
            cprint("EXCETPION: close_app_win",e,self,color="red")

    def title(self,title=None):
        if title is None:
            return self.tk.title()
        else:
            #return self.tk.title(title)
            self.args["title"] = title
            return self.tk.title(""+str(self.args["title"])+" "+str(lf_nr)+":"+str(rnd_id))
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
        sstart = time.time()
        #time.sleep(0.1)
        if not _global_short_key:
            return 1

        global _shift_key
        #cprint("<GUI>",event,color="yellow")
        value = 255
        if "Release" in str(event.type) or str(event.type) == '5' or str(event.type) == '3':
            value = 0
        cprint("<GUI>",event.state,data,value,[event.type,event.keysym],color="yellow")
        #print(event)
        if "state" in dir(event) and "keysym" in dir(event):
            #print([event.state,event.keysym,event.type])
            if event.state == 4  and str(2) == str(event.type): # strg + s
                if str(event.keysym) == "s":
                    cprint("tTtT ReW "*20)
                    #print("numbersign !!")
                    PRESETS.backup_presets()
                    FIXTURES.backup_patch()
                    save_window_position()

                    e =  master.setup_elem["SAVE\nSHOW"]
                    #print(e)
                    b = BLINKI(e)
                    b.blink()
                if str(event.keysym) == "c":
                    PRESETS.backup_presets()
                    FIXTURES.backup_patch()

                    save_window_position()
                    #self.elem.config(activebackground="lightgrey")
                    LOAD_SHOW_AND_RESTAT("").cb(force=1)
                #cprint("oipo "*10,round(int(time.time()-sstart)*1000,2))
                return

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
                try:
                    if _shift_key:
                        _ENCODER_WINDOW.title("SHIFT/FINE ")
                    else:
                        _ENCODER_WINDOW.title("ENCODER") 
                except Exception as e:
                    cprint("exc9800",e)

            elif event.keysym in "ebfclrmsRx" and value: 
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
                elif "R" == event.keysym:
                    modes.val("REC-FX",1)
                elif "x" == event.keysym:
                    modes.val("REC-FX",1)
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
            elif "numbersign" == event.keysym and value: # is char "#"
                cprint("numbersign !!")
                PRESETS.backup_presets()
                FIXTURES.backup_patch()

                save_window_position()

                for e in master.setup_cmd:
                    cprint(e)
                e =  master.setup_elem["SAVE\nSHOW"]
                cprint(e)
                b = BLINKI(e)
                b.blink()
                #e = Xevent(fix=0,elem=None,attr="SAVE\nSHOW",mode="SETUP")
                #e.cb(event=event)
            elif "End" == event.keysym:
                FIXTURES.fx_off("all")
                CONSOLE.fx_off("all")
                CONSOLE.flash_off("all")
            elif "Delete" == event.keysym:
                #PRESETS.delete(nr)
                if value:
                    modes.val("DEL",1)

        cprint("oipo "*10,round(int(time.time()-sstart)*1000,2))
 
class WindowManager():
    def __init__(self):
        self.windows = {}
        self.obj = {}
        self.nr= 0
        self.first=""
        self.window_init_buffer = {}

    def update(self,w,name="",obj=None):
        name = str(name)

        for k in self.windows:
            if k == name:
                self.windows[str(name)] = w
                self.obj[str(name)] = obj

    def new(self,w,name="",obj=None,wcb=None):
        name = str(name)

        if wcb and name:
            self.window_init_buffer[name] = wcb

        if not self.first:
            if name:
                self.first = name
            else:
                self.first = str(self.nr)

            if w:
                w.tk.state(newstate='normal')
                w.tk.attributes('-topmost',True)

        if name:
            self.windows[str(name)] = w
            self.obj[str(name)] = obj
        else:
            self.windows[str(self.nr)] = w
            self.obj[str(self.nr)] = obj
            self.nr+=1

    def mainloop(self):
        self.windows[self.first].mainloop()

    def get_win(self,name):
        cprint(self,".get_win(name) =",name)
        name = str(name)
        if name in self.windows:
            out = self.windows[name]
            cprint(out)
            return out

    def get(self,name):
        return get_win(name)

    def get_obj(self,name):
        name = str(name)
        if name in self.windows:
            out = self.obj[name]
            return out

    def create(self,name):
        cprint( "create Window",name)

        if name in self.window_init_buffer:
            c = self.window_init_buffer[name] 
            print(c)
            print(dir(c))
            w,obj,cb_ok = c.create()
            window_manager.update(w,name,obj)

            if cb_ok:
                cb_ok()

            resize = 1
            if "resize" in c.args:
                if not c.args["resize"]:
                    resize = 0
            #if resize:
            get_window_position(_filter=name,win=w) 

            if name in ["ENCODER"]:
                global _ENCODER_WINDOW 
                _ENCODER_WINDOW = w
            if name in ["DIMMER","FIXTURES"]:
                refresher_fix.reset() # = Refresher()

    def _check(self,name):
        try:
            self.windows[name].tk.state(newstate='normal')
            return 1
        except Exception as e:
            cprint("exception",e,color="red")
            cprint("info",name,self.windows[name],color="red")

    def top(self,name):
        name = str(name)
        if name not in self.windows:
            cprint(name,"not in self.windows",self.windows.keys())
            return 

        if not self._check(name):
            self.create(name)
        
        w = self.windows[name]
        #def get_lineno():
        print(" 2.1- ln",movewin.get_lineno(),w,str(type(w)))
        #if type(w) is type(window_create_buffer):
        if not str(type(w)).startswith("<class 'function'>"): 
            w.tk.attributes('-topmost',True)
            w.tk.attributes('-topmost',False)
            w.tk.update_idletasks()
        else:
            print(" 2.2-",w)
            w()


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
    #master._refresh_fix()
    #master._refresh_exec()
LOAD_SHOW()

master = MASTER()


class Refresher():
    def __init__(self):
        self.time = time.time()
        self.time_max = time.time()
        self.time_delta = 15
        self.update = 1
        self.name = "name" # exec
        self.cb = None #self.dummy_cb
    def dummy_cb(self):
        cprint(self,"dummy_cd()",time.time()-self.time)

    def reset(self):
        self.time = time.time() 
        self.update = 1

    def refresh(self):
        if self.update: 
            if self.time+self.time_delta < time.time():
                self._refresh()
        else:
            self.time = time.time() 

    def _refresh(self):
        cprint("_refresh()",self.name,self)
        if not INIT_OK:
            return

        self.time_max = time.time()
        self.time     = time.time()
        self.update = 0
        try:
            if self.cb:
                self.cb()
            else:
                self.dummy_cb()
        except Exception as e:
            cprint("_refresh except:",e,"cb:",self.cb)
            traceback.print_exc()
            cprint()
        cprint("t=",self.time_max- time.time())

    def loop(self,args={}):
        while 1:
            try:
                if INIT_OK:
                    self.refresh()
                    #tkinter.Tk.update_idletasks(gui_menu_gui.tk)
            except Exception as e:
                cprint("loop exc",e)
                traceback.print_exc()
                cprint("== cb EXCEPT",e,color="red")
                cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
                cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")

            time.sleep(0.2)

print("main",__name__)


__run_main = 0
if __name__ == "__main__":
    __run_main = 1
else:
    import __main__ 
    if "unittest" not in dir(__main__):
        __run_main = 1



refresher_fix = Refresher()
refresher_fix.time_delta = 0.50 
refresher_fix.name = "fix"
refresher_fix.reset() 
refresher_fix.cb = master._refresh_fix

refresher_exec = Refresher()
refresher_exec.time_delta = 10 #0
refresher_exec.name = "exec"
refresher_exec.reset() 
refresher_exec.cb = master._refresh_exec

refresher_exec = Refresher()
refresher_exec.time_delta = 10 #0
refresher_exec.name = "exec-fader"
refresher_exec.reset() 
refresher_exec.cb = refresh_exec_fader_cfg

def loops(**args):
    time.sleep(5) # wait until draw all window's 
    cprint("-> run loops")
    thread.start_new_thread(refresher_fix.loop,())
    thread.start_new_thread(refresher_exec.loop,())

class window_create_sdl_buffer():
    def __init__(self,args,cls,data,cb_ok=None,scroll=0,gui=None):
        self.args   = args.copy()
        self.cls    = cls
        self.cb_ok  = cb_ok
        self.data   = data
        self.scroll = scroll
        self.gui    = gui

    def create(self,hidde=0):
        cprint()
        return [self.cls,self.cls,None] #w,obj,cb_ok

class window_create_buffer():
    def __init__(self,args,cls,data,cb_ok=None,scroll=0,gui=None):
        self.args   = args.copy()
        self.cls    = cls
        self.cb_ok  = cb_ok
        self.data   = data
        self.scroll = scroll
        self.gui    = gui

    def create(self,hidde=0):
        cprint()
        cprint()
        cprint("window_create_buffer.create()",id(self),self.args["title"],color="green")

        obj = None
        w = Window(self.args)
        out = []
        f = None
        h = None

        if self.scroll:
            head = None
            foot = None
            if "head" in self.args:
                head = self.args["head"]
            if "foot" in self.args:
                foot = self.args["foot"]
            w1 = ScrollFrame(w.tk,width=self.args["width"],height=self.args["height"],foot=foot,head=head)
            if type(w1) is list:
                try:
                    h = w1[0]
                    f = w1[2]
                except:pass

                w1 = w1[1]
        else:
            w1 = tk.Frame(w.tk,width=self.args["width"],height=self.args["height"])
            w1.pack()
        try:
            obj=self.cls(self.gui,w1,self.data,foot=f,head=h) 
        except:
            obj=self.cls(self.gui,w1,self.data) 
        return w,obj,self.cb_ok


if __run_main:
    cprint("main")
    #thread.start_new_thread(refresher_fix.loop,())
    #thread.start_new_thread(refresher_exec.loop,())
    

    TOP = _POS_TOP + 15
    L0 = _POS_LEFT 
    L1 = _POS_LEFT + 95
    L2 = _POS_LEFT + 920 
    W1 = 810
    H1 = 550
    HTB = 23 # hight of the titlebar from window manager

    pos_list = read_window_position()
    

    data = []
    #data.append({"text":"COMMAND"})
    #data.append({"text":"CONFIG"})
    data.append({"text":"PATCH"})
    data.append({"text":"DIMMER"})
    data.append({"text":"FIXTURES"})
    data.append({"text":"FIX-LIST"})
    data.append({"text":"EXEC","name":"EXEC-BTN"})
    data.append({"text":"EXEC-WING"})
    data.append({"text":"---"})
    data.append({"text":"SETUP"})
    data.append({"text":"COMMAND"})
    data.append({"text":"LIVE"})
    data.append({"text":"FX"})
    data.append({"text":"ENCODER"})
    data.append({"text":"COLORPICKER","name":"COLOR"})
    data.append({"text":"---"})
    data.append({"text":"FIXTURE-EDITOR","name":"FIX-EDIT"})
    data.append({"text":"CONFIG"})
    data.append({"text":"SDL-CONFIG"})
    data.append({"text":"CLOCK"})
    data.append({"text":"SDL-DMX"})
    #data.append({"text":"SDL-FIX"})

    name="MAIN"
    args = {"title":"MAIN","master":1,"width":80,"height":H1,"left":L0,"top":TOP,"resize":1}

    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_menu 
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    window_manager.top(name)

    gui_menu_gui = window_manager.get_win(name)
    gui_menu = window_manager.get_obj(name)
    master._refresh_fix()


    # --------------------------------
    name="EXEC"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data  = PRESETS
    cls   = draw_exec #GUI_ExecWingLayout
    cb_ok = None #set_exec_fader_all
    

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    #print(dir(cls))
    #print(cls)
    #sys.exit()
    name="SDL-CONFIG"
    def sdl_config():
        cmd="nohup /usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/config.py &"
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/config.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name="SDL-DMX"
    def sdl_config():
        cmd="nohup /usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/config.py &"
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/dmx.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="FIX-LIST"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/fix.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="CONFIG"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = GUI_CONF
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="DIMMER"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_DIM
    data = FIXTURES
    ok_cb=None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="FIXTURES"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_FIX
    ok_cb=None
    data = FIXTURES

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # -------------------------------
    name="FIXTURE-EDITOR"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data=[]
    for i in range(12*6):
        data.append({"text"+str(i):"test"})
    
    cls = GUI_FixtureEditor
    #cls = GUI_FaderLayout
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    #window_manager.top(name)

    
    # -------------------------------
    name="MASTER-WING"
    args = {"title":name,"master":0,"width":75,"height":405,"left":L0,"top":TOP+H1-220,"resize":0}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data=[]
    for i in range(2):
        data.append({"MASTER"+str(i):"MASTER"})

    cls = GUI_MasterWingLayout #(w1,data)
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # -------------------------------
    name="EXEC-WING"
    args = {"title":name,"master":0,"width":600,"height":415,"left":L1,"top":TOP+H1+HTB*2,"H1":H1,"W1":W1}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    data=[]
    for i in range(10*3):
        data.append({"EXEC"+str(i):"EXEC"})

    cls   = GUI_ExecWingLayout
    cb_ok = set_exec_fader_all

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="ENCODER"
    args = {"title":name,"master":0,"width":620,"height":113,"left":L0+710,"top":TOP+H1+15+HTB*2}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_enc #(master,w.tk)#Xroot)
    cb_ok = None
    data = FIXTURES #master

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name = "SETUP"
    args = {"title":name +" SHOW:"+master.base.show_name,
                "master":0,"width":445,"height":42,"left":L1+10+W1,"top":TOP,"resize":10}
    args["title"]  = "SETUP SHOW:"+master.base.show_name
    geo = split_window_position(pos_list,name)
    try:
        geo["width"] = args["width"]
        geo["height"] = args["height"]
    except:pass

    if geo:
        args.update(geo)

    cls = draw_setup #(master,w.tk)
    data = []
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name = "COMMAND"
    args = {"title":name,"master":0,"width":415,"height":130,"left":L1+10+W1,"top":TOP+81,"resize":10}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_command #(master,w.tk)
    data = []
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name = "LIVE"
    args = {"title":name,"master":0,"width":415,"height":42,"left":L1+10+W1,"top":TOP+235,"resize":10}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_live #(master,w.tk)
    data = []
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name = "CLOCK"
    args = {"title":name,"master":0,"width":335,"height":102,"left":L1+10+W1+80,"top":TOP+H1+HTB+160,"resize":0}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cclock = X_CLOCK()
    cls = cclock.draw_clock 
    data = []
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name="FX"
    args = {"title":name,"master":0,"width":415,"height":297,"left":L1+10+W1,"top":TOP+302,"resize":0}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_fx #(master,w.tk)
    data = []
    cb_ok = None

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    name="PATCH"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP,"foot":1,"head":1}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = GUI_PATCH
    data = FIXTURES

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c) #,obj)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name="COLORPICKER"
    args = {"title":name,"master":0,"width":600,"height":113,"left":L1+5,"top":TOP+5+HTB*2+H1}
    geo = split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    #w = Window(args)
    #draw_colorpicker(master,w.tk,FIXTURES,master)
    cls = draw_colorpicker #(master,w.tk,FIXTURES,master)
    data = [FIXTURES,master]
    cb_ok = None #FIXTURES

    c = window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    name="TableA"
    #w = Window(name,master=0,width=W1,height=H1,left=L1,top=TOP)
    #space_font = tk.font.Font(family="FreeSans", size=1 ) #, weight="bold")
    #x=TableFrame(root=w.tk)#,left=80,top=620)
    #w.show()
    #data =[]
    #for a in range(40):
    #    data.append(["E","E{}".format(a+1)])

    #x.draw(data=data,head=["E","C"],config=[12,5,5])
    #w=x.bframe

    #window_manager.new(w,name)



    master.render()
    window_manager.top("Table")
    #w = frame_fix #Window("OLD",master=0,width=W1,height=500,left=130,top=TOP)
    #window_manager.new(w,name)



    #if "--easy" in sys.argv:
    #load_window_position()



    thread.start_new_thread(loops,())
    mc_fix = MC_FIX()
    def mc_fix_loop():
        time.sleep(5)
        while 1:
            try:
                #print(1)
                data = FIXTURES.fixtures 
                mc_fix.set(index="fix",data=data)
            except Exception as e:
                print("MC_FIX EXCEPTION",e)
            time.sleep(1/10)

    thread.start_new_thread(mc_fix_loop,())
    
    try:
        window_manager.mainloop()
    finally:
        BASE_PATH = "/opt/LibreLight/Xdesk/"
        movewin.process_kill(BASE_PATH+"tksdl/")
        master.exit()

