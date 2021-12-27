#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of librelight.

librelight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

librelight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with librelight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""

import time
import tkinter 
import sys
import _thread as thread
import tkinter as tk

from tkinter import font


import lib.chat as chat

root = tk.Tk()
root["bg"] = "red"

#default_font = font.Font(family='Helvetica', size=12, weight='bold')
default_font = font.Font(family='Helvetica', size=10, weight='normal')
#default_font.configure(size=9)
root.option_add("*Font", default_font)


from collections import OrderedDict


CUES    = OrderedDict()
groups  = OrderedDict()

BLIND = 0
STORE = 0
POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]
client = chat.tcp_sender()

class Xevent():
    def __init__(self,elem,attr=None,data=None,mode=None):
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode
    def encoder(self,attr,data,elem,action=""):
        if action == "click":
            if self.data["ATTRIBUT"][attr]["ACTIVE"]:
                self.data["ATTRIBUT"][attr]["ACTIVE"] = 0
                self.elem["bg"] = "grey"
            else:
                self.data["ATTRIBUT"][attr]["ACTIVE"] = 1
                self.elem["bg"] = "yellow"
            return 1

    
        v=data["ATTRIBUT"][attr]["VALUE"]
        change=0
        if action == "+":
            v+= 4.11
            change=1
        elif action == "-":
            v-= 4.11
            change=1

            
        if v < 0:
            v=0
        elif v > 256:
            v=256
            
        if change:
            data["ATTRIBUT"][attr]["ACTIVE"] = 1
            elem["bg"] = "yellow"
            data["ATTRIBUT"][attr]["VALUE"] = v
            elem["text"] = str(attr)+' '+str(round(v,2))
            self.update_dmx(attr=attr,data=data)
            
            
    def update_dmx(self,attr,data):
        global BLIND
        dmx = data["DMX"]
        val = None
        if attr == "VDIM":
            for attr in data["ATTRIBUT"]:
                dmx = data["DMX"]
                if data["ATTRIBUT"][attr]["NR"] < 0:
                    continue
                dmx += data["ATTRIBUT"][attr]["NR"]
                #print(attr)
                val = data["ATTRIBUT"][attr]["VALUE"]
                if data["ATTRIBUT"][attr]["MASTER"]:
                    val = val * (data["ATTRIBUT"]["VDIM"]["VALUE"] / 255.)
                if val is not None:            
                    cmd = "d{}:{}".format(dmx,int(val))
                    #print("cmd",cmd)
                    if not BLIND:
                        client.send(cmd )
                    else:
                        pass#print("BLIND ! cmd",cmd)
                    
            
        elif data["ATTRIBUT"][attr]["NR"] >= 0:
            dmx += data["ATTRIBUT"][attr]["NR"]
            val = data["ATTRIBUT"][attr]["VALUE"]
            if data["ATTRIBUT"][attr]["MASTER"]:
                if "VDIM" in data["ATTRIBUT"]:
                    val = val * (data["ATTRIBUT"]["VDIM"]["VALUE"] / 255.)
            if val is not None:            
                cmd = "d{}:{}".format(dmx,int(val))
                #print("cmd",cmd)
                if not BLIND:
                    client.send(cmd )
                else:
                    pass#print("BLIND ! cmd",cmd)

            
    def cb(self,event):
        #print("cb",self,event,data)
        print("cb",self.attr,self.mode,event)
        #print(self.obj.keys())
        try:
            #v = self.data["ATTRIBUT"][self.attr]
            
            change = 0
            if self.mode == "COMMAND":
                global STORE
                global BLIND
                if self.attr == "CLEAR":
                    if event.num == 1:

                        if STORE:
                            self.data.val_commands["STORE"] = 0
                            STORE = 0
                            self.data.elem_commands["STORE"]["bg"] = "white"

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

                        
                if self.attr == "BLIND":
                    
                    if event.num == 1:
                        
                        if self.data.val_commands[self.attr]:
                            self.data.val_commands[self.attr] = 0
                            BLIND = 0
                            self.data.elem_commands[self.attr]["bg"] = "white"
                        else:
                            self.data.val_commands[self.attr] = 1
                            BLIND = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                        print("BLIND",self.data.val_commands)

                if self.attr == "STORE":
                    
                    if event.num == 1:
                        
                        if self.data.val_commands[self.attr]:
                            self.data.val_commands[self.attr] = 0
                            STORE = 0
                            self.data.elem_commands[self.attr]["bg"] = "white"
                        else:
                            self.data.val_commands[self.attr] = 1
                            STORE = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                        print("BLIND",self.data.val_commands)
                        
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
                            #self.encoder(attr=attr,data=data,elem=elem,action="click")
                            data["ATTRIBUT"][attr]["ACTIVE"] = 1
                            elem["bg"] = "yellow"
                            

                        if not data["ATTRIBUT"][attr]["ACTIVE"]:
                            continue
                        
                        if event.num == 4:
                            self.encoder(attr=attr,data=data,elem=elem,action="+")
                            #if attr == "DIM":
                            #    self.encoder(attr="VDIM",data=data,elem=elem,action="+")
                        elif event.num == 5:
                            self.encoder(attr=attr,data=data,elem=elem,action="-")
                            #if attr == "DIM":
                            #     self.encoder(attr="VDIM",data=data,elem=elem,action="-")
                return 0
                                


                
            if event.num == 1:
                self.encoder(attr=self.attr,data=self.data,elem=self.elem,action="click")

            elif event.num == 4:
                self.encoder(attr=self.attr,data=self.data,elem=self.elem,action="+")
            elif event.num == 5:
                self.encoder(attr=self.attr,data=self.data,elem=self.elem,action="-")
            

                

        
        except Exception as e:
            print("== cb EXCEPT",e)
            print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        #print(self.elem["text"],self.attr,self.data)
        
                                            
        
def wheel(event,d=None):
    print("wheel",event,d)
    
import copy

class Master():
    def __init__(self):
        self.load()
        self.all_attr =[]
        self.elem_attr = {}
        
        self.commands =["BLIND","CLEAR","STORE"]
        self.elem_commands = {}
        self.val_commands = {}

        self.presets = OrderedDict()
        self.elem_presets = {}
        for i in range(8*6):
            self.presets["Preset"+str(i)] = [1]
        
    def load(self):
        fixture = OrderedDict()
        
        DATA = OrderedDict()
        DATA["DIM"]   = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 4, "MASTER": "", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 5, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fix = {"DMX": 20, "UNIVERS": 2, "NAME": "IRGB", "ATTRIBUT": DATA}

        DATA = OrderedDict()
        DATA["VDIM"]  = {"NR": -1, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 2, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 1, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fix3 = {"DMX": 20, "UNIVERS": 2, "NAME": "V+RGB", "ATTRIBUT": DATA}

        DATA = OrderedDict()
        DATA["DIM-FINE"]  = {"NR": 8, "MASTER": "", "MODE": "F", "VALUE": 5.0,"ACTIVE":0}
        DATA["VDIM"]  = {"NR": -1, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["PAN"]   = {"NR": 0, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["PAN-FINE"]   = {"NR": 1, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT"]  = {"NR": 2, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT-FINE"]  = {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 6, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 7, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 8, "MASTER": "1", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fixTMH = {"DMX": 20, "UNIVERS": 2, "NAME": "MH-BEAM", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fixTMH)
        fi["DMX"] = 241
        fixture["2001"] = fi

        fi = copy.deepcopy(fixTMH)
        fi["DMX"] = 461
        fixture["2002"] = fi

        fi = copy.deepcopy(fix3)
        fi["DMX"] = 441
        fixture["2003"] = fi

        fi = copy.deepcopy(fix3)
        fi["DMX"] = 461
        fixture["2005"] = fi
        

        
        fi = copy.deepcopy(fix)
        fi["DMX"] = 401
        fixture["1001"] = fi
        
        fi = copy.deepcopy(fix)
        fi["DMX"] = 421
        fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        fixture["1002"] = fi

        fi = copy.deepcopy(fix)
        fi["DMX"] = 441
        fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        fixture["1003"] = fi
        
        self.fixtures = fixture
        self.preset = OrderedDict()
        #["IRIS   OPEN", {"74": {"IRIS": 0.0, "_activ": 1, "_selection_nr": 1}}],
        for i in range(60):
            self.preset["NAME"] = "PRESET "+str(i+1)
            DATA = OrderedDict()
            DATA["2001"] = {"VDIM":200,"RED":2}
            DATA["2002"] = {"VDIM":100,"RED":2}
            DATA["2003"] = {"VDIM":50,"RED":2}
            
            self.preset["DATA"] = DATA
            
            
    def draw_fix(self,fix,data):
        i=0
        c=0
        r=0
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Button(frame,bg="lightblue", text="FIX:"+str(fix)+" "+data["NAME"],width=20)
        b.bind("<Button>",Xevent(elem=b).cb)
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
            
            b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=10)
            self.elem_attr[fix][attr] = b
            b.bind("<Button>",Xevent(elem=b,attr=attr,data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
                
    def draw_enc(self):
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

        
        b = tk.Button(frame,bg="lightblue", text="ENCODER")
        #b.bind("<Button>",Xevent(elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r+=1      
        for attr in self.all_attr:
            if attr.endswith("-FINE"):
                continue
            v=0
            b = tk.Button(frame,bg="orange", text=str(attr)+'',width=10)
            b.bind("<Button>",Xevent(elem=b,attr=attr,data=self,mode="ENCODER").cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
    def draw_command(self):
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
       
        b = tk.Button(frame,bg="lightblue", text="COMMANDS")
        #b.bind("<Button>",Xevent(elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r+=1      
        for comm in self.commands:
            v=0
            
            b = tk.Button(frame,bg="white", text=str(comm),width=10)
            if comm not in self.elem_commands:
                self.elem_commands[comm] = b
                self.val_commands[comm] = 0
            b.bind("<Button>",Xevent(elem=b,attr=comm,data=self,mode="COMMAND").cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
    def draw_preset(self):
        i=0
        c=0
        r=0
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Label(frame, text="--------------------------------------- ---------------------------------------")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r=0
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="PRESET")
        #b.bind("<Button>",Xevent(elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r+=1      
        for k in self.presets:
            v=0
            b = tk.Button(frame,bg="white", text=str(k),height=2)
            b.bind("<Button>",Xevent(elem=b,attr=k,data=self,mode="COMMAND").cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=8:
                c=0
                r+=1
    def render(self):
        for fix in self.fixtures:
            data = self.fixtures[fix]
            print( fix)
            self.draw_fix(fix,data)
        self.draw_enc()
        self.draw_command()
        self.draw_preset()

master =Master()
master.render()


root.mainloop()

    
