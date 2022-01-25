#! /usr/bin/python
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
import random
rnd_id = str(random.randint(1000,9000))
rnd_id += " Beta 22.01"
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

import _thread as thread
import traceback

import tkinter
import tkinter as tk
from tkinter import font


import lib.chat as chat
import lib.motion as motion

from collections import OrderedDict

show_name = "GloryCamp2021"
#show_name = "JMS"
#show_name = "Dimmer"


CUES    = OrderedDict()
groups  = OrderedDict()

class Modes():
    def __init__(self):
        self.modes = {}
        self.__cfg = {}
        self.__cd = None
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
        self.__check(mode)

        if mode == "CLEAR":
            self.modes["STORE"] = 0
            self.callback("STORE")
        self.modes[mode] = value
        return value
    def callback(self,mode):
        if self.__cb is not None and mode in self.modes:
            value = self.modes[mode]
            self.__cb(mode=mode,value=value)

modes = Modes()
modes.modes["BLIND"] = 0
modes.modes["STORE "] = 0
modes.modes["FLASH"] = 0
modes.modes["STONY_FX"] = 0
modes.modes["SELECT"] = 0
modes.modes["ACTIVATE"] = 0
modes.modes["CFG_BTN"] = 0
modes.modes["LABEL"] = 0

POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]
client = chat.tcp_sender()

fade = 2 #2 #0.1 #1.13
fade_on = 1
fx_prm = {"SIZE":20,"SPEED":100,"OFFSET":50,"BASE":"-","START":0}

def build_cmd(dmx,val,args=[fade],flash=0,xpfx="",attr=""):
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
    return cmd


def update_raw_dmx(data ,value=None,args=[fade],flash=0,pfx="d",fx=0):
    cmd = []
    if flash:
        pfx += "f"

    for row in data:
        if fx:
            if value is not None: 
                # z.b. flush off
                xcmd = str(value)+":"+row["FX"].split(":",1)[-1]
            else:
                xcmd = row["FX"]
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
                    xcmd = "{:0.4f}".format(row["VALUE"])

                for arg in args:
                    if type(arg) is float:
                        xcmd += ":{}".format(arg)
                    else:
                        xcmd += ":{:0.4f}".format(arg)
                #print( "pack: FIX",row["FIX"],row["ATTR"], xcmd)
        #xcmd += ":{}".format(row["ATTR"])
        cmd.append( xcmd)
    
    return cmd

def update_dmx(attr,data,value=None,args=[fade],flash=0,pfx=""):
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

        return cmd
    except Exception as e:
        print("== cb EXCEPT",e)
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        raise e

class dummy_event():
    def __init__(self):
        self.num =0
        self.type = 4 #press 5 release
        self.set_value=-1
    
class Xevent():
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode
    def encoder(self,fix,attr,data,elem,action="",xfade=None):
        if action == "click":
            if self.data["ATTRIBUT"][attr]["ACTIVE"]:
                self.data["ATTRIBUT"][attr]["ACTIVE"] = 0
                self.elem["bg"] = "grey"
            else:
                self.data["ATTRIBUT"][attr]["ACTIVE"] = 1
                self.elem["bg"] = "yellow"
            return 1

    
        v2=data["ATTRIBUT"][attr]["VALUE"]
        change=0
        increment = 4.11
        if action == "+":
            v2+= increment
            v = "+{:0.4f}".format( increment ) #) #4.11"
            change=1
        elif action == "-":
            v2-= increment
            v = "-{:0.4f}".format( increment ) #) #4.11"
            change=1
        elif type(action) is int or type(action) is float:
            #v2-= increment
            #v = "-{:0.4f}".format( increment ) #) #4.11"
            v2 = action
            change=1

            
        if v2 < 0:
            v2=0
        elif v2 > 256:
            v2=256
            
        if change:
            data["ATTRIBUT"][attr]["ACTIVE"] = 1
            elem["bg"] = "yellow"
            #v2 = v
            #v = data["ATTRIBUT"][attr]["VALUE"]
            data["ATTRIBUT"][attr]["VALUE"] = v2
            elem["text"] = "{} {:0.2f}".format(attr,v2)
            #worker.fade_dmx(fix,attr,data,v,v2,ft=0)
            if xfade:
                cmd=update_dmx(attr=attr,data=data)
            else:
                cmd=update_dmx(attr=attr,data=data,args=[0])

            #data["ATTRIBUT"][attr]["VALUE"] = v2
            if cmd and not modes.val("BLIND"):
                client.send(cmd)
    def clear(self,event=None):

        if modes.val("STORE"):
            self.data.val_commands["STORE"] = 0
            modes.val("STORE",0)# = 0
            self.data.elem_commands["STORE"]["bg"] = "grey"

        else: 
            for fix in self.data.FIXTURES.fixtures:
                print( "clr",fix)
                data = self.data.FIXTURES.fixtures[fix]
                #print("elm",self.data.elem_attr[fix])
                for attr in data["ATTRIBUT"]:
                    if attr.endswith("-FINE"):
                        continue
                    self.data.elem_attr[fix][attr]["bg"] = "grey"
                    data["ATTRIBUT"][attr]["ACTIVE"] = 0
                #print(data["ATTRIBUT"])
            print( "CB CLEAR" )

    def command(self,event):       
        if self.mode == "COMMAND":
            
            if self.attr == "CLEAR":
                if event.num == 1:
                    self.clear()

                    
            if self.attr.startswith("SZ:"):#SIN":
                #global fx_prm
                k = "SIZE"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] *=1.2
                elif event.num == 5:
                    fx_prm[k] /=1.2
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 0:
                    fx_prm[k] =0
                self.data.elem_fx_commands[self.attr]["text"] = "SZ:{:0.0f}".format(fx_prm[k])
            if self.attr.startswith("SP:"):#SIN":
                #global fx_prm
                k = "SPEED"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] *=1.2
                elif event.num == 5:
                    fx_prm[k] /=1.2
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 0:
                    fx_prm[k] =0

                if fx_prm[k] < 0.1:
                    self.data.elem_fx_commands[self.attr]["text"] = "SP:off".format(fx_prm[k])
                else:
                    self.data.elem_fx_commands[self.attr]["text"] = "SP:{:0.0f}".format(fx_prm[k])
            if self.attr.startswith("ST:"):#SIN":
                #global fx_prm
                k = "START"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] *=1.2
                elif event.num == 5:
                    fx_prm[k] /=1.2
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 4000:
                    fx_prm[k] = 4000
                if fx_prm[k] < 0:
                    fx_prm[k] =0

                self.data.elem_fx_commands[self.attr]["text"] = "ST:{:0.0f}".format(fx_prm[k])
            if self.attr.startswith("OF:"):#SIN":
                #global fx_prm
                k = "OFFSET"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if fx_prm[k] <= 0:
                        fx_prm[k] = 1
                    fx_prm[k] *=1.2
                elif event.num == 5:
                    fx_prm[k] /=1.2
                #fx_prm[k] =int(fx_prm[k])
                
                if fx_prm[k] > 1024:
                    fx_prm[k] = 1024
                if fx_prm[k] < 0:
                    fx_prm[k] =0

                self.data.elem_fx_commands[self.attr]["text"] = "OF:{:0.0f}".format(fx_prm[k])
            if self.attr.startswith("BS:"):
                k = "BASE"
                if event.num == 1:
                    fx_prm[k] = "0"
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    fx_prm[k] = "+"
                elif event.num == 5:
                    fx_prm[k] = "-"
                self.data.elem_fx_commands[self.attr]["text"] = "BS:{}".format(fx_prm[k])
            if self.attr.startswith("FX:"):#SIN":
                if event.num == 1:
                    cmd = ""
                    offset = 0
                    offset_flag=0
                    start = fx_prm["START"]
                    base  = fx_prm["BASE"]

                    for fix in self.data.FIXTURES.fixtures:
                        data = self.data.FIXTURES.fixtures[fix]
                        #print( "ADD FX",fix)
                        for attr in data["ATTRIBUT"]:
                            if attr.endswith("-FINE"):
                                continue

                            fx=""
                            if "SIN" in self.attr:
                                fx = "sinus"
                            elif "FD" in self.attr:
                                fx = "fade"
                            elif "ON2" in self.attr:
                                fx = "on2"
                            elif "ON" in self.attr:
                                fx = "on"
                            elif "BUM2" in self.attr:
                                fx = "bump2"
                            elif "BUM" in self.attr:
                                fx = "bump"
                            elif "COS" in self.attr:
                                fx = "cosinus"

                            if fx:
                                if fx_prm["SPEED"] < 0.1:
                                    fx = "off"
                            else:
                                if "DIM" in self.attr:
                                    base=""
                                    if attr == "DIM":
                                        if fx_prm["SPEED"] < 0.1:
                                            fx = "off"
                                        else:
                                            fx = "fade"
                                elif "TILT" in self.attr:
                                    base=""
                                    if attr == "PAN":
                                        fx = "off"
                                    if attr == "TILT":
                                        if fx_prm["SPEED"] < 0.1:
                                            fx = "off"
                                        else:
                                            fx = "sinus"
                                elif "PAN" in self.attr:
                                    base=""
                                    if attr == "PAN":
                                        if fx_prm["SPEED"] < 0.1:
                                            fx = "off"
                                        else:
                                            fx = "cosinus" 
                                    if attr == "TILT":
                                       fx = "off"
                                elif "CIR" in self.attr:
                                    base=""
                                    if attr == "PAN":
                                        if fx_prm["SPEED"] < 0.1:
                                            fx = "off"
                                        else:

                                            fx = "cosinus" 
                                    if attr == "TILT":
                                        if fx_prm["SPEED"] < 0.1:
                                            fx = "off"
                                        else:
                                            fx = "sinus"
                            if fx:
                                fx += ":{:0.0f}:{:0.0f}:{:0.0f}:{:0.0f}:{}:".format(fx_prm["SIZE"],fx_prm["SPEED"],start,offset,base)
                                offset_flag=1

                            if "FX" not in data["ATTRIBUT"][attr]:
                                data["ATTRIBUT"][attr]["FX"] =""
                            print("ADD FX",fix,attr,fx,data["ATTRIBUT"][attr]["ACTIVE"])
                            if data["ATTRIBUT"][attr]["ACTIVE"] and fx:
                                print("++ADD FX",fix,attr,fx)
                                data["ATTRIBUT"][attr]["FX"] = fx #"sinus:40:100:10"
                            
                                cmd+=update_dmx(attr,data,pfx="fx",value=fx)#,flash=FLASH)
                        if fx_prm["OFFSET"] > 0.5 and offset_flag:  
                            offset_flag=0
                            offset += fx_prm["OFFSET"] # add offset on next fixture
                        #print("offset",offset)
                    if cmd and not modes.val("BLIND"):
                        client.send(cmd)

            elif self.attr == "FX OFF":
                if event.num == 1:
                    client.send("fx0:alloff:,fxf:alloff:")
                    self.data.elem_fx_commands[self.attr]["bg"] = "magenta"
                    for fix in self.data.FIXTURES.fixtures:
                        data = self.data.FIXTURES.fixtures[fix]
                        for attr in data["ATTRIBUT"]:
                            data["ATTRIBUT"][attr]["FX"] = ""

            elif self.attr == "FLASH":
                if event.num == 1:
                    if modes.val("FLASH"):
                        modes.val("FLASH",0)# = 0
                        self.data.elem_commands[self.attr]["bg"] = "grey"
                    else:
                        modes.val("FLASH",1)# = 1
                        self.data.elem_commands[self.attr]["bg"] = "green"
            elif self.attr == "BLIND":
                
                if event.num == 1:
                    
                    if self.data.val_commands[self.attr]:
                        self.data.val_commands[self.attr] = 0
                        modes.val("BLIND",0)# = 0
                        self.data.elem_commands[self.attr]["bg"] = "grey"
                    else:
                        self.data.val_commands[self.attr] = 1
                        modes.val("BLIND",1)# = 1
                        self.data.elem_commands[self.attr]["bg"] = "red"
                    print("BLIND",self.data.val_commands)
            
            elif self.attr == "FADE":
                global fade
                global fade_on
                if fade < 0.01:
                    fade = 0.01
                elif fade > 100.0:
                    fade = 100
                if event.num == 4:
                    fade *= 1.1
                elif event.num == 5:
                    fade /= 1.1
                elif event.num == 1:
                    if fade_on:
                        fade_on = 0
                        self.data.elem_commands[self.attr]["bg"] = "grey"
                    else:
                        fade_on = 1
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

                self.data.elem_commands[self.attr]["text"] = "Fade{:0.2f}".format(fade)
            elif self.attr == "CFG-BTN":
                #global modes #CFG_BTN
                if event.num == 1:
                    if modes.val("CFG_BTN"):
                        modes.val("CFG_BTN",0)# = 0
                        self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                    else:
                        modes.val("CFG_BTN",1)# = 1
                        self.data.elem_commands[self.attr]["bg"] = "red"
            elif self.attr == "ACTIVATE": 
                #global modes# ACTIVATE
                if event.num == 1:
                    if modes.val("ACTIVATE"):
                        modes.val("ACTIVATE",0)# = 0
                        self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                    else:
                        modes.val("ACTIVATE",1)# = 1
                        self.data.elem_commands[self.attr]["bg"] = "red"
                
            elif self.attr == "SELECT":
                #global modes# SELECT
                #global CFG_BTN
                if event.num == 1:
                    if modes.val("SELECT"):
                        modes.val("SELECT",0)# = 0
                        self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                    else:
                        modes.val("SELECT",1)# = 1
                        self.data.elem_commands[self.attr]["bg"] = "red"
            elif self.attr == "LABEL":
                #global modes #LABEL
                #global CFG_BTN
                if event.num == 1:
                    if modes.val("LABEL"):
                        modes.val("LABEL", 0)
                        self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                    else:
                        modes.val("LABEL", 1)
                        self.data.elem_commands[self.attr]["bg"] = "red"
            elif self.attr == "STONY_FX":
                if event.num == 1:
                    if modes.val("STONY_FX"):
                        modes.val("STONY_FX", 0)
                        self.data.elem_fx_commands[self.attr]["bg"] = "grey"
                    else:
                        modes.val("STONY_FX", 1)
                        self.data.elem_fx_commands[self.attr]["bg"] = "red"

            elif self.attr == "STORE":
                
                if event.num == 1:
                    
                    if self.data.val_commands[self.attr]:
                        self.data.val_commands[self.attr] = 0
                        modes.val("STORE",0)
                        self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                    else:
                        self.data.val_commands[self.attr] = 1
                        modes.val("STORE", 1)
                        self.data.elem_commands[self.attr]["bg"] = "red"
                    print("BLIND",self.data.val_commands)
            elif self.attr == "BACKUP":
                self.data.PRESETS.backup_presets()
                self.data.FIXTURES.backup_patch()
            return 0


            
    def cb(self,event):
        #print("cb",self,event,data)
        print("cb",self.attr,self.mode,event)
        print(["type",event.type,"num",event.num])
        #print(dir(event.type))
        #print(dir(event),[str(event.type)])#.keys())
        try:
            #v = self.data["ATTRIBUT"][self.attr]
            #global modes
            #global STORE
            #global BLIND
            #global FLASH
            #global STONY_FX
            #global LABEL
            #global SELECT
            #global ACTIVATE 
            #global CFG_BTN
            change = 0
            if "keysym" in dir(event):
                if "Escape" == event.keysym:
                    self.clear()
                    #CLEAR
                    return 0

            if self.mode == "COMMAND":
                self.command(event)
            elif self.mode == "ROOT":
                if event.keysym=="Escape":
                    
                    pass
                    #STORE = 0
                    #LABEL = 0

            elif self.mode == "INPUT":
                print("INP",self.data.entry.get())
                if event.keycode == 36:
                    x=self.data.entry.get()
                    client.send(x)
                    #self.data.entry.clean()

                #self.data
                #chat.send("")
            elif self.mode == "INPUT2":
                print("INP2",self.data.entry2.get())
                if event.keycode == 36:
                    x=self.data.entry2.get()
                    client.send(x)
                    #self.data.entry.clean()

            elif self.mode == "INPUT3":
                print("INP3",self.data.entry3.get())
                if event.keycode == 36:
                    x=self.data.entry3.get()
                    client.send(x)
                    #self.data.entry.clean()

                #self.data
                #chat.send("")
            elif self.mode == "PRESET":
                nr = self.attr #int(self.attr.split(":")[1])-1
                #print( "RRR", [str(event.type) , event.type] )
                #print( "PRESET EVENT",event.num)
                if event.num == 1:
                    if str(event.type) == '4': #4 ButtonPress
                        #if str(event.type) == "ButtonRelease" or event.type == '5':
                        if modes.val("STORE"):
                            self.data.preset_store(nr)
                            modes.val("STORE",0)
                        elif modes.val("CFG_BTN"):
                            import tkinter.simpledialog
                            txt = tkinter.simpledialog.askstring("CFG-BTN","GO,FLASH,TOGGLE,SWOP\n EXE:"+str(nr))
                            if "CFG" not in self.data.PRESETS.val_presets[nr]:
                                self.data.PRESETS.val_presets[nr]["CFG"] = OrderedDict()
                            if "BUTTON" not in self.data.PRESETS.val_presets[nr]["CFG"]:
                                self.data.PRESETS.val_presets[nr]["CFG"]["BUTTON"] = ""

                            self.data.PRESETS.val_presets[nr]["CFG"]["BUTTON"] = txt
                            sdata=self.data.PRESETS.val_presets[nr]
                            BTN="go"
                            if "CFG" in sdata:#["BUTTON"] = "GO"
                                if "BUTTON" in sdata["CFG"]:
                                    BTN = sdata["CFG"]["BUTTON"]
                            label = self.data.PRESETS.label_presets[nr] # = label
                            txt=str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
                            self.data.elem_presets[nr]["text"] = txt
                            modes.val("CFG_BTN",0)# = 0
                            self.data.elem_commands["CFG-BTN"]["bg"] = "grey"
                        elif modes.val("LABEL"):#else:
                            label = "lalaal"
                            import tkinter.simpledialog
                            label = tkinter.simpledialog.askstring("LABEL","Preset "+str(nr))
                            if label is not None:

                                self.data.elem_presets[nr]["text"] = label
                                self.data.PRESETS.label_presets[nr] = label
                                sdata=self.data.PRESETS.val_presets[nr]
                                BTN="go"
                                if "CFG" in sdata:#["BUTTON"] = "GO"
                                    if "BUTTON" in sdata["CFG"]:
                                        BTN = sdata["CFG"]["BUTTON"]
                                txt=str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
                                #txt = "Preset:"+str(nr)+":\n"+str(len(l))+":"+label
                                self.data.elem_presets[nr]["text"] = txt
                                modes.val("LABEL", 0)
                                self.data.elem_commands["LABEL"]["bg"] = "lightgrey"
                        elif modes.val("ACTIVATE"):
                            self.data.preset_select(nr)
                            self.data.preset_go(nr,xfade=0,event=event)
                            modes.val("ACTIVATE", 0)
                            self.data.elem_commands["ACTIVATE"]["bg"] = "lightgrey"
                        elif modes.val("SELECT"):
                            self.data.preset_select(nr)
                        else:
                            self.data.preset_go(nr,event=event)
                    else:
                        self.data.preset_go(nr,event=event)
                        
                if event.num == 3:
                    if not modes.val("STORE"):
                        self.data.preset_go(nr,xfade=0,event=event)
                        
                return 0
            elif self.mode == "INPUT":
                return 0
            if self.mode == "ENCODER":
                #if self.attr == "VDIM":
                #    self.attr = "DIM"
                for fix in self.data.FIXTURES.fixtures:
                    data = self.data.FIXTURES.fixtures[fix]
                    
                    for attr in data["ATTRIBUT"]:
                        if attr.endswith("-FINE"):
                            continue
                        elem = self.data.elem_attr[fix][attr]
                        if self.attr != attr:
                            continue
                        if event.num == 1:
                            #self#encoder(attr=attr,data=data,elem=elem,action="click")
                            data["ATTRIBUT"][attr]["ACTIVE"] = 1
                            elem["bg"] = "yellow"
                            if "FX" in data["ATTRIBUT"][attr]:#["FX"]:# = 1
                                if data["ATTRIBUT"][attr]["FX"]:# = 1
                                    elem["fg"] = "blue"
                                else:
                                    elem["fg"] = "blue"
                                    elem["fg"] = "black"
                            

                        if not data["ATTRIBUT"][attr]["ACTIVE"]:
                            continue
                        
                        if event.num == 4:
                            self.encoder(fix=fix,attr=attr,data=data,elem=elem,action="+")
                            #if attr == "DIM":
                            #    self.encoder(attr="VDIM",data=data,elem=elem,action="+")
                        elif event.num == 5:
                            self.encoder(fix=fix,attr=attr,data=data,elem=elem,action="-")
                            #if attr == "DIM":
                            #     self.encoder(attr="VDIM",data=data,elem=elem,action="-")
                        if  "set_value" in dir(event)  and event.set_value >=0:
                            print("ENCODER set_value and set_fade",event)
                            #print(dir(event))
                            if "set_fade" in dir(event) and event.set_fade >0:
                                 print("event.set_fade",event.set_fade)
                                 self.encoder(fix=fix,attr=attr,data=data,elem=elem,action=event.set_value,xfade=1)
                            else:
                                 self.encoder(fix=fix,attr=attr,data=data,elem=elem,action=event.set_value)
                return 0
                                


                
            if event.num == 1:
                self.encoder(fix=0,attr=self.attr,data=self.data,elem=self.elem,action="click")

            elif event.num == 4:
                self.encoder(fix=0,attr=self.attr,data=self.data,elem=self.elem,action="+")
            elif event.num == 5:
                self.encoder(fix=0,attr=self.attr,data=self.data,elem=self.elem,action="-")
            

                
            #finally:
            #    pass
        except Exception as e:
            print("== cb EXCEPT",e)
            print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
            traceback.print_exc()
        #print(self.elem["text"],self.attr,self.data)
        
                                            
        
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
        pass
    def _load(self,filename):
        xfname = "show/"+show_name+"/"+str(filename)+".sav"
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
            if "ATTRIBUT" in jdata:  # translate old FIXTURES.fixtures start with 0 to 1          
                for attr in jdata["ATTRIBUT"]:
                    if "NR" in jdata["ATTRIBUT"][attr]:
                        nr = jdata["ATTRIBUT"][attr]["NR"]
                        if nr == 0:
                            nrnull = 1
                            break

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
        xfname = "show/"+show_name+"/"+str(filename)+".sav"
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
        print("init",self)
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

        self.all_attr =["DIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.fx_commands =["STONY_FX","FX OFF","\n"
                ,"FX:CIR","FX:PAN","FX:TILT","FX:DIM","\n"
                ,"SZ:","SP:","ST:","OF:","BS:-","\n"
                , "FX:SIN","FX:COS","FX:BUM","FX:BUM2","FX:FD","FX:ON","FX:ON2" ]
        self.commands =["\n","BLIND","CLEAR","STORE","EDIT","MOVE","\n","CFG-BTN","LABEL"
                ,"BACKUP","SET","","","SELECT","ACTIVATE","FLASH","FADE"
                ]
        self.elem_fx_commands = {}
        self.val_fx_commands = {}
        self.elem_commands = {}
        self.val_commands = {}

        self.elem_presets = {}
        self.PRESETS = Presets()
        self.PRESETS.load_presets()
        self.FIXTURES = Fixtures()
        self.FIXTURES.load_patch()
        
        for i in range(8*8):
            if i not in self.PRESETS.val_presets:
                name = "Preset:"+str(i+1)+":\nXYZ"
                #self.presets[i] = [i]
                self.PRESETS.val_presets[i] = OrderedDict() # FIX 
                self.PRESETS.val_presets[i]["CFG"] =  OrderedDict() # CONFIG 
                self.PRESETS.label_presets[i] = "-"

  
    def load(self,fname=""):
        pass
    def exit(self):
        print("__del__",self)
        self.PRESETS.backup_presets()
        print("********************************************************")
        self.FIXTURES.backup_patch()
        print("*********del",self,"***********************************************")
    def refresh_gui(self):
        for fix in self.FIXTURES.fixtures:                            
            sdata = self.FIXTURES.fixtures[fix]                            
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
                    else:
                        elem["bg"] = "grey"

    def preset_store(self,nr):
        print("STORE PRESET")
        self.val_commands["STORE"] = 0
        global STORE
        STORE = 0
        self.elem_commands["STORE"]["bg"] = "lightgrey"

        CFG = OrderedDict()
        if "CFG" in self.PRESETS.val_presets[nr]: #["CFG"] 
            CFG = self.PRESETS.val_presets[nr]["CFG"] 
        sdata = {}
        sdata["CFG"] = CFG # OrderedDict()
        sdata["CFG"]["FADE"] = fade
        sdata["CFG"]["DEALY"] = 0
        #sdata["CFG"]["BUTTON"] = "GO"
        for fix in self.FIXTURES.fixtures:                            
            data = self.FIXTURES.fixtures[fix]
            for attr in data["ATTRIBUT"]:
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    if fix not in sdata:
                        sdata[fix] = {}
                    if attr not in sdata[fix]:
                        sdata[fix][attr] = OrderedDict()
                        if not modes.val("STONY_FX"):
                            sdata[fix][attr]["VALUE"] = data["ATTRIBUT"][attr]["VALUE"]
                            #sdata[fix][attr]["FADE"] = fade
                        else:
                            sdata[fix][attr]["VALUE"] = None #data["ATTRIBUT"][attr]["VALUE"]

                        if "FX" not in data["ATTRIBUT"][attr]: 
                             data["ATTRIBUT"][attr]["FX"] =""
                        
                        sdata[fix][attr]["FX"] = data["ATTRIBUT"][attr]["FX"] 
    
        print("sdata",len(sdata))
        
        self.PRESETS.val_presets[nr] = sdata
        if len(sdata) > 1:
            fx_color = 0
            val_color = 0
            for fix in sdata:
                if fix == "CFG":
                    continue
                #print( "$$$$",fix,sdata[fix])
                for attr in sdata[fix]:
                    if "FX" in sdata[fix][attr]:
                        if sdata[fix][attr]["FX"]:
                            fx_color = 1
                    if "VALUE" in sdata[fix][attr]:
                        if sdata[fix][attr]["VALUE"] is not None:
                            val_color = 1

            self.elem_presets[nr]["fg"] = "black"
            if val_color:
                self.elem_presets[nr]["bg"] = "yellow"
                if fx_color:
                    self.elem_presets[nr]["fg"] = "blue"
            else:   
                if fx_color:
                    self.elem_presets[nr]["bg"] = "cyan"
        else:
            self.elem_presets[nr]["fg"] = "black"
            self.elem_presets[nr]["bg"] = "grey"
        #self.elem_presets[nr].option_add("*Font", FontBold)
        label = ""
        if nr in self.PRESETS.label_presets:
            #print(dir(self.data))
            label = self.PRESETS.label_presets[nr]

        BTN="go"
        if "CFG" in sdata:#["BUTTON"] = "GO"
            if "BUTTON" in sdata["CFG"]:
                BTN = sdata["CFG"]["BUTTON"]
        txt = str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label 
        self.elem_presets[nr]["text"] = txt 
        #print("GO CFG ",self.PRESETS.val_presets)
           

    def preset_select(self,nr):
        print("SELECT PRESET")
        sdata = self.PRESETS.val_presets[nr]
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
                    #self#encoder(attr=attr,data=data,elem=elem,action="click")
                    self.FIXTURES.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                    elem["bg"] = "yellow"
    def preset_go(self,nr,xfade=fade,event=None):
        print("GO PRESET FADE",nr)

        rdata = self.PRESETS.get_raw_map(nr)
        cfg   = self.PRESETS.get_cfg(nr)
        fcmd  = self.FIXTURES.update_raw(rdata)
        #virtcmd  = self.data.FIXTURES.get_virtual(rdata)


        xFLASH = 0
        value=None
        #xfade = fade
        if modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "SEL"): #FLASH
            self.preset_select(nr)
            return 0
        elif modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL"): #FLASH
            xFLASH = 1
            xfade = 0
            if event:
                if str(event.type) == "ButtonRelease" or event.type == '5' :
                    # 4 fix vor ThinkPad / Debian 11
                    if xFLASH:
                        value = "off"

        vvcmd = update_raw_dmx( rdata ,value,[xfade] ) 
        fxcmd = update_raw_dmx( rdata ,value,[xfade],fx=1) 

        cmd = []
        for vcmd,d in [[vvcmd,"d"],[fxcmd,"fx"]]:
            if xFLASH:
                d+="f"
            for i,v in enumerate(fcmd):
                DMX = fcmd[i]["DMX"]
                if DMX and vcmd[i]:
                    xcmd = ",{}{}:{}".format(d,DMX,vcmd[i])
                    cmd.append( xcmd )

                if "VIRTUAL" in fcmd[i]:
                    for a in fcmd[i]["VIRTUAL"]:
                        DMX = fcmd[i]["VIRTUAL"][a]
                        if DMX and vcmd[i]:
                            xcmd = ",{}{}:{}".format(d,DMX,vcmd[i])
                            cmd.append( xcmd )

        cmd = "".join(cmd)
        print("cmd",cmd) 
        if cmd and not modes.val("BLIND"):
            client.send(cmd )
        
        self.refresh_gui()

        
    def draw_dim(self,fix,data,c=0,r=0,frame=None):
        Font = font.Font(family='Helvetica', size=9, weight='normal')
        FontBold = font.Font(family='Helvetica', size=10, weight='bold')
        i=0
        if frame is None:
            frame = tk.Frame(root,bg="black")
            frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Button(frame,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #c+=1
        #r+=1
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
            b = tk.Button(frame,bg="lightblue",font=FontBold, text=""+str(fix)+" "+data["NAME"],width=4)
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="grey",font=FontBold, text=str(attr)+' '+str(round(v,2)),width=6)
            self.elem_attr[fix][attr] = b
            b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=12:
                c=0
                r+=1
        return c,r
    def draw_patch(self,xframe):
        r=0
        c=0
        frame_dim = xframe
        root = frame_dim
        dim_frame = tk.Frame(root,bg="black")
        dim_frame.pack(fill=tk.X, side=tk.TOP)
        root = frame_patch

        
        fix_frame = tk.Frame(root,bg="black")
        canvas = tk.Canvas(root)
        def yview(event):
            print("yevent",event)
            print(dir(canvas))
            #yview_moveto', 'yview_scroll'
            yyy=20.1
            
            fix_frame.yview_moveto(yyy)
            #canvas.yview_moveto(yyy)
            #yyy=20
            #canvas.yview_scroll(yyy,"units")
        #def sconfig(event):
        #    global canvas
        #    canvas.configure(scrollregion=canvas.bbox("all"),width=400,height=200)
        #fix_frame.bind("<Configure>",sconfig)
        #myscrollbar=tk.Scrollbar(root,orient="vertical",command=canvas.yview)
        #myscrollbar=tk.Scrollbar(root,orient="vertical",command=yview)
        #myscrollbar.pack(side="right",fill="y") 
        #canvas.create_window((0, 0), window=fix_frame, anchor="nw")
        #canvas.pack(fill=tk.X, side=tk.TOP)

        fix_frame = tk.Frame(root,bg="black")
        fix_frame.pack(fill=tk.X, side=tk.TOP)
        #fix_frame = canvas

        #fix_frame.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
        #canvas.configure(yscrollcommand=myscrollbar.set)
        i=0
        c=0
        r=0
        for fix in self.FIXTURES.fixtures:
            i+=1
            data = self.FIXTURES.fixtures[fix]
            print( fix ,data )
            
            #if(len(data["ATTRIBUT"].keys()) <= 1):
            #    c,r=self.draw_dim(fix,data,c=c,r=r,frame=dim_frame)
            #else:
            if 1:
                #self._draw_fix(fix,data,root=fix_frame)
                frame = fix_frame
                
                b = tk.Button(frame,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
                b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                #r+=1
                if fix not in self.elem_attr:
                    self.elem_attr[fix] = {}
                    
                patch = ["DMX","UNIVERS"]
                for k in patch:
                    v=data[k]
                    b = tk.Button(frame,bg="grey", text=str(k)+' '+str(v),width=8)
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
                    
                    b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
                    self.elem_attr[fix][attr] = b
                    #b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
                    b.grid(row=r, column=c, sticky=tk.W+tk.E)
                    c+=1
                    if c >=8:
                        c=1
                        r+=1
                c=0
                r+=1
                
        #fix_frame
        #canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
    def draw_fix(self,xframe):
        r=0
        c=0
        frame_dim=xframe
        frame_fix=xframe
        root = frame_dim
        dim_frame = tk.Frame(root,bg="black")
        dim_frame.pack(fill=tk.X, side=tk.TOP)
        root = frame_fix
        fix_frame = tk.Frame(root,bg="black")
        fix_frame.pack(fill=tk.X, side=tk.TOP)
        Font = font.Font(family='Helvetica', size=9, weight='normal')
        FontBold = font.Font(family='Helvetica', size=10, weight='bold')
        #self.tk.default_font.configure(size=9)
        #self.tk.option_add("*Font", FontBold)
        #dim_frame.configure(font=Font)
        #fix_frame.configure(font=Font)
        i=0
        c=0
        r=0
        dim_end=0
        for fix in self.FIXTURES.fixtures:
            i+=1
            data = self.FIXTURES.fixtures[fix]
            print( fix ,data )
            
            if(len(data["ATTRIBUT"].keys()) <= 1):
                c,r=self.draw_dim(fix,data,c=c,r=r,frame=dim_frame)
            else:
                if not dim_end:
                    dim_end=1
                    c=0
                    r=0
                #self._draw_fix(fix,data,root=fix_frame)
                frame = fix_frame
            
                b = tk.Button(frame,bg="lightblue",font=FontBold, text="FIX:"+str(fix)+" "+data["NAME"],width=20)
                b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                #r+=1
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
                    
                    b = tk.Button(frame,bg="grey",font=FontBold, text=str(attr)+' '+str(round(v,2)),width=8)
                    self.elem_attr[fix][attr] = b
                    b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
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
        #frame = tk.Frame(root,bg="black")
        #frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Label(frame,bg="black", text="--------------------------------- ---------------------------------------")
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r=0
        
        frame = tk.Frame(root2,bg="black")
        frame.pack( side=tk.TOP,expand=1,fill="both")

        
        b = tk.Button(frame,bg="lightblue", text="ENCODER",width=6)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
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
        #frame = tk.Frame(root,bg="black")
        #frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Label(frame,bg="black", text="------------------------------ ---------------------------------------")
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r=0
        
        #frame = tk.Frame(root2,bg="black")
        frame = tk.Frame(frame_fx,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="FX.",width=6)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
        c+=1
        for comm in self.fx_commands:
            if comm == "\n":
                c=0
                r+=1
                continue
            v=0
            
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
            if comm not in self.elem_fx_commands:
                self.elem_fx_commands[comm] = b
                self.val_fx_commands[comm] = 0
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=self,mode="COMMAND").cb)
            if comm == "BLIND":
                b["bg"] = "grey"
            if comm == "CLEAR":
                b["bg"] = "grey"
            if comm == "STONY_FX":
                b["bg"] = "grey"
            if comm == "FADE":
                b["bg"] = "green"
            if comm == "FX OFF":
                b["bg"] = "magenta"
            if comm == "SZ:":
                b["text"] = "SZ:{:0.0f}".format(fx_prm["SIZE"])
            if comm == "SP:":
                b["text"] = "SP:{:0.0f}".format(fx_prm["SPEED"])
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
    def draw_command(self,xframe):
        frame_cmd=xframe
        i=0
        c=0
        r=0
        #frame = tk.Frame(root,bg="black")
        #frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Label(frame,bg="black", text="------------------------------ ---------------------------------------")
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r=0
        
        #frame = tk.Frame(root2,bg="black")
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
            if comm == "STONY_FX":
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
                b["text"] = "FADE:{:0.02f}".format(fade)
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
       
        b = tk.Button(frame,bg="lightblue", text="EXEC")
        #b.bind("<Button>",Xevent(elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r+=1      
        for k in self.PRESETS.val_presets:
            v=0
            label = ""
            if k in self.PRESETS.label_presets:
                label = self.PRESETS.label_presets[k]
                print([label])

            sdata=self.PRESETS.val_presets[k]
            BTN="go"
            if "CFG" in sdata:#["BUTTON"] = "GO"
                if "BUTTON" in sdata["CFG"]:
                    BTN = sdata["CFG"]["BUTTON"]
            txt=str(k)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
            b = tk.Button(frame,bg="grey", text=txt,width=8,height=2)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            
            if k in self.PRESETS.val_presets and len(self.PRESETS.val_presets[k]) :
                b["bg"] = "yellow"
                sdata = self.PRESETS.val_presets[k]
                if len(sdata) > 1:
                    fx_color = 0
                    val_color = 0
                    for fix in sdata:
                        if fix == "CFG":
                            continue
                        #print( "$$$$",fix,sdata[fix])
                        for attr in sdata[fix]:
                            if "FX" in sdata[fix][attr]:
                                if sdata[fix][attr]["FX"]:
                                    fx_color = 1
                            if "VALUE" in sdata[fix][attr]:
                                if sdata[fix][attr]["VALUE"] is not None:
                                    val_color = 1

                    b["fg"] = "black"
                    if val_color:
                        b["bg"] = "gold"
                        if fx_color:
                            b["fg"] = "blue"
                    else:   
                        if fx_color:
                            b["bg"] = "cyan"
                else:
                    b["bg"] = "grey"
            if "SEL" in txt:
                b["fg"] = "black"
                b["bg"] = "blue"
            elif "GO" in txt:
                b["fg"] = "black"
            elif "FL" in txt:
                b["fg"] = "red"

            if k not in self.elem_presets:
                self.elem_presets[k] = b
                #self.PRESETS.val_presets[preset] = 0
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
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
        b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT3").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","fx:alloff:::")
    def draw_colorpicker(self,xframe):
        import lib.colorpicker as colp

        #colp.colorpicker(xframe,width=600,height=100, xcb=Xevent(fix=0,elem=None,attr="COLORPICKER",data=self,mode="INPUT").cb)
        #xcb = cb
        e = dummy_event()
        r = Xevent(fix=0,elem=None,attr="RED",data=self,mode="ENCODER") #.cb
        g = Xevent(fix=0,elem=None,attr="GREEN",data=self,mode="ENCODER") #.cb
        b = Xevent(fix=0,elem=None,attr="BLUE",data=self,mode="ENCODER") #.cb
        def _cb(event,data):
            print("PPPPPPPOOOOOORRR",event,data)
            print(event.num)
            if "color" in data and (event.num == 1 or event.num == 3 or event.num==2):
                e.num=5
                e.type=1
                cr=-1
                cg=-1
                cb=-1
                color = data["color"]
                if event.num == 1: 
                    e.set_fade=fade
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]
                elif event.num == 2: 
                    e.num=1
                    e.type=4
                    e.set_value=-1
                else:
                    e.set_fade=-1

                e.set_value=cr#color[0]
                r.cb(e)
                e.set_value=cg#color[1]
                g.cb(e)
                e.set_value=cb#color[2]
                b.cb(e)
                e.set_value=-1
                e.set_fade=-1
                 
                print("PICK COLOR:",data["color"])
                #self.encoder(fix=fix,attr=attr,data=data,elem=elem,action="+")
        colp.colorpicker(xframe,width=600,height=100, xcb=_cb)
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
        Xroot.bind("<Key>",Xevent(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        #self.draw_patch()
        #self.draw_fix()
        #input()
        #self.draw_enc()
        #self.draw_command()
        #self.draw_fx()
        self.draw_input()
        #self.draw_preset()

def ScrollFrame(root,width=50,height=100,bd=1):
    print("ScrollFrame init",width,height)
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
    return bframe
#frame = ScrollFrame(root)

class GUIHandler():
    def __init__(self):
        pass
    def update(self,fix,attr,args={}):
        #print("GUIHandler",fix,attr,args)
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
        #self.PRESETS.label_presets = l

    def backup_patch(self):
        filename = "patch"
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        self._backup(filename,data,labels)

    def update_raw(self,rdata):
        #print("update_raw",rdata)
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
                print( sdata)
                sDMX = (sdata["UNIVERS"]*512)+sdata["DMX"]  
                #sDMX =sdata["DMX"]  

            if attr not in ATTR:
                continue
        
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
            if v2 is not None:
                ATTR[attr]["VALUE"] = v2

            #self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
            text = str(attr)+' '+str(round(v,2))
            self.gui.update(fix,attr,args={"text":text})
        return cmd


class Presets(Base):
    def __init__(self):
        super().__init__() 
        #self.load()

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
        
        
    def backup_presets(self):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        self._backup(filename,data,labels)
        

    def get_cfg(self,nr):
        if nr not in self.val_presets:
            print(self,"error get_cfg no nr:",nr)
            return {}
        if "CFG" in self.val_presets[nr]:
            return self.val_presets[nr]["CFG"]

    def get_raw_map(self,nr):
        print("get_raw_map",nr)
        if nr not in self.val_presets:
            self.val_presets[nr] = OrderedDict()
            self.val_presets[nr]["VALUE"] = 0
            self.val_presets[nr]["FX"] = ""
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
                #x["DMX"]  = sdata[fix][attr]["NR"] 

                out.append(x)
        return out

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
        self.b = tk.Label(self.frame,bg="blue", text="MAIN:MENU",width=13,height=1)
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        r+=1
        for row in data:
            #print(i)
            #row = data[i]
            self.b = tk.Button(self.frame,bg="lightblue", text=row["text"],width=13,height=3)
            self.b.bind("<Button>",BEvent({"NR":i,"text":row["text"]},self.callback).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            r+=1
            i+=1
        self.frame.pack()
    def callback(self,event,data={}):
        print(self,event,data)
        window_manager.top(data["text"])# = WindowManager()

lf_nr = 0
class GUIWindow():
    def __init__(self,title="tilte",master=0,width=100,height=100,left=None,top=None):
        global lf_nr
        if master: 
            #Font = font.Font(family='Helvetica', size=9, weight='normal')
            self.tk = tkinter.Tk()#font=Font) #Toplevel()
            #Font = font.Font(family='Helvetica', size=9, weight='normal')
            #FontBold = font.Font(family='Helvetica', size=10, weight='bold')
            #self.tk.default_font.configure(size=9)
            #self.tk.option_add("*Font", FontBold)
            #self.tk.configure(font=Font)
        else:
            self.tk = tkinter.Toplevel()
        self.tk["bg"] = "black"
        self.tk.bind("<Button>",self.callback)
        self.tk.bind("<Key>",self.callback)
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
        #self.frame.pack()
    def mainloop(self):
        self.tk.mainloop()
    def callback(self,event,data={}):
        print("<GUI>",self,event,data)
        #if "keysym" in dir(event):
        #    if "Escape" == event.keysym:
        #        e=dummy_event()
        #        e.num=1
        #        self._event_clear(e)
        
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

window_manager = WindowManager()

master =GUI()

w = GUIWindow("MAIN",master=1,width=130,height=450,left=0,top=65)
data = []
#data.append({"text":"COMMAND"})
data.append({"text":"EXEC"})
data.append({"text":"DIMMER"})
data.append({"text":"FIXTURES"})
#data.append({"text":"PRESET"})
#data.append({"text":"PATCH"})
#data.append({"text":"ENCODER"})
f = GUI_menu(w.tk,data)
window_manager.new(w)

name="DIMMER"
w = GUIWindow(name,master=0,width=800,height=400,left=140,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
#frame_dim = w1 # w.tk
#master.draw_dim(w1.tk)
window_manager.new(w,name)

name="FIXTURES"
w = GUIWindow(name,master=0,width=800,height=400,left=140,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
#frame_fix = w1 #w.tk
master.draw_fix(w1)#.tk)
window_manager.new(w,name)


name="ENCODER"
ww = GUIWindow(name,master=0,width=800,height=50,left=140,top=500)
Xroot = ww.tk
#default_font = font.Font(family='Helvetica', size=12, weight='bold')
Font = font.Font(family='Helvetica', size=9, weight='normal')
FontBold = font.Font(family='Helvetica', size=10, weight='bold')
#default_font.configure(size=9)
Xroot.option_add("*Font", FontBold)
w = None
root = tk.Frame(Xroot,bg="black",width="10px")
root.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root3 = tk.Frame(Xroot,bg="black",width="20px")
root3.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)
root2 = tk.Frame(Xroot,bg="black",width="1px")
master.draw_enc(root2)
root2.pack(fill=tk.BOTH,expand=0, side=tk.LEFT)


#w = GUIWindow("GRID",master=0,width=1000,height=200,left=232,top=65)
#data = []
#for i in range(10):
#    data.append({"text":"P {:02}".format(i+1)})
#w = GUI_grid(w.tk,data)
#window_manager.new(w)

name = "COMMAND"
w = GUIWindow(name,master=0,width=350,height=200,left=950,top=65)
master.draw_command(w.tk)
window_manager.new(w,name)

name="EXEC"
w = GUIWindow(name,master=0,width=800,height=400,left=140,top=65)
#frame_exe = w.tk
master.draw_preset(w.tk)
window_manager.new(w,name)

name="PATCH"
w = GUIWindow(name,master=0,width=800,height=400,left=140,top=65)
w1 = ScrollFrame(w.tk,width=800,height=400)
frame_patch = w1 #w.tk
window_manager.new(w,name)

name="FX"
w = GUIWindow(name,master=0,width=350,height=250,left=950,top=305)
#frame_fx = w.tk
master.draw_fx(w.tk)
window_manager.new(w,name)

#LibreLightDesk
name="COLERPICKER"
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

