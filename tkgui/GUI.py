
import _thread as thread
import time
import copy

from collections import OrderedDict

import tkinter 
tk = tkinter 

from idlelib.tooltip import Hovertip

import tkgui.dialog  as dialoglib
dialog = dialoglib.Dialog()

import __main__ as MAIN

from lib.cprint import *


import lib.mytklib as mytklib
import lib.fixlib  as fixlib
import lib.showlib as showlib
import lib.libtk   as libtk
import lib.tkevent as tkevent

        



class LOAD_FIXTURE():
    def __init__(self,parent=None,name="<name>"):
        self.name=name
        self.master = None
        self.parent=parent
        #self.x = _LOAD_FIXTURE(parent,name)
        #self.cb = self.x.cb
    def cb(self,event=None,fixture={}):
        print("LOAD_FIXTURE",self.name,event)
        print(self,"cb")
        self.parent.clear()
        if fixture:
            print(len(fixture))
            self.parent.load(fixture)


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
        self.canvas.bind("<Button>",libtk.Event("XXX").event)
        self.canvas.bind("<Key>",libtk.Event("XXX").event)
        self.canvas.bind("<KeyRelease>",libtk.Event("XXX").event)

        
        #self.bframe=tk.Frame(self.frame,relief=tk.GROOVE,bg="magenta")#,width=width,height=height,bd=bd)
        #self.bframe.pack(side="top",fill="both",expand=1) #x=0,y=0)
        #self.HFrame()
    def event(self,event,**args):
        input_event_blocker.set( self.e , self.e_txt)
        input_event_blocker.event(event) #,args)


    def HFrame(self,main=None):  
        self.el = tk.Label(self.hframe,text="Filter:")
        self.el.pack(side="left")
        self.e_txt = tk.StringVar()
        #self.e = tk.Entry(self.hframe,state="readonly",textvariable=self.e_txt)
        self.e = tk.Entry(self.hframe,textvariable=self.e_txt)
        #self.e = tk.Button(self.hframe,textvariable=self.e_txt,relief="sunken",width=20)
        self.e["bg"] = "#fff"
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        #self.e_txt.set(self.e_txt.get()+"<")
        self.e.bind("<Key>",self.event)
        self.e.bind("<Button>",self.event)
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
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="lightblue", text="NAME",width=14,anchor="w")
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
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



class GUIHandler():
    def __init__(self):
        pass
    def update(self,fix,attr,args={}):
        print("GUIHandler.update()",fix,attr,args)
        for i,k in enumerate(args):
            v = args[k] 
            #print("GUI-H", i,k,v)



class X_CLOCK():
    def __init__(self):
        self._last_label_id = 1
        self._label_ring = [ "labelA","labelB"]
        self.b = tk.Canvas()
        self.bb = tk.Canvas()
        self.xfont  = tk.font.Font(family="FreeSans", size=65, weight="bold")
        self.xfont1 = tk.font.Font(family="FreeSans", size=25, weight="bold")

        self.write_text(text1="text1",text2="text2")

    def write_text(self,text1="text1",text2="text2"):
        tag = self._label_ring[self._last_label_id]
        self.bb.create_text(170,41,text=text1,fill="#aa0" ,font=self.xfont,tag=tag)
        self.bb.create_text(160,91,text=text2,fill="#aa0" ,font=self.xfont1,tag=tag)
        self.delete_tag()
        time.sleep(0.2)

    def loop_clock(self,b=None):
        while 1:
            #print("x",self.bb,dir(self.bb))
            #print(self,"x")
            s = time.strftime("%X")
            d = time.strftime("%Y-%m-%d")
            try:
                self.write_text(text1=s,text2=d)
            except:
                break
                cprint("CLOSE XCLOCK",self)

    def delete_tag(self):
        self._last_label_id += 1
        if self._last_label_id >=len(self._label_ring ):
            self._last_label_id = 0
        tag = self._label_ring[self._last_label_id]
        self.bb.delete(tag)

    def draw_clock(self,gui,xframe,data=[]):
        #print("draw_clock",self)
        xframe.pack(fill="both",expand=1)
        frame = tk.Frame(xframe,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
        
        self.bb = tk.Canvas(frame,bg="black", height=105,bd=0,width=6,highlightthickness=0) 
        self.bb.pack(fill="both",expand=1)

        thread.start_new_thread(self.loop_clock,())

        return self.bb





def draw_sub_dim(gui,fix,data,c=0,r=0,frame=None):
    i=0
    if frame is None:
        frame = tk.Frame(root,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)

    if fix not in gui.elem_attr:
        gui.elem_attr[fix] = {}
        
    attr_list = []    
    for attr in data["ATTRIBUT"]:
        if attr not in gui.all_attr:
            gui.all_attr.append(attr)

        if attr not in gui.elem_attr[fix]:
            gui.elem_attr[fix][attr] = []
        
        if attr.endswith("-FINE"):
            continue
        if attr.startswith("_"):
            continue
        attr_list.append(attr)


    for attr in attr_list:#data["ATTRIBUT"]:
        v= data["ATTRIBUT"][attr]["VALUE"]
        b = tk.Button(frame,bg="lightblue", text=""+str(fix),width=3,anchor="w")
        b.config(padx=1)
        b.bind("<Button>",tkevent.tk_event(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="lightblue", text=data["NAME"],width=10,anchor="w")
        b.config(padx=1)
        b.bind("<Button>",tkevent.tk_event(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="grey", text="S",width=2,anchor="c")
        b.config(padx=1)
        myTip = Hovertip(b,'SELECT')
        b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b,attr="_ACTIVE",mode="ENCODER",data=data).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        gui.elem_attr[fix]["S"] = b
        c+=1
        b = tk.Button(frame,bg="grey", text=str(round(v,2)),width=10,anchor="w")
        b.config(padx=1)
        gui.elem_attr[fix][attr] = b
        b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=12:
            c=0
            r+=1
    return c,r



class GUI_DIM():
    def __init__(self,gui,xframe,data):
        self.gui = gui
        self.data = data
        self.xframe = xframe
        self.draw()
    def draw(self):
        FIXTURES = self.data
        gui=self.gui
        xframe=self.xframe

        r=0
        c=0
        frame_dim=xframe
        for widget in xframe.winfo_children():
            widget.destroy()


        root = frame_dim
        dim_frame = tk.Frame(root,bg="black")
        dim_frame.pack(fill=tk.X, side=tk.TOP)

        i=0
        c=0
        r=0
        dim_end=0
        for fix in FIXTURES.fixtures:
            i+=1
            data = FIXTURES.fixtures[fix]
            #print("DIMMER----",data)
            if fix not in gui.elem_attr:
                gui.elem_attr[fix] = {}
            
            kix = []
            for ix in data["ATTRIBUT"].keys():
                #print("DIMMER----",ix)
                if not ix.startswith("_") and not ix.endswith("-FINE"):
                    kix.append(ix)

            if "DIM" in kix and len(kix) == 1:
                c,r=draw_sub_dim(gui,fix,data,c=c,r=r,frame=dim_frame)



class GUI_FIX():
    def __init__(self,gui,xframe,data):
        self.gui = gui
        self.data = data
        self.xframe = xframe
        self.draw()

    def draw(self):
        FIXTURES = self.data
        gui=self.gui
        xframe=self.xframe

        r=0
        c=0
        frame_dim=xframe
        frame_fix=xframe
        for widget in xframe.winfo_children():
            widget.destroy()

        root = frame_dim
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
            if fix not in gui.elem_attr:
                gui.elem_attr[fix] = {}
            
            kix = []
            for ix in data["ATTRIBUT"].keys():
                if not ix.startswith("_") and not ix.endswith("-FINE"):
                    kix.append(ix)

            if "DIM" in kix and len(kix) == 1:
                continue


            if not dim_end:
                dim_end=1
                c=0
                r=0
            #gui._draw_fix(fix,data,root=fix_frame)
            frame = fix_frame
        
            b = tk.Button(frame,bg="lightblue", text="ID:"+str(fix),width=6,anchor="w")
            b.bind("<Button>",tkevent.tk_event(fix=fix,mode="SELECT",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="#55f", text=data["NAME"],width=10,anchor="w")
            b.bind("<Button>",tkevent.tk_event(fix=fix,attr="ALL",mode="ENCODER",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            b = tk.Button(frame,bg="grey", text="S",width=2,anchor="c")
            b.config(padx=1)
            myTip = Hovertip(b,'SELECT')
            b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b,attr="_ACTIVE",mode="ENCODER",data=data).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            gui.elem_attr[fix]["S"] = b
            c+=1

            #r+=1
            start_c=3
            c=start_c
            attr_list = []    
            for attr in data["ATTRIBUT"]:
                
                if attr.endswith("-FINE"):
                    continue
                #if attr.startswith("_"):
                #    continue
                attr_list.append(attr)


            for attr in attr_list:#data["ATTRIBUT"]:
                virtual = 0

                if attr not in gui.all_attr:
                    gui.all_attr.append(attr)
                if attr not in gui.elem_attr[fix]:
                    gui.elem_attr[fix][attr] = ["line1348",fix,attr]
                v= data["ATTRIBUT"][attr]["VALUE"]
                
                if data["ATTRIBUT"][attr]["NR"] <= 0:
                    virtual = 1
                
                if attr.startswith("_"):
                    continue
                if virtual:
                    b = tk.Button(frame,bg="darkgrey", text=str(attr)+' '+str(round(v,2)),relief="solid",width=12, anchor="w")
                else:
                    b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=12, anchor="w")
                gui.elem_attr[fix][attr] = b
                b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
                b.grid(row=r, column=c, sticky=tk.W+tk.E,ipadx=0,ipady=0,padx=0,pady=0)
                c+=1
                if c >=8:
                    c=start_c
                    r+=1
            c=0
            r+=1
            

        #master._refresh_exec()
        #master.refresh_exec()



class _SET_PATCH():
    def __init__(self,k,v,fix,data,_cb=None):
        self._cb = _cb
        self.v = v
        self.button = None
        self.k = k
        self.fix = fix
        self.data = data
    def attr(self,_event=None):
        k = self.k
        data = self.data
        fix = self.fix
        txt = "k={} v={}".format(self.k,self.v)
        print(txt)
        print( "fix", self.fix )
        print( "row data",self.data)
        val = ""
        if k in self.data:
            val = self.data[k]
        #txt = dialog.askstring("SET","SET: {}={}".format(self.k,self.v),initialvalue=val)
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print("_SET.attr",txt)
            v = txt
            if v is not None:
                err = 1
                if k in self.data:
                    if k == "NAME":
                        self.data[k] = v
                        err = 0
                    if k == "DMX":
                        v = int(v)
                        if v <= 512 and v >= 0:
                            self.data[k] = v
                            err = 0
                    if k == "UNIVERS":
                        v = int(v)
                        if v > 15:
                            v=15
                        if v < 0:
                            v=0
                        self.data[k] = v
                        err = 0

                if self.button:

                    if err:
                        self.button["bg"] = "red"
                    else:
                        self.button["bg"] = "#fff"
                        self.button["text"] = "{}".format(v)
                        if self._cb:
                            self._cb()
            print( "row data",self.data)

        dialog._cb = _cb
        dialog.askstring("SET","SET: {}={}".format(self.k,self.v),initialvalue=val)

    def set_button(self,button):
        self.button = button 



class GUI_PATCH():
    #def __init__(self,gui,yframe):
    def __init__(self,gui,yframe,data,head=None,foot=None):
        self.gui = gui
        self.yframe = yframe
        self.data = data

        self._head = head
        self._foot = foot

        self.fader_elem = []

        self.draw()

    def draw(self): #,gui,yframe):
        FIXTURES = self.data
        gui = self.gui
        yframe = self.yframe

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
        def head(i,c,r,xframe=None):
            b = tk.Button(xframe,bg="grey", text="Z:{} ID".format(z+1),width=6,anchor="e")
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="grey", text="NAME",width=14,anchor="w")
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            rgb  = "#aaa"
            b = tk.Button(xframe,bg=rgb, text="TYPE",width=8)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="Uni",width=3)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="DMX",width=2)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="CH's",width=4)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="from - to",width=8)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="DMX-SUM",width=6)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="TEST",width=4)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg=rgb, text="DMX Collision!",width=15)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="orange", text="DELETE",width=15)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            c=0
            r+=1
            return i,c,r
        #i,c,r = head(i,c,r)
        dmx_ch_sum = 0
        dmx_collision = {}

        for fix in FIXTURES.fixtures:
            data = FIXTURES.fixtures[fix]

            max_dmx = FIXTURES.get_max_dmx_nr(fix) 
            
            for i in range(data["DMX"],data["DMX"]+max_dmx[1]):
                k = "{}.{}".format(data["UNIVERS"],i)
                if k in dmx_collision:
                    dmx_collision[k] += 1
                else:
                    dmx_collision[k] = 0
        z=0
        print("F:H:",self._head,self._foot)
        if self._head:
            #l = tk.Label(self._head,text="llklk")
            #l.pack()
            head(0,0,0,xframe=self._head)

        for fix in FIXTURES.fixtures:
            #if z % 20 == 0:
            #    i,c,r = head(i,c,r,xframe=xframe)
            z+=1
            collision = []
            i+=1
            data = FIXTURES.fixtures[fix]
                            
            b = tk.Button(xframe,bg="lightblue", text=""+str(fix),width=6,anchor="e")
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            command = _SET_PATCH("NAME",data["NAME"],fix,data)
            b = tk.Button(xframe,bg="grey", text=data["NAME"],width=14,anchor="w",command=command.attr)
            command.set_button(b)
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            LABEL = ""
            if len(data["ATTRIBUT"]) == 1:
                LABEL = "DIMMER"
            elif  "PAN" in data["ATTRIBUT"] or  "TILT" in data["ATTRIBUT"] :
                LABEL = "MOVER"
            else:
                LABEL = {}
                for a in data["ATTRIBUT"]:
                    nr = data["ATTRIBUT"][a]["NR"]
                    if a[0] != "_":
                        LABEL[nr] = a[0]
                keys = list(LABEL.keys())
                keys.sort()
                L2 =""
                for k in keys:
                    L2 += LABEL[k]
                LABEL = L2

                    
            b = tk.Button(xframe,bg="#aaa", text=LABEL,width=8,anchor="w")
            #b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            b["activebackground"] = "#aaa"
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="EDIT",width=3)
            b.bind("<Button>",tkevent.tk_event(fix=fix,mode="SELECT",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="#ddd", text="[ ][x]",width=1)
            b.bind("<Button>",tkevent.tk_event(fix=fix,mode="SELECT",elem=b).cb)
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

                command = _SET_PATCH(k,v,fix,data) #,_cb=highlight2(fix) ) #,_cb=self.draw)
                b = tk.Button(xframe,bg="grey", text=str(v),width=2,command=command.attr)
                command.set_button(b)
                

                b.grid(row=r, column=c, sticky=tk.W+tk.E)
                c+=1
                if c >=8:
                    c=start_c
                    r+=1

            max_dmx = FIXTURES.get_max_dmx_nr(fix) 
            
            dmx_ch_sum += max_dmx[1]
            for i in range(data["DMX"],data["DMX"]+max_dmx[1]):
                k = "{}.{}".format(data["UNIVERS"],i)
                if k in dmx_collision:
                    if dmx_collision[k]:
                        collision.append(k)
            # CH's
            b = tk.Button(xframe,bg="#aaa", text="{:3} ({})".format(max_dmx[1] , max_dmx[0]),width=4) #a,anchor="w")
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            b["activebackground"] = "#aaa"
            c+=1
                
            # from - to    
            b = tk.Button(xframe,bg="#aaa", text="{:03} - {:03}".format(data["DMX"],max_dmx[1]+(data["DMX"]-1)),width=8,anchor="w")
            b["activebackground"] = "#aaa"
            b.grid(row=r, column=c, sticky=tk.W+tk.E)

            c+=1
            b = tk.Button(xframe,bg="#aaa",fg="#225", text="{} : {:03}".format(z,dmx_ch_sum),width=6,anchor="w")
            b["activebackground"] = "#aaa"
            b.grid(row=r, column=c, sticky=tk.W+tk.E)



            c+=1
            def x(fix):
                def xx():
                    print("TEST",fix)
                    if fix in FIXTURES.fixtures:
                        data = FIXTURES.fixtures[fix]
                        # print(data)
                        MAIN.highlight(fix)
                return xx

            #print(fix)
            #TEST BTN
            b = tk.Button(xframe,bg="grey",fg="#000", text="TEST",width=4,anchor="w",command=x(fix))
            myTip = Hovertip(b,'BLINK DIMMER')
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            #b.command = x
            #exit()

            c+=1
            bg = "#252"
            if collision:
                bg = "#f22"
            else: 
                collision = ""
            b = tk.Button(xframe,bg=bg, text="{}".format(",".join(collision)),width=14,anchor="w")
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            b["activebackground"] = bg

            c+=1
            def x_del(fix):
                def xx():
                    print( "DELETE FIXTURE !!!",fix)
                    if str(fix) in FIXTURES.fixtures:
                        del FIXTURES.fixtures[fix]
                return xx


            b = tk.Button(xframe,bg="orange",fg="#000", text="DELETE",width=12,anchor="w")
            b["command"] = x_del(fix)
            myTip = Hovertip(b,'DELETE FIXTURE')
            b.grid(row=r, column=c, sticky=tk.W+tk.E)

            c=0
            r+=1








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
            #self.b.bind("<Button>",tkevent.tk_event(fix=fix,elem=b).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            c+=1
            if c % 8 == 0:
                r+=1
                c=0
            i+=1
        self.frame.pack()















class EXEC_FADER():
    def __init__(self,frame,nr,cb=None,fader_cb=None,**args):
        self.frame = frame
        self.nr= nr
        self.id=nr
        self.elem = []
        self._cb = cb
        self._fader_cb = fader_cb
        width=11
        frameS = tk.Frame(self.frame,bg="#005",width=width)
        frameS.pack(fill=tk.Y, side=tk.LEFT)
        self.frame=frameS

    def fader_event(self,a1="",a2=""):
        print("   EXEC_FADER.fader_event",[self.nr,a1,a2],self.label["text"],self.attr["text"])
        if self._fader_cb:
            self._fader_cb(a1,a2,nr=self.nr)

    def event(self,a1="",a2=""):
        print("   EXEC_FADER.event",[self.nr,a1,a2],self.label["text"],self.attr["text"])
        if self._cb:
            self._cb(a1,a2,nr=self.nr)

    def set_attr(self,_event=None):
        txt= self.attr["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            print(self,"set_attr._cb()",data)
            if "Value" in data and type( data["Value"]) is str:
                txt = data["Value"]
                self._set_attr(txt)
        dialog._cb = _cb
        dialog.askstring("ATTR","set attr:",initialvalue=txt)
        
    def _set_attr(self,txt=""):
        if type(txt) is str:
            self.attr["text"] = "{}".format(txt)
            #print("_set_attr",[self])
    def set_label(self,name=""):
        #print("set_label",self.b,name)
        self.label["text"] = name
    def set_mode(self,_event=None):
        txt= self.mode["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"set_mode._cb()",txt)
            #w = MAIN.WindowContainer("config",master=1,width=200,height=140,left=L1,top=TOP)
            #w.pack()
            self._set_mode(txt)
            #w.show()
        dialog._cb = _cb
        dialog.askstring("MODE S/F:","SWITCH or FADE",initialvalue=txt)

    def _set_mode(self,txt=""):
        print("_set_mode",txt)
        if type(txt) is str:
            self.mode["text"] = "{}".format(txt[0].upper())
            #print("_set_mode",[self])
    def _refresh(self):
        pass

    def go(self,event=None,X=None,Y=None):
        print(self,"go()",event,self.attr["text"])
        #print(dir(event))
        print(event.num,event.state,event.type)
        nr = self.id+80
        if event.state > 0:
            value = 0
            MAIN.master.exec_go(nr-1,xfade=None,val=value)
        else:
            value = 1
            MAIN.master.exec_go(nr-1,xfade=None,val=value)

    def pack(self,init=None,from_=255,to=0,**args):
        width=11
        r=0
        c=0
        j=0
        self.font8 = ("FreeSans",8)
        frameS=self.frame
        self.b = tk.Scale(frameS,bg="lightblue", width=28,from_=from_,to=to,command=self.fader_event)
        self.b.pack(fill=tk.Y, side=tk.TOP)
        if init is not None:
            self.b.set(init)
        self.elem.append(self.b)

        self.b = tk.Button(frameS,bg="lightblue",text="{}".format(self.nr), width=5,command=libtk.test_command,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.label = self.b
        if 1: #self.nr <= 10:

            self.elem.append(self.b)
            self.b = tk.Button(frameS,bg="lightblue",text="", width=5,font=self.font8 )
            self.b.bind("<Button>",self.go) #BEvent({"NR":self.id+80,"text":""},self.go).cb)
            self.b.bind("<ButtonRelease>",self.go) #BEvent({"NR":self.id+80,"text":""},self.go).cb)
            #b = self.b
            #k = ""
            #gui = MAIN.master
            #self.b.bind("<Button>",tkevent.tk_event(fix=0,elem=b,attr=k,data=gui,mode="EXEC").cb)
            #self.b.bind("<ButtonRelease>",tkevent.tk_event(fix=0,elem=b,attr=k,data=gui,mode="EXEC").cb)
            self.attr=self.b
            self.b.pack(fill=tk.BOTH, side=tk.TOP)
            self.elem.append(self.b)
            f = tk.Frame(frameS)
        ##f.pack()
        #self.b = tk.Button(f,bg="lightblue",text="<+", width=1,command=self.set_mode,font=self.font8 )
        #self.mode=self.b
        ##self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        #self.elem.append(self.b)

        #self.b = tk.Button(frameS,bg="lightblue",text="F", width=4,command=self.set_mode,font=self.font8 )
        #self.mode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.TOP)
        ##self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        #self.elem.append(self.b)

        #self.b = tk.Button(f,bg="lightblue",text="+>", width=1,command=self.set_mode,font=self.font8 )
        #self.mode=self.b
        ##self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        #self.elem.append(self.b)

        self.b = tk.Label(frameS,bg="black",text="", width=4,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)



class GUI_ExecWingLayout():
    def __init__(self,root,frame,data,title="tilte",width=800,start=81):
        self.font8 = ("FreeSans",8)
        self.dmx=1
        self.univ=0
        self.start=start-1
        r=0
        c=0
        i=1
        self.elem=[]
        self.fader_elem = []
        self.header=[]
        self.data = data

        self.frame = tk.Frame(frame,bg="#000",width=width,border=2)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        r=0
        c=0
        pb=10
        self.pb=pb
        for j,row in enumerate(data):
            if c % pb == 0 or c==0:
                h=hex(j*10)[2:].rjust(2,"0")
                frameS = tk.Frame(self.frame,bg="#000",width=width,border=2)
                frameS.pack(fill=tk.BOTH, side=tk.TOP)
                p=j//pb+1
                if j < 10:
                    txt="x-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
                else:
                    txt="x-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
                self.b = tk.Label(frameS,bg="lightblue",text=txt,width=25,font=self.font8 )
                self.header.append(self.b)

                self.b.pack(fill=None, side=tk.LEFT)
                self.b = tk.Label(frameS,bg="black",text="" ,width=11,font=self.font8 )
                self.b.pack(fill=tk.BOTH, side=tk.LEFT)
                try:
                    frameS = tk.Frame(self.frame,bg="#a000{}".format(h),width=width,border=2)
                except:
                    frameS = tk.Frame(self.frame,bg="#a0aadd",width=width,border=2)
                c=0
            #print(frameS)
            #e= libtk.ELEM_FADER(frameS,nr=j+1,cb=self.event_cb)
            e= EXEC_FADER(frameS,nr=j+1,fader_cb=self.event_cb)
            if j >= 10:
                e.pack(from_=400,to=0,init=100)
            else:
                e.pack(from_=200,to=0,init=100)
            self.elem.append(e)
            self.fader_elem.append(e)
            frameS.pack(fill=tk.X, side=tk.TOP)
            c+=1
            i+=1
        self.frame.pack()
        self._event_redraw()

    def set_fader(self,nr,val,color="",info="info",change=0):
        mute = 1
        if nr == 2:
            mute = 1
        if info != "dmx_in":
            mute=1
        if not mute:print("set_fader",nr,val,info)
        if nr < len(self.elem):
            try:
                ee = self.elem[nr].elem[0]
                ee.set(val) 
                if color:
                    ee["bg"] = color
            except Exception as e:
                if change:
                    self.event_cb(a1=val,nr=nr)
                #cprint("set_fader",e,color="red")
                #raise e
        #self.frame.update_idle_task()
        if not mute:print("set_fader",nr,val,info)

        return # STOP

    def event_cb(self,a1="",a2="",nr=None,**args):
        #print(" ExecWing.event_cb:",nr,a1,a2,args)
        
        nr += 1
        jdata= {"CMD":"X-MASTER","NR":nr,"VALUE":int(a1)}

        if nr >= 1 and nr <= 10:
            jdata["CMD"] = "EXEC-SIZE-MASTER"
            jdata["NR"] = nr +self.start

        if nr >= 11 and nr <= 20:
            jdata["CMD"] = "EXEC-SPEED-MASTER"
            jdata["NR"] = nr-10 +self.start

        if nr >= 21 and nr <= 30:
            jdata["CMD"] = "EXEC-OFFSET-MASTER"
            jdata["NR"] = nr-20 +self.start

        #print("   ExecWing.event_cb",jdata)
        j = [jdata]
        MAIN.jclient_send(j)

    def set_name(self,_event=None):
        txt = self.name["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"._cb()",txt)
            self.name["text"] = "{}".format(txt)
            print("change_dmx",[_event,self])
        dialog._cb = _cb
        dialog.askstring("FIXTURE NAME:","NAME:",initialvalue=txt)

    def event_value(self,_event=None):
        nr=self.dmx
        txt= self.entry_dmx["text"]
        
    def _event_redraw(self,_event=None):
        nr = 0
        print("change_dmx",[_event,self])
        for i,btn in enumerate(self.elem):
            btn.set_label("{} D:{}".format(i+1,nr))
            btn.nr = nr+i

        pb=self.pb
        for j,e in enumerate(self.header):
            p=j+1
            #p=nr/pb
            if p == 1:
                txt="SIZE-MASTER:{} {}-{}".format(p,1+self.start,10+self.start)#p*pb-pb+1,p*pb) 
            elif p == 2:
                txt="SPEED-MASTER:{} {}-{}".format(p,1+self.start,10+self.start)#p*pb-pb+1,p*pb) 
            elif p == 3:
                txt="OFFSET-MASTER:{} {}-{}".format(p,1+self.start,10+self.start)#p*pb-pb+1,p*pb) 
            else:
                txt="X-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
            #txt="BANK:{} {}-{}".format(p,p*pb-pb+nr,p*pb+nr) 
            print("---",j,txt,e)
            e["text"] = txt
            
class GUI_MasterWingLayout():
    def __init__(self,root,frame,data,title="tilte",width=800):
        #xfont = tk.font.Font(family="FreeSans", size=5, weight="bold")
        self.font8 = ("FreeSans",8)
        self.dmx=1
        self.univ=0
        r=0
        c=0
        i=1
        self.elem=[]
        self.header=[]
        self.data = data
        #self.frame = tk.Frame(root,bg="black",width=width)
        #self.frame.pack(fill=tk.BOTH, side=tk.TOP)

        #self.b = tk.Label(self.frame,bg="#fff",text="Master Wing") #,font=font8 )
        #self.b.pack(fill=None, side=tk.LEFT)
        #self.frame = tk.Frame(root,bg="black",width=width)
        #self.frame.pack(fill=tk.BOTH, side=tk.TOP)

        #self.b = tk.Label(self.frame,bg="black",text="") # spacer
        #self.b.pack(fill=tk.Y, side=tk.LEFT)

        #self.frame = tk.Frame(root,bg="magenta",width=width,border=2) # fader frame
        #self.frame.pack(fill=tk.BOTH, side=tk.TOP)
        self.frame=frame
        r=0
        c=0
        pb=1
        self.pb=pb
        for j,row in enumerate(data):
            if c % pb == 0 or c==0:
                h=hex(j*10)[2:].rjust(2,"0")
                frameS = tk.Frame(self.frame,bg="#000",width=width,border=2)
                frameS.pack(fill=tk.BOTH, side=tk.TOP)
                p=j//pb+1
                if j < 1:
                    txt="x-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
                else:
                    txt="x-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
                self.b = tk.Label(frameS,bg="lightblue",text=txt,width=25,font=self.font8 )
                self.header.append(self.b)

                self.b.pack(fill=None, side=tk.LEFT)
                self.b = tk.Label(frameS,bg="black",text="" ,width=11,font=self.font8 )
                self.b.pack(fill=tk.BOTH, side=tk.LEFT)
                try:
                    frameS = tk.Frame(self.frame,bg="#a000{}".format(h),width=width,border=2)
                except:
                    frameS = tk.Frame(self.frame,bg="#a0aadd",width=width,border=2)
                c=0
            #print(frameS)
            e= libtk.ELEM_FADER(frameS,nr=j+1,fader_cb=self.event_cb)
            if j >= 2:
                e.pack(from_=400,to=0,init=100)
            else:
                e.pack(from_=200,to=0,init=100)
            self.elem.append(e)
            frameS.pack(fill=tk.X, side=tk.TOP)
            c+=1
            i+=1
        self.frame.pack()
        self._event_redraw()

    def event_cb(self,a1="",a2="",nr=None,**args):
        print(" MasterWing.event_cb:",nr,a1,a2,args)
        nr += 1
        jdata= {"CMD":"X-MASTER","NR":nr,"VALUE":int(a1)}
        if nr == 1:
            jdata["CMD"] = "SIZE-MASTER"
            jdata["NR"] = 1 #nr
        if nr == 2:
            jdata["CMD"] = "SPEED-MASTER"
            jdata["NR"] = 1 #nr 


        print(" MasterWing.event_cb",jdata)
        j = [jdata]
        MAIN.jclient_send(j)

    def set_name(self,_event=None):
        txt = self.name["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"._cb()",txt)
            self.name["text"] = "{}".format(txt)
            print("set_name",[_event,self])
        dialog._cb = _cb
        dialog.askstring("FIXTURE NAME:","NAME:",initialvalue=txt)

    def event_value(self,_event=None):
        nr=self.dmx
        txt= self.entry_dmx["text"]
        
    def _event_redraw(self,_event=None):
        nr = 0
        print("_event_redraw",[_event,self])
        for i,btn in enumerate(self.elem):
            btn.set_label("{} D:{}".format(i+1,nr))
            btn.nr = nr+i

        pb=self.pb
        for j,e in enumerate(self.header):
            p=j+1
            #p=nr/pb
            if p == 1:
                txt="SIZE-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
            else:
                txt="SPEED-MASTER:{} {}-{}".format(p,p*pb-pb+1,p*pb) 
            #txt="BANK:{} {}-{}".format(p,p*pb-pb+nr,p*pb+nr) 
            print("---",j,txt,e)
            e["text"] = txt


class BEvent():
    def __init__(self,data,cb):
        self._data = data
        self._cb = cb
    def cb(self,event):
        #print(self,event)
        self._cb(event,self._data)





class GUI_menu():
    def __init__(self,root,frame ,data,title="tilte"):
        global tk
        global INIT_OK
        self.frame = frame
        self.data = data
        self.elem = {}
        self.draw()

    def draw(self):
        cprint("***",self,"draw")
        r=0
        c=0
        i=1
        self.b = tk.Label(self.frame,bg="lightblue", text="MAIN:MENU",width=8,height=1)
        self.TITLE = self.b
        self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
        r+=1
        h = 2
        for row in self.data:
            print("  draw",row)
            #row = data[i]
            if row["text"] == "---":
                h=1
            if "name" in row:
                self.b = tk.Button(self.frame,bg="lightgrey", text=row["name"],width=8,height=h)
            else:
                self.b = tk.Button(self.frame,bg="lightgrey", text=row["text"],width=8,height=h)

            self.b.bind("<Button>",BEvent({"NR":i,"text":row["text"]},self.on_top).cb)
            self.b.grid(row=r, column=c, sticky=tk.W+tk.E)#,anchor="w")
            row["elem"] = self.b
            self.elem[row["text"]] = row
            r+=1
            i+=1
        self.frame.pack()
        INIT_OK = 1
        self.start_loop()

    def start_loop(self):
        print(self,"--- start_bg_loop ----- xxxx")
        thread.start_new_thread(mytklib.tk_btn_bg_loop,(self.TITLE,))

    def on_top(self,event,data={}):
        print("menue.on_top",data)
        MAIN.window_manager.top(data["text"])

    def update(self,button,text):
        #print(self,button,text)
        for k in self.elem:
            v=self.elem[k]
            #print(self,k,v)
            if button == k:
                v["elem"]["text"] = k+"\n"+text

    def config(self,button,attr,value):
        #print("config",self,button,attr,value)
        for k in self.elem:
            v=self.elem[k]
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

