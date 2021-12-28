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

import json
import time
import sys
import _thread as thread

import tkinter
import tkinter as tk
from tkinter import font


import lib.chat as chat
import lib.motion as motion

root = tk.Tk()
root["bg"] = "grey" #white
root.title( __file__)
#default_font = font.Font(family='Helvetica', size=12, weight='bold')
Font = font.Font(family='Helvetica', size=9, weight='normal')
FontBold = font.Font(family='Helvetica', size=9, weight='bold')
#default_font.configure(size=9)
root.option_add("*Font", Font)


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

def update_dmx(attr,data):
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


            
class Worker():
    def __init__(self):
        self.fade = OrderedDict()
        self.timer = time.time()
    def loop(self):
        while 1:
            self.next()
            
    def next(self):
        if self.timer+(1/30.) < time.time():
            try:
                lock.acquire()
                #if self.timer+1 < time.time():
                self.timer = time.time()
                #print("next")
                for fix in self.fade:
                    for attr in self.fade[fix]:
                        if 1:#len(self.fade[])>=2:
                            fd=self.fade[fix][attr][0]
                            xx=fd.next()
                            if xx:
                                x=fd.value
                                #print("fade",xx,xx)
                                data=self.fade[fix][attr][1]
                                try:   
                                    data["ATTRIBUT"][attr]["VALUE"] = x                       
                                    update_dmx(attr,data)                            
                                except Exception as e:
                                    print("next EXCEPTION",e)
            finally:
                #lock.acquire()
                lock.release()               
                            
        else:
            time.sleep(0.1)
    
    def fade_dmx(self,fix,attr,data,v,v2,ft=None):
        if ft is None:
            ft = 4
        if data["ATTRIBUT"][attr]["MODE"] == "S":
            ft=0
        #print("fade_dmx",fix,attr,v,v2)
        try:
            lock.acquire()
            if fix not in self.fade:
                self.fade[fix] = OrderedDict()
            if attr not in self.fade[fix]:
                self.fade[fix][attr] = OrderedDict()
            self.fade[fix][attr] = [motion.FadeFast(v,v2,ft),data]
        finally:
            #lock.acquire()
            lock.release()
        

worker = Worker()
lock = thread.allocate_lock()
thread.start_new_thread(worker.loop,())

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
            v2 = v
            v = data["ATTRIBUT"][attr]["VALUE"]
            data["ATTRIBUT"][attr]["VALUE"] = v2
            elem["text"] = str(attr)+' '+str(round(v2,2))
            worker.fade_dmx(fix,attr,data,v,v2,ft=0)
            #update_dmx(attr=attr,data=data)

        


            
    def cb(self,event):
        #print("cb",self,event,data)
        print("cb",self.attr,self.mode,event)
        #print(self.obj.keys())
        try:
            #v = self.data["ATTRIBUT"][self.attr]
            global STORE
            global BLIND
            change = 0
            
            if self.mode == "COMMAND":
                
                if self.attr == "CLEAR":
                    if event.num == 1:

                        if STORE:
                            self.data.val_commands["STORE"] = 0
                            STORE = 0
                            self.data.elem_commands["STORE"]["bg"] = "lightgrey"

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

                        
                elif self.attr == "BLIND":
                    
                    if event.num == 1:
                        
                        if self.data.val_commands[self.attr]:
                            self.data.val_commands[self.attr] = 0
                            BLIND = 0
                            self.data.elem_commands[self.attr]["bg"] = "lightgrey"
                        else:
                            self.data.val_commands[self.attr] = 1
                            BLIND = 1
                            self.data.elem_commands[self.attr]["bg"] = "red"
                        print("BLIND",self.data.val_commands)
                
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
                return 0
            elif self.mode == "PRESET":
                nr = self.attr #int(self.attr.split(":")[1])-1
                if event.num == 1:
                    if STORE:
                        print("STORE PRESET")
                        sdata = {}
                        for fix in self.data.fixtures:                            
                            data = self.data.fixtures[fix]
                            for attr in data["ATTRIBUT"]:
                                if data["ATTRIBUT"][attr]["ACTIVE"]:
                                    if fix not in sdata:
                                        sdata[fix] = {}
                                    if attr not in sdata[fix]:
                                        sdata[fix][attr] = data["ATTRIBUT"][attr]["VALUE"]
                    
                        print(sdata)
                        
                        self.data.val_presets[nr] = sdata
                        if len(sdata):
                            self.data.elem_presets[nr]["bg"] = "yellow"
                        else:
                            self.data.elem_presets[nr]["bg"] = "grey"
                        #self.data.elem_presets[nr].option_add("*Font", FontBold)
                        label = ""
                        if nr in self.data.label_presets:
                            #print(dir(self.data))
                            label = self.data.label_presets[nr]
                        self.data.elem_presets[nr]["text"] = "Preset:"+str(nr)+":\n"+str(len(sdata))+":"+label
                        print(self.data.val_presets)
                           
                        self.data.val_commands["STORE"] = 0
                        STORE = 0
                        self.data.elem_commands["STORE"]["bg"] = "lightgrey"
                    else:
                        print("GO PRESET")
                        if nr not in self.data.val_presets:
                            self.data.val_presets[nr] = OrderedDict()
                        sdata = self.data.val_presets[nr]
                        for fix in sdata:
                            for attr in sdata[fix]:
                                v2 = sdata[fix][attr]
                                #print(fix,attr,v)
                                if fix in self.data.fixtures:
                                    #print("==",self.data.fixtures[fix]["ATTRIBUT"])
                                    if attr in self.data.fixtures[fix]["ATTRIBUT"]:
                                        data = self.data.fixtures[fix]
                                        v=self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"]
                                        
                                        self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"] = v2
                                        self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
                                        #update_dmx(attr,data)
                                        worker.fade_dmx(fix,attr,data,v,v2)
                                  
                                        
                                
                        
                        print(sdata)
                if event.num == 3:
                    if not STORE:
                        print("GO PRESET 3")
                        if nr not in self.data.val_presets:
                            self.data.val_presets[nr] = OrderedDict()
                        sdata = self.data.val_presets[nr]
                        for fix in sdata:
                            for attr in sdata[fix]:
                                v2 = sdata[fix][attr]
                                #print(fix,attr,v)
                                if fix in self.data.fixtures:
                                    #print("==",self.data.fixtures[fix]["ATTRIBUT"])
                                    if attr in self.data.fixtures[fix]["ATTRIBUT"]:
                                        data = self.data.fixtures[fix]
                                        v=self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"]
                                        #self.data.fixtures[fix]["ATTRIBUT"][attr]["VALUE"] = v
                                        #print(str(attr)+' '+str(round(v,2)))
                                        #self.data.elem_attr[fix][attr]["text"] = str(attr)+' '+str(round(v,2))
                                        #update_dmx(attr,data)
                                        print("go",fix,attr,v,v2)
                                        worker.fade_dmx(fix,attr,data,v,v2,ft=0)
                                        
                                
                        
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
                            #self.encoder(attr=attr,data=data,elem=elem,action="click")
                            data["ATTRIBUT"][attr]["ACTIVE"] = 1
                            elem["bg"] = "yellow"
                            

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
        self.all_attr =["DIM","VDIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.commands =["BLIND","CLEAR","STORE","EDIT","","","","BACKUP","SET","","SELECT","ACTIVATE","","","",]
        self.elem_commands = {}
        self.val_commands = {}

        self.presets = OrderedDict()
        self.elem_presets = {}
        self.val_presets = OrderedDict()
        self.label_presets = OrderedDict()
        x=self.load_presets()
        
        for i in range(8*6):
            if i not in self.presets:
                name = "Preset:"+str(i+1)+":\nXYZ"
                self.presets[i] = [i]
                self.val_presets[i] = OrderedDict()
                self.label_presets[i] = ""
        
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
        #fixture["1001"] = fi
        
        fi = copy.deepcopy(fix)
        fi["DMX"] = 421
        fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        #fixture["1002"] = fi

        fi = copy.deepcopy(fix)
        fi["DMX"] = 441
        fi["ATTRIBUT"]["BLUE"]["VALUE"] = 22
        #fixture["1003"] = fi
        
        DATA = OrderedDict()
        DATA["VDIM"]  = {"NR": -1, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["RED"]   = {"NR": 2, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["GREEN"] = {"NR": 1, "MASTER": "1", "MODE": "F", "VALUE": 255.0,"ACTIVE":0}
        DATA["BLUE"]  = {"NR": 0, "MASTER": "1", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        fix3 = {"DMX": 20, "UNIVERS": 2, "NAME": "V+RGB", "ATTRIBUT": DATA}


        fi = copy.deepcopy(fix3)
        fi["DMX"] = 330
        fixture["2001"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 335
        fixture["2002"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 240
        fixture["2003"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 245
        fixture["2004"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 250
        fixture["2005"] = fi
        fi = copy.deepcopy(fix3)
        fi["DMX"] = 355
        fixture["2006"] = fi


        
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
        #fixture["2001"] = fi

        fi = copy.deepcopy(fixTMH)
        fi["DMX"] = 461
        #fixture["2002"] = fi

         
        DATA = OrderedDict()
        DATA["DIM"]  = {"NR": 17, "MASTER": "1", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["PAN"]   = {"NR": 0, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["PAN-FINE"]   = {"NR": 1, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT"]  = {"NR": 2, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["TILT-FINE"]  = {"NR": 3, "MASTER": "", "MODE": "F", "VALUE": 127.0,"ACTIVE":0}
        DATA["COLOR"]   = {"NR": 8, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["GOBO"] = {"NR": 9, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["G-ROT"]  = {"NR": 8, "MASTER": "", "MODE": "S", "VALUE": 192.0,"ACTIVE":0}
        DATA["PRINSMA"] = {"NR": 10, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["P-ROT"] = {"NR": 11, "MASTER": "", "MODE": "S", "VALUE": 0.0,"ACTIVE":0}
        DATA["FOCUS"] = {"NR": 14, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["ZOOM"] = {"NR": 13, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["FROST"] = {"NR": 15, "MASTER": "", "MODE": "F", "VALUE": 0.0,"ACTIVE":0}
        DATA["CONTROL"]  = {"NR": 5, "MASTER": "", "MODE": "S", "VALUE": 5.0,"ACTIVE":0}
        fixREUSH = {"DMX": 300, "UNIVERS": 2, "NAME": "RUSH-BEAM", "ATTRIBUT": DATA}

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 201
        fixture["701"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 220
        fixture["702"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 239
        fixture["703"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 258
        fixture["704"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 277
        fixture["705"] = fi

        fi = copy.deepcopy(fixREUSH)
        fi["DMX"] = 296
        fixture["706"] = fi
        

        
       
        self.fixtures = fixture

    def load_presets(self):
        print("load_presets")
        f = open("preset.sav","r")
        lines = f.readlines()
        f.close()    
        self.val_presets = OrderedDict()
        self.presets = OrderedDict()
        for line in lines:
            
            key,label,data = line.split("\t",2)
            key = int(key)
            print("load_presets",key)
            data = json.loads(data)
            self.val_presets[key] = data
            self.label_presets[key] = label
            self.presets[key] = 0
        return self.val_presets
        
    def backup_presets(self):
        print("backup_presets")
        f = open("preset.sav","w")
        for key in self.val_presets:
            preset = self.val_presets[key]
            label = ""#"Name-"+str(key)
            if key in self.label_presets:
                label = self.label_presets[key]
            if label == "Name-"+str(key):
                label = ""
            f.write(str(key)+"\t"+label+"\t"+json.dumps(preset)+"\n")
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
        frame = tk.Frame(root,bg="black")
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
            if c >=14:
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
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        
        b = tk.Button(frame,bg="lightblue", text="ENCODER",width=10)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
        c+=1
        for attr in self.all_attr:
            if attr.endswith("-FINE"):
                continue
            v=0
            b = tk.Button(frame,bg="orange", text=str(attr)+'',width=10)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=attr,data=self,mode="ENCODER").cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            if c >=10:
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
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
       
        b = tk.Button(frame,bg="lightblue", text="COMMANDS",width=10)
        #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
        
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        #r+=1
        c+=1
        for comm in self.commands:
            v=0
            
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=10)
            if comm not in self.elem_commands:
                self.elem_commands[comm] = b
                self.val_commands[comm] = 0
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=self,mode="COMMAND").cb)
            if comm:
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

        b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
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
            label = ""
            if k in self.label_presets:
                label = self.label_presets[k]
                print(label)
            b = tk.Button(frame,bg="grey", text="Preset:"+str(k)+"\n"+str(len(self.val_presets[k]))+":"+label,width=8,height=2)
            b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
            
            if k in self.val_presets and len(self.val_presets[k]) :
                b["bg"] = "yellow"
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
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

        b = tk.Label(frame,bg="black", text="--------------------------------------- ---------------------------------------")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        r=0
        
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
        
        b = tk.Label(frame, text="send:")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Entry(frame,bg="grey", text="",width=39)
        b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT").cb)
        b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=self,mode="INPUT").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
    def render(self):
        r=0
        c=0
        dim_frame = tk.Frame(root,bg="black")
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
        
        

master =Master()
master.render()


root.mainloop()
sys.exit()
    
