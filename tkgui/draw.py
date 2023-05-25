

import tkinter as tk
import traceback

from __main__ import *


class MiniButton:
    def __init__(self,root,width=72,height=38,text="button"):
        self.text=text
        self.rb = tk.Frame(root, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.bb = tk.Canvas(self.rb, highlightbackground = "black", highlightthickness = 1, bd=1,relief=tk.RAISED)
        self.bb.configure(width=width, height=height)
        self.fg = "#002"
        self.label = []
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        # !! BLOCK's other bindings like GO
        #self.bind("<Button-1>", self.on_b1)
        #self.bind("<ButtonPress>", self.on_press)
        #self.bind("<ButtonRelease>", self.on_release)
        #self.bind("<ButtonRelease-1>", self.on_release)
        self._last_label_id = 0
        self._label_ring = ["labelA","labelB"]
        self.activebackground="lightgrey"
        self.defaultBackground="grey"

    def on_b1(self, e):
        print("on_b1",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.SUNKEN)#abackground=self.activebackground)
        return 1
    def on_press(self, e):
        print("on_press",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.SUNKEN)#abackground=self.activebackground)
        return 1
    def on_release(self, e):
        print("on_release",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.RAISED)#abackground=self.activebackground)
        return 1
    def on_enter(self, e):
        #print("on_enter",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.FLAT)#abackground=self.activebackground)
        return 1

    def on_leave(self, e):
        #print("on_leave",e)
        self.bb.config(background=self.defaultBackground)
        self.bb.config(relief=tk.RAISED)#abackground=self.activebackground)
        return 1

    def _label(self,text="1\n2\n3\n"):
        z = 0
        tag = self._label_ring[self._last_label_id]
        #self.bb.delete("label")
        self.label = []
        for t in text.split("\n"):
            self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag)
            #self.l["color"] = self.fg
            self.label.append(self.l)
            
            z+=1
        self.delete_tag()
    def delete_tag(self):
        self._last_label_id += 1
        if self._last_label_id >=len(self._label_ring ):
            self._last_label_id = 0
        tag = self._label_ring[self._last_label_id]
        self.bb.delete(tag)

    def _configure(self,**args):
        if "text" in args:
            if self.text != args["text"]:
                self.text = args["text"]
                self._label(self.text)
        if "bg" in args:
            #print(dir(self.bb))
            self.bb.configure(bg=args["bg"])
            self.defaultBackground=args["bg"]
        if "fg" in args:
            #print(dir(self.bb))
            self.fg=args["fg"]
            #if len(self.label):
            #    self.label[0].configure(color="red") #args["fg"])
            #self.defaultBackground=args["fg"]
    def configure(self,**args):
        self._configure(**args)
    def config(self,**args):
        self._configure(**args)
    def bind(self,etype="<Button>",cb=None):
        #bb.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
        if cb:
            self.bb.bind(etype,cb)
    def grid(self,row=0, column=0, sticky=""):
        self.bb.pack() #(row=row, column=column, sticky=sticky)
        self.rb.grid(row=row, column=column, sticky=sticky)
 


class ExecButton(MiniButton):
    def __init__(self,root,width=72,height=38,text="button"):
        #self.text = "1\n2\n3\n"
        super().__init__(root,width,height,text)
        self.x9font = tk.font.Font(family="FreeSans", size=9, weight="bold")
        self.x8font = tk.font.Font(family="FreeSans", size=8, weight="bold")
        self.x7font = tk.font.Font(family="FreeSans", size=7, weight="bold")
        self.x6font = tk.font.Font(family="FreeSans", size=6, weight="bold")
        self.x5font = tk.font.Font(family="FreeSans", size=5, weight="bold")
        #print(self,"init()",[self.text])
    def config(self,**args):
        self._configure(**args)
        self._label()
    def configure(self,**args):
        self._configure(**args)
        self._label()
    def dbg_info(self):
        print(self,"_label()",[self.text])
        for i in dir(self.bb):
            print("-",i)
    def _label(self,text=None):
        if type(text) is str:
            if self.text == text:
                return
            self.text = text
        else:
            text = self.text[:]
        
        tag = self._label_ring[self._last_label_id]
        #self.bb.delete("labelB")
        #self.bb.delete("labelA")
        txt2 = text
        try:
            text = text.split("\n")[1]
        except:pass


        if "grün" in text.lower() or "green" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="green",tag=tag)
        elif "purple" in text.lower() or "purple" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#800080",tag=tag)
        elif "lime" in text.lower() or "lime" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#00ff00",tag=tag)
        elif "blau" in text.lower() or "blue" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="blue",tag=tag)
        elif "rot" in text.lower() or "red" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="red",tag=tag)
        elif "orange" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="orange",tag=tag)
        elif "weiß" in text.lower() or "white" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="white",tag=tag)
        elif "cyan" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="cyan",tag=tag)
        elif "gelb" in text.lower() or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="yellow",tag=tag)
        elif "pink" in text.lower() or "pink" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#ff69b4",tag=tag)
        elif "mage" in text.lower() or "mage" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="magenta",tag=tag)

        if "nebel" in text.lower()  or "smoke" in text.lower() or "haze" in text.lower():
            self.l = self.bb.create_rectangle(10,29,60,39,fill="white",tag=tag)
        if "mh " in text.lower() or " mh" in text.lower() :
            self.l = self.bb.create_rectangle(30,29,35,32,fill="black",tag=tag)
            self.l = self.bb.create_rectangle(28,34,37,39,fill="black",tag=tag)
        if "off" in text.lower(): 
            self.l = self.bb.create_rectangle(50,30,55,35,fill="black",tag=tag)
        if "dim" in text.lower() or "front" in text.lower()  or "on" in text.lower(): 
            #self.l = self.bb.create_line(56,30,60,28,fill="black",tag=tag)
            self.l = self.bb.create_rectangle(50,30,55,35,fill="white",tag=tag)
            #self.l = self.bb.create_line(56,36,58,36,fill="black",tag=tag)
        if "circle" in text.lower(): 
            self.l = self.bb.create_oval(30,29,40,39,fill="",tag=tag)
        if "pan" in text.lower(): 
            self.l = self.bb.create_line(20,34 ,45,34,fill="black",arrow=tk.BOTH,tag=tag)
        if "tilt" in text.lower(): 
            self.l = self.bb.create_line(30,25 ,30,43,fill="black",arrow=tk.BOTH,tag=tag)

        text = txt2
        z = 0
        for t in text.split("\n"):
            ts = 10
            _max = 7
            if z==1 and len(t) >= _max:
                ts = int(10 - (len(t)-_max)/1.5)
                if ts < 5:
                    ts = 5
                xfont = self.x9font
                if 1:
                    if ts == 9:
                        xfont = self.x9font
                    elif ts == 8:
                        xfont = self.x8font
                    elif ts == 7:
                        xfont = self.x7font
                    elif ts == 6:
                        xfont = self.x7font
                    elif ts == 5:
                        xfont = self.x7font

                if len(t) > 14:
                    t2 = t[:14]
                    t3 = t[14:]
                    self.l = self.bb.create_text(37,z*10+9-2,text=t2,anchor="c",tag=tag,fill=self.fg,font=xfont)
                    self.l = self.bb.create_text(37,z*10+9+6,text=t3,anchor="c",tag=tag,fill=self.fg,font=xfont)
                else:
                    self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg,font=xfont)
                #self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg)
            else:
                self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg)
            z+=1
        #self.bb.update(0)
        #self.bb.after(0)

        self.delete_tag()



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
    for comm in gui.commands.commands:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0
        if comm == "BLIND":
            b["bg"] = "grey"
            myTip = Hovertip(b,'BLIND MODE\nNO CHANGE on DMX-OUTPUT')
        if comm == "CLEAR":
            b["bg"] = "grey"
            myTip = Hovertip(b,'CLEAR ALL SELECTED\nFIXTURES ATTRIBUTES')
        if comm == "REC-FX":
            b["bg"] = "grey"
            myTip = Hovertip(b,'RECORD ONLY FX\nINTO EXEC')
        if comm == "FADE":
            b["bg"] = "green"
            myTip = Hovertip(b,'adjust fade time')
        if comm == "S-KEY":
            b["bg"] = "green"
            myTip = Hovertip(b,'keyboard short-key\non or  off')
        if comm == "FX OFF":
            b["bg"] = "magenta"
        if comm == "SIZE:":
            b["text"] = "SIZE:{:0.0f}".format(fx_prm["SIZE"])
        if comm == "SPEED:":
            b["text"] = "SPEED:{:0.0f}".format(fx_prm["SPEED"])
        if comm == "DELAY":
            b["text"] = "FADE:\n{:0.02f}".format(DELAY.val())
        if comm == "FADE":
            b["text"] = "FADE:\n{:0.02f}".format(FADE.val())
        if comm == "START:":
            b["text"] = "START:{:0.0f}".format(fx_prm["START"])
        if comm == "OFFSET:":
            b["text"] = "OFFSET:{:0.0f}".format(fx_prm["OFFSET"])
        if comm == "FX-X:":
            b["text"] = "FX-X:{}".format(fx_prm["FX-X"])
        if comm == "BASE:":
            b["text"] = "BASE:{}".format(fx_prm["BASE"])

        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="COMMAND").cb)
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=8:
            c=0
            r+=1

def draw_exec(gui,xframe,PRESETS):
    draw_preset(gui,xframe,PRESETS)


def draw_preset(gui,xframe,PRESETS):

    i=0
    c=0
    r=0
    root = xframe
    
    frame = tk.Frame(root,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
    #time.sleep(0.1)
    gui.elem_presets = {}
    i=0
    for k in PRESETS.val_presets:
        if i%(10*8)==0 or i ==0:
            c=0
            #b = tk.Label(frame,bg="black", text="" )
            b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
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

        b.config(text="xx")
        c+=1
        if c >=10:
            c=0
            r+=1
    time.sleep(0.1)
    gui._refresh_exec()
    #gui.refresh_exec()
    #gui.refresh_exec()
    print("##################################")


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


def draw_colorpicker(gui,xframe,FIXTURES,master):
    import lib.colorpicker as colp

    class _CB():
        def __init__(gui,FIXTURES,master):
            gui.old_color = (0,0,0)
        def cb(gui,event,data):
            print("CB.cb",gui,event,data)
            cprint("colorpicker CB")
            if "color" not in data:
                return 0
            if gui.old_color == data["color"]:
                pass #return 0
            
            #gui.old_color = data["color"]
            color = data["color"]
            
            print("e",event,data)
            print("e",dir(event))#.keys())
            try:
                print("e.state",event.state)
            except:pass
            set_fade = FADE.val() #fade

            event_ok = 0
            event_num = 0
            event_state = 0
            if event is None:
                event_ok = 1
                event_num = 3
            elif event.num == 1:
                event_ok = 1
                event_num = event.num 
            elif event.num == 3:
                event_ok = 1
                event_num = event.num 
            elif event.num==2:
                event_ok = 1
                event_num = event.num 
            elif event.state in [256,1024]:
                event_ok = 1
                event_state = event.state


            if "color" in data and event_ok:
                cr=None
                cg=None
                cb=None
                cw=0
                ca=0
                set_fade=0

                if event_num == 1: 
                    if FADE._is():
                        set_fade=FADE.val() #fade
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]
                elif event_num == 3: 
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]
                elif event_num == 2: 
                    cr= "click"
                    cg= "click"
                    cb= "click"
                    cw= "click"
                    ca= "click"
                elif event_state == 256:
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]


                if cr is not None:
                    FIXTURES.encoder(fix=0,attr="RED",xval=cr,xfade=set_fade)
                if cg is not None:
                    FIXTURES.encoder(fix=0,attr="GREEN",xval=cg,xfade=set_fade)
                if cb is not None:
                    FIXTURES.encoder(fix=0,attr="BLUE",xval=cb,xfade=set_fade)
                FIXTURES.encoder(fix=0,attr="WHITE",xval=cw,xfade=set_fade)
                FIXTURES.encoder(fix=0,attr="AMBER",xval=ca,xfade=set_fade)
                master.refresh_fix()
                 
                print("PICK COLOR:",data["color"])
    _cb=_CB(FIXTURES,master)
    colp.colorpicker(xframe,width=580,height=113, xcb=_cb.cb)
    return 0

    canvas=tk.Canvas(xframe,width=600,height=113)
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
    #b = tk.Button(frame,bg="lightblue", text="",width=6)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #c+=1
    #b = tk.Button(frame,bg="lightblue", text="",width=6)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #c+=1
    #b = tk.Button(frame,bg="lightblue", text="",width=6)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #c+=1
    #b = tk.Button(frame,bg="lightblue", text="",width=6)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #c+=1
    #b = tk.Button(frame,bg="lightblue", text="",width=6)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    ##c+=1
    #for attr in ["xx"]*23: # gui.all_attr:
    eat = gui.all_attr

    if len(eat) < 24:
        for i in range(24-len(eat)):
            eat.append("")
    for attr in eat:
        if attr.endswith("-FINE"):
            continue
        v=0
        if attr.startswith("_"):
            continue

        b = tk.Button(frame,bg="#6e6e6e", text=str(attr)+'',width=7)#, anchor="w")
        if attr == "DIM":
            b = tk.Button(frame,bg="#ff7f00", text=str(attr)+'',width=7)#, anchor="w")
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=attr,data=gui,mode="ENCODER2").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E ,ipadx=0,ipady=0,padx=0,pady=0)#,expand=True)
        c+=1
        if c >=8:
            c=0
            r+=1

    b = tk.Button(frame,bg="#bfff00", text="INV-ATTR",width=6)
    myTip = Hovertip(b,'INVERT ATTRIBUT SELECTION')
    b.bind("<Button>",Xevent(fix="SEL",elem=b,attr="INV-ATTR",data=gui,mode="INVERT").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    #b = tk.Button(frame,bg="#00a7ff", text="INV-FIX",width=6)
    #myTip = Hovertip(b,'INVERT FIXTURE SELECTION')
    #b.bind("<Button>",Xevent(fix="ALL",elem=b,attr="INV-FIX",data=gui,mode="INVERT").cb)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #c+=1

def _draw_fx(frame,c,r,gui,mode="FX"):
    ct  = gui.fx
    prm = fx_prm
    if mode=="FX-MOVE":
        ct  = gui.fx_moves
        prm = fx_prm_move
    elif mode=="FX-GENERIC":
        ct  = gui.fx_generic
        prm = fx_prm #_generic

    for comm in ct.commands:
        if comm == "\n\n":
            b = tk.Label(frame,bg="black", text="-",font=space_font)
            b.grid(row=r, column=c,pady=0,padx=0, sticky=tk.W+tk.E)
            c=0
            r+=1
            continue
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        if "PAN/TILT" in comm: 
            b = tk.Button(frame,bg="grey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in ct.elem:
            #comm = comm.replace("\n","")
            ct.elem[comm] = b
            ct.val[comm] = 0
        b.bind("<Button>",Xevent_fx(fix=0,elem=b,attr=comm,data=gui,mode=mode).cb)
        if comm == "REC-FX":
            b["bg"] = "grey"
        elif comm == "FX OFF":
            b["bg"] = "magenta"
        elif comm[:3] == "FX:":
            b["text"] = comm
            b["bg"] = "#ffbf00"
        elif comm[:3] == "MO:":
            b["text"] = comm 
            b["bg"] = "lightgreen"
        elif comm.startswith( "SIZE:"):
            b["text"] = "SIZE:\n{:0.0f}".format(prm["SIZE"])
            b["bg"] = "lightgreen"
        elif comm.startswith( "SPEED:"):
            b["text"] = "SPEED:\n{:0.0f}".format(prm["SPEED"])
            b["bg"] = "lightgreen"
        elif comm.startswith("START:"):
            b["bg"] = "lightgreen"
            b["text"] = "START:\n{:0.0f}".format(prm["START"])
        elif comm.startswith( "OFFSET:"):
            b["bg"] = "lightgreen"
            b["text"] = "OFFSET:\n{:0.0f}".format(prm["OFFSET"])
        elif comm[:3] == "BASE:":
            b["bg"] = "lightgreen"
            b["text"] = "BASE:\n{}".format(prm["BASE"])
        elif comm[0] == "M":
            b["text"] = comm 
            b["bg"] = "lightgrey"

        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=6:
            c=0
            r+=1
    return c,r



def draw_fx(gui,xframe):
    frame_fx=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_fx,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    b = tk.Button(frame,bg="lightblue", text="FX.",width=6)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1

    c,r = _draw_fx(frame,c,r,gui,mode="FX-MOVE")
    r+=1

    b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    r+=1
    c=0

    c,r = _draw_fx(frame,c,r,gui,mode="FX")

    b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    r+=1
    c=0

    c,r = _draw_fx(frame,c,r,gui,mode="FX-GENERIC")


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
    for comm in ["SAVE\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS","SAVE &\nRESTART","DRAW\nGUI"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        if comm == "SAVE\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=5,height=2)
        elif comm == "LOAD\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=5,height=2)
        elif comm == "SAVE\nSHOW AS":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        elif comm == "SAVE &\nRESTART":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        elif comm == "DRAW\nGUI":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="grey", text=str(comm),width=5,height=2)

        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0

        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="SETUP").cb)

        if comm == "BASE:":
            b["text"] = "BASE:{}".format(prm["BASE"])
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=7:
            c=0
            r+=1










class X_CLOCK():
    def __init__(self):
        self._last_label_id = 1
        self._label_ring = [ "labelA","labelB"]

    def loop_clock(self,b):
        xfont = tk.font.Font(family="FreeSans", size=65, weight="bold")
        xfont1 = tk.font.Font(family="FreeSans", size=25, weight="bold")
        while 1:
            tag = self._label_ring[self._last_label_id]
            #b["text"] = 
            d = time.strftime("%Y-%m-%d")
            s = time.strftime("%X")
            #b.delete("all")
            b.create_text(170,41,text=s,fill="#aa0" ,font=xfont,tag=tag)
            b.create_text(160,91,text=d,fill="#aa0" ,font=xfont1,tag=tag)
        
            self.delete_tag()
            time.sleep(0.2)
            #exit()
    def delete_tag(self):
        self._last_label_id += 1
        if self._last_label_id >=len(self._label_ring ):
            self._last_label_id = 0
        tag = self._label_ring[self._last_label_id]
        self.bb.delete(tag)
    def draw_clock(self,gui,xframe):
        frame_cmd=xframe
        
        frame = tk.Frame(frame_cmd,bg="black")
        frame.pack(fill=tk.X, side=tk.TOP)
        comm = "xx"
        
        xfont = tk.font.Font(family="FreeSans", size=25, weight="bold")
        b = tk.Canvas(frame,bg="black", height=105,bd=0,width=6,highlightthickness=0) #,bd="black")
        self.bb = b
        #b = tk.Button(frame,bg="lightgrey", text=str(comm),width=26,height=2,font=xfont)
        #b.config(activebackground="lightgreen")
        #b.config(background="lightgreen")
        b.pack(fill="both",expand=1) #row=0, column=0, sticky=tk.W+tk.E)
        #b["text"] = time.strftime("%Y-%m-%d %X")
        thread.start_new_thread(self.loop_clock,(b,))




def draw_live(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    c+=1
    for comm in ["FADE","DELAY","PAN/TILT\nFADE","PAN/TILT\nDELAY"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="LIVE").cb)

        if "FADE" == comm:
            b["text"] = "FADE:\n{:0.2}".format(FADE.val())
        if "DELAY" == comm:
            b["text"] = "DELAY:\n{:0.2}".format(DELAY.val())
        if "PAN/TILT\nFADE" == comm:
            b["text"] = "PAN/TILT\nFADE:{:0.2}".format(FADE_move.val())

        if "FADE" in comm:
            b["bg"] = "green"
            b.config(activebackground="lightgreen")
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=5:
            c=0
            r+=1

