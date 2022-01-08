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
import sys
if "__file__" in dir():
    sys.stdout.write("\x1b]2;"+str(__file__)+"\x07") # terminal title
else:
    sys.stdout.write("\x1b]2;"+str("__file__")+"\x07") # terminal title

import json
import time
import sys
import _thread as thread

import tkinter
import tkinter as tk
from tkinter import font


import lib.chat as chat
import lib.motion as motion

Xroot = tk.Tk()
Xroot["bg"] = "black" #white
Xroot.title( __file__)


root = tk.Frame(Xroot,bg="black",width="100px")
root.pack(fill=tk.BOTH, side=tk.LEFT)
root3 = tk.Frame(Xroot,bg="black",width="20px")
root3.pack(fill=tk.BOTH, side=tk.LEFT)
root2 = tk.Frame(Xroot,bg="black",width="1px")
root2.pack(fill=tk.BOTH, side=tk.LEFT)

#default_font = font.Font(family='Helvetica', size=12, weight='bold')
Font = font.Font(family='Helvetica', size=9, weight='normal')
FontBold = font.Font(family='Helvetica', size=10, weight='bold')
#default_font.configure(size=9)
Xroot.option_add("*Font", FontBold)


from collections import OrderedDict

show_name = "GloryCamp2021"
show_name = "GloryCamp2021"
#show_name = "Dimmer"


CUES    = OrderedDict()
groups  = OrderedDict()

BLIND = 0
STORE = 0
FLASH = 0
STONY_FX = 0
LABEL = 0
SELECT = 0
CFG_BTN = 0
POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]
client = chat.tcp_sender()

fade = 2 #2 #0.1 #1.13
fade_on = 1
fx_prm = {"SIZE":20,"SPEED":100,"OFFSET":50}

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


def update_dmx(attr,data,value=None,args=[fade],flash=0,pfx=""):
    global BLIND
    dmx = data["DMX"]
    val = None
    cmd=""

    try:
        if attr == "DIM" and data["ATTRIBUT"][attr]["NR"] < 0: #VDIM
            print( "VDIM")
            for attr in data["ATTRIBUT"]:
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

        if BLIND:
            cmd=""

        return cmd
    except Exception as e:
        print("== cb EXCEPT",e)
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        raise e

class dummy_event():
    def __init__(self):
        self.num =0
    
class Xevent():
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode
    def encoder(self,fix,attr,data,elem,action=""):
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
            v2-= 4.11
            v = "-{:0.4f}".format( increment ) #) #4.11"
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
            
            cmd=update_dmx(attr=attr,data=data,args=[0])
            #data["ATTRIBUT"][attr]["VALUE"] = v2
            client.send(cmd)

        


            
    def cb(self,event):
        #print("cb",self,event,data)
        print("cb",self.attr,self.mode,event)
        #print(dir(event),[str(event.type)])#.keys())
        try:
            #v = self.data["ATTRIBUT"][self.attr]
            global STORE
            global BLIND
            global FLASH
            global STONY_FX
            global LABEL
            global SELECT
            global CFG_BTN
            change = 0
            
            if self.mode == "COMMAND":
                
                if self.attr == "CLEAR":
                    if event.num == 1:

                        if STORE:
                            self.data.val_commands["STORE"] = 0
                            STORE = 0
                            self.data.elem_commands["STORE"]["bg"] = "grey"

                        else: 
                            for fix in self.data.fixtures:
                                print( "clr",fix)
                                data = self.data.fixtures[fix]
                                #print("elm",self.data.elem_attr[fix])
                                for attr in data["ATTRIBUT"]:
                                    if attr.endswith("-FINE"):
                                        continue
                                    self.data.elem_attr[fix][attr]["bg"] = "grey"
                                    data["ATTRIBUT"][attr]["ACTIVE"] = 0
                                #print(data["ATTRIBUT"])
                            print( "CB CLEAR" )

                        
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
                    self.data.elem_commands[self.attr]["text"] = "SZ:{:0.0f}".format(fx_prm[k])
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
                    self.data.elem_commands[self.attr]["text"] = "SP:{:0.0f}".format(fx_prm[k])
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

                    self.data.elem_commands[self.attr]["text"] = "OF:{:0.0f}".format(fx_prm[k])
                if self.attr.startswith("FX:"):#SIN":
                    if event.num == 1:
                        cmd = ""
                        offset = 0
                        for fix in self.data.fixtures:
                            data = self.data.fixtures[fix]
                            #print( "ADD FX",fix)
                            for attr in data["ATTRIBUT"]:
                                if attr.endswith("-FINE"):
                                    continue

                                fx=""
                                if "SIN" in self.attr:
                                    fx = "sinus"
                                elif "FD" in self.attr:
                                    fx = "fade"
                                elif "ON2-" in self.attr:
                                    fx = "on2-"
                                elif "ON-" in self.attr:
                                    fx = "on-"
                                elif "ON2" in self.attr:
                                    fx = "on2"
                                elif "ON" in self.attr:
                                    fx = "on"
                                elif "BUM-" in self.attr:
                                    fx = "bump-"
                                elif "BUM" in self.attr:
                                    fx = "bump"
                                elif "COS" in self.attr:
                                    fx = "cosinus"
                                if fx:
                                    fx += ":{:0.0f}:{:0.0f}:{:0.0f}".format(fx_prm["SIZE"],fx_prm["SPEED"],offset)#fx_prm["OFFSET"])
                                else:
                                    if "CIR" in self.attr:
                                        if attr == "PAN":
                                            fx = "cosinus:{:0.0f}:{:0.0f}:{:0.0f}".format(fx_prm["SIZE"],fx_prm["SPEED"],offset)#fx_prm["OFFSET"])
                                        if attr == "TILT":
                                           fx = "sinus:{:0.0f}:{:0.0f}:{:0.0f}".format(fx_prm["SIZE"],fx_prm["SPEED"],offset)#fx_prm["OFFSET"])

                                if "FX" not in data["ATTRIBUT"][attr]:
                                    data["ATTRIBUT"][attr]["FX"] =""
                                print("ADD FX",fix,attr,fx,data["ATTRIBUT"][attr]["ACTIVE"])
                                if data["ATTRIBUT"][attr]["ACTIVE"]:
                                    print("++ADD FX",fix,attr,fx)
                                    data["ATTRIBUT"][attr]["FX"] = fx #"sinus:40:100:10"
                                
                                    cmd+=update_dmx(attr,data,pfx="fx",value=fx)#,flash=FLASH)
                            if fx_prm["OFFSET"] > 0.5:  
                                offset += fx_prm["OFFSET"] # add offset on next fixture
                            #print("offset",offset)
                        if cmd and not BLIND:
                            client.send(cmd)

                elif self.attr == "FX OFF":
                    if event.num == 1:
                        client.send("fx0:alloff:,fxf:alloff:")
                        self.data.elem_commands[self.attr]["bg"] = "magenta"
                        for fix in self.data.fixtures:
                            data = self.data.fixtures[fix]
                            for attr in data["ATTRIBUT"]:
                                data["ATTRIBUT"][attr]["FX"] = ""

                elif self.attr == "FLASH":
                    if event.num == 1:
                        if FLASH:
                            FLASH = 0
                            self.data.elem_commands[self.attr]["bg"] = "grey"
                        else:
                            FLASH = 1
                            self.data.elem_commands[self.attr]["bg"] = "green"
                elif self.attr == "BLIND":
                    
                    if event.num == 1:
                        
                        if self.data.val_commands[self.attr]:
                            self.data.val_commands[self.attr] = 0
                            BLIND = 0
                            self.data.elem_commands[self.attr]["bg"] = "grey"
                        else:
                            self.data.val_commands[self.attr] = 1
                            BLIND = 1
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
                    global CFG_BTN
                    if event.num == 1:
                        if CFG_BTN:
                            CFG_BTN = 0
                            self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                        else:
                            CFG_BTN = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                elif self.attr == "SELECT":
                    global SELECT
                    #global CFG_BTN
                    if event.num == 1:
                        if SELECT:
                            SELECT = 0
                            self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                        else:
                            SELECT = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                elif self.attr == "LABEL":
                    global LABEL
                    #global CFG_BTN
                    if event.num == 1:
                        if LABEL:
                            LABEL = 0
                            self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                        else:
                            LABEL = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                elif self.attr == "STONY_FX":
                    if event.num == 1:
                        if STONY_FX:
                            STONY_FX = 0
                            self.data.elem_commands[self.attr]["bg"] = "grey"
                        else:
                            STONY_FX = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"

                elif self.attr == "STORE":
                    
                    if event.num == 1:
                        
                        if self.data.val_commands[self.attr]:
                            self.data.val_commands[self.attr] = 0
                            STORE = 0
                            self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                        else:
                            self.data.val_commands[self.attr] = 1
                            STORE = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                        print("BLIND",self.data.val_commands)
                elif self.attr == "BACKUP":
                    self.data.backup_presets()
                    self.data.backup_patch()
                return 0
            elif self.mode == "ROOT":
                if event.keysym=="Escape":
                    
                    pass
                    #STORE = 0
                    #LABEL = 0

            elif self.mode == "INPUT":
                print(self.data.entry.get())
                if event.keycode == 36:
                    x=self.data.entry.get()
                    client.send(x)
                    #self.data.entry.clean()

                #self.data
                #chat.send("")
            elif self.mode == "INPUT2":
                print(self.data.entry2.get())
                if event.keycode == 36:
                    x=self.data.entry2.get()
                    client.send(x)
                    #self.data.entry.clean()

            elif self.mode == "INPUT3":
                print(self.data.entry3.get())
                if event.keycode == 36:
                    x=self.data.entry3.get()
                    client.send(x)
                    #self.data.entry.clean()

                #self.data
                #chat.send("")
            elif self.mode == "PRESET":
                nr = self.attr #int(self.attr.split(":")[1])-1
                if event.num == 1:
                    if STORE:
                        print("STORE PRESET")
                        sdata = {}
                        sdata["CFG"] = OrderedDict()
                        sdata["CFG"]["FADE"] = fade
                        sdata["CFG"]["DEALY"] = 0
                        sdata["CFG"]["BUTTON"] = "GO"
                        for fix in self.data.fixtures:                            
                            data = self.data.fixtures[fix]
                            for attr in data["ATTRIBUT"]:
                                if data["ATTRIBUT"][attr]["ACTIVE"]:
                                    if fix not in sdata:
                                        sdata[fix] = {}
                                    if attr not in sdata[fix]:
                                        sdata[fix][attr] = OrderedDict()
                                        if not STONY_FX:
                                            sdata[fix][attr]["VALUE"] = data["ATTRIBUT"][attr]["VALUE"]
                                            #sdata[fix][attr]["FADE"] = fade
                                        else:
                                            sdata[fix][attr]["VALUE"] = None #data["ATTRIBUT"][attr]["VALUE"]

                                        if "FX" not in data["ATTRIBUT"][attr]: 
                                             data["ATTRIBUT"][attr]["FX"] =""
                                        
                                        sdata[fix][attr]["FX"] = data["ATTRIBUT"][attr]["FX"] 
                    
                        print(sdata)
                        
                        self.data.val_presets[nr] = sdata
                        if len(sdata) > 1:
                            fx_color = 0
                            val_color = 0
                            for fix in sdata:
                                if fix == "CFG":
                                    continue
                                print( "$$$$",fix,sdata[fix])
                                for attr in sdata[fix]:
                                    if "FX" in sdata[fix][attr]:
                                        if sdata[fix][attr]["FX"]:
                                            fx_color = 1
                                    if "VALUE" in sdata[fix][attr]:
                                        if sdata[fix][attr]["VALUE"] is not None:
                                            val_color = 1

                            self.data.elem_presets[nr]["fg"] = "black"
                            if val_color:
                                self.data.elem_presets[nr]["bg"] = "yellow"
                                if fx_color:
                                    self.data.elem_presets[nr]["fg"] = "blue"
                            else:   
                                if fx_color:
                                    self.data.elem_presets[nr]["bg"] = "cyan"
                        else:
                            self.data.elem_presets[nr]["fg"] = "black"
                            self.data.elem_presets[nr]["bg"] = "grey"
                        #self.data.elem_presets[nr].option_add("*Font", FontBold)
                        label = ""
                        if nr in self.data.label_presets:
                            #print(dir(self.data))
                            label = self.data.label_presets[nr]

                        BTN="go"
                        if "CFG" in sdata:#["BUTTON"] = "GO"
                            if "BUTTON" in sdata["CFG"]:
                                BTN = sdata["CFG"]["BUTTON"]
                        txt = str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label 
                        self.data.elem_presets[nr]["text"] = txt 
                        print(self.data.val_presets)
                           
                        self.data.val_commands["STORE"] = 0
                        STORE = 0
                        self.data.elem_commands["STORE"]["bg"] = "lightgrey"
                    elif CFG_BTN:
                        import tkinter.simpledialog
                        txt = tkinter.simpledialog.askstring("CFG-BTN","GO,FLASH,TOGGLE,SWOP\n EXE:"+str(nr))
                        if "CFG" not in self.data.val_presets[nr]:
                            self.data.val_presets[nr]["CFG"] = OrderedDict()
                        if "BUTTON" not in self.data.val_presets[nr]["CFG"]:
                            self.data.val_presets[nr]["CFG"]["BUTTON"] = ""

                        self.data.val_presets[nr]["CFG"]["BUTTON"] = txt
                        sdata=self.data.val_presets[nr]
                        BTN="go"
                        if "CFG" in sdata:#["BUTTON"] = "GO"
                            if "BUTTON" in sdata["CFG"]:
                                BTN = sdata["CFG"]["BUTTON"]
                        label = self.data.label_presets[nr] # = label
                        txt=str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
                        self.data.elem_presets[nr]["text"] = txt
                        CFG_BTN = 0
                        self.data.elem_commands["CFG-BTN"]["bg"] = "grey"
                    elif LABEL:#else:
                        label = "lalaal"
                        import tkinter.simpledialog
                        label = tkinter.simpledialog.askstring("LABEL","Preset "+str(nr))
                        self.data.elem_presets[nr]["text"] = label
                        self.data.label_presets[nr] = label
                        sdata=self.data.val_presets[nr]
                        BTN="go"
                        if "CFG" in sdata:#["BUTTON"] = "GO"
                            if "BUTTON" in sdata["CFG"]:
                                BTN = sdata["CFG"]["BUTTON"]
                        txt=str(nr)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
                        #txt = "Preset:"+str(nr)+":\n"+str(len(l))+":"+label
                        self.data.elem_presets[nr]["text"] = txt
                        LABEL = 0
                        self.data.elem_commands["LABEL"]["bg"] = "lightgrey"
                    elif SELECT:
                        print("SELECT PRESET")
                        sdata = self.data.val_presets[nr]
                        cmd = ""
                        for fix in sdata:
                            if fix == "CFG":
                                continue
                            for attr in sdata[fix]:
                                v2 = sdata[fix][attr]["VALUE"]
                                v2_fx = sdata[fix][attr]["FX"]
                                #print( self.data.elem_attr)
                                elem = self.data.elem_attr[fix][attr]
                                #self#encoder(attr=attr,data=data,elem=elem,action="click")
                                self.data.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                                elem["bg"] = "yellow"
                    else:
                        print("GO PRESET")
                        if nr not in self.data.val_presets:
                            self.data.val_presets[nr] = OrderedDict()
                            self.data.val_presets[nr]["VALUE"] = 0
                            self.data.val_presets[nr]["FX"] = ""
                        sdata = self.data.val_presets[nr]
                        cmd = ""
                        for fix in sdata:
                            if fix == "CFG":
                                continue
                            for attr in sdata[fix]:
                                v2 = sdata[fix][attr]["VALUE"]
                                v2_fx = sdata[fix][attr]["FX"]
                                #print(fix,attr,v2, fix in self.data.fixtures,self.data.fixtures.keys(),2)
                                if fix in self.data.fixtures:
                                    #print("==",self.data.fixtures[fix]["ATTRIBUT"])
                                    #print( "==", attr, self.data.fixtures[fix], self.data.fixtures.keys(),4 )
                                    if attr in self.data.fixtures[fix]["ATTRIBUT"]:
                                        #print( attr)
                                        data = self.data.fixtures[fix]
                                        v=self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"]
                                        if v2 is not None:
                                            self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"] = v2
                                        self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
                                        if sdata["CFG"]["BUTTON"] == "SEL": #FLASH

                                            pdata = self.data.val_presets[nr]
                                            cmd = ""
                                            for fix in pdata:
                                                if fix == "CFG":
                                                    continue
                                                for attr in pdata[fix]:
                                                    v2 = pdata[fix][attr]["VALUE"]
                                                    v2_fx = pdata[fix][attr]["FX"]
                                                    #print( self.data.elem_attr)
                                                    elem = self.data.elem_attr[fix][attr]
                                                    #self#encoder(attr=attr,data=data,elem=elem,action="click")
                                                    self.data.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                                                    elem["bg"] = "yellow"


                                        xFLASH = 0
                                        if FLASH or sdata["CFG"]["BUTTON"] == "FL": #FLASH
                                            xFLASH = 1
                                        if str(event.type) == "ButtonRelease":
                                            if xFLASH:
                                                cmd+=update_dmx(attr,data,value="off",flash=xFLASH)
                                                if v2_fx:
                                                    cmd+=update_dmx(attr,data,pfx="fxf",value="off",flash=xFLASH)#,flash=FLASH)
                                        else:
                                            if fade_on:
                                                xfade = fade
                                            else:
                                                xfade = 0
                                            cmd+=update_dmx(attr,data,args=[xfade],flash=xFLASH)
                                            if v2_fx:
                                                cmd+=update_dmx(attr,data,pfx="fx",value=v2_fx,flash=xFLASH)#,flash=FLASH)
                                        #worker.fade_dmx(fix,attr,data,v,v2)
                        print("cmd",cmd) 
                        if cmd:
                            client.send(cmd )
                                        
                                
                        
                        #print(sdata)
                if event.num == 3:
                    if not STORE:
                        print("GO PRESET")
                        if nr not in self.data.val_presets:
                            self.data.val_presets[nr] = OrderedDict()
                            self.data.val_presets[nr]["VALUE"] = None
                            self.data.val_presets[nr]["FX"] = ""
                        sdata = self.data.val_presets[nr]
                        cmd = ""
                        for fix in sdata:
                            if fix == "CFG":
                                continue
                            for attr in sdata[fix]:
                                v2 = sdata[fix][attr]["VALUE"]
                                v2_fx = sdata[fix][attr]["FX"]
                                #print(fix,attr,v)
                                if fix in self.data.fixtures:
                                    #print("==",self.data.fixtures[fix]["ATTRIBUT"])
                                    if attr in self.data.fixtures[fix]["ATTRIBUT"]:
                                        data = self.data.fixtures[fix]
                                        v=self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"]
                                        if v2 is not None:
                                            self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"] = v2
                                        self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
                                        if str(event.type) == "ButtonRelease":
                                            if FLASH :
                                                cmd+=update_dmx(attr,data,value="off",flash=FLASH)
                                                if v2_fx:
                                                    cmd+=update_dmx(attr,data,pfx="fxf",value="off",flash=FLASH)#,flash=FLASH)
                                        else:
                                            cmd+=update_dmx(attr,data,args=[0],flash=FLASH)
                                            if v2_fx:
                                                cmd+=update_dmx(attr,data,pfx="fx",value=v2_fx,flash=FLASH)#,flash=FLASH)
                                        #worker.fade_dmx(fix,attr,data,v,v2)
                                  
                        if cmd:
                            client.send(cmd )
                                        
                                        
                                
                        
                return 0
            elif self.mode == "INPUT":
                return 0
            if self.mode == "ENCODER":
                #if self.attr == "VDIM":
                #    self.attr = "DIM"
                for fix in self.data.fixtures:
                    data = self.data.fixtures[fix]
                    
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
        #print(self.elem["text"],self.attr,self.data)
        
                                            
        
def wheel(event,d=None):
    print("wheel",event,d)
    
import copy

frame_fix = tk.Frame(root,bg="lightblue",width="100px")
frame_fix.pack(fill=tk.BOTH, side=tk.TOP)

class Master():
    def __init__(self):
        self.load()
        self.all_attr =["DIM","VDIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.commands =["BLIND","CLEAR","STORE","EDIT","","CFG-BTN","LABEL","SELECT"
                ,"BACKUP","SET","","","SELECT","ACTIVATE","FLASH","FADE"
                ,"STONY_FX","FX OFF", "FX:SIN","FX:COS","FX:CIR","SZ:","SP:","OF:"
                ,"FX:BUM","FX:BUM-","FX:FD","FX:ON","FX:ON-","FX:ON2","FX:ON2-" ]
        self.elem_commands = {}
        self.val_commands = {}

        self.elem_presets = {}
        self.load_presets()
        self.load_patch()
        
        for i in range(8*8):
            if i not in self.val_presets:
                name = "Preset:"+str(i+1)+":\nXYZ"
                #self.presets[i] = [i]
                self.val_presets[i] = OrderedDict() # FIX 
                self.val_presets[i]["CFG"] =  OrderedDict() # CONFIG 
                self.label_presets[i] = "-"

  
    def exit(self):
        print("__del__",self)
        self.backup_presets()
        print("********************************************************")
        self.backup_patch()
        print("*********del",self,"***********************************************")
    def load(self):
        fixture = OrderedDict()

        DATA = OrderedDict()
        DATA["DIM"]   = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        fix = {"DMX": 20, "UNIVERS": 2, "NAME": "D", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fix)
        fi["DMX"] = 1
        fi["NAME"] = "F1"
        fixture["1"] = fi
        fi = copy.deepcopy(fix)
        fi["DMX"] = 2
        fi["NAME"] = "F2"
        fixture["2"] = fi
        fi = copy.deepcopy(fix)
        fi["DMX"] = 3
        fi["NAME"] = "F3"        
        fixture["3"] = fi
        fi = copy.deepcopy(fix)
        fi["DMX"] = 4
        fi["NAME"] = "F4"        
        fixture["4"] = fi
        fi = copy.deepcopy(fix)
        fi["DMX"] = 11
        fi["NAME"] = "FL"
        fixture["11"] = fi
        fi = copy.deepcopy(fix)
        fi["DMX"] = 24
        fi["NAME"] = "P"
        fixture["24"] = fi
        
        DATA = OrderedDict()
        DATA["DIM"]   = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 4, "MASTER": "", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 5, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fix = {"DMX": 20, "UNIVERS": 2, "NAME": "IRGB", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fix)
        fi["DMX"] = 401
        fixture["1001"] = fi
        
        fi = copy.deepcopy(fix)
        fi["DMX"] = 421
        #fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        #fixture["1002"] = fi

        fi = copy.deepcopy(fix)
        fi["DMX"] = 441
        #fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        #fixture["1003"] = fi
        
        DATA = OrderedDict()
        DATA["VDIM"]  = {"NR": -1, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 2, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 1, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fix3 = {"DMX": 20, "UNIVERS": 2, "NAME": "V+RGB", "ATTRIBUT": DATA}


        fi = copy.deepcopy(fix3)
        fi["DMX"] = 330
        #fixture["2001"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 335
        #fixture["2002"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 240
        #fixture["2003"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 245
        #fixture["2004"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 250
        #fixture["2005"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 355
        #fixture["2006"] = fi


        
        DATA = OrderedDict()
        DATA["SHUTTER"]  = {"NR": 5,  "MASTER": "", "MODE": "S", "VALUE": 5.0,"ACTIVE":0}
        DATA["VDIM"]     = {"NR": -1, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["PAN"]      = {"NR": 0, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["PAN-FINE"] = {"NR": 1, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT"]     = {"NR": 2, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT-FINE"]= {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["RED"]      = {"NR": 6, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"]    = {"NR": 7, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]     = {"NR": 8, "MASTER": "1", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fixTMH = {"DMX": 20, "UNIVERS": 2, "NAME": "MH-BEAM", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fixTMH)
        fi["DMX"] = 241
        fixture["3001"] = fi

        fi = copy.deepcopy(fixTMH)
        fi["DMX"] = 261
        fixture["3002"] = fi

         
        DATA = OrderedDict()
        DATA["DIM"]  = {"NR": 17, "MASTER": "1", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["PAN"]   = {"NR": 0, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["PAN-FINE"]   = {"NR": 1, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT"]  = {"NR": 2, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT-FINE"]  = {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["COLOR"]   = {"NR": 8, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["GOBO"] = {"NR": 9, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["G-ROT"]  = {"NR": 8, "MASTER": "", "MODE": "S", "VALUE": 192.0,"ACTIVE":0}
        DATA["PRISMA"] = {"NR": 10, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["P-ROT"] = {"NR": 11, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["FOCUS"] = {"NR": 14, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["ZOOM"] = {"NR": 13, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["FROST"] = {"NR": 15, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["SHUTTER"] = {"NR": 16, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["CONTROL"]  = {"NR": 5, "MASTER": "", "MODE": "S", "VALUE": 5.0,"ACTIVE":0}
        fixREUSH = {"DMX": 300, "UNIVERS": 2, "NAME": "RUSH-BEAM", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 220
        fixture["701"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 201
        fixture["702"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 277
        fixture["703"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 296
        fixture["704"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 239
        fixture["705"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 258
        fixture["706"] = fi
        

        
       
        #self.fixtures = fixture
        
        
    def load_patch(self):
        filename="patch"
        d,l = self._load(filename)
        self.fixtures = OrderedDict()
        for i in l:
            sdata = d[i]
            for attr in sdata["ATTRIBUT"]:
                sdata["ATTRIBUT"][attr]["ACTIVE"] = 0
            print("load",filename,sdata)
            #if "CFG" not in sdata:
            #    sdata["CFG"] = OrderedDict()
            self.fixtures[str(i)] = sdata
        #self.label_presets = l
        
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
            if "ATTRIBUT" in jdata:  # translate old fixtures start with 0 to 1          
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
        
    def backup_patch(self):
        filename = "patch"
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        self._backup(filename,data,labels)
    def backup_presets(self):
        filename = "presets"
        data   = self.val_presets
        labels = self.label_presets
        self._backup(filename,data,labels)
        
    def _backup(self,filename,data,labels):
        #fixture
        xfname = "show/"+show_name+"/"+str(filename)+".sav"
        print("backup",xfname)
        f = open(xfname,"w")
        for key in data:
            line = data[key]
            print(line)
            label = "label" 
            if key in labels:
                label = labels[key]
            if label == "Name-"+str(key):
                label = ""
            print(xfname,"load",key,label,len(line))
            f.write( "{}\t{}\t{}\n".format( key,label,json.dumps(line) ) )
        f.close()
            
    def draw_dim(self,fix,data,c=0,r=0,frame=None):
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
            b = tk.Button(frame,bg="lightblue", text=""+str(fix)+" "+data["NAME"],width=4)
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=6)
            self.elem_attr[fix][attr] = b
            b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=12:
                c=0
                r+=1
        return c,r
    def draw_fix(self,fix,data):
        i=0
        c=0
        r=0
        frame = tk.Frame(frame_fix,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Button(frame,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
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
            
            b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=8)
            self.elem_attr[fix][attr] = b
            b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=1
                r+=1
                
    def draw_enc(self):
        i=0
        c=0
        r=0
        #frame = tk.Frame(root,bg="black")
        #frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r=0
        
        frame = tk.Frame(root2,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        
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
            if c >=7:
                c=0
                r+=1
    def draw_command(self):
        i=0
        c=0
        r=0
        #frame = tk.Frame(root,bg="black")
        #frame.pack(fill=tk.X, side=tk.TOP)

        #b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
        #b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r=0
        
        frame = tk.Frame(root2,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="COMM.",width=6)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
        c+=1
        for comm in self.commands:
            v=0
            
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6)
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
            if comm == "OF:":
                b["text"] = "OF:{:0.0f}".format(fx_prm["OFFSET"])
            if comm:
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=6:
                c=0
                r+=1
    def draw_preset(self):
        i=0
        c=0
        r=0
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r=0
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="EXEC")
        #b.bind("<Button>",Xevent(elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r+=1      
        for k in self.val_presets:
            v=0
            label = ""
            if k in self.label_presets:
                label = self.label_presets[k]
                print([label])

            sdata=self.val_presets[k]
            BTN="go"
            if "CFG" in sdata:#["BUTTON"] = "GO"
                if "BUTTON" in sdata["CFG"]:
                    BTN = sdata["CFG"]["BUTTON"]
            txt=str(k)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label
            b = tk.Button(frame,bg="grey", text=txt,width=8,height=2)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            
            if k in self.val_presets and len(self.val_presets[k]) :
                b["bg"] = "yellow"
                sdata = self.val_presets[k]
                if len(sdata) > 1:
                    fx_color = 0
                    val_color = 0
                    for fix in sdata:
                        if fix == "CFG":
                            continue
                        print( "$$$$",fix,sdata[fix])
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
            
            if k not in self.elem_presets:
                self.elem_presets[k] = b
                #self.val_presets[preset] = 0
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

        b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
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
    def render(self):
        r=0
        c=0
        Xroot.bind("<Key>",Xevent(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        dim_frame = tk.Frame(frame_fix,bg="black")
        dim_frame.pack(fill=tk.X, side=tk.TOP)
        for fix in self.fixtures:
            data = self.fixtures[fix]
            print( fix )
            
            if(len(data["ATTRIBUT"].keys()) <= 1):
                c,r=self.draw_dim(fix,data,c=c,r=r,frame=dim_frame)
            else:
                self.draw_fix(fix,data)
        self.draw_enc()
        self.draw_command()
        self.draw_input()
        self.draw_preset()
        
try:
    master =Master()
    master.render()

    root.mainloop()
    
finally:
    master.exit()

