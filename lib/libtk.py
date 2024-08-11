#!/usr/bin/python3

import os
import time
import json
import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

import tkinter
tk = tkinter

import __main__ as MAIN

from lib.cprint import cprint
import lib.libwin as libwin
import lib.showlib as showlib
import lib.libconfig as libconfig
import lib.fixlib as fixlib

import tkgui.dialog  as dialoglib
dialog = dialoglib.Dialog()


for i in dir(MAIN):
    print(i)

#_config = MAIN._load_config()
_config = libconfig._load_config()

_POS_LEFT = 0
_POS_TOP  = 15
try: 
    for row in _config:
        #print("   config:",row)
        if "POS_LEFT" in row:
           _POS_LEFT = int(row["POS_LEFT"]) 
        if "POS_TOP" in row:
           _POS_TOP = int(row["POS_TOP"]) 
except Exception as e:
    cprint("Exception:",e)



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

def test_command(a1="",a2=""):
    print([a1,a2])

def online_help(page):
    print("INIT:online_help",page)

    try:
        #page = page.replace("&","")
        #page = page.replace("=","")
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

    def set_nr(self,_event=None):
        txt= self.elem_nr["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            self._set_nr(txt)
            if self._cb:
                self._cb([self,"set_nr",txt])
        dialog._cb = _cb
        dialog.askstring("ATTR","set NR:",initialvalue=txt)

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
            #w = MAIN.WindowContainer("config",master=1,width=200,height=140,left=L1,top=TOP)
            #w.pack()
            self._set_mode(txt)
            #w.show()
            if self._cb:
                self._cb([self,"set_mode",txt])
        dialog._cb = _cb
        dialog.askstring("MODE S/F:","SWITCH or FADE",initialvalue=txt)

    def _set_nr(self,txt=""):
        if type(txt) is str:
            try: 
                x = int(txt)
                if x <= 0:
                    txt = "off"
                    self.attr["bg"] = "#fa0"
                    self.elem_nr["bg"] = "#fa0"
                else:
                    self.attr["bg"] = "lightblue"
                    self.elem_nr["bg"] = "lightblue"
            except:pass
            self.elem_nr["text"] = "{}".format(txt)
        if self._cb:
            self._cb([self,"_set_nr",txt])

    def _set_attr(self,txt=""):
        self._set_mode("-")
        if type(txt) is str:
            self.attr["text"] = "{}".format(txt)
            if txt.startswith("EMPTY"):
                self.attr["bg"] = "#fa0"
            else:
                if txt in MAIN._FIX_FADE_ATTR:
                    self._set_mode("F")
                else:
                    self._set_mode("S")

        if self._cb:
            self._cb([self,"_set_attr",txt])


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

        self.b = tk.Button(frameS,bg="#ffa",text="{}".format(self.nr), width=4,command=test_command,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.label = self.b
        self.elem.append(self.b)
        
        self.b = tk.Scale(frameS,bg="#ffa", width=28,from_=from_,to=to,command=self.fader_event)
        self.elem_fader = self.b
        self.b.pack(fill=tk.Y, side=tk.TOP)
        if init is not None:
            self.b.set(init)
        self.elem.append(self.b)
        
        self.b = tk.Button(frameS,bg="lightblue",text="0", width=4,command=self.set_nr,font=self.font8 )
        self.elem_nr=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)

        self.b = tk.Button(frameS,bg="lightblue",text="", width=5,command=self.set_attr,font=self.font8 )
        self.attr=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)
        f = tk.Frame(frameS)
        #f.pack()


        self.b = tk.Button(frameS,bg="lightblue",text="", width=4,command=self.set_mode,font=self.font8 )
        self.mode=self.b
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        #self.b.pack(fill=tk.BOTH, side=tk.LEFT)
        self.elem.append(self.b)

        #self.b = tk.Button(frameS,bg="lightblue",text="+>", width=4,command=self.set_mode,font=self.font8 )
        #self.xmode=self.b
        #self.b.pack(fill=tk.BOTH, side=tk.TOP)
        #self.elem.append(self.b)

        self.b = tk.Label(frameS,bg="black",text="", width=4,font=self.font8 )
        self.b.pack(fill=tk.BOTH, side=tk.TOP)
        self.elem.append(self.b)


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


def frame_of_show_list(frame,cb=None):
    c=0
    r=0
    base = showlib.Base()
    for i in ["name","stamp"]: #,"create"]:
        b = tk.Label(frame,bg="grey",text=i)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
    r+=1
    blist = showlib.list_shows()
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

class on_focus():
    def __init__(self,name,mode):
        self.name = name
        self.mode = mode
    def cb(self,event=None):
        #print("on_focus",event,self.name,self.mode)
        try:
            e = MAIN.master.commands.elem["."]
        except:pass

        if self.mode == "Out":
            cmd="xset -display :0.0 r rate 240 20"
            #print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#aaa"
                e["activebackground"] = "#aaa"
            except:pass
        if self.mode == "In":
            cmd = "xset -display :0.0 r off"
            #print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#fff"
                e["activebackground"] = "#fff"
            except:pass

class DummyCallback():
    def __init__(self,name="name"):
        self.name = name
    def cb(self,event=None):
        cprint("DummyCallback.cb",[self.name,event])

class WindowContainer():
    def __init__(self,args): #title="title",master=0,width=100,height=100,left=None,top=None,exit=0,cb=None,resize=1):
        global MAIN #lf_nr
        self.args = {"title":"title","master":0,"width":100,"height":100,"left":None,"top":None,"exit":0,"cb":None,"resize":1}
        self.args.update(args)
        
        cprint("WindowContainer.init()",self.args["title"],color="yellow")
        #cprint("WindowContainer.init()",id(self.args),color="yellow")
        #cprint("  ",self.args,color="yellow")

        ico_path="./icon/"
        self.cb = MAIN.cb

        if self.args["master"]: 
            self.tk = tkinter.Tk()
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
            self.tk.withdraw() # do not draw
            self.tk.resizable(self.args["resize"],self.args["resize"])
            self.tk.tk_setPalette(background='#bbb', foreground='black', activeBackground='#aaa', activeForeground="black")

            defaultFont = tkinter.font.nametofont("TkDefaultFont")
            cprint(defaultFont)
            defaultFont.configure(family="FreeSans",
                                   size=10,
                                   weight="bold")
            # MAIN MENUE
            try:
                self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"main.png"))
            except Exception as e:
                cprint(" Exception GUIWindowContainer.__init__",e)
        else:
            # addtional WINDOW
            self.tk = tkinter.Toplevel()
            self.tk.iconify()
            #self.tk.withdraw() # do not draw
            self.tk.protocol("WM_DELETE_WINDOW", self.close)
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
                cprint(" Exception on load window icon",self.args["title"])
                cprint(" Exception:",e)
            #time.sleep(3)
            self.tk.deiconify()



        self.tk["bg"] = "black"
        self.tk.bind("<Button>",self.callback)
        self.tk.bind("<Key>",self.callback)
        self.tk.bind("<KeyRelease>",self.callback)
        self.tk.bind("<FocusIn>", on_focus(self.args["title"],"In").cb)
        self.tk.bind("<FocusOut>", on_focus(self.args["title"],"Out").cb)

        self.tk.title(""+str(self.args["title"])+" "+str(MAIN.lf_nr)+":"+str(MAIN.rnd_id))
        MAIN.lf_nr+=1
        #self.tk.geometry("270x600+0+65")
        geo ="{}x{}".format(self.args["width"],self.args["height"])
        if self.args["left"] is not None:
            geo += "+{}".format(self.args["left"])
            if self.args["top"] is not None:
                geo += "+{}".format(self.args["top"])

        #self._event_clear = MAIN.tk_event(fix=0,elem=None,attr="CLEAR",data=self,mode="ROOT").cb
        self.tk.geometry(geo)
        self.show()

    def update_idle_task(self):
        if MAIN.INIT_OK:
            tkinter.Tk.update_idletasks(MAIN.gui_menu_gui.tk)

    def close(self,event=None):
        cprint("WindowContainer.close",self.args["title"],color="red")
        #cprint("  ",self.title)
        #cprint("  ",self.args)

        if self.args["title"] == "MAIN":
            MAIN.save_show()
            self.tk.destroy()
        try:
            self.tk.destroy()
        except Exception as e:
            cprint("WindowContainer.close err",e,color="red")

    def title(self,title=None):
        if title is None:
            return self.tk.title()
        else:
            #return self.tk.title(title)
            self.args["title"] = title
            return self.tk.title(""+str(self.args["title"])+" "+str(MAIN.lf_nr)+":"+str(MAIN.rnd_id))
    def show(self):
        self.tk.deiconify()
        pass
    def mainloop(self):
        #save_window_position_loop() #like autosave
        try:
            self.tk.mainloop()
        finally:
            self.tk.quit()
            cmd="xset -display :0.0 r rate 240 15"
            #print(cmd)
            os.system(cmd)

    def callback(self,event,data={}):#value=255):
        sstart = time.time()
        #time.sleep(0.1)
        if not MAIN._global_short_key:
            return 1

        #global MAIN #_shift_key
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
                    MAIN.save_show()

                    e = MAIN.master.setup_elem["SAVE\nSHOW"]
                    b = BLINKI(e)
                    b.blink()
                if str(event.keysym) == "c":
                    if MAIN.save_show():
                        MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)

                return

        if "keysym" in dir(event):
            if "Escape" == event.keysym:
                #MAIN.FIXTURES.clear()
                fixlib.clear(MAIN.FIXTURES.fixtures)
                MAIN.modes.val("ESC",1)
                MAIN.master.refresh_fix()
            elif event.keysym in ["Shift_L","Shift_R"]:
                #cprint(event.type)
                if "KeyRelease" in str(event.type) or str(event.type) in ["3"]:
                    MAIN._shift_key = 0
                else:
                    MAIN._shift_key = 1
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                #global MAIN #_ENCODER_WINDOW
                try:
                    if MAIN._shift_key:
                        MAIN._ENCODER_WINDOW.title("SHIFT/FINE ")
                    else:
                        MAIN._ENCODER_WINDOW.title("ENCODER") 
                except Exception as e:
                    cprint("exc9800",e)
                    #raise e

            elif event.keysym in "ebfclrmsRx" and value: 
                if "e" == event.keysym:
                    MAIN.modes.val("EDIT",1)
                elif "b" == event.keysym:
                    MAIN.modes.val("BLIND",1)
                elif "f" == event.keysym:
                    MAIN.modes.val("FLASH",1)
                elif "c" == event.keysym:
                    MAIN.modes.val("CFG-BTN",1)
                elif "l" == event.keysym:
                    MAIN.modes.val("LABEL",1)
                elif "r" == event.keysym:
                    MAIN.modes.val("REC",1)
                elif "R" == event.keysym:
                    MAIN.modes.val("REC-FX",1)
                elif "x" == event.keysym:
                    MAIN.modes.val("REC-FX",1)
                elif "m" == event.keysym:
                    x=MAIN.modes.val("MOVE",1)
                    if not x:
                        MAIN.EXEC.clear_move()
                elif "s" == event.keysym:
                    MAIN.modes.val("SELECT",1)
            elif event.keysym in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
                nr = int( event.keysym[1:]) # F:1-12
                nr = nr-1+81  
                cprint("F-KEY",value,nr,event.keysym)
                #print(event)
                MAIN.master.exec_go(nr-1,xfade=None,val=value)
            elif event.keysym in ["1","2","3","4","5","6","7","8","9","0"]:
                nr = int( event.keysym)
                if nr == 0:
                    nr = 10
                nr = nr-1+161  
                cprint("NUM-KEY",value,nr)
                MAIN.master.exec_go(nr-1,xfade=None,val=value)
            elif "numbersign" == event.keysym and value: # is char "#"
                cprint("numbersign !!")
                MAIN.save_show()

                for e in MAIN.master.setup_cmd:
                    cprint(e)
                e =  MAIN.master.setup_elem["SAVE\nSHOW"]
                cprint(e)
                b = BLINKI(e)
                b.blink()
                #e = MAIN.tk_event(fix=0,elem=None,attr="SAVE\nSHOW",mode="SETUP")
                #e.cb(event=event)
            elif "End" == event.keysym:
                MAIN.FIXTURES.fx_off("all")
                MAIN.CONSOLE.fx_off("all")
                MAIN.CONSOLE.flash_off("all")
            elif "Delete" == event.keysym:
                #MAIN.EXEC.delete(nr)
                if value:
                    MAIN.modes.val("DEL",1)

        #cprint("oipo "*10,round(int(time.time()-sstart)*1000,2))
 
class window_create_buffer():
    # könnte auch direkt im WindowContainer object eingebaut werden !?

    def __init__(self,args,cls,data,cb_ok=None,scroll=0,gui=None):
        self.args   = args.copy()
        self.cls    = cls
        self.cb_ok  = cb_ok
        self.data   = data
        self.scroll = scroll
        self.gui    = gui

    def create(self,hidde=0):

        obj = None
        w = WindowContainer(self.args)
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

class PopupList():
    def __init__(self,name="<NAME>",master=0,width=400,height=450,exit=1,left=_POS_LEFT+400,top=_POS_TOP+100,cb=None,bg="black"):
        self.name = name
        self.frame = None
        self.bg=bg
        self.cb = cb
        if cb is None: 
            cb = DummyCallback #("load_show_list.cb")
        #w = WindowContainer(self.name,master=master,width=width,height=height,exit=exit,left=left,top=top,cb=cb)
        args = {"title":self.name,"master":master,"width":width,"height":height,"exit":exit,"left":left,"top":top,"cb":cb}
        w = WindowContainer(args)
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

def showwarning(msg="<ERROR>",title="<TITLE>"):
    cprint("showwarning","MSG:",msg,"tilte:",title)

    if IS_GUI:
        _main = tkinter.Tk()
        defaultFont = tkinter.font.nametofont("TkDefaultFont")

        cprint("showwarning",defaultFont)

    if IS_GUI:
        defaultFont.configure(family="FreeSans",
                               size=10,
                               weight="normal")
        
        geo ="{}x{}".format(20,20)
        _main.geometry(geo)
        def _quit():
            time.sleep(1/10)
            _main.quit()
        thread.start_new_thread(_main.mainloop,())


        r=tkinter.messagebox.showwarning(message=msg,title=title,parent=None)
