
import tkinter as tk
from __main__ import *
import __main__ as _M
import lib.mytklib as mytklib

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
        self.canvas.bind("<Button>",Event("XXX").event)
        self.canvas.bind("<Key>",Event("XXX").event)
        self.canvas.bind("<KeyRelease>",Event("XXX").event)

        
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


def ScrollFrame(root,width=50,height=100,bd=1,bg="black",head=None,foot=None):
    rframe=tk.Frame(root) 
    rframe.pack(side="top",fill="both",expand=1) #x=0,y=0)

    # frame grid start =========
    if head:
        height -= 25
        hframe=tk.Frame(rframe) 
        #l = tk.Label(hframe,text="frame")
        #l.pack()
        hframe.pack(side="top",fill="x",expand=0) #x=0,y=0)

    aframe=tk.Frame(rframe) 
    aframe.pack(side="top",fill="both",expand=1) #x=0,y=0)

    if foot:
        height -= 25
        fframe=tk.Frame(rframe) 
        #l = tk.Label(fframe,text="frame")
        #l.pack()
        fframe.pack(side="top",fill="x",expand=0) #x=0,y=0)
        # frame grid end ==========


    canvas=tk.Canvas(aframe,width=width-24,height=height)
    if bg == "":
        bg="orange"
    canvas["bg"] = bg # "black" #"green"
    bframe=tk.Frame(canvas,width=width,height=height,relief=tk.GROOVE)
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
    if head or foot:
        return [hframe,bframe,fframe]

    return bframe

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
        print("draw_clock",self)
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
        b.bind("<Button>",Xevent(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="lightblue", text=data["NAME"],width=10,anchor="w")
        b.config(padx=1)
        b.bind("<Button>",Xevent(fix=fix,mode="D-SELECT",elem=b).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Button(frame,bg="grey", text="S",width=2,anchor="c")
        b.config(padx=1)
        myTip = Hovertip(b,'SELECT')
        b.bind("<Button>",Xevent(fix=fix,elem=b,attr="_ACTIVE",mode="ENCODER",data=data).cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        gui.elem_attr[fix]["S"] = b
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
            if fix not in gui.elem_attr:
                gui.elem_attr[fix] = {}
            
            kix = []
            for ix in data["ATTRIBUT"].keys():
                if not ix.startswith("_") and not ix.endswith("-FINE"):
                    kix.append(ix)

            if "DIM" in kix and len(kix) == 1:
                c,r=draw_sub_dim(gui,fix,data,c=c,r=r,frame=dim_frame)
                continue

            break



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
            b.bind("<Button>",Xevent(fix=fix,mode="SELECT",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="#55f", text=data["NAME"],width=10,anchor="w")
            b.bind("<Button>",Xevent(fix=fix,attr="ALL",mode="ENCODER",elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            b = tk.Button(frame,bg="grey", text="S",width=2,anchor="c")
            b.config(padx=1)
            myTip = Hovertip(b,'SELECT')
            b.bind("<Button>",Xevent(fix=fix,elem=b,attr="_ACTIVE",mode="ENCODER",data=data).cb)
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

                if attr not in gui.all_attr:
                    gui.all_attr.append(attr)
                if attr not in gui.elem_attr[fix]:
                    gui.elem_attr[fix][attr] = ["line1348",fix,attr]
                v= data["ATTRIBUT"][attr]["VALUE"]
                
                if attr.startswith("_"):
                    continue
                b = tk.Button(frame,bg="grey", text=str(attr)+' '+str(round(v,2)),width=12, anchor="w")
                gui.elem_attr[fix][attr] = b
                b.bind("<Button>",Xevent(fix=fix,elem=b,attr=attr,mode="ENCODER",data=data).cb)
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
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(xframe,bg="grey", text="NAME",width=14,anchor="w")
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
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
            b = tk.Button(xframe,bg=rgb, text="DMX Collision!",width=12)
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
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1

            command = _SET_PATCH("NAME",data["NAME"],fix,data)
            b = tk.Button(xframe,bg="grey", text=data["NAME"],width=14,anchor="w",command=command.attr)
            command.set_button(b)
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
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
            #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            b["activebackground"] = "#aaa"
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
                        highlight(fix)
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

            c=0
            r+=1



def GUI_LOAD_FIXTURE_LIST(frame,data={"EMPTY":"None"},cb=None,bg="black"):
    #print("__func__",__func__)
    print("#",sys._getframe().f_code.co_name)
    blist = data
    blist = blist[:100]

    frame.configure(bg=bg)

    # table header
    c=0
    for r,row in enumerate(blist):
        bg="lightgrey"
        dbg="grey"
        dbg="lightgrey"
        c+=1
        b = tk.Label(frame,bg="grey",text=str("Nr."))
        b.grid(row=r, column=c, sticky=tk.W) #+tk.E)
        c+=1
        for k,v in row.items():
            b = tk.Label(frame,bg="grey",text=k)
            b.grid(row=r, column=c, sticky=tk.W) #+tk.E)
            c+=1
        break
    
    if not cb:
        cb = DummyCallback()

    # table data
    for r,row in enumerate(blist):
        c=1

        bg="lightgrey"
        #dbg="grey"
        b = tk.Button(frame,text=r+1,anchor="w",bg=dbg,width=6,relief="sunken")
        b.grid(row=r+1, column=c, sticky=tk.W ) #+tk.E)
        c+=1
        bg="grey"
        dbg="grey"
        for k,v in row.items():
            #if v > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*4)):
            #    dbg = "lightgreen"
            #elif v > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*24*7)):
            #    dbg = "green"


            if c == 2:
                _cb2 = _M.BaseCallback(cb=cb,args={"key":k,"val":v,"data":row}).cb
                b = tk.Button(frame,text=v,anchor="w",height=1,bg=bg,command=_cb2)
            else: 
                b = tk.Button(frame,text=v,anchor="w",bg=dbg,relief="flat")
                b.config(activebackground=dbg)
            b.grid(row=r+1, column=c, sticky=tk.W+tk.E)
            c+=1
            bg="lightgrey"
            dbg="lightgrey"


class GUI_FixtureEditor():
    def __init__(self,root,frame,data,title="tilte",width=800):
        #xfont = tk.font.Font(family="FreeSans", size=5, weight="bold")
        self.font8 = ("FreeSans",8)
        self.dmx=1
        self.univ=0
        self.elem=[]
        self.fader_elem = []
        self.pw = None
        self.header=[]
        self.data = data
        self.title = title
        self.width = width
        #cprint("GUI:",root,title)
        self.root = root
        self.frame = frame
        self.draw()

    def draw(self):
        root = self.frame

        title = self.title
        width = self.width
        data = self.data

        self.fader_elem = []
        # HEAD 2
        
        self.frame = tk.Frame(root,bg="grey",width=width)
        self.frame.pack(fill="both", side=tk.TOP)

        self.b = tk.Label(self.frame,bg="#ddd",text="NAME:")
        self.b.pack(fill=None, side=tk.LEFT)
        self.b = tk.Button(self.frame,bg="lightblue",text="MAC-500", width=11)
        self.name=self.b
        self.b["command"] = self.set_name
        self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="lightblue",text="UNIV:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b_univ = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        
        self.entry_univ=self.b_univ
        self.b_univ["command"] = self.event_univ
        self.b_univ.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="lightblue",text="DMX:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        self.entry_dmx=self.b
        self.b["command"] = self.event_dmx
        self.b.pack( side=tk.LEFT)

        self.b_xdmx = tk.Label(self.frame,bg="lightgreen",text="5")
        self.b_xdmx.pack(fill=None, side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#ddd",text="TYPE:")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="IMPORT", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_import
        self.b.pack( side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="USER", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_user
        self.b.pack( side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="GLOBAL", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_global
        self.b.pack( side=tk.LEFT)


        self.b = tk.Label(self.frame,bg="#ddd",text="")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="SAVE", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.save_fixture
        self.b.pack( side=tk.LEFT)
        

        #self.b = tk.Button(self.frame,bg="lightblue",text="SAVE AS", width=5)#,command=self.event) #bv.change_dmx)
        #self.b["command"] = self.save_as_fixture
        #self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="black",text="") # spacer
        self.b.pack(fill=tk.Y, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="lightblue",text="HELP", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = _M.online_help("fixture-editor")
        self.b.pack( side=tk.LEFT)

        # HEAD 1
        
        #root = tk.Frame(root,bg="black",width=width)
        #root.pack(fill=tk.BOTH, side=tk.TOP)

        self.frame = tk.Frame(root,bg="grey",width=width)
        self.frame.pack(fill="x", side=tk.TOP)

        self.b = tk.Label(self.frame,bg="#fff",text="Fixture Editor") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#aaa",text="FILE:") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b_path = tk.Label(self.frame,bg="#fff",text="~/LibreLight/fixtures/lalla.json") #,font=self.font8 )
        self.b_path.pack(fill=None, side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#aaa",text="----") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b_info = tk.Label(self.frame,bg="#fff",text="") #,font=self.font8 )
        self.b_info.pack(fill=None, side=tk.LEFT)
        # DATA
        self.frame = ScrollFrame(root,bg="#003",width=2000 ,height=1000,bd=2) # fader frame


        self.r=0
        self.c=0
        self.pb=12
        self.j = 0

        for page_nr in range(12):
            self.draw_bank(page_nr)

        self._event_redraw()

    def draw_bank(self,page_nr):
        title = self.title
        width = self.width

        idx = self.pb*page_nr
        data = self.data[idx:idx+self.pb]

        c = idx
        for j,row in enumerate(data):
            if c % self.pb == 0 or c==0:
                h=hex(j*10)[2:].rjust(2,"0")
                frameS = tk.Frame(self.frame,bg="#000",width=width,border=2)
                frameS.pack(fill=tk.BOTH, side=tk.TOP)
                bank_nr=j//self.pb+1
                txt="BANK:{} {}-{}".format(bank_nr,bank_nr*self.pb-self.pb+1,bank_nr*self.pb) 
                self.b = tk.Label(frameS,bg="lightblue",text=txt,width=15,font=self.font8 )
                self.header.append(self.b)

                self.b.pack(fill=None, side=tk.LEFT)
                self.b = tk.Label(frameS,bg="black",text="" ,width=11,font=self.font8 )
                self.b.pack(fill=tk.BOTH, side=tk.LEFT)

                try:
                    frameS = tk.Frame(self.frame,bg="#a000{}".format(h),width=width,border=2)
                except:
                    frameS = tk.Frame(self.frame,bg="#a0aadd",width=width,border=2)
                self.c=0

            e= ELEM_FADER(frameS,nr=j+1,cb=self._cb,fader_cb=self._fader_cb)
            e.pack()
            #e.attr["bg"] = "red"
            self.fader_elem.append(e)
            self.elem.append(e)
            frameS.pack(fill=tk.X, side=tk.TOP)
            c+=1

    def _fader_cb(self,arg,name="<name>",**args):
        print("   FixtureEditor._cb",args,arg,name)
        #print("    ",name,"_cb.args >>",args,arg[1:])
        self.count_ch()
    
        try:
            a1 = arg #arg[2]
            nr = args["nr"] #.nr
            j=[]
            jdata = {'VALUE': int(a1), 'args': [] , 'FADE': 0,'DMX': str(nr)}
            ##print("   ",jdata)
            j.append(jdata)
            jclient_send(j)
        except Exception as e:
            print("exec",arg,args)
            print(e)

    def _cb(self,arg,name="<name>",**args):
        #print(" FixtureEditor._cb")
        #print(" ",name,"_cb.args >>",args,arg[1:])
        self.count_ch()
    

    def count_ch(self):
        #print("FixtureEditor.count_ch:")
        #e._set_attr( "---")
        ch_s = []
        j=-1
        self.b_info["text"] = "xx"

        for i,elem in enumerate(self.elem):
            #print(dir(elem))
            txt = elem.attr["text"]
            if txt:
                #print("count_ch:",i,txt)
                elem.attr["bg"] = "#0f0"
                elem.attr["activebackground"] = "#0fa"
                ch_s.append([i,txt])
                j=i
            else:
                elem.attr["bg"] = "lightgrey"
                elem.attr["activebackground"] = "white"
        self.b_info["text"] = "CH's: {} USED: {}".format(j+1,len(ch_s))

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


    def save_as_fixture(self,event=None):
        print("save_as_fix",self,event)
        self.count_ch()

    def save_fixture(self,event=None):
        print("save_fix",self,event)
        self.count_ch()


    def open_fixture_list_global(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="GLOBAL")
    def open_fixture_list_import(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="IMPORT")
    def open_fixture_list_user(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="USER")
        
    def _open_fixture_list(self,mode=""):
        name = "FIXTURE-{}".format(mode)
        line1="Fixture Library"
        line2="CHOOS to EDIT >> DEMO MODUS"
        line3="CHOOS to EDIT >> DEMO MODUS"

        cb = None #LOAD_FIXTURE(self,"USER").cb 
        self.pw = _M.PopupList(name,width=600,cb=cb,left=_M._POS_LEFT+620,bg="#333")
        frame = self.pw.sframe(line1=line1,line2=line2) #,line3=line3)


        def cb(event=None,args={}):
            print("open_fixture_list.cb(")
            print("   ",args)
            if self.pw:
                self.pw.w.tk.destroy()
            data = args["data"]
            self.b_path["text"] = data["name"] #"load_MH2"
            self.name["text"] = data["name"] #"load_MH2"
            self.name["text"] = data["name"] #"load_MH2"
            xpath = data["xpath"] + "/" + data["xfname"]
            fdata = _M._read_sav_file(xpath)
            a = []
            m = []
            for row in fdata:
                #print("row:  ",row.keys())
                #print("a-")
                for k,fixture in row.items():#keys():
                    #v = row[k]
                    if "NAME" not in fixture:
                        continue
                    if fixture["NAME"] != args["val"]:
                        continue

                    print("a    :",k,str(fixture)[:120],"...")
                    #print("a    ::",type(k),":",type(fixture))
                    if "ATTRIBUT" in fixture:
                        for at in fixture["ATTRIBUT"]:
                            if at.startswith("_"):
                                 continue
                            a.append(at)
                            if at.endswith("-FINE"):
                                m.append("-")
                            elif at in ["PAN","TILT","DIM","RED","GREEN","BLUE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]:
                                m.append("F")
                            else:
                                m.append("S")
                            #m.append("F")

            self._load_fix(None,a,m)
            self.close_fixture_list()

        blist = _M._load_fixture_list(mode=mode)
        
        r=GUI_LOAD_FIXTURE_LIST(frame,data=blist,cb=cb,bg="#333")

    def close_fixture_list(self):
        if self.pw:
            self.pw.w.tk.destroy()

    def clear(self,_event=None,attr=[]):
        attr = [""]*100
        mode = [""]*100
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "clean..."
        self.close_fixture_list()

    def load(self,_event=None,attr=[]):
        attr = ["LOAD"]*10
        mode = ["X"]*10
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "clean..."
        self.close_fixture_list()

    def load_EMPTY(self,_event=None,attr=[]):
        #attr = [,"RED","GREEN","BLUE"]
        #mode = ["F","F","F","F"]
        self._load_mh(None)#,attr,mode)
    def load_DIM(self,_event=None,attr=[]):
        attr = ["DIM"]
        mode = ["F"]
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_DIM"
        self.close_fixture_list()
    def load_LED(self,_event=None,attr=[]):
        attr = ["DIM","RED","GREEN","BLUE"]
        mode = ["F","F","F","F"]
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_LED"
        self.close_fixture_list()
    def load_MH(self,_event=None,attr=[]):
        if not attr:
            attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO"]
        mode = []
        for a in attr:
            if a.endswith("-FINE"):
                mode.append("-")
            elif a in ["PAN","TILT","DIM","RED","GREEN","BLUE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]:
                mode.append("F")
            else:
                mode.append("S")

        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_MH"
        self.close_fixture_list()
    def load_MH2(self,_event=None,attr=[]):
        attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO","G-ROT","PRISM","P-ROT","ZOOM","CONTR"]
        mode = ["F","F","F","F","S","F","F","F","F","S","S","S","S","F","S"]
        self.b_path["text"] = "load_MH2"
        self._load_fix(None,attr,mode)
        self.close_fixture_list()

    def _load_fix(self,_event=None,attr=[],mode=[]):
        print("load_fixture",[_event,self])
        #for i,e in enumerate(self.elem):
        for i,e in enumerate(self.elem):
            #print(self,"event",_event,e)
            #print("event",_event,e)
            e._set_attr( "")
            if len(attr) > i:
                e._set_attr( attr[i])
            e._set_mode( "---")
            if len(mode) > i:
                e._set_mode( mode[i])
        self.count_ch() 

    def event_univ(self,_event=None):
        nr=self.univ
        txt= self.entry_univ["text"]
        #def _cb(txt):
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"event_univ._cb()",txt)
            try:
                nr = int(txt)
            except TypeError:
                print("--- abort ---")
                return 0
            self.univ = nr
            self._event_redraw(_event)
        dialog._cb = _cb
        dialog.askstring("Universe","Univ 0-15",initialvalue=txt)

    def event_dmx(self,_event=None):
        nr=self.dmx
        txt= self.entry_dmx["text"]
        #txt = dialog.askstring("DMX","ArtNet 1-512 (7680 max)",initialvalue=txt)
        #def _cb(txt):
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"event_dmx._cb()",txt)
            try:
                nr = int(txt)
            except TypeError:
                print("--- abort ---")
                return 0
            self.dmx = nr
            if self.dmx <= 0:
                self.dmx = 1
            if self.dmx > 512:
                self.univ = (self.dmx-1)//512
                self.dmx = (self.dmx-1)%512+1
            self._event_redraw(_event)
        dialog._cb = _cb
        dialog.askstring("DMX","ArtNet 1-512 (7680 max)",initialvalue=txt)

        
    def _event_redraw(self,_event=None):
        self.entry_dmx["text"] = "{}".format(self.dmx)
        self.entry_univ["text"] = "{}".format(self.univ)
        nr = self.univ*(512)+self.dmx
        self.b_xdmx["text"] = " {}  ".format(nr)

        print("change_dmx",[_event,self])
        for i,btn in enumerate(self.elem):
            #print("event",_event,btn)
            #print("btn",btn)
            dmx=nr+i
            nr2 = dmx%512 
            btn.set_label("{} {}.{}\n D:{}".format(i+1,self.univ,nr2,dmx))
            btn.nr = nr+i

        pb=self.pb
        for j,e in enumerate(self.header):
            p=j+1
            #p=nr/pb
            txt="BANK:{} {}-{}".format(p,p*pb-pb+nr,(p*pb+nr)-1) 
            print("---",j,txt,e)
            e["text"] = txt
        self.count_ch() 

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







class ELEM_FADER():
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
        if self._fader_cb:
            self._fader_cb(a1,a2,nr=self.nr)

    def event(self,a1="",a2=""):
        if self._cb:
            self._cb([self,"event",a1,a2])

    def set_attr(self,_event=None):
        txt= self.attr["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            #print(self,"set_attr._cb()",txt)
            self._set_attr(txt)
            if self._cb:
                self._cb([self,"set_attr",txt])
        dialog._cb = _cb
        dialog.askstring("ATTR","set attr:",initialvalue=txt)
        
    def _set_attr(self,txt=""):
        if type(txt) is str:
            self.attr["text"] = "{}".format(txt)
            #print("_set_attr",[self])
        if self._cb:
            self._cb([self,"_set_attr",txt])

    def set_label(self,name=""):
        #print("set_label",self.b,name)
        self.label["text"] = name
        if self._cb:
            self._cb([self,"set_label",name])

    def set_mode(self,_event=None):
        txt= self.mode["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"set_mode._cb()",txt)
            #w = _M.Window("config",master=1,width=200,height=140,left=L1,top=TOP)
            #w.pack()
            self._set_mode(txt)
            #w.show()
            if self._cb:
                self._cb([self,"set_mode",txt])
        dialog._cb = _cb
        dialog.askstring("MODE S/F:","SWITCH or FADE",initialvalue=txt)

    def _set_mode(self,txt=""):
        if type(txt) is str:
            txt = txt[0].upper()
            self.mode["text"] = "{}".format(txt)
            #print("_set_mode",[self])
        if self._cb:
            self._cb([self,"_set_mode",txt])

    def _refresh(self):
        pass
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

        self.b = tk.Button(frameS,bg="lightblue",text="{}".format(self.nr), width=4,command=test,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.label = self.b
        self.elem.append(self.b)
        self.b = tk.Button(frameS,bg="lightblue",text="", width=5,command=self.set_attr,font=self.font8 )
        self.attr=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)
        f = tk.Frame(frameS)
        #f.pack()
        self.b = tk.Button(f,bg="lightblue",text="<+", width=1,command=self.set_mode,font=self.font8 )
        #self.mode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        #self.elem.append(self.b)

        self.b = tk.Button(frameS,bg="lightblue",text="", width=4,command=self.set_mode,font=self.font8 )
        self.mode=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        self.elem.append(self.b)

        self.b = tk.Button(f,bg="lightblue",text="+>", width=1,command=self.set_mode,font=self.font8 )
        #self.mode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        #self.elem.append(self.b)

        self.b = tk.Label(frameS,bg="black",text="", width=4,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)









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
            #w = _M.Window("config",master=1,width=200,height=140,left=L1,top=TOP)
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
            #PRESETS.go(self.id+80)
            _M.master.preset_go(nr-1,xfade=None,val=value)
        else:
            value = 1
            #PRESETS.go(self.id+80)
            _M.master.preset_go(nr-1,xfade=None,val=value)

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

        self.b = tk.Button(frameS,bg="lightblue",text="{}".format(self.nr), width=5,command=test,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.label = self.b
        if 1: #self.nr <= 10:

            self.elem.append(self.b)
            self.b = tk.Button(frameS,bg="lightblue",text="", width=5,font=self.font8 )
            self.b.bind("<Button>",self.go) #BEvent({"NR":self.id+80,"text":""},self.go).cb)
            self.b.bind("<ButtonRelease>",self.go) #BEvent({"NR":self.id+80,"text":""},self.go).cb)
            #b = self.b
            #k = ""
            #gui = _M.master
            #self.b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
            #self.b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
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


def test(a1="",a2=""):
    print([a1,a2])

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
            #e= ELEM_FADER(frameS,nr=j+1,cb=self.event_cb)
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
        jclient_send(j)

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
            e= ELEM_FADER(frameS,nr=j+1,fader_cb=self.event_cb)
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
        jclient_send(j)

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

            self.b.bind("<Button>",BEvent({"NR":i,"text":row["text"]},self.callback).cb)
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

    def callback(self,event,data={}):
        #print("callback543",self,event,data)
        print("callback543",self,event) #,data)
        import __main__ as m
        m.window_manager.top(data["text"])
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

