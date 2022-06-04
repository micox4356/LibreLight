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
rnd_id += " Beta 22.05 "
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
                    cprint("-#-# clear mode",mode,m,value,color="red")
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
jclient = chat.tcp_sender()#port=50001)
import zlib
def jclient_send(data):
    t_start = time.time()
    jtxt = data
    jdatas = []
    for jdata in data:
        if "DMX" in jdata:
            try:
                if int(jdata["DMX"]) >= 1: # ignore DMX lower one
                     jdatas.append(jdata)
                else:
                     cprint("jclient_send, ignore DMX ",jdata["DMX"],color="red")
            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint("-----",color="red")
            
    jtxt = jdatas
    jtxt = json.dumps(jtxt)
    jtxt = jtxt.encode()
    #jtxt = zlib.compress(jtxt)
    jclient.send(b"\00 "+ jtxt +b"\00 ")
    print(round((time.time()-t_start)*1000,4),"milis")
    cprint(round(time.time(),4),color="yellow")

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
fx_prm_move = {"SIZE":100,"SPEED":30,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":25}
fx_prm      = {"SIZE":100,"SPEED":30,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":25}
fx_modes    = ["RED","GREEN","BLUE","MAG","YELLOW","CYAN"]
fx_mo       = ["sinus","on","rnd","bump","bump2","fade","cosinus"]

class FX_handler():
    def __init__():
        pass



def reshape_preset(data ,value=None,xfade=0,flash=0):

    if flash:
        xfade = 0

    out = []
    for row in data:
        cprint("reshape_preset",row)
        line = {}
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


        if row["VALUE"] is not None:
            if value is None: 
                v=row["VALUE"]
                if type(v) is float:
                    line["VALUE"]  = v #round(v,3)
                else:
                    line["VALUE"]  = v


        v = xfade 
        if type( v ) is float:
            line["FADE"] = round(v,4)
        else:
            line["FADE"] = v
        
        if 0:
            cprint("reshape_preset j",line,color="red") 
        out.append(line)
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
 
class Xevent():
    """ global input event Handeler for short cut's ... etc
    """
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


    def setup(self,event):       
        cprint("xevent.SETUP",[self.mode,self.attr],color="red")
        if self.mode == "SETUP":
            if self.attr == "BACKUP\nSHOW":
                self.elem["bg"] = "orange"
                self.elem["text"] = "SAVING..."
                self.elem["bg"] = "red"
                tkinter.Tk.update_idletasks(gui_menu_gui.tk)
                #self.elem["fg"] = "orange"
                self.elem.config(activebackground="orange")
                modes.val(self.attr,1)
                PRESETS.backup_presets()
                FIXTURES.backup_patch()
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
                cb = LOAD_SHOW_AND_RESTAT #(j).cb
                pw = PopupList(name,cb=cb)
                frame = pw.sframe(line1=line1,line2=line2)
                r = _load_show_list(frame,cb=cb)

    
                self.elem["bg"] = "red"
                self.elem.config(activebackground="red")
                #w.tk.attributes('-topmost',False)
            else:
                r=tkinter.messagebox.showwarning(message="{}\nnot implemented".format(self.attr.replace("\n"," ")),parent=None)
        return 1

    def fx_command(self,event):       
        if self.mode == "FX":
            
            if self.attr.startswith("SZ:"):#SIN":
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

                #if event.num == 1:
            elif self.attr == "REC-FX":
                print("ELSE",self.attr)
                modes.val(self.attr,1)

            

            return 0



    def live(self,event):       
        if self.mode == "LIVE":
                    
            if self.attr == "FADE":
                fade = FADE.val()
                print("EVENT CHANGE FADE",fade)
                if fade < 0.01:
                    FADE.val(0.01)
                elif fade > 100.0:
                    pass #fade = 100
                if event.num == 4:
                    fade *= 1.1
                elif event.num == 5:
                    fade /= 1.1
                elif event.num == 1:
                    if FADE._is():
                        FADE.off()# = 0
                        self.data.elem_commands[self.attr]["bg"] = "grey"
                        self.elem.config(activebackground="grey")
                    else:
                        FADE.on()# = 1
                        self.data.elem_commands[self.attr]["bg"] = "green"
                        self.elem.config(activebackground="lightgreen")
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
                fade = FADE.val(fade)
                self.data.elem_commands[self.attr]["text"] = "Fade{:0.2f}".format(fade)
    def command(self,event):       
        if self.mode == "COMMAND":
            
            if self.attr == "CLEAR":
                if event.num == 1:
                    ok = FIXTURES.clear()
                    if ok:
                        master.refresh_fix()
                    modes.val(self.attr,0)


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
    def encoder(self,event):
        if self.mode == "ENCODER":
            cprint("Xevent","ENC",self.fix,self.attr,self.mode)
            #cprint(self.data)
            val=""
            if event.num == 1:
                val ="click"
            elif event.num == 4:
                val ="+"
            elif event.num == 5:
                val ="-"

            if val:
                if self.attr == "DIM" and self.fix == 0 and val == "click":
                    pass    
                else:
                    FIXTURES.encoder(fix=self.fix,attr=self.attr,xval=val)
                
            master.refresh_fix()

            
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
            elif self.mode == "FX":
                self.fx_command(event)
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
                        self.data.preset_go(nr,xfade=0,event=event,val=255)
                        
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
        self._init()

    def _init(self):
        show_name = "GloryCamp2021"
        #show_name = "JMS"
        show_name = "DemoShow"
        #show_name = "Dimmer"
        self.home = os.environ['HOME'] 
        self.show_path0 = self.home +"/LibreLight/"
        self.show_path  = self.show_path0 
        self.show_path1 = self.show_path0 + "/show/"
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

        self._check()
    def _set(self,fname):
        ok= os.path.isdir(self.show_path1+"/"+fname)
        ini = self.show_path0+"init.txt"
        print("SET SHOW NAME",fname,ok,ini)
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
        #self._init()
        #self._check()
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
            #print(jdata)
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
        #self._init()
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


class MiniButton:
    def __init__(self,root,width=72,height=38,text="button"):
        self.text=text
        self.rb = tk.Frame(root, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.bb = tk.Canvas(self.rb, highlightbackground = "black", highlightthickness = 1, bd=1,relief=tk.RAISED)
        self.bb.configure(width=width, height=height)

    def _label(self,text="1\n2\n3\n"):
        z = 0
        self.bb.delete("label")

        for t in text.split("\n"):
            self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag="label")
            z+=1
    def configure(self,**args):
        if "text" in args:
            self.text = args["text"]
            self._label(self.text)
        if "bg" in args:
            #print(dir(self.bb))
            self.bb.configure(bg=args["bg"])
    def config(self,**args):
        self.configure(**args)
    def bind(self,etype="<Button>",cb=None):
        #bb.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
        if cb:
            self.bb.bind(etype,cb)
    def grid(self,row=0, column=0, sticky=""):
        self.bb.pack() #(row=row, column=column, sticky=sticky)
        self.rb.grid(row=row, column=column, sticky=sticky)
        
class ExecButton(MiniButton):
    def __init__(self,root,width=72,height=38,text="button"):
        super().__init__(root,width,height,text)

    def _label(self,text="1\n2\n3\n"):
        z = 0
        self.bb.delete("label")
        txt2 = text
        try:
            text = text.split("\n")[1]
        except:pass
        if "grün" in text.lower() or "green" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="green",tag="label")
        elif "blau" in text.lower() or "blue" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="blue",tag="label")
        elif "rot" in text.lower() or "red" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="red",tag="label")
        elif "orange" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="orange",tag="label")
        elif "weiß" in text.lower() or "white" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="white",tag="label")
        elif "cyan" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="cyan",tag="label")
        elif "gelb" in text.lower() or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="yellow",tag="label")
        elif "mage" in text.lower() or "mage" in text.lower():
            self.l = self.bb.create_rectangle(10,27,20,37,fill="magenta",tag="label")

        if "nebel" in text.lower()  or "smoke" in text.lower() or "haze" in text.lower():
            self.l = self.bb.create_rectangle(10,27,60,37,fill="white",tag="label")
        if "mh " in text.lower() or " mh" in text.lower() :
            self.l = self.bb.create_rectangle(30,27,35,32,fill="black",tag="label")
            self.l = self.bb.create_rectangle(28,34,37,37,fill="black",tag="label")
        if "off" in text.lower(): 
            self.l = self.bb.create_rectangle(50,30,55,35,fill="black",tag="label")
        if "dim" in text.lower() or "front" in text.lower()  or "on" in text.lower(): 
            #self.l = self.bb.create_line(56,30,60,28,fill="black",tag="label")
            self.l = self.bb.create_rectangle(50,30,55,35,fill="white",tag="label")
            #self.l = self.bb.create_line(56,36,58,36,fill="black",tag="label")
        if "circle" in text.lower(): 
            self.l = self.bb.create_oval(30,27,40,37,fill="",tag="label")
        if "pan" in text.lower(): 
            self.l = self.bb.create_line(20,34 ,45,34,fill="black",arrow=tk.BOTH,tag="label")
        if "tilt" in text.lower(): 
            self.l = self.bb.create_line(30,25 ,30,43,fill="black",arrow=tk.BOTH,tag="label")

        text = txt2
        for t in text.split("\n"):
            #print(t)
            self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag="label")
            z+=1
        
class GUI():
    def __init__(self):
        #super().__init__() 
        self.base = Base ()
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
        self.commands =["\n","ESC","CFG-BTN","LABEL","-","DEL","\n"
                ,"SELECT","FLASH","GO","-","MOVE","\n"
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
    def button_refresh(self,name,color,color2=None,text="",fg=None):
        cprint("button_refresh",name,color)
        #if color == "gold":
        #    color2 = "yellow"
        if color2 is None:
            color2 = color
        if text:
            text = "\n"+str(text)
        if name in self.elem_commands:
            self.elem_commands[name]["bg"] = color
            self.elem_commands[name]["text"] = name+ text
            self.elem_commands[name].config(activebackground=color2)
            if fg:
                self.elem_commands[name]["fg"] = fg
                #print(dir(self.elem_commands[name]))
        elif name in self.elem_fx_commands:
            #todo
            self.elem_fx_commands[name]["bg"] = color
            self.elem_fx_commands[name].config(activebackground=color2)
            if fg:
                self.elem_fx_commands[name]["fg"] = fg
                #print(dir(self.elem_fx_commands[name]))
    def btn_cfg(self,nr):
        txt = PRESETS.btn_cfg(nr) 
        txt = tkinter.simpledialog.askstring("CFG-BTN","GO=GO FL=FLASH\nSEL=SELECT EXE:"+str(nr+1),initialvalue=txt)
        if txt:
            PRESETS.btn_cfg(nr,txt)
            self.elem_presets[nr].configure(text= PRESETS.get_btn_txt(nr))
        modes.val("CFG-BTN",0)
    def label(self,nr):
        txt = PRESETS.label(nr) 
        txt = tkinter.simpledialog.askstring("LABEL","EXE:"+str(nr+1),initialvalue=txt)
        if txt:
            PRESETS.label(nr,txt) 
            self.elem_presets[nr].configure(text = PRESETS.get_btn_txt(nr))
        modes.val("LABEL", 0)
    def xcb(self,mode,value=None):
        cprint("MODE CALLBACK",mode,value,color="green",end="")
        #cprint(self,"xcb","MODE CALLBACK",mode,value,color="green")
        if value:
            cprint("===== ON  ======",color="red")
            txt = ""
            if mode == "REC-FX":
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
            if k in PRESETS.val_presets and len(PRESETS.val_presets[k]) :
                sdata = PRESETS.val_presets[k]
                #print("sdata7654",sdata)
                BTN="go"
                if "CFG" in sdata:#["BUTTON"] = "GO"
                    if "BUTTON" in sdata["CFG"]:
                        BTN = sdata["CFG"]["BUTTON"]
                txt=str(k+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
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
                            b.configure(bg = "cyan")
                            b.config(activebackground="#55d4ff")
                else:
                    b.configure(bg="grey")
                    b.config(activebackground="#aaaaaa")

            if "\n" in txt:
                txt = txt.split("\n")[0]

            if ifval:
                if "SEL" in txt:
                    b.configure(fg= "black")
                    b.configure(bg = "#55f")
                    b.config(activebackground="#6666ff")

                elif "ON" in txt:
                    b.configure(bg = "#ffcc00")
                    b.configure(fg = "#00c")

                elif "GO" in txt:
                    b.configure(fg="black")
                elif "FL" in txt:
                    b.configure(fg = "#7f00ff")
            else: 
                b.configure(bg="grey")
                b.configure(fg="black")


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
        #vcmd = reshape_preset( rdata ,value,[],xfade=xfade,fx=1) 
        vcmd = reshape_preset( rdata ,value,xfade=xfade) 

        cmd = []

        for i,v in enumerate(fcmd):
            print("go",i,v)
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
            cmd.append(vcmd[i])

        if cmd and not modes.val("BLIND"):
            jclient_send(cmd)

    def render(self):
        #Xroot.bind("<Key>",Xevent(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        #self.draw_input()
        pass
        


def draw_sub_dim(gui,fix,data,c=0,r=0,frame=None):
    i=0
    if frame is None:
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

    if fix not in gui.elem_attr:
        gui.elem_attr[fix] = {}
        
    for attr in data["ATTRIBUT"]:
        
        if attr not in gui.all_attr:
            gui.all_attr.append(attr)
        if attr not in gui.elem_attr[fix]:
            gui.elem_attr[fix][attr] = []
        if attr.endswith("-FINE"):
            continue
        v= data["ATTRIBUT"][attr]["VALUE"]
        b = tk.Button(frame,bg="lightblue", text=""+str(fix),width=3,anchor="w")
        b.config(padx=1)
        b.bind("<Button>",Xevent(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="lightblue", text=data["NAME"],width=10,anchor="w")
        b.config(padx=1)
        b.bind("<Button>",Xevent(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="grey", text=str(round(v,2)),width=10,anchor="w")
        b.config(padx=1)
        gui.elem_attr[fix][attr] = b
        b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=12:
            c=0
            r+=1
    return c,r




def draw_patch(gui,yframe):
    #print(dir(yframe))
    #yframe.clear()
    for widget in yframe.winfo_children():
        widget.destroy()

    xframe = tk.Frame(yframe,bg="black")
    xframe.pack()
    def yview(event):
        print("yevent",event)
        yyy=20.1
        xframe.yview_moveto(yyy)

    i=0
    c=0
    r=0
    b = tk.Button(xframe,bg="lightblue", text="ID",width=6,anchor="e")
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Button(xframe,bg="lightblue", text="NAME",width=14,anchor="w")
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Button(xframe,bg="#ddd", text="TYPE",width=3)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Button(xframe,bg="#ddd", text="Uni",width=1)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Button(xframe,bg="#ddd", text="DMX",width=1)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Button(xframe,bg="#ddd", text="CH's",width=1)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1

    c=0
    r+=1
    for fix in FIXTURES.fixtures:
        i+=1
        data = FIXTURES.fixtures[fix]
                        
        b = tk.Button(xframe,bg="lightblue", text=""+str(fix),width=6,anchor="e")
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(xframe,bg="lightblue", text=data["NAME"],width=14,anchor="w")
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if len(data["ATTRIBUT"]) == 1:
            b = tk.Button(xframe,bg="#ddd", text="DIMMER",width=8,anchor="w")
        elif "PAN" in data["ATTRIBUT"] or  "TILT" in data["ATTRIBUT"] :
            b = tk.Button(xframe,bg="#ddd", text="MOVER",width=8,anchor="w")
        else:
            b = tk.Button(xframe,bg="#ddd", text="",width=8,anchor="w")
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(xframe,bg="#ddd", text="EDIT",width=3)
        b.bind("<Button>",Xevent(fix=fix,mode="SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(xframe,bg="#ddd", text="[ ][x]",width=1)
        b.bind("<Button>",Xevent(fix=fix,mode="SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        #r+=1

        start_c=3
        c=start_c
        if fix not in gui.elem_attr:
            gui.elem_attr[fix] = {}
            
        patch = ["UNIVERS","DMX"]
        for k in patch:
            v=data[k]
            #b = tk.Button(xframe,bg="grey", text=str(k)+' '+str(v),width=8)
            b = tk.Button(xframe,bg="grey", text=str(v),width=2)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=start_c
                r+=1
        b = tk.Button(xframe,bg="grey", text="{}".format(len(data["ATTRIBUT"])),width=3)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(xframe,bg="#aaa", text="{:03}-{:03}".format(data["DMX"],len(data["ATTRIBUT"])+(data["DMX"])-1),width=6,anchor="w")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        if 0: #for attr in data["ATTRIBUT"]:
            
            if attr not in gui.all_attr:
                gui.all_attr.append(attr)
            if attr not in gui.elem_attr[fix]:
                gui.elem_attr[fix][attr] = []
            if attr.endswith("-FINE"):
                continue
            v= data["ATTRIBUT"][attr]["VALUE"]
            
            b = tk.Button(xframe,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
            #gui.elem_attr[fix][attr] = b
            #b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=start_c
                r+=1
        c=0
        r+=1
           


def draw_fix(gui,xframe,yframe=None):
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
            c,r=draw_sub_dim(gui,fix,data,c=c,r=r,frame=dim_frame)
        else:
            if not dim_end:
                dim_end=1
                c=0
                r=0
            #gui._draw_fix(fix,data,root=fix_frame)
            frame = fix_frame
        
            b = tk.Button(frame,bg="lightblue", text="ID:"+str(fix),width=6,anchor="w")
            b.bind("<Button>",Xevent(fix=fix,mode="SELECT",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="#55f", text=data["NAME"],width=10,anchor="w")
            b.bind("<Button>",Xevent(fix=fix,attr="ALL",mode="ENCODER",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            #r+=1
            start_c=3
            c=start_c
            if fix not in gui.elem_attr:
                gui.elem_attr[fix] = {}
                
            for attr in data["ATTRIBUT"]:
                
                if attr.endswith("-FINE"):
                    continue
                if attr not in gui.all_attr:
                    gui.all_attr.append(attr)
                if attr not in gui.elem_attr[fix]:
                    gui.elem_attr[fix][attr] = ["line1348",fix,attr]
                v= data["ATTRIBUT"][attr]["VALUE"]
                
                b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
                gui.elem_attr[fix][attr] = b
                b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                if c >=8:
                    c=start_c
                    r+=1
            c=0
            r+=1
            



def draw_enc(gui,xframe):

    for widget in xframe.winfo_children():
        widget.destroy()

    root2 = xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(xframe,bg="black")
    frame.pack( side=tk.LEFT,expand=0,fill="both")

    
    b = tk.Button(frame,bg="lightblue", text="ENCODER",width=6)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    #for attr in ["xx"]*23: # gui.all_attr:
    eat = gui.all_attr

    if len(eat) < 23:
        for i in range(23-len(eat)):
            eat.append("")
    for attr in eat:
        if attr.endswith("-FINE"):
            continue
        v=0
        
        b = tk.Button(frame,bg="orange", text=str(attr)+'',width=6)
        if attr == "DIM":
            b = tk.Button(frame,bg="yellow", text=str(attr)+'',width=6)
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=attr,data=gui,mode="ENCODER").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=8:
            c=0
            r+=1



def draw_fx(gui,xframe):
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
    for comm in gui.fx_commands:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        if "PAN/TILT" in comm: 
            b = tk.Button(frame,bg="grey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.elem_fx_commands:
            comm = comm.replace("\n","")
            gui.elem_fx_commands[comm] = b
            gui.val_fx_commands[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="FX").cb)
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




def draw_setup(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    #b = tk.Button(frame,bg="lightblue", text="SETUP",width=6)
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #r+=1
    c+=1
    for comm in ["BACKUP\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        if comm == "BACKUP\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        elif comm == "LOAD\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="grey", text=str(comm),width=6,height=2)
        if comm not in gui.elem_commands:
            gui.elem_commands[comm] = b
            gui.val_commands[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="SETUP").cb)

        if comm == "BS:":
            b["text"] = "BS:{}".format(fx_prm["BASE"])
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=5:
            c=0
            r+=1



def draw_live(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    c+=1
    for comm in ["FADE","DELAY:0.0","PAN/TILT\nFADE:x.x","PAN/TILT\nDELAY:0.0"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.elem_commands:
            gui.elem_commands[comm] = b
            gui.val_commands[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="LIVE").cb)
        if "FADE" == comm:
            b["text"] = "FADE:2.0"
        if "FADE" in comm:
            b["bg"] = "green"
            b.config(activebackground="lightgreen")
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=5:
            c=0
            r+=1

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

    def cb(self,event=None):
        if not self.fname:
            return 0
        if self.base.show_name == self.fname:
            cprint("filename is the same",self.fname)
            return 0
        self.base._set(self.fname)
        #base = Base()
        #show_path = base.show_path1 + base.show_name
        print("LOAD SHOW:",event,self.fname)
        if 0: #disable load show ... error gui[elem] ..
            LOAD_SHOW()
            refresher.reset() # = Refresher()
            master._refresh_fix()
            master._refresh_exec()
            draw_patch(master,main_preset_frame)
        #os.system('''kill "$(ps aux | grep -i  'python3 LibreLightDesk.py' | head -n1 | awk '{print $2}')"''')
        import os,sys

        print(sys.executable, os.path.abspath(__file__), *sys.argv)
        #input()
        #ok /usr/bin/python3 /opt/LibreLight/Xdesk/_LibreLightDesk.py _LibreLightDesk.py
        #err /opt/LibreLight/Xdesk/_LibreLightDesk.py /opt/LibreLight/Xdesk/_LibreLightDesk.py _LibreLightDesk.py

        #os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        os.execl("/usr/bin/python3", "/opt/LibreLight/Xdesk/_LibreLightDesk.py", "_LibreLightDesk.py")
        sys.exit()
                
class PopupList():
    def __init__(self,name="<NAME>",master=0,width=400,height=450,exit=1,left=400,top=100,cb=None,bg="black"):
        self.name = name
        self.frame = None
        self.bg=bg
        self.cb = cb
        if cb is None: 
            cb = DummyCallback #("load_show_list.cb")
        w = GUIWindow(self.name,master=master,width=width,height=height,exit=exit,left=left,top=top,cb=cb)
        self.w = w

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
        frame.pack(side="left") #fill=tk.BOTH,expand=1, side=tk.TOP)
        self.frame = frame
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

def draw_command(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    # b = tk.Button(frame,bg="lightblue", text="COMM.",width=6)
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #r+=1
    c+=1
    for comm in gui.commands:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.elem_commands:
            gui.elem_commands[comm] = b
            gui.val_commands[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="COMMAND").cb)
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


def draw_preset(gui,xframe):

    i=0
    c=0
    r=0
    root = xframe
    
    frame = tk.Frame(root,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    i=0
    for k in PRESETS.val_presets:
        if i%(10*8)==0 or i ==0:
            c=0
            b = tk.Label(frame,bg="black", text="" )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            r+=1
            c=0
            b = tk.Button(frame,bg="lightblue", text="EXEC " )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="lightblue", text="BANK " + str(int(i/(8*8))+1) )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="lightblue", text="NAME"  )
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


        #bb = tk.Frame(frame, highlightbackground = "red", highlightthickness = 1, bd=0)
        #bb = tk.Canvas(frame, highlightbackground = "black", highlightthickness = 1, bd=1)
        #bb.configure(width=70, height=38)
        txt=str(k+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label

        b = ExecButton(frame,text=txt)

        #b = tk.Button(bb,bg="grey", text=txt,width=7,height=2)
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
        b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
        
        if k not in gui.elem_presets:
            gui.elem_presets[k] = b
        #b.pack(expand=1)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=10:
            c=0
            r+=1
    gui.refresh_exec()


def draw_input(gui):
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
    gui.entry = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","d0:127,fx241:sinus:50:50:10,fx243:cosinus:50:50:10,d201:127,fx201:sinus:50:300:10")
    r+=1
    b = tk.Entry(frame,bg="grey", text="",width=20)
    gui.entry2 = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","d1:0:4")
    r+=1
    b = tk.Entry(frame,bg="grey", text="",width=20)
    gui.entry3 = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    #b.bind("<B1-Motion>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","fx:alloff:::")


def draw_colorpicker(gui,xframe):
    import lib.colorpicker as colp

    class _CB():
        def __init__(gui):
            gui.old_color = (0,0,0)
        def cb(gui,event,data):
            cprint("colorpicker CB")
            if "color" in data and gui.old_color != data["color"] or event.num==2:
                gui.old_color = data["color"]
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
        

class TableFrame():
    def __init__(self,root, width=50,height=100,bd=1):
        self.root=root
        self.a = _TableFrame(self.root)
        f=self.a.HFrame()
        f=self.a.Sframe(f, width=width,height=height,bd=bd)
        self.a.draw([["A","11"],["B",4],["E",""],["R","R"],["Z","Z"],["U","U"]])

        self.b = _TableFrame(self.root) #äself.root)
        b=self.b.HFrame()
        b=self.b.Sframe(b, width=width,height=height,bd=bd)
        self.b.draw([["AA","1a1"],["BBB",114],["EE","22"],["RRR","RRR"],["TTZ","TTZ"],["ZZU","ZZU"]])

        self.c = _TableFrame(self.root)
        c=self.c.HFrame()
        c=self.c.Sframe(c, width=width,height=height,bd=bd)
        self.c.draw([["A","11"],["B",4],["E",""],["R","R"],["Z","Z"],["U","U"]][::-1])

        self.bframe=None
    def draw(self,data=[1,2],head=[],config=[]):
        pass

class _TableFrame():
    def __init__(self,main):
        self.main = main
        self.frame=tk.Frame(self.main,relief=tk.GROOVE,bg="yellow")#,width=width,height=height,bd=bd)
        self.frame.pack(side="top",fill="x",expand=1) #x=0,y=0)

        self.hframe=tk.Frame(self.frame,relief=tk.GROOVE,bg="yellow")#,width=width,height=height,bd=bd)
        self.hframe.pack(side="top",fill="x",expand=0) #x=0,y=0)
        

        self.aframe=tk.Frame(self.main,relief=tk.GROOVE)#,width=width,height=height,bd=bd)
        #aframe.place(x=0,y=0)
        self.aframe.pack(side="top",fill="both",expand=1) #x=0,y=0)

        self.canvas=tk.Canvas(self.aframe,width=100-24,height=150)
        self.canvas["bg"] = "blue" #black" #"green"
        self.bframe=tk.Frame(self.canvas)#,width=width,height=height)
        self.bframe["bg"] = "blue"
        self.scrollbar=tk.Scrollbar(self.aframe,orient="vertical",command=self.canvas.yview,width=20)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left",expand=1,fill="both")
        self.canvas.create_window((0,0),window=self.bframe,anchor='nw')
        self.bframe.bind("<Configure>",scroll(self.canvas).config)
        self.canvas.bind("<Button>",Event("XXX").event)
        self.canvas.bind("<Key>",Event("XXX").event)
        self.canvas.bind("<KeyRelease>",Event("XXX").event)

        
        #self.bframe=tk.Frame(self.frame,relief=tk.GROOVE,bg="magenta")#,width=width,height=height,bd=bd)
        #self.bframe.pack(side="top",fill="both",expand=1) #x=0,y=0)
        #self.HFrame()
    def HFrame(self,main=None):  
        self.e = tk.Label(self.hframe,text="Filter:")
        self.e.pack(side="left")
        self.e = tk.Entry(self.hframe)
        self.e.pack(side="left")
    def Sframe(self,main=None, **args):  
        pass

    def draw(self,data=[1,2],head=[],config=[]):
        yframe = self.bframe
        if 1: 
            xframe = tk.Frame(yframe,bg="black")
            xframe.pack(side="top", expand=1,fill="both")
            def yview(event):
                print("yevent",event)
                yyy=20.1
                xframe.yview_moveto(yyy)

            i=0
            c=0
            r=0
            b = tk.Button(xframe,bg="lightblue", text="ID",width=6,anchor="e")
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="lightblue", text="NAME",width=14,anchor="w")
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="TYPE",width=3)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="Uni",width=1)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="DMX",width=1)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="CH's",width=1)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            c=0
            r+=1

            for i,p in enumerate(data):
                for j in data[i]:
                    b = tk.Button(xframe,bg="lightblue", text=""+str(j),width=6,anchor="e")
                    b.grid(row=r, column=c, sticky=tk.W+tk.E)
                    c+=1
                c=0
                r+=1
                    
        return self.bframe


def ScrollFrame(root,width=50,height=100,bd=1,bg="black"):
    #print("ScrollFrame init",width,height)
    aframe=tk.Frame(root,relief=tk.GROOVE)#,width=width,height=height,bd=bd)
    #aframe.place(x=0,y=0)
    aframe.pack(side="left",fill="both",expand=1) #x=0,y=0)

    canvas=tk.Canvas(aframe,width=width-24,height=height)
    if bg == "":
        bg="orange"
    canvas["bg"] = bg # "black" #"green"
    bframe=tk.Frame(canvas,width=width,height=height)
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
            print("++++")
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

                print(k,j)#,sdata)
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

    def backup_patch(self):
        filename = "patch"
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        #self.base._init()
        self.base._backup(filename,data,labels)

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

    def encoder(self,fix,attr,xval="",xfade=0):
        cprint("FIXTURES.encoder",fix,attr,xval,xfade,color="yellow")

        if attr == "CLEAR":
            self.clear()
            return 0

        if attr == "ALL":
            x=self.select(fix,attr,mode="toggle")
            return x

        if fix not in self.fixtures:
            jdata=[{"MODE":"---"}]
            ii =0
            jclient_send(jdata)
            for fix in self.fixtures:
                ii+=1
                #cprint(fix,attr,xval)
                data = self.fixtures[fix]
                if "-FINE" in attr.upper():
                    continue
                elif attr == "ALL":
                    pass

                elif (attr in data["ATTRIBUT"] or attr == "ALL") and "-FINE" not in attr.upper()   :
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
                #print(jdata)
                jclient_send(jdata)
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

class Presets():
    def __init__(self):
        #super().__init__() 
        self.base = Base()
        #self.load()
        self._last_copy = None
        self._last_move = None


    def load_presets(self): 
        #self._load()
        filename="presets"
        #self.base._init()
        d,l = self.base._load(filename)
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
        ok=0
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
            cprint("REPAIR CFG's",ok,sdata["CFG"],color="red")
        return ok
        
    def backup_presets(self):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        #self.base._init()
        self.base._backup(filename,data,labels)
        

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

class BufferVar():
    def __init__(self,elem):
        self.elem = elem
    def change_dmx(self,event=""):
        nr=1
        txt=""
        txt = tkinter.simpledialog.askstring("FADER-DMX-START",""+str(nr+1),initialvalue=txt)
        print("change_dmx",[event,self])

class ELEM_FADER():
    def __init__(self,frame,nr,**args):
        self.frame = frame
        self.nr= nr
        self.id=nr
        self.elem = []
        width=11
        frameS = tk.Frame(self.frame,bg="#005",width=width)
        frameS.pack(fill=tk.Y, side=tk.LEFT)
        self.frame=frameS

    def event(self,a1="",a2=""):
        print(self,"event",[self.nr,a1,a2])
        j=[]
        jdata = {'VALUE': int(a1), 'args': [] , 'FADE': 0,'DMX': str(self.nr)}
        j.append(jdata)
        jclient_send(j)
    def set_nr(self,nr,btn=1):
        self.nr=nr
        try:
            self.elem[btn]["text"]="{} D:{}".format(self.id,nr)
        except:pass

    def set_attr(self,_event=None):
        txt= self.attr["text"]
        txt = tkinter.simpledialog.askstring("ATTR","set attr:",initialvalue=txt)
        
        self._set_attr(txt)
    def _set_attr(self,txt=""):
        if type(txt) is str:
            self.attr["text"] = "{}".format(txt)
            print("_set_attr",[self])

    def set_mode(self,_event=None):
        txt= self.mode["text"]
        txt = tkinter.simpledialog.askstring("MODE S/F:","SWITCH or FADE",initialvalue=txt)

        w = GUIWindow("config",master=1,width=200,height=140,left=L1,top=TOP)
        #w.pack()
        self._set_mode(txt)
    def _set_mode(self,txt=""):
        if type(txt) is str:
            self.mode["text"] = "{}".format(txt[0].upper())
            print("_set_attr",[self])
    def _refresh(self):
        pass
    def pack(self,**args):
        width=11
        r=0
        c=0
        j=0
        font8 = ("FreeSans",8)
        frameS=self.frame
        self.b = tk.Scale(frameS,bg="lightblue", width=11,from_=255,to=0,command=self.event)
        self.b.pack(fill=tk.Y, side=tk.TOP)
        self.elem.append(self.b)

        self.b = tk.Button(frameS,bg="lightblue",text="{}".format(self.nr), width=4,command=test,font=font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)
        self.b = tk.Button(frameS,bg="lightblue",text="", width=5,command=self.set_attr,font=font8 )
        self.attr=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)
        f = tk.Frame(frameS)
        #f.pack()
        self.b = tk.Button(f,bg="lightblue",text="<+", width=1,command=self.set_mode,font=font8 )
        self.mode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        self.elem.append(self.b)

        self.b = tk.Button(frameS,bg="lightblue",text="F", width=4,command=self.set_mode,font=font8 )
        self.mode=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        self.elem.append(self.b)

        self.b = tk.Button(f,bg="lightblue",text="+>", width=1,command=self.set_mode,font=font8 )
        self.mode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        self.elem.append(self.b)

        self.b = tk.Label(frameS,bg="black",text="", width=4,font=font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)


class GUI_FaderLayout():
    def __init__(self,root,data,title="tilte",width=800):
        #xfont = tk.font.Font(family="FreeSans", size=5, weight="bold")
        font8 = ("FreeSans",8)
        r=0
        c=0
        i=1
        self.elem=[]
        self.header=[]
        self.data = data
        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)

        self.b = tk.Label(self.frame,bg="#fff",text="Fixture Editor") #,font=font8 )
        self.b.pack(fill=None, side=tk.LEFT)
        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        self.b = tk.Label(self.frame,bg="#ddd",text="NAME:")
        self.b.pack(fill=None, side=tk.LEFT)
        self.b = tk.Button(self.frame,bg="lightblue",text="MAC-500", width=11)
        self.name=self.b
        self.b["command"] = self.set_name
        self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="lightblue",text="UNIV:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        self.entry=self.b
        self.b["command"] = self.event
        self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="lightblue",text="DMX:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        self.entry=self.b
        self.b["command"] = self.event
        self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#ddd",text="TYPE:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="LIST", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list
        self.b.pack( side=tk.LEFT)
        
        self.b = tk.Label(self.frame,bg="black",text="") # spacer
        self.b.pack(fill=tk.Y, side=tk.LEFT)

        self.frame = tk.Frame(root,bg="magenta",width=width,border=2) # fader frame
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        r=0
        c=0
        pb=12
        self.pb=pb
        for j,row in enumerate(data):
            if c % pb == 0 or c==0:
                h=hex(j*10)[2:].rjust(2,"0")
                frameS = tk.Frame(self.frame,bg="#000",width=width,border=2)
                frameS.pack(fill=tk.BOTH, side=tk.TOP)
                p=j//pb+1
                txt="BANK:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
                self.b = tk.Label(frameS,bg="lightblue",text=txt,width=15,font=font8 )
                self.header.append(self.b)

                self.b.pack(fill=None, side=tk.LEFT)
                self.b = tk.Label(frameS,bg="black",text="" ,width=11,font=font8 )
                self.b.pack(fill=tk.BOTH, side=tk.LEFT)

                frameS = tk.Frame(self.frame,bg="#a000{}".format(h),width=width,border=2)
                c=0
            #print(frameS)
            e= ELEM_FADER(frameS,nr=j+1)
            e.pack()
            self.elem.append(e)
            frameS.pack(fill=tk.X, side=tk.TOP)
            c+=1
            i+=1
        self.frame.pack()
    def set_name(self,_event=None):
        txt = self.name["text"]
        txt = tkinter.simpledialog.askstring("FIXTURE NAME:","NAME:",initialvalue=txt)
        self.name["text"] = "{}".format(txt)
        print("change_dmx",[_event,self])


    def open_fixture_list(self):
        name = "FIXTURE-LIB"
        line1="Fixture Library"
        line2="CHOOS to EDIT >> DEMO MODUS"
        cb = LOAD_FIXTURE
        #cb.master=self
        pw = PopupList(name,cb=cb,left=800,bg="red")
        frame = pw.sframe(line1=line1,line2=line2)
        r=_load_fixture_list(frame,cb=cb,master=self,bg="red")


        #self.elem["bg"] = "red"
        #self.elem.config(activebackground="red")
        #w.tk.attributes('-topmost',False)

    def load_EMPTY(self,_event=None,attr=[]):
        #attr = [,"RED","GREEN","BLUE"]
        #mode = ["F","F","F","F"]
        self._load_mh(None)#,attr,mode)
    def load_DIM(self,_event=None,attr=[]):
        attr = ["DIM"]
        mode = ["F"]
        self._load_fix(None,attr,mode)
    def load_LED(self,_event=None,attr=[]):
        attr = ["DIM","RED","GREEN","BLUE"]
        mode = ["F","F","F","F"]
        self._load_fix(None,attr,mode)
    def load_MH(self,_event=None,attr=[]):
        attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO"]
        mode = ["F","F","F","F","S","F","F","F","F","S"]
        self._load_fix(None,attr,mode)
    def load_MH2(self,_event=None,attr=[]):
        attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO","G-ROT","PRISM","P-ROT","ZOOM","CONTR"]
        mode = ["F","F","F","F","S","F","F","F","F","S","S","S","S","F","S"]
        self._load_fix(None,attr,mode)

    def _load_fix(self,_event=None,attr=[],mode=[]):
        print("load_fixture",[_event,self])
        #for i,e in enumerate(self.elem):
        for i,e in enumerate(self.elem):
            #print(self,"event",_event,e)
            print("event",_event,e)
            e._set_attr( "---")
            if len(attr) > i:
                e._set_attr( attr[i])
            e._set_mode( "---")
            if len(mode) > i:
                e._set_mode( mode[i])

    def event(self,_event=None):
        nr=1
        txt="dd"
        txt= self.entry["text"]
        txt = tkinter.simpledialog.askstring("FADER-DMX-START",""+str(nr+1),initialvalue=txt)
        try:
            nr = int(txt)
        except TypeError:
            print("--- abort ---")
            return 0
        self.entry["text"] = "{}".format(nr)
        print("change_dmx",[_event,self])
        for i,e in enumerate(self.elem):
            #print(self,"event",_event,e)
            print("event",_event,e)
            e.set_nr(nr+i)

        pb=self.pb
        for j,e in enumerate(self.header):
            p=j+1
            #p=nr/pb
            txt="BANK:{} {}-{}".format(p,p*pb-pb+nr,p*pb+nr-1) 
            print("---",j,txt,e)
            e["text"] = txt
            

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
        self.data2 = {}
        self.frame = tk.Frame(root,bg="black",width=width)
        self.frame.pack(fill=tk.BOTH, side=tk.LEFT)
        r=0
        c=0
        i=1
        self.b = tk.Label(self.frame,bg="lightblue", text="MAIN:MENU",width=8,height=1)
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        r+=1
        for row in data:
            #print(i)
            #row = data[i]
            self.b = tk.Button(self.frame,bg="lightgrey", text=row["text"],width=8,height=2)
            self.b.bind("<Button>",BEvent({"NR":i,"text":row["text"]},self.callback).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            row["elem"] = self.b
            self.data2[row["text"]] = row
            r+=1
            i+=1
        self.frame.pack()
    def callback(self,event,data={}):
        print("callback543",self,event,data)
        window_manager.top(data["text"])# = WindowManager()
    def update(self,button,text):
        #print(self,button,text)
        for k in self.data2:
            v=self.data2[k]
            #print(self,k,v)
            if button == k:
                v["elem"]["text"] = k+"\n"+text
    def config(self,button,attr,value):
        print(self,button,attr,value)
        for k in self.data2:
            v=self.data2[k]
            #print(self,k,v)
            if button == k:
                #print(dir(v["elem"]))
                if attr == "bg":
                    if value == "":
                        value = "lightgrey"
                    v["elem"][attr] = str(value)
                if attr == "activebackground":
                    if value == "":
                        value = "lightgrey"
                    v["elem"][attr] = str(value)

lf_nr = 0
        
from tkinter import PhotoImage 

class GUIWindow():
    def __init__(self,title="tilte",master=0,width=100,height=100,left=None,top=None,exit=0,cb=None):
        global lf_nr
        #ico_path="/opt/LibreLight/Xdesk/icon/"
        ico_path="./icon/"
        self.cb = cb
        if master: 
            self.tk = tkinter.Tk()
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
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            
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
    def close_app_win(self,event=None):
        print("close_app_win",self,event)
        if exit:
            #self.tk.quit()
            self.tk.destroy()
            #for i in dir(self.tk):
            #    print("i",i)
        try:
            self.cb("<exit>").cb()
        except Exception as e:
            print("EXCETPION close_app",e)

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
            elif event.keysym in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
                nr = int( event.keysym[1])
                nr = nr-1+81  
                cprint("F-KEY",value,nr)
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

FIXTURES = Fixtures()

def LOAD_SHOW():
    PRESETS.load_presets()
    FIXTURES.load_patch()
    #draw_enc(gui,root2)
    #master._refresh_fix()
    #master._refresh_exec()
LOAD_SHOW()

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
            time.sleep(0.2)

refresher = Refresher()
thread.start_new_thread(refresher.loop,())

TOP = 15
L1 = 95
L2 = 920 
W1 = 810
H1 = 550
HTB = 23 # hight of the titlebar from window manager

w = GUIWindow("MAIN",master=1,width=85,height=H1//2,left=0,top=TOP)
gui_menu_gui = w
data = []
#data.append({"text":"COMMAND"})
data.append({"text":"PATCH"})
data.append({"text":"DIMMER"})
data.append({"text":"FIXTURES"})
data.append({"text":"EXEC"})
gui_menu = GUI_menu(w.tk,data)

window_manager.new(w)

name="EXEC"
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
w1 = ScrollFrame(w.tk,width=W1,height=H1)
#frame_exe = w.tk
draw_preset(master,w1)#w.tk)
window_manager.new(w,name)

name="DIMMER"
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
w2 = ScrollFrame(w.tk,width=W1,height=H1)
#frame_dim = w1 # w.tk
#master.draw_dim(w1.tk)
window_manager.new(w,name)

name="FIXTURES"
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
w1 = ScrollFrame(w.tk,width=W1,height=H1)
#frame_fix = w1 #w.tk
draw_fix(master,w1,w2)#.tk)
window_manager.new(w,name)


name="FIXTURE-EDITOR"
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
w1 = ScrollFrame(w.tk,width=W1,height=H1)
data=[]
for i in range(24+12):
    data.append({"text"+str(i):"test"})
GUI_FaderLayout(w1,data)
#frame_fix = w1 #w.tk
#master.draw_fix(w1,w2)#.tk)

window_manager.new(w,name)

name="ENCODER"
ww = GUIWindow(name,master=0,width=600,height=100,left=720,top=HTB*2+TOP+H1)
Xroot = ww.tk
w = None
root = tk.Frame(Xroot,bg="black",width="10px")
print("print pack",root)
root.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root3 = tk.Frame(Xroot,bg="black",width="20px")
root3.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root2 = tk.Frame(Xroot,bg="black",width="1px")
draw_enc(master,root2)
root2.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)

name = "SETUP"
w = GUIWindow(name,master=0,width=415,height=42,left=10+L1+W1,top=TOP)
w.tk.title("SETUP   SHOW:"+master.base.show_name)
draw_setup(master,w.tk)
window_manager.new(w,name)

name = "COMMAND"
w = GUIWindow(name,master=0,width=415,height=130,left=10+L1+W1,top=98)
draw_command(master,w.tk)
window_manager.new(w,name)

name = "LIVE"
w = GUIWindow(name,master=0,width=415,height=42,left=10+L1+W1,top=255)
draw_live(master,w.tk)
window_manager.new(w,name)

name="FX"
w = GUIWindow(name,master=0,width=415,height=250,left=10+L1+W1,top=328)
#frame_fx = w.tk
draw_fx(master,w.tk)
window_manager.new(w,name)


name="PATCH"
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
w1 = ScrollFrame(w.tk,width=W1,height=H1)
main_preset_frame = w1
draw_patch(master,main_preset_frame)
window_manager.new(w,name)

#LibreLightDesk
name="COLORPICKER"
w = GUIWindow(name,master=0,width=580,height=100,left=L1,top=20+HTB*2+H1)
draw_colorpicker(master,w.tk)
window_manager.new(w,name)

name="TableA"
w# = GUIWindow(name,master=0,width=580,height=100,left=80,top=620)
w = GUIWindow(name,master=0,width=W1,height=H1,left=L1,top=TOP)
x=TableFrame(root=w.tk)#,left=80,top=620)
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
#w = frame_fix #GUIWindow("OLD",master=0,width=W1,height=500,left=130,top=TOP)
window_manager.new(w,name)

try:
    #root.mainloop()
    #tk.mainloop()
    window_manager.mainloop()
    
finally:
    master.exit()

