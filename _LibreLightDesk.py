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

(c) 2012 micha@uxsrv.de
"""
import random
rnd_id = str(random.randint(1000,9000))
rnd_id += " Beta 22.02 "
import subprocess
try:
    rnd_id += subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
except:
    rnd_id += " no git"

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
import tkinter.simpledialog


import lib.chat as chat
import lib.motion as motion

from collections import OrderedDict



CUES    = OrderedDict()
groups  = OrderedDict()

class Modes():
    def __init__(self):
        self.modes = {}
        self.__cfg = {}
        self.__cb = None
    def val(self,mode,value=None):
        if value is not None:
            return self.set(mode,value)
        elif mode in self.modes:
            return self.modes[mode]
    def get(self,mode,value=None):
        return slef.val(mode,value)
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
        out = 0
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
            out = 1
            return 1
        elif value:
            for m in self.modes:
                if m not in protected and mode not in protected and m != mode:
                    if self.modes[m]:
                        self.modes[m]= 0
                        self.callback(m)
            if self.modes[mode]:
                if modes == "MOVE":
                    PRESETS.clear_move()
                if modes == "COPY":
                    PRESETS.clear_copy()
                self.modes[mode] = 0 # value
            else:
                self.modes[mode] = 1 #value
            out = 1
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
jclient = chat.tcp_sender()#port=50001)
import zlib
def jclient_send(data):
    t_start = time.time()
    jtxt = data
    jtxt = json.dumps(jtxt)
    jtxt = jtxt.encode()
    #jtxt = zlib.compress(jtxt)
    jclient.send(b"\00 "+ jtxt +b"\00 ")
    print(round((time.time()-t_start)*1000,4),"milis")
    cprint(round(time.time(),4),color="yellow")

class _FadeTime():
    def __init__(self):
        self._value = 2
        self._on = 1
    def inc(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value += round(value,4)
            else:
                self._value += value
        return self._value
    def val(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value = round(value,4)
            else:
                self._value = value
        return self._value
    def on(self):
        self._on = 1
    def off(self):
        self._on = 0
    def _is(self):
        if self._on:
            return 1
        return 0

FADE = _FadeTime()  #2 #0.1 #1.13
fx_prm_move = {"SIZE":100,"SPEED":30,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":25}
fx_prm      = {"SIZE":100,"SPEED":30,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":25}
fx_modes    = ["RED","GREEN","BLUE","MAG","YELLOW","CYAN"]
fx_mo       = ["sinus","on","rnd","bump","bump2","fade","cosinus"]

class FX_handler():
    def __init__():
        pass



def build_cmd(dmx,val,args=[],flash=0,xpfx="",attr=""):
    if not args:
        args.append(FADE.val())
    cmd=""
    if xpfx:
        pfx=xpfx  
    elif flash:
        pfx ="df"
    else:
        pfx ="d"
    if type(val) is float or type(val) is int:
        cmd += ",{}{}:{:0.4f}".format(pfx,dmx,val)
    else:
        cmd += ",{}{}:{}".format(pfx,dmx,val)
   
    if flash:
        cmd += ":0:0"#.format(val)
    else:
        for val in args:
            if type(val) is float or type(val) is int:
                cmd += ":{:0.4f}".format(val)
            else:
                cmd += ":{}".format(val)
    if attr:
        cmd += ":"+str(attr)
    #cprint("build_cmd",cmd,color="red")
    return cmd


def update_raw_dmx(data ,value=None,args=[],xfade=0,flash=0,pfx="d",fx=0):

    if flash:
        xfade = 0

    if not args: # and xfade is not None:# and FADE._is():
        args.append(xfade)
    else:
        args[0] = xfade

    cmd = []
    jcmd = []
    if flash:
        pfx += "f"

    for row in data:
        jxcmd={}
        if type(value) is float:
            jxcmd["VALUE"] = value #round(value,3)
        else:
            jxcmd["VALUE"] = value
        jxcmd["args"] = []

        if fx:
            if value is not None: 
                # z.b. flush off
                xcmd = str(value)+":"+row["FX"].split(":",1)[-1]
                jxcmd["FX"] = row["FX"].split(":",1)[-1]

            else:
                xcmd = row["FX"]
                jxcmd["FX"] = row["FX"]

            if row["FX2"]:
                jxcmd["FX2"] = row["FX2"]
        else:
            if row["VALUE"] is None:
                xcmd = ""
            else:
                if value is not None: 
                    if type(value) is float:
                        xcmd = "{:0.4f}".format(value)
                    else:
                        xcmd = "{}".format(value)
                else:
                    v=row["VALUE"]
                    xcmd = "{:0.4f}".format(v)
                    #cprint([v])
                    if type(v) is float:
                        jxcmd["VALUE"]  = v #round(v,3)
                    else:
                        jxcmd["VALUE"]  = v

                for arg in args:
                    if type(arg) is float:
                        xcmd += ":{:0.4f}".format(arg)
                        jxcmd["args"].append(v)#round(arg,3))
                    else:
                        xcmd += ":{}".format(arg)
                        jxcmd["args"].append(arg)#round(arg,3))
                #print( "pack: FIX",row["FIX"],row["ATTR"], xcmd)

        #xcmd += ":{}".format(row["ATTR"])
        v= xfade #FADE.val() #rxcmd["args"][0]
        if type( v ) is float:
            jxcmd["FADE"] = round(v,4)
        else:
            jxcmd["FADE"] = v
        #if ("VALUE" in jxcmd and jxcmd["VALUE"] is not None) or "FX" in jxcmd and jxcmd["FX"]:
        jcmd.append( jxcmd)
        cmd.append( xcmd)
        #if xcmd:
        #    cprint("update_raw_dmx j",jxcmd,color="red") 
        #    cprint("update_raw_dmx x",xcmd,color="red") 
    return cmd,jcmd

def update_dmx(attr,data,value=None,args=None,flash=0,pfx=""):
    xfade = 0
    if not args:
        args=[]
        xfade = FADE.val()
        args.append(xfade)

    #global modes #BLIND
    #print("update_dmx",data)
    dmx = data["DMX"]
    dmx = (data["UNIVERS"]*512)+data["DMX"]
    val = None
    cmd=""

    try:
        if attr == "DIM" and data["ATTRIBUT"][attr]["NR"] < 0: #VDIM
            #print( "VDIM")
            for attr in data["ATTRIBUT"]:
                dmx = (data["UNIVERS"]*512) + data["DMX"]
                dmx = data["DMX"]
                if data["ATTRIBUT"][attr]["NR"] < 0: #virtual channels
                    continue
                dmx += data["ATTRIBUT"][attr]["NR"]-1
                mode = ""
                if "MODE" in data["ATTRIBUT"][attr]:
                    mode = data["ATTRIBUT"][attr]["MODE"]
                #print(attr)
                val = data["ATTRIBUT"][attr]["VALUE"]
                if data["ATTRIBUT"][attr]["MASTER"]:
                    val = val * (data["ATTRIBUT"]["DIM"]["VALUE"] / 255.)
                    if val is not None:            
                     
                        #cmd += ",d{}:{:0.4f}".format(dmx,int(val))
                        if value is not None:
                            val = value
                        if mode == "F": #FADE
                            cmd += build_cmd(dmx,val,args=args,flash=flash,xpfx=pfx,attr=attr)
                        else:
                            cmd += build_cmd(dmx,val,args=[0],flash=flash,xpfx=pfx,attr=attr)
                        #print("cmd",cmd)
                    
            
        elif data["ATTRIBUT"][attr]["NR"] > 0: 
            dmx += data["ATTRIBUT"][attr]["NR"]-1
            val = data["ATTRIBUT"][attr]["VALUE"]
            mode = ""
            if "MODE" in data["ATTRIBUT"][attr]:
                mode = data["ATTRIBUT"][attr]["MODE"]

            if data["ATTRIBUT"][attr]["MASTER"]:
                #if "VDIM" in data["ATTRIBUT"]:
                if "DIM" in data["ATTRIBUT"] and data["ATTRIBUT"]["DIM"]["NR"] < 0: #VDIM
                    val = val * (data["ATTRIBUT"]["DIM"]["VALUE"] / 255.)
            if val is not None:            
                #cmd += ",d{}:{}".format(dmx,int(val))
                if value is not None:
                    val = value
                if mode == "F": #FADE
                    cmd += build_cmd(dmx,val,args=args,flash=flash,xpfx=pfx,attr=attr)
                else:
                    cmd += build_cmd(dmx,val,args=[0],flash=flash,xpfx=pfx,attr=attr)
                #print("cmd",cmd)

        if modes.val("BLIND"):
            cmd=""

        #cprint("update_dmx",cmd,color="red") 
        return cmd
    except Exception as e:
        cprint("== cb EXCEPT",e,color="red")
        cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
        cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        raise e

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
 
class Xevent():
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode

    def fx(self,event):
        cprint("Xevent.fx",self.attr,self.fix,event)
        jdatas = []
        fx2 = {}
        if event.num == 4:
            cprint("FX:COLOR CHANGE",fx_prm,color="red")
            txt = "FX:RED" 
            fx_prm["MODE"] += 1
            if fx_prm["MODE"] > len(fx_modes):
                fx_prm["MODE"]=0
            txt = "FX:\n"+fx_modes[fx_prm["MODE"]]

            master.elem_fx_commands["FX:RED"]["text"] = txt
        elif event.num == 5:
            cprint("FX:COLOR CHANGE",fx_prm,color="red")
            txt = "FX:RED" 
            fx_prm["MODE"] -= 1
            if fx_prm["MODE"] < 0:
                fx_prm["MODE"]= len(fx_modes)-1
            txt = "FX:\n"+fx_modes[fx_prm["MODE"]]
            master.elem_fx_commands["FX:RED"]["text"] = txt
        elif event.num == 1:
            offset = 0
            start = fx_prm["START"]
            base  = fx_prm["BASE"]
            xfixtures = []
            fix_active =FIXTURES.get_active() 
            for fix in fix_active:
                if fix == "CFG":
                    continue
                xfixtures.append(fix)
            x=0
            if not xfixtures:
                cprint("470 fx() ... init no fixture selected",color="red")
                return 0
            wings = []
            l = len(xfixtures)
            if fx_prm["WING"] and l > 1:
                w = l // fx_prm["WING"]
                teiler = l//w
                if teiler < 2:
                    teiler = 2
                for i in range(teiler):
                    j = i*w
                    wing = xfixtures[j:j+w]
                    if i%2==0:
                        wing = wing[::-1]
                    print("wing",i,"j",j,"w",w,"wing",wing)
                    wings.append(wing)
                if l > j+w:
                    wing = xfixtures[j+w:]
                    wings.append(wing)
            else:
                wings.append(xfixtures)

            for wing in wings:

                wlen = len(wing)
                coffset= 0 # 1024/wlen * (offset/255)

                for fix in wing:
                    data = FIXTURES.fixtures[fix]
                    for attr in data["ATTRIBUT"]:
                        jdata = {"MODE":"FX"}
                        jdata["VALUE"] = None
                        jdata["FIX"] = fix
                        jdata["DMX"] = FIXTURES.get_dmx(fix,attr)
                        jdata["ATTR"] =attr
                        if attr.endswith("-FINE"):
                            continue

                        csize  = fx_prm["SIZE"]
                        cspeed = fx_prm["SPEED"]
                        cstart = fx_prm["START"]
                        cbase  = fx_prm["BASE"]
                        width  = fx_prm["WIDTH"]
                        invert = fx_prm["INVERT"]
                        coffset= round(offset,1)

                        fx=""
                        if "SIN" in self.attr:
                            fx = "sinus"
                        elif "FD" in self.attr:
                            fx = "fade"
                        elif "RND" in self.attr:
                            fx = "rnd"
                        elif "ON" in self.attr:
                            fx = "on"
                        elif "BUM2" in self.attr:
                            fx = "bump2"
                        elif "BUM" in self.attr:
                            fx = "bump"
                        elif "COS" in self.attr:
                            fx = "cosinus"

                        if fx:
                            if fx_prm["SPEED"] < 0:
                                fx = "off"
                        else:
                            if ":DIM" in self.attr:
                                base=""
                                ffxb= fx_mo[fx_prm["MO"]] 
                                if attr == "DIM":
                                    if fx_prm["SPEED"] < 0:
                                        fx = "off"
                                    else:
                                        fx = ffxb #"fade"
                            elif ":TILT" in self.attr:
                                base=""
                                if attr == "PAN":
                                    fx = "off"
                                if attr == "TILT":
                                    if fx_prm["SPEED"] < 0:
                                        fx = "off"
                                    else:
                                        fx = "sinus"
                            elif ":PAN" in self.attr:
                                base=""
                                if attr == "PAN":
                                    if fx_prm["SPEED"] < 0:
                                        fx = "off"
                                    else:
                                        fx = "cosinus" 
                                if attr == "TILT":
                                   fx = "off"
                            elif ":CIR" in self.attr:
                                base=""
                                if attr == "PAN":
                                    if fx_prm["SPEED"] < 0:
                                        fx = "off"
                                    else:

                                        fx = "cosinus" 
                                if attr == "TILT":
                                    if fx_prm["SPEED"] < 0:
                                        fx = "off"
                                    else:
                                        fx = "sinus"
                            elif ":RED" in self.attr:

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
                                elif "GREEN" in fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#in self.attr:
                                    base="-"
                                    if attr == "RED":
                                        fx =  ffxb#"off" 
                                elif "GREEN" in fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#in self.attr:
                                    if attr == "GREEN":
                                        fx = ffxb# "off"
                                        fx=ffx
                                    if attr == "BLUE":
                                        fx =  ffxb#"off"
                                elif "BLUE" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#self.attr:
                                    base="-"
                                    if attr == "RED":
                                        fx = ffxb# "off" 
                                    if attr == "GREEN":
                                        fx = ffxb# "off"
                                    if attr == "BLUE":
                                        fx = ffxb# "off"
                                        fx=ffx
                                elif "YELLOW" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#self.attr:
                                    base="-"
                                    if attr == "RED":
                                        fx = ffxb# "off" 
                                        fx=ffx
                                    if attr == "GREEN":
                                        fx = ffxb# "off"
                                        fx=ffx
                                    if attr == "BLUE":
                                        fx = "off"
                                elif "CYAN" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#self.attr:
                                    base="-"
                                    if attr == "RED":
                                        fx = ffxb# "off" 
                                    if attr == "GREEN":
                                        fx = ffxb# "off"
                                        fx=ffx
                                    if attr == "BLUE":
                                        fx = ffxb# "off"
                                        fx=ffx
                                elif "MAG" in  fx_modes[fx_prm["MODE"]]:#fx_prm["MODE"]:#self.attr:
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
                            fjdata["OFFSET"]= round(coffset,2)
                            fjdata["INVERT"]= int(invert)
                            fjdata["BASE"]  = cbase
                            jdata["FX2"] = fjdata
                            data["ATTRIBUT"][attr]["FX2"] = fjdata
                            jdatas.append(jdata)


                    if fx_prm["OFFSET"] > 0.5: # and 
                        aoffset = (100/wlen) * (fx_prm["OFFSET"]/100) 
                        if fx_prm["DIR"] <= 0:
                            offset -= aoffset 
                        else:
                            offset += aoffset 
                        offset = round(offset,2)
            if jdatas and not modes.val("BLIND"):
                jclient_send(jdatas)
            master.refresh_fix()


    def command(self,event):       
        if self.mode == "COMMAND":
            
            if self.attr == "CLEAR":
                if event.num == 1:
                    ok = FIXTURES.clear()
                    if ok:
                        master.refresh_fix()
                    modes.val(self.attr,0)

                    
            elif self.attr.startswith("SZ:"):#SIN":
                #global fx_prm
                k = "SIZE"
                if event.num == 1:
                    fx_prm[k] =30
                elif event.num == 3:
                    fx_prm[k] =100
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] +=5
                elif event.num == 5:
                    fx_prm[k] -=5
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 0:
                    fx_prm[k] =0
                if fx_prm[k] == 6: #bug
                    fx_prm[k] =5
                self.data.elem_fx_commands[self.attr]["text"] = "SZ:\n{:0.0f}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("SP:"):#SIN":
                #global fx_prm
                k = "SPEED"
                if event.num == 1:
                    fx_prm[k] = 6
                elif event.num == 3:
                    fx_prm[k] = 60
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 0.06
                    elif fx_prm[k] < 5:
                        fx_prm[k] *=1.2
                    else:
                        fx_prm[k] +=5 #1.1
                elif event.num == 5:
                    if fx_prm[k] <= 5:
                        fx_prm[k] *=0.8
                    else:
                        fx_prm[k] -= 5 #1.1
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 0.05:
                    fx_prm[k] =0
                if fx_prm[k] > 5 and fx_prm[k] < 10: #bug
                    fx_prm[k] =5

                if fx_prm[k] < 0:
                    self.data.elem_fx_commands[self.attr]["text"] = "SP:\noff".format(fx_prm[k])
                else:
                    self.data.elem_fx_commands[self.attr]["text"] = "SP:\n{:0.02f}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("ST:"):#SIN":
                #global fx_prm
                k = "START"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] += 5 #1.1
                elif event.num == 5:
                    fx_prm[k] -= 5 #1.1
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 5:
                    fx_prm[k] =0
                if fx_prm[k] == 6: #bug
                    fx_prm[k] =5

                self.data.elem_fx_commands[self.attr]["text"] = "ST:\n{:0.0f}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("MO:"):# on,sinus,bump
                #global fx_prm
                k = "MO"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    fx_prm[k] -=1
                    if fx_prm[k] < 0:
                        fx_prm[k] = len(fx_mo)-1
                elif event.num == 5:
                    fx_prm[k] +=1
                    if fx_prm[k] >= len(fx_mo):
                        fx_prm[k] = 0
                txt = fx_mo[fx_prm[k]] 
                self.data.elem_fx_commands[self.attr]["text"] = "MO:\n{}".format(txt)
                cprint(fx_prm)
            elif self.attr.startswith("WIDTH:"):#SIN":
                #global fx_prm
                k = "WIDTH"
                if event.num == 1:
                    fx_prm[k] = 25
                elif event.num == 2:
                    fx_prm[k] = 50
                elif event.num == 3:
                    fx_prm[k] = 100
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    elif fx_prm[k] == 50:
                        fx_prm[k] = 100
                    elif fx_prm[k] == 5:
                        fx_prm[k] = 25
                    elif fx_prm[k] == 25:
                        fx_prm[k] = 50
                    else:
                        fx_prm[k] += 5 #*=1.1
                elif event.num == 5:
                    if fx_prm[k] == 50:
                        fx_prm[k] = 25
                    elif fx_prm[k] == 100:
                        fx_prm[k] = 50
                    else:
                        fx_prm[k] -=5 #/=1.1
                    
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] < 0:
                    fx_prm[k] = 0
                if fx_prm[k] > 100:
                    fx_prm[k] = 100
                if fx_prm[k] == 6: #bug
                    fx_prm[k] =5
                if fx_prm[k] > 25 and fx_prm[k] < 50: #bug
                    fx_prm[k] =50
                if fx_prm[k] > 50 and fx_prm[k] < 100: #bug
                    fx_prm[k] =100

                self.data.elem_fx_commands[self.attr]["text"] = "WIDTH:\n{:0.0f}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("DIR:"):#SIN":
                #global fx_prm
                k = "DIR"
                if event.num == 1:
                    fx_prm[k] = 1
                elif event.num == 3:
                    fx_prm[k] = -1
                elif event.num == 4:
                    fx_prm[k] = 1
                elif event.num == 5:
                    fx_prm[k] =-1
                txt = fx_prm[k] 
                self.data.elem_fx_commands[self.attr]["text"] = "DIR:\n{}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("INVERT:"):#SIN":
                #global fx_prm
                k = "INVERT"
                if event.num == 1:
                    fx_prm[k] = 0
                elif event.num == 3:
                    fx_prm[k] = 1
                elif event.num == 4:
                    fx_prm[k] = 1
                elif event.num == 5:
                    fx_prm[k] =0
                if fx_prm[k] == 6: #bug ?
                    fx_prm[k] =5
                self.data.elem_fx_commands[self.attr]["text"] = k+":\n{}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("WING:"):#SIN":
                #global fx_prm
                k = "WING"
                if event.num == 1:
                    fx_prm[k] = 1
                elif event.num == 3:
                    fx_prm[k] = 2
                elif event.num == 4:
                    fx_prm[k] += 1
                elif event.num == 5:
                    fx_prm[k] -=1
                if fx_prm[k] > 100:
                    fx_prm[k] = 100
                if fx_prm[k] < 1:
                    fx_prm[k] =1
                    
                txt = fx_prm[k] 
                self.data.elem_fx_commands[self.attr]["text"] = "WING:\n{}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("OF:"):#SIN":
                #global fx_prm
                k = "OFFSET"
                if event.num == 1:
                    fx_prm[k] = 50
                elif event.num == 2:
                    fx_prm[k] *= 2
                elif event.num == 3:
                    fx_prm[k] = 100
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] +=5 #*=1.1
                elif event.num == 5:
                    fx_prm[k] -=5 #/=1.1
                #fx_prm[k] =int(fx_prm[k])
                
                #if fx_prm[k] > 512:
                #    fx_prm[k] = 512
                if fx_prm[k] < 5:
                    fx_prm[k] =0
                if fx_prm[k] == 6: #bug
                    fx_prm[k] =5

                self.data.elem_fx_commands[self.attr]["text"] = "OF:\n{:0.0f}".format(fx_prm[k])
                cprint(fx_prm)
            elif self.attr.startswith("BS:"):
                k = "BASE"
                if event.num == 1:
                    fx_prm[k] = "-"
                elif event.num == 3:
                    fx_prm[k] = "0"
                elif event.num == 4:
                    fx_prm[k] = "+"
                elif event.num == 5:
                    fx_prm[k] = "0"
                self.data.elem_fx_commands[self.attr]["text"] = "BS:\n{}".format(fx_prm[k])
            elif self.attr.startswith("FX:"):#SIN":
                self.fx(event)

            elif self.attr == "FX OFF":
                if event.num == 1:
                    FIXTURES.fx_off("all")
                    CONSOLE.fx_off("all")
                    CONSOLE.flash_off("all")
                    master.refresh_fix()
                    return 0


            
            elif self.attr == "FADE":
                fade = FADE.val()
                print("EVENT CHANGE FADE",fade)
                if fade < 0.01:
                    FADE.val(0.01)
                elif fade > 100.0:
                    fade = 100
                if event.num == 4:
                    fade *= 1.1
                elif event.num == 5:
                    fade /= 1.1
                elif event.num == 1:
                    if FADE._is():
                        FADE.off()# = 0
                        self.data.elem_commands[self.attr]["bg"] = "grey"
                    else:
                        FADE.on()# = 1
                        self.data.elem_commands[self.attr]["bg"] = "green"
                elif event.num == 2:
                    if fade > 1 and fade < 4:
                        fade = 4
                    elif fade > 3 and fade < 6:
                        fade = 6
                    elif fade > 5 and fade < 7:
                        fade = 8
                    elif fade > 7 and fade < 9:
                        fade = 10
                    elif fade > 9:
                        fade = 0.01
                    elif fade < 1:
                        fade = 1.1
                fade = round(fade,3)
                FADE.val(fade)
                self.data.elem_commands[self.attr]["text"] = "Fade{:0.2f}".format(fade)

            elif self.attr == "BACKUP":
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()
                #time.sleep(1)
                modes.val(self.attr,0)
            else:
                if event.num == 1:
                    print("ELSE",self.attr)
                    modes.val(self.attr,1)

            return 0


            
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

            if self.mode == "COMMAND":
                self.command(event)
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
                                modes.val("MOVE",0)
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
                        self.data.preset_go(nr,xfade=0,event=event,val=255)
                        
                return 0
            elif self.mode == "INPUT":
                return 0
            if self.mode == "ENCODER":
                cprint("ENC",self.fix,self.attr,self.mode)
                cprint(self.data)
                val=""
                if event.num == 1:
                    val ="click"
                elif event.num == 4:
                    val ="+"
                elif event.num == 5:
                    val ="-"

                if val:
                    FIXTURES.encoder(fix=self.fix,attr=self.attr,xval=val)
                    
                master.refresh_fix()

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
                                            
        
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
        show_name = "GloryCamp2021"
        #show_name = "JMS"
        show_name = "DemoShow"
        #show_name = "Dimmer"
        self.home = os.environ['HOME'] 
        self.show_path = self.home +"/LibreLight/"
        try:
            f = open(self.show_path+"init.txt","r")
            for line in f.readlines():
                cprint(line)
                if not line.startswith("#"):
                    show_name = line.strip()
                    show_name = show_name.replace(".","")
                    show_name = show_name.replace("\\","")
                    show_name = show_name.replace("/","")
        except Exception as e:
            cprint("shownamw exception",color="red")
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/show/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/" +show_name +"/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        pass
    def _load(self,filename):
        xfname = self.show_path+"/"+str(filename)+".sav"
        print("load",xfname)
        f = open(xfname,"r")
        lines = f.readlines()
        f.close()    
        data   = OrderedDict()
        labels = OrderedDict()
        
        for line in lines:
            
            key,label,rdata = line.split("\t",2)
            key = int(key)
            #print(xfname,"load",key,label)
            #print(line)
            jdata = json.loads(rdata,object_pairs_hook=OrderedDict)
            nrnull = 0
            print(jdata)
            #if "ATTRIBUT" in jdata:  # translate old FIXTURES.fixtures start with 0 to 1          
            #    for attr in jdata["ATTRIBUT"]:
            #        row = jdata["ATTRIBUT"][attr]
            #        if type(row) is OrderedDict:
            #            #print(row)
            #            if "VALUE" in row:
            #                v = row["VALUE"]
            #                if type(v) is float:
            #                    v = round(v,4)
            #                    jdata["ATTRIBUT"][attr]["VALUE"] = round(v,4)
            #                    print("preset v",key,label,attr,v)
            if "ATTRIBUT" in jdata:  # translate old FIXTURES.fixtures start with 0 to 1          
                for attr in jdata["ATTRIBUT"]:
                    pass
                    #if "VALUE" in jdata["ATTRIBUT"][attr]:
                    #    v = jdata["ATTRIBUT"][attr]["VALUE"]
                    #    if type(v) is float:
                    #        jdata["ATTRIBUT"][attr]["VALUE"] = round(v,4)
                    #        #print("fix v",attr,v)

                    #if "NR" in jdata["ATTRIBUT"][attr]:
                    #    nr = jdata["ATTRIBUT"][attr]["NR"]
                    #    if nr == 0:
                    #        nrnull = 1
                    #        break

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

    def _backup(self,filename,data,labels):
        #fixture
        #xfname = "show/"+show_name+"/"+str(filename)+".sav"
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


class Event():
    def __init__(self,name):
        self.name=name
        #print("init",self)
    def event(self,event):
        print(self.name,event)
class scroll():
    def __init__(self,canvas):
        self.canvas=canvas
    def config(self,event):
        canvas = self.canvas
        canvas.configure(scrollregion=canvas.bbox("all"))#,width=400,height=200)


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


class GUI(Base):
    def __init__(self):
        super().__init__() 
        self.load()
        self._XX = 0

        self.all_attr =["DIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.fx_commands =["REC-FX","FX OFF","\n"
                ,"FX:CIR","FX:PAN","FX:TILT","MO:ON""\n"
                ,"MSZ:","MSP:","MST:","MOF:","MBS:-","\n"
                ,"FX:DIM","FX:\nRED", "WIDTH:\n25","DIR:\n1","INVERT:\n0","WING:\n2","\n"
                ,"SZ:\n","SP:\n","ST:\n","OF:\n","BS:\n-","\n"
                , "FX:SIN","FX:COS","FX:BUM","FX:BUM2","FX:FD","FX:ON","FX:RND" ]
        self.commands =["\n","ESC","CFG-BTN","LABEL","BACKUP","DEL","\n"
                ,"SELECT","FLASH","GO","FADE","MOVE","\n"
                ,"BLIND","CLEAR","REC","EDIT","COPY","\n" 
                ]
        self.elem_fx_commands = {}
        self.val_fx_commands = {}
        self.elem_commands = {}
        self.val_commands = {}

        self.elem_presets = {}
        
        for i in range(8*8*8):
            if i not in PRESETS.val_presets:
                name = "Preset:"+str(i+1)+":\nXYZ"
                #self.presets[i] = [i]
                PRESETS.val_presets[i] = OrderedDict() # FIX 
                PRESETS.val_presets[i]["CFG"] =  OrderedDict() # CONFIG 
                PRESETS.label_presets[i] = "-"

        modes.set_cb(self.xcb)
    def button_refresh(self,name,color,color2=None,fg=None):
        cprint("button_refresh",name,color)
        #if color == "gold":
        #    color2 = "yellow"
        if color2 is None:
            color2 = color
        if name in self.elem_commands:
            self.elem_commands[name]["bg"] = color
            self.elem_commands[name].config(activebackground=color2)
            if fg:
                self.elem_commands[name]["fg"] = fg
                print(dir(self.elem_commands[name]))
        elif name in self.elem_fx_commands:
            #todo
            self.elem_fx_commands[name]["bg"] = color
            self.elem_fx_commands[name].config(activebackground=color2)
            if fg:
                self.elem_fx_commands[name]["fg"] = fg
                print(dir(self.elem_fx_commands[name]))
    def btn_cfg(self,nr):
        txt = PRESETS.btn_cfg(nr) 
        txt = tkinter.simpledialog.askstring("CFG-BTN","GO=GO FL=FLASH\nSEL=SELECT EXE:"+str(nr+1),initialvalue=txt)
        if txt:
            PRESETS.btn_cfg(nr,txt)
            self.elem_presets[nr]["text"] = PRESETS.get_btn_txt(nr)
        modes.val("CFG-BTN",0)
    def label(self,nr):
        txt = PRESETS.label(nr) 
        txt = tkinter.simpledialog.askstring("LABEL","EXE:"+str(nr+1),initialvalue=txt)
        if txt:
            PRESETS.label(nr,txt) 
            self.elem_presets[nr]["text"] = PRESETS.get_btn_txt(nr)
        modes.val("LABEL", 0)
    def xcb(self,mode,value=None):
        cprint("MODE CALLBACK",mode,value,color="green",end="")
        #cprint(self,"xcb","MODE CALLBACK",mode,value,color="green")
        if value:
            cprint("===== ON  ======",color="red")
            if mode == "REC-FX":
                modes.val("REC",1)
            self.button_refresh(mode,color="red")#,fg="blue")
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

            if k in PRESETS.val_presets and len(PRESETS.val_presets[k]) :
                sdata = PRESETS.val_presets[k]
                #print("sdata7654",sdata)
                BTN="go"
                if "CFG" in sdata:#["BUTTON"] = "GO"
                    if "BUTTON" in sdata["CFG"]:
                        BTN = sdata["CFG"]["BUTTON"]
                txt=str(k)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
                #txt+=str(self._XX)
                b["text"] = txt
                b["bg"] = "yellow"
                b.config(activebackground="yellow")
                if len(sdata) > 1:
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

                    b["fg"] = "black"
                    if val_color:
                        b["bg"] = "gold"
                        b.config(activebackground="#ffaa55")
                        if fx_color:
                            b["fg"] = "blue"
                    else:   
                        if fx_color:
                            b["bg"] = "cyan"
                            b.config(activebackground="#55d4ff")
                else:
                    b["bg"] = "grey"
                    b.config(activebackground="#aaaaaa")

            if "\n" in txt:
                txt = txt.split("\n")[0]
            if "SEL" in txt:
                b["fg"] = "black"
                b["bg"] = "#5555ff"
                b.config(activebackground="#6666ff")

            elif "ON" in txt:
                b["bg"] = "#ffcc00"
                b["fg"] = "#00c"

            elif "GO" in txt:
                b["fg"] = "black"
            elif "FL" in txt:
                b["fg"] = "#7f00ff"


    def refresh_fix(self):
        refresher.reset() # = Refresher()
    def _refresh_fix(self):
        for fix in FIXTURES.fixtures:                            
            sdata = FIXTURES.fixtures[fix]                            
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
        
        master.refresh_exec()
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
                    elem = self.elem_attr[fix][attr]
                    FIXTURES.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                    elem["bg"] = "yellow"
    def preset_go(self,nr,val=None,xfade=None,event=None,button=""):
        t_start = time.time()
        if xfade is None and FADE._is():
            xfade = FADE.val()
        

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
            if type(val) is not None and val == 0 :
                value = "off"
            if event:
                if str(event.type) == "ButtonRelease" or event.type == '5' :
                    value = "off"

            cprint("preset_go() FLUSH",value,color="red")
            fcmd  = FIXTURES.update_raw(rdata,update=0)
            self._preset_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH)
                
        elif not val:
            cprint("preset_go() STOP",value,color="red")
        elif button == "on" or ( modes.val("ON") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["on","ON"])):
            fcmd  = FIXTURES.update_raw(rdata)
            self._preset_go(rdata,cfg,fcmd,value,xfade=0,xFLASH=xFLASH)
        elif button == "go" or ( modes.val("GO") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["go","GO"])): 
            fcmd  = FIXTURES.update_raw(rdata)
            self._preset_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH)



        if not (modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL")): #FLASH
            self.refresh_exec()
            self.refresh_fix()
        cprint("preset_go",time.time()-t_start)

    def _preset_go(self,rdata,cfg,fcmd,value=None,xfade=None,event=None,xFLASH=0):
        if xfade is None and FADE._is():
            xfade = FADE.val()

        cprint("PRESETS._preset_go()",len(rdata))
        vvcmd,jvvcmd = update_raw_dmx( rdata ,value,[],xfade=xfade ) 
        fxcmd,jfxcmd = update_raw_dmx( rdata ,value,[],xfade=xfade,fx=1) 

        cmd = []
        for vcmd,d in [[jvvcmd,"d"],[jfxcmd,"fx"]]:
            if xFLASH:
                d+="f"
            for i,v in enumerate(fcmd):
                if xFLASH:
                    vcmd[i]["FLASH"] = 1

                DMX = fcmd[i]["DMX"]
                if "VALUE" in vcmd[i] and type(vcmd[i]["VALUE"]) is float:
                    vcmd[i]["VALUE"] = round(vcmd[i]["VALUE"],3)
                if value is not None:
                    vcmd[i]["VALUE"] = value 
                if value == "off":
                    if "FX2" in vcmd:
                        vcmd[i]["FX2"]["TYPE"] = value

                if DMX and vcmd[i]:
                    vcmd[i]["DMX"] = DMX

                if "VIRTUAL" in fcmd[i]:
                    for a in fcmd[i]["VIRTUAL"]:
                        DMX = fcmd[i]["VIRTUAL"][a]
                        if DMX and vcmd[i]:
                            vcmd[i]["DMX"] = DMX
                #if vcmd[i]["VALUE"] is not None or ("FX2" in vcmd[i] and vcmd[i]["FX2"]):
                #    cprint("jvcmd",vcmd[i])
                #    cmd.append(vcmd[i])
                #elif vcmd[i]["VALUE"] is not None or ("FX" in vcmd[i] and vcmd[i]["FX"]):
                #    cprint("jvcmd",vcmd[i])
                #    cmd.append(vcmd[i])
                #cprint("jvcmd",vcmd[i])
                cmd.append(vcmd[i])

        if cmd and not modes.val("BLIND"):
            jclient_send(cmd)

        
    def draw_sub_dim(self,fix,data,c=0,r=0,frame=None):
        i=0
        if frame is None:
            frame = tk.Frame(root,bg="black")
            frame.pack(fill=tk.X, side=tk.TOP)

        if fix not in self.elem_attr:
            self.elem_attr[fix] = {}
            
        for attr in data["ATTRIBUT"]:
            
            if attr not in self.all_attr:
                self.all_attr.append(attr)
            if attr not in self.elem_attr[fix]:
                self.elem_attr[fix][attr] = []
            if attr.endswith("-FINE"):
                continue
            v= data["ATTRIBUT"][attr]["VALUE"]
            b = tk.Button(frame,bg="lightblue", text=""+str(fix)+" "+data["NAME"],width=4)
            b.bind("<Button>",Xevent(fix=fix,mode="D-SELECT",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=6)
            self.elem_attr[fix][attr] = b
            b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=12:
                c=0
                r+=1
        return c,r
    def draw_patch(self,yframe):
        
        xframe = tk.Frame(yframe,bg="black")
        xframe.pack()
        def yview(event):
            print("yevent",event)
            yyy=20.1
            xframe.yview_moveto(yyy)

        i=0
        c=0
        r=0
        for fix in FIXTURES.fixtures:
            i+=1
            data = FIXTURES.fixtures[fix]
                            
            b = tk.Button(xframe,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            #r+=1
            if fix not in self.elem_attr:
                self.elem_attr[fix] = {}
                
            patch = ["DMX","UNIVERS"]
            for k in patch:
                v=data[k]
                b = tk.Button(xframe,bg="grey", text=str(k)+' '+str(v),width=8)
                #self.elem_attr[fix][attr] = b
                #b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                if c >=8:
                    c=1
                    r+=1
            for attr in data["ATTRIBUT"]:
                
                if attr not in self.all_attr:
                    self.all_attr.append(attr)
                if attr not in self.elem_attr[fix]:
                    self.elem_attr[fix][attr] = []
                if attr.endswith("-FINE"):
                    continue
                v= data["ATTRIBUT"][attr]["VALUE"]
                
                b = tk.Button(xframe,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
                #self.elem_attr[fix][attr] = b
                #b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                if c >=8:
                    c=1
                    r+=1
            c=0
            r+=1
                
    def draw_fix(self,xframe,yframe=None):
        r=0
        c=0
        frame_dim=xframe
        if yframe:
            frame_dim=yframe
        frame_fix=xframe
        root = frame_dim
        dim_frame = tk.Frame(root,bg="black")
        dim_frame.pack(fill=tk.X, side=tk.TOP)
        root = frame_fix
        fix_frame = tk.Frame(root,bg="black")
        fix_frame.pack(fill=tk.X, side=tk.TOP)
        i=0
        c=0
        r=0
        dim_end=0
        for fix in FIXTURES.fixtures:
            i+=1
            data = FIXTURES.fixtures[fix]
            #print("draw_fix", fix ,data )
            
            if(len(data["ATTRIBUT"].keys()) <= 1):
                c,r=self.draw_sub_dim(fix,data,c=c,r=r,frame=dim_frame)
            else:
                if not dim_end:
                    dim_end=1
                    c=0
                    r=0
                #self._draw_fix(fix,data,root=fix_frame)
                frame = fix_frame
            
                b = tk.Button(frame,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
                b.bind("<Button>",Xevent(fix=fix,mode="SELECT",elem=b).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                #r+=1
                if fix not in self.elem_attr:
                    self.elem_attr[fix] = {}
                    
                for attr in data["ATTRIBUT"]:
                    
                    if attr.endswith("-FINE"):
                        continue
                    if attr not in self.all_attr:
                        self.all_attr.append(attr)
                    if attr not in self.elem_attr[fix]:
                        self.elem_attr[fix][attr] = ["line1348",fix,attr]
                    v= data["ATTRIBUT"][attr]["VALUE"]
                    
                    b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
                    self.elem_attr[fix][attr] = b
                    b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
                    b.grid(row=r, column=c, sticky=tk.W+tk.E)
                    c+=1
                    if c >=8:
                        c=1
                        r+=1
                c=0
                r+=1
                
    def draw_enc(self,xframe):
        root2 = xframe
        i=0
        c=0
        r=0
        
        frame = tk.Frame(root2,bg="black")
        frame.pack( side=tk.TOP,expand=1,fill="both")

        
        b = tk.Button(frame,bg="lightblue", text="ENCODER",width=6)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        for attr in self.all_attr:
            if attr.endswith("-FINE"):
                continue
            v=0
            b = tk.Button(frame,bg="orange", text=str(attr)+'',width=6)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=attr,data=self,mode="ENCODER").cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
    def draw_fx(self,xframe):
        frame_fx=xframe
        i=0
        c=0
        r=0
        
        frame = tk.Frame(frame_fx,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="FX.",width=6)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        for comm in self.fx_commands:
            if comm == "\n":
                c=0
                r+=1
                continue
            v=0
            
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
            if comm not in self.elem_fx_commands:
                comm = comm.replace("\n","")
                self.elem_fx_commands[comm] = b
                self.val_fx_commands[comm] = 0
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=self,mode="COMMAND").cb)
            if comm == "BLIND":
                b["bg"] = "grey"
            elif comm == "CLEAR":
                b["bg"] = "grey"
            elif comm == "REC-FX":
                b["bg"] = "grey"
            elif comm == "FADE":
                b["bg"] = "green"
            elif comm == "FX OFF":
                b["bg"] = "magenta"
            elif comm[:3] == "FX:":
                b["text"] = comm #"BS:{}".format(fx_prm["BASE"])
                b["bg"] = "#ffbf00"
            elif comm == "MO:on":
                b["text"] = comm #"BS:{}".format(fx_prm["BASE"])
                b["bg"] = "lightgreen"
            elif comm == "MO:on":
                b["text"] = comm #"BS:{}".format(fx_prm["BASE"])
                b["bg"] = "lightgreen"
            elif comm == "SZ:":
                b["text"] = "SZ:\n{:0.0f}".format(fx_prm["SIZE"])
                b["bg"] = "lightgreen"
            elif comm == "SP:":
                b["text"] = "SP:\n{:0.0f}".format(fx_prm["SPEED"])
                b["bg"] = "lightgreen"
            elif comm == "ST:":
                b["bg"] = "lightgreen"
                b["text"] = "ST:\n{:0.0f}".format(fx_prm["START"])
            elif comm == "OF:":
                b["bg"] = "lightgreen"
                b["text"] = "OF:\n{:0.0f}".format(fx_prm["OFFSET"])
            elif comm == "BS:-":
                b["bg"] = "lightgreen"
                b["text"] = "BS:\n{}".format(fx_prm["BASE"])
            elif comm[0] == "M":
                b["text"] = comm #"BS:{}".format(fx_prm["BASE"])
                b["bg"] = "lightgrey"

            if comm:
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=6:
                c=0
                r+=1
    def draw_command(self,xframe):
        frame_cmd=xframe
        i=0
        c=0
        r=0
        
        frame = tk.Frame(frame_cmd,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="COMM.",width=6)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
        c+=1
        for comm in self.commands:
            if comm == "\n":
                c=0
                r+=1
                continue
            v=0
            
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
            if comm not in self.elem_commands:
                self.elem_commands[comm] = b
                self.val_commands[comm] = 0
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=self,mode="COMMAND").cb)
            if comm == "BLIND":
                b["bg"] = "grey"
            if comm == "CLEAR":
                b["bg"] = "grey"
            if comm == "REC-FX":
                b["bg"] = "grey"
            if comm == "FADE":
                b["bg"] = "green"
            if comm == "FX OFF":
                b["bg"] = "magenta"
            if comm == "SZ:":
                b["text"] = "SZ:{:0.0f}".format(fx_prm["SIZE"])
            if comm == "SP:":
                b["text"] = "SP:{:0.0f}".format(fx_prm["SPEED"])
            if comm == "FADE":
                b["text"] = "FADE:{:0.02f}".format(FADE.val())
            if comm == "ST:":
                b["text"] = "ST:{:0.0f}".format(fx_prm["START"])
            if comm == "OF:":
                b["text"] = "OF:{:0.0f}".format(fx_prm["OFFSET"])
            if comm == "BS:":
                b["text"] = "BS:{}".format(fx_prm["BASE"])
            if comm:
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=5:
                c=0
                r+=1
    def draw_preset(self,xframe):

        i=0
        c=0
        r=0
        root = xframe
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        i=0
        for k in PRESETS.val_presets:
            if i%(8*8)==0 or i ==0:
                c=0
                b = tk.Label(frame,bg="black", text="X" )
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                r+=1
                c=0
                b = tk.Button(frame,bg="lightblue", text="EXEC " )
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                b = tk.Button(frame,bg="lightblue", text="PAGE " + str(int(i/(8*8))+1) )
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                b = tk.Button(frame,bg="lightblue", text="<NAME>"  )
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                r+=1
                c=0
            i+=1
            v=0
            label = ""
            #if k in PRESETS.label_presets:
            #    label = PRESETS.label_presets[k]
            #    #print([label])

            sdata=PRESETS.val_presets[k]
            BTN="go"
            if "CFG" in sdata:#["BUTTON"] = "GO"
                if "BUTTON" in sdata["CFG"]:
                    BTN = sdata["CFG"]["BUTTON"]
            txt=str(k+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
            b = tk.Button(frame,bg="grey", text=txt,width=8,height=2)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            
            if k not in self.elem_presets:
                self.elem_presets[k] = b
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
        self.refresh_exec()
    def draw_input(self):
        i=0
        c=0
        r=0
        frame = tk.Frame(root2,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Label(frame,bg="black", text="------------------------ ---------------------------------------")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r=0
        
        frame = tk.Frame(root2,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
        
        b = tk.Label(frame, text="send:")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Entry(frame,bg="grey", text="",width=50)
        self.entry = b
        b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT").cb)
        b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","d0:127,fx241:sinus:50:50:10,fx243:cosinus:50:50:10,d201:127,fx201:sinus:50:300:10")
        r+=1
        b = tk.Entry(frame,bg="grey", text="",width=20)
        self.entry2 = b
        b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT2").cb)
        b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT2").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","d1:0:4")
        r+=1
        b = tk.Entry(frame,bg="grey", text="",width=20)
        self.entry3 = b
        b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT3").cb)
        #b.bind("<B1-Motion>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT3").cb)
        b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT3").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","fx:alloff:::")
    def draw_colorpicker(self,xframe):
        import lib.colorpicker as colp

        class _CB():
            def __init__(self):
                self.old_color = (0,0,0)
            def cb(self,event,data):
                cprint("colorpicker CB")
                if "color" in data and self.old_color != data["color"] or event.num==2:
                    self.old_color = data["color"]
                else:
                    return 0
                color = data["color"]

                print("e",event,data)
                print("e",dir(event))#.keys())
                try:
                    print("e.state",event.state)
                except:pass
                set_fade = FADE.val() #fade
                
                if "color" in data and (event.num == 1 or event.num == 3 or event.num==2 or event.state in [256,1024]):
                    cr=None
                    cg=None
                    cb=None
                    if event.num == 1: 
                        set_fade=FADE.val() #fade
                        cr = color[0]
                        cg = color[1]
                        cb = color[2]
                    elif event.num == 3: 
                        cr = color[0]
                        cg = color[1]
                        cb = color[2]
                        set_fade=0
                    elif event.num == 2: 
                        cr= "click"
                        cg= "click"
                        cb= "click"
                    elif event.state == 256:
                        cr = color[0]
                        cg = color[1]
                        cb = color[2]
                        set_fade=0

                    else:
                        set_fade=0


                    if cr is not None:
                        FIXTURES.encoder(fix=0,attr="RED",xval=cr,xfade=set_fade)
                    if cg is not None:
                        FIXTURES.encoder(fix=0,attr="GREEN",xval=cg,xfade=set_fade)
                    if cb is not None:
                        FIXTURES.encoder(fix=0,attr="BLUE",xval=cb,xfade=set_fade)
                    master.refresh_fix()
                     
                    print("PICK COLOR:",data["color"])
        _cb=_CB()
        colp.colorpicker(xframe,width=600,height=100, xcb=_cb.cb)
        return 0

        canvas=tk.Canvas(xframe,width=600,height=100)
        canvas["bg"] = "yellow" #"green"
        canvas.pack()
        # RGB
        x=0
        y=0
        j=0
        d = 20
        for i in range(0,d+1):
            fi = int(i*255/d)
            f = 255-fi
            if i > d/2: 
                pass#break
            color = '#%02x%02x%02x' % (f, fi, fi)
            print( "farbe", i*10, j, f,fi,fi,color)
            r = canvas.create_rectangle(x, y, x+20, y+20, fill=color)
            x+=20
            

    def render(self):
        #Xroot.bind("<Key>",Xevent(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        self.draw_input()

def ScrollFrame(root,width=50,height=100,bd=1):
    #print("ScrollFrame init",width,height)
    aframe=tk.Frame(root,relief=tk.GROOVE)#,width=width,height=height,bd=bd)
    #aframe.place(x=0,y=0)
    aframe.pack(side="left",fill="both",expand=1) #x=0,y=0)

    canvas=tk.Canvas(aframe,width=width-24,height=height)
    canvas["bg"] = "black" #"green"
    bframe=tk.Frame(canvas)#,width=width,height=height)
    bframe["bg"] = "blue"
    scrollbar=tk.Scrollbar(aframe,orient="vertical",command=canvas.yview,width=20)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right",fill="y")
    canvas.pack(side="left",expand=1,fill="both")
    canvas.create_window((0,0),window=bframe,anchor='nw')
    bframe.bind("<Configure>",scroll(canvas).config)
    canvas.bind("<Button>",Event("XXX").event)
    canvas.bind("<Key>",Event("XXX").event)
    canvas.bind("<KeyRelease>",Event("XXX").event)
    return bframe
#frame = ScrollFrame(root)

class GUIHandler():
    def __init__(self):
        pass
    def update(self,fix,attr,args={}):
        print("GUIHandler.update()",fix,attr,args)
        for i,k in enumerate(args):
            v = args[k] 
            #print("GUI-H", i,k,v)
            
class Fixtures(Base):
    def __init__(self):
        super().__init__() 
        #self.load()
        self.fixtures = OrderedDict()
        self.gui = GUIHandler()

        
    def load_patch(self):
        filename="patch"
        d,l = self._load(filename)
        self.fixtures = OrderedDict()
        for i in l:
            sdata = d[i]
            for attr in sdata["ATTRIBUT"]:
                sdata["ATTRIBUT"][attr]["ACTIVE"] = 0
            #print("load",filename,sdata)
            #if "CFG" not in sdata:
            #    sdata["CFG"] = OrderedDict()
            self.fixtures[str(i)] = sdata
        #PRESETS.label_presets = l

    def backup_patch(self):
        filename = "patch"
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        self._backup(filename,data,labels)

    def fx_off(self,fix=None):
        if not fix or fix == "all":
            #self.data.elem_fx_commands[self.attr]["bg"] = "magenta"
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

    def get_dmx(self,fix,attr):
        #cprint("get_dmx",[fix,attr])
        if fix in self.fixtures:
            data = self.fixtures[fix]
            if "DMX" in data:
                DMX = int(data["DMX"])
            else:
                return -1
            if "UNIVERS" in data:
                DMX += (int(data["UNIVERS"])*512)
            adata = self.get_attr(fix,attr)
            #-hier ende 8.2.22
            #cprint("adata",adata,DMX)

            if adata:
                if "NR" in adata:
                    NR = adata["NR"] 
                    if NR:
                        DMX+=NR-1
                    else:
                        return -2
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

    def encoder(self,fix,attr,xval="",xfade=0):
        #cprint("FIXTURES.encoder",fix,attr,xval,xfade,color="yellow")

        if attr == "CLEAR":
            self.clear()
            return 0

        if fix not in self.fixtures:
            jdata=[{"MODE":"---"}]
            ii =0
            jclient_send(jdata)
            for fix in self.fixtures:
                ii+=1
                #cprint(fix,attr,xval)
                data = self.fixtures[fix]
                if attr in data["ATTRIBUT"]:
                    if xval == "click":
                        self.select(fix,attr,mode="on")
                    elif data["ATTRIBUT"][attr]["ACTIVE"]:
                        if fix: # prevent endless recursion
                            self.encoder(fix,attr,xval,xfade)
            jdata=[{"MODE":ii}]
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
        if xval == "+":
            v2+= increment
            jdata["INC"] = increment
            change=1
        elif xval == "-":
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
        out = {} 
        if change:
            data["ATTRIBUT"][attr]["ACTIVE"] = 1
            data["ATTRIBUT"][attr]["VALUE"] = round(v2,4)

            jdata["FADE"] = 0
            if xfade:
                jdata["FADE"] = xfade

            if not modes.val("BLIND"):
                jdata = [jdata]
                print(jdata)
                jclient_send(jdata)
        return v2

    def get_active(self):
        cprint("get_active",self,"get_active")
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


    def select(self,fix=None,attr=None,mode="on"):
        cprint("FIXTURES.select()",fix,attr,mode,color="yellow")
        out = 0

        if fix in self.fixtures:
            data = self.fixtures[fix]
            if attr in data["ATTRIBUT"]:
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
                if attr.endswith("-FINE"):
                    continue
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    out +=1
                    data["ATTRIBUT"][attr]["ACTIVE"] = 0
        return out

class Presets(Base):
    def __init__(self):
        super().__init__() 
        #self.load()
        self._last_copy = None
        self._last_move = None


    def load_presets(self): 
        filename="presets"
        d,l = self._load(filename)
        for i in d:
            sdata = d[i]
            if "CFG" not in sdata:
                sdata["CFG"] = OrderedDict()
            if "FADE" not in sdata["CFG"]:
                sdata["CFG"]["FADE"] = 4
            if "DELAY" not in sdata["CFG"]:
                sdata["CFG"]["DELAY"] = 0
            if "BUTTON" not in sdata["CFG"]:
                sdata["CFG"]["BUTTON"] = "GO"
        self.val_presets = d
        self.label_presets = l

    def check_cfg(self,nr=None):
        cprint("PRESETS.check_cfg()",nr)
        ok = 0
        if nr is not None:
            ok += self._check_cfg(nr)
        else:
            for nr in self.val_presets:
                ok += self._check_cfg(nr)
        return ok

    def _check_cfg(self,nr):
        #cprint("PRESETS._check_cfg()",nr)
        ok=0
        if nr in self.val_presets:
            sdata = self.val_presets[nr]
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
            if ok:
                cprint("REPAIR CFG's",nr,sdata["CFG"],color="red")
        else:
            cprint("nr not in data ",nr,color="red")
        return ok
        
    def backup_presets(self):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        self._backup(filename,data,labels)
        

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
                    print(x,len(x))
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
        if nr:
            if self._last_copy is not None:
                ok = self._copy(self._last_copy,nr,overwrite=overwrite)
                return ok #ok
            else:
                self._last_copy = nr
                cprint("PRESETS.copy START ",color="red")
                return 0
        return 1 # on error reset move
    def _copy(self,nr_from,nr_to,overwrite=1):
        cprint("PRESETS._copy",nr_from,"to",nr_to)
        self.check_cfg(nr_from)
        if self._last_copy is None:
            cprint("PRESETS._copy last nr is None")
            return 0
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
            cprint("PRESETS.copy OK",color="red")
            return 1

    def move(self,nr):
        cprint("PRESETS.move",self._last_copy,"to",nr)
        if nr: 
            last = self._last_copy
            ok= self.copy(nr,overwrite=0)
            if ok and last:
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
        print("rec",self,"rec()",data,arg)
        self.check_cfg(nr)
        self.val_presets[nr] = data
        return 1
           
def test(a1="",a2=""):
    print([a1,a2])


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

def change_dmx(event=""):
    print("change_dmx",event)

class GUI_fader():
    def __init__(self,root,data,title="tilte",width=800):

        self.data = data
        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        r=0
        c=0
        i=1
        self.b = tk.Label(self.frame,bg="lightblue",text="Fixture Editor" )
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        c+=1
        self.b = tk.Label(self.frame,bg="black",text="" ,width=11)
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        c+=1
        self.b = tk.Label(self.frame,bg="lightblue",text="DMX START:")
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        c+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="1", width=11,command=change_dmx)
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        #r+=1

        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        r=0
        c=0
        for j,row in enumerate(data):

            if c % 12 == 0:
                r+=1
                c=0
                frameS = tk.Frame(self.frame,bg="red",width=width)
                frameS.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
                r+=1
                self.b = tk.Label(frameS,bg="black",text="" ,width=11)
                self.b.pack(fill=tk.BOTH, side=tk.TOP)
                r+=1
                self.b = tk.Label(frameS,bg="lightblue",text="PAGE:{}".format(j//12+1) ,width=11)
                self.b.pack(fill=tk.BOTH, side=tk.TOP)
                c=0
            frameS = tk.Frame(self.frame,bg="#005",width=width)
            frameS.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            f = FixtureEditor(j+1)
            self.b = tk.Scale(frameS,bg="lightblue", width=11,from_=255,to=0,command=f.event)
            self.b.pack(fill=tk.Y, side=tk.TOP)

            self.b = tk.Button(frameS,bg="lightblue",text="DMX:{}".format(j+1), width=4,command=test)
            self.b.pack(fill=tk.BOTH, side=tk.TOP)
            self.b = tk.Button(frameS,bg="lightblue",text="PAN", width=4,command=test)
            self.b.pack(fill=tk.BOTH, side=tk.TOP)
            self.b = tk.Button(frameS,bg="lightblue",text="FADE", width=4,command=test)
            self.b.pack(fill=tk.BOTH, side=tk.TOP)
            #self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            c+=1
            i+=1
        self.frame.pack()
class GUI_grid():
    def __init__(self,root,data,title="tilte",width=800):

        self.data = data
        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.LEFT)
        r=0
        c=0
        i=1
        for row in data:

            self.b = tk.Button(self.frame,bg="lightblue", text=row["text"],width=11,height=4)
            #self.b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            c+=1
            if c % 8 == 0:
                r+=1
                c=0
            i+=1
        self.frame.pack()

class BEvent():
    def __init__(self,data,cb):
        self._data = data
        self._cb = cb
    def cb(self,event):
        #print(self,event)
        self._cb(event,self._data)

class GUI_menu():
    def __init__(self,root,data,title="tilte",width=800):
        global tk
        self.data = data

        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.LEFT)
        r=0
        c=0
        i=1
        self.b = tk.Label(self.frame,bg="lightblue", text="MAIN:MENU",width=10,height=1)
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        r+=1
        for row in data:
            #print(i)
            #row = data[i]
            self.b = tk.Button(self.frame,bg="lightblue", text=row["text"],width=10,height=3)
            self.b.bind("<Button>",BEvent({"NR":i,"text":row["text"]},self.callback).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            r+=1
            i+=1
        self.frame.pack()
    def callback(self,event,data={}):
        print("callback543",self,event,data)
        window_manager.top(data["text"])# = WindowManager()

lf_nr = 0
class GUIWindow():
    def __init__(self,title="tilte",master=0,width=100,height=100,left=None,top=None):
        global lf_nr
        if master: 
            self.tk = tkinter.Tk()
            defaultFont = tkinter.font.nametofont("TkDefaultFont")
            print(defaultFont)
            defaultFont.configure(family="FreeSans",
                                   size=10,
                                   weight="bold")
            #self.tk.option_add("*Font", FontBold)
        else:
            self.tk = tkinter.Toplevel()
        #print(title,self.tk.__doc__)

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
    def title(self,title=None):
        if title is None:
            return self.tk.title()
        else:
            return self.tk.title(title)
    def show(self):
        pass
    def mainloop(self):
        try:
            self.tk.mainloop()
        finally:
            self.tk.quit()
    def callback(self,event,data={}):#value=255):
        print()
        print()
        cprint("<GUI>",event,color="yellow")
        cprint("<GUI>",event.state,data,[event.type],color="yellow")
        value = 255
        if "Release" in str(event.type) or str(event.type) == '5' or str(event.type) == '3':
            value = 0
        if "keysym" in dir(event):
            if "Escape" == event.keysym:
                FIXTURES.clear()
                modes.val("ESC",1)
                master.refresh_fix()
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
            elif event.keysym in ["1","2","3","4","5","6","7","8","9","0"]:
                nr = int( event.keysym)
                if nr == 0:
                    nr =10
                cprint("F-KEY",value,nr)
                xfade = 0
                if FADE._is():
                    xfade = 0
                master.preset_go(128-1+nr,xfade=xfade,val=value)
            elif event.keysym in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
                nr = int( event.keysym[1])-1
                cprint("F-KEY",value,nr)
                xfade = 0
                if FADE._is():
                    xfade = 0
                master.preset_go(65-1+nr,xfade=xfade,val=value)
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
        self.nr= 0
        self.first=""
    def new(self,w,name=""):
        if not self.first:
            if name:
                self.first = name
            else:
                self.first = str(self.nr)
            w.tk.attributes('-topmost',True)


        if name:
            self.windows[str(name)] = w
        else:
            self.windows[str(self.nr)] = w
            self.nr+=1
        #w.show()
    def mainloop(self):
        self.windows[self.first].mainloop()
    def top(self,name):
        name = str(name)
        if name in self.windows:
            self.windows[name].tk.attributes('-topmost',True)
            self.windows[name].tk.attributes('-topmost',False)
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


window_manager = WindowManager()

CONSOLE = Console()
PRESETS = Presets()
PRESETS.load_presets()

FIXTURES = Fixtures()
FIXTURES.load_patch()



master = GUI()

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
        master._refresh_fix()
        master._refresh_exec()
    def loop(self,args={}):
        while 1:
            self.refresh()
            time.sleep(0.1)

refresher = Refresher()
thread.start_new_thread(refresher.loop,())

w = GUIWindow("MAIN",master=1,width=100,height=450,left=0,top=65)
data = []
#data.append({"text":"COMMAND"})
data.append({"text":"EXEC"})
data.append({"text":"DIMMER"})
data.append({"text":"FIXTURES"})
f = GUI_menu(w.tk,data)
window_manager.new(w)

name="EXEC"
w = GUIWindow(name,master=0,width=800,height=400,left=110,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
#frame_exe = w.tk
master.draw_preset(w1)#w.tk)
window_manager.new(w,name)

name="DIMMER"
w = GUIWindow(name,master=0,width=800,height=400,left=110,top=65)
w2 = ScrollFrame(w.tk,width=800,height=400)
#frame_dim = w1 # w.tk
#master.draw_dim(w1.tk)
window_manager.new(w,name)

name="FIXTURES"
w = GUIWindow(name,master=0,width=800,height=400,left=110,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
#frame_fix = w1 #w.tk
master.draw_fix(w1,w2)#.tk)
window_manager.new(w,name)


name="FADER"
w = GUIWindow(name,master=0,width=800,height=400,left=110,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
data=[]
for i in range(24):
    data.append({"text"+str(i):"test"})
GUI_fader(w1,data)
#frame_fix = w1 #w.tk
#master.draw_fix(w1,w2)#.tk)

window_manager.new(w,name)

name="ENCODER"
ww = GUIWindow(name,master=0,width=800,height=50,left=110,top=500)
Xroot = ww.tk
w = None
root = tk.Frame(Xroot,bg="black",width="10px")
print("print pack",root)
root.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root3 = tk.Frame(Xroot,bg="black",width="20px")
root3.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root2 = tk.Frame(Xroot,bg="black",width="1px")
master.draw_enc(root2)
root2.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)

name = "COMMAND"
w = GUIWindow(name,master=0,width=350,height=200,left=920,top=65)
master.draw_command(w.tk)
window_manager.new(w,name)


name="PATCH"
w = GUIWindow(name,master=0,width=800,height=400,left=110,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
master.draw_patch(w1)
window_manager.new(w,name)

name="FX"
w = GUIWindow(name,master=0,width=410,height=250,left=920,top=305)
#frame_fx = w.tk
master.draw_fx(w.tk)
window_manager.new(w,name)

#LibreLightDesk
name="COLORPICKER"
w = GUIWindow(name,master=0,width=580,height=100,left=80,top=620)
master.draw_colorpicker(w.tk)
window_manager.new(w,name)


#Xroot = tk.Tk()
#Xroot["bg"] = "black" #white
#Xroot.title( xtitle+" "+str(rnd_id) )
#Xroot.geometry("1024x800+130+65")


master.render()

#w = frame_fix #GUIWindow("OLD",master=0,width=800,height=500,left=130,top=65)
window_manager.new(w,name)
        
try:

    #root.mainloop()
    #tk.mainloop()

    window_manager.mainloop()
    
finally:
    master.exit()

