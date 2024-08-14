#!/usr/bin/python3

import os
import time

import tkinter
import tkinter.simpledialog
tk = tkinter 
from idlelib.tooltip import Hovertip

import __main__ as MAIN
import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
from lib.cprint import cprint


class InputEventBlocker():
    def __init__(self):
        self.__init = 0
        self.cursor = "88888"

    def set(self,el,txt):
        self.e = el
        self.e_txt = txt
        self.cursor = "88888"

    def init(self):
        if self.__init == 0:
            try:
                self.el = tk.Button()
                self.e_txt = tk.StringVar()
                self.__init = 1
            except Exception as e:
                pirnt("init() exception",e)
    def _lock(self):
        MAIN._global_short_key = 0
        try:MAIN.master.commands.elem["S-KEY"]["bg"] = "red"
        except Exception as e:cprint("exc",self,e)
        cmd="xset -display :0.0 r rate 240 15"
        print(cmd)
        os.system(cmd)

    def _unlock(self):
        MAIN._global_short_key = 1
        try:MAIN.master.commands.elem["S-KEY"]["bg"] = "green"
        except Exception as e:cprint("exc",self,e)
        cmd = "xset -display :0.0 r off"
        print(cmd)
        os.system(cmd)


    def lock(self):
        self._lock()
        #self.e["bg"] = "red"
        #self.el.config({"background": "grey"})
        #self.e.focus()

    def unlock(self):
        self._unlock()
        #self.e["bg"] = "blue"
        #self.el.config({"background": "yellow"})
        #self.el.focus_set()

    def event(self,event,**args):
        self.init()
        #print()

        cprint(self,event,args)
        #print("###-",self.e_txt,dir(self.e_txt))
        if "S-KEY" not in MAIN.master.commands.elem:
            #cprint("<GLOBAL-GUI-EVENT-DISABLED>",event,color="red")
            return 

        if "num" in dir(event):
            self.lock()
        if "keysym" in dir(event):
            t=self.e_txt.get()
            if t and t[-1] == "<":
                t = t[:-1]
            if event.keysym == "Return" or event.keysym == "Tab" or event.keysym == "ISO_Left_Tab":
                self.unlock() 
                #self.e_txt.set(t)
            cprint("filter: get()",MAIN._global_short_key,t)
            t2 = t
            if MAIN._global_short_key == 0:
                if event.keysym == "BackSpace":
                    if len(t) > 1:
                        t2 = t[:-1]
                    else:
                        t2=""
                elif event.keysym == "Escape":
                    t2=""
                elif event.keysym == "space":
                    t2=t+" "
                elif event.char in "äöüÄÖÜ-_,.;:#'*+~":
                    t2=t+event.char
                elif len(event.keysym) == 1:
                    t2=t+event.keysym
            
                #self.e_txt.set(t2+"<")
        #time.sleep(0.2)

input_event_blocker = InputEventBlocker()

class DialogEvent():
    def __init__(self):
        self.el    = None
        self.e_txt = None
        self.master = None

    def _event(self,event,**args):
        print(self,"_event",event)
        if 10:#else:
            input_event_blocker.set( self.e , self.e_txt)
            input_event_blocker.event(event) #,args)

        if "keysym" in dir(event):
            if event.keysym == "Return":# or event.keysym == "Tab" or event.keysym == "ISO_Left_Tab":
                self.master.ok()

            elif event.keysym == "Escape":
                self.master.close()
            else:
                pass
                #self.el.focus()

class Dialog():
    def __init__(self):
        self.d = tkinter.simpledialog
        self._exit = None
        self._cb = self.dummy_cb
        self.data = {"Value:",None}
        #self.tk = tkinter.Toplevel() # break MAIN FONT !!
    def dummy_cb(self,_return):
        print("dialog.dummy_cb()",self,_return)
        pass

    def askstring(self,title="title",prompt="prompt:",initialvalue=""):
        old = 0
        if old:
            title = "*"+title
            txt = self.askstring_old(title=title,prompt=prompt,initialvalue=initialvalue)
            self._exit = {"Value":txt}
            self.data = {"Value":txt}
            self._cb(self._exit)
        else:
            title = "#"+title
            self.askstring_new(title=title,prompt=prompt,initialvalue=initialvalue)
    
    def askstring_old(self,title="title",prompt="prompt:",initialvalue=""):
        print(self.d)
        print(dir(self.d))
        txt = self.d.askstring(title=title,prompt=prompt,initialvalue=initialvalue)
        return txt

    def _close(self):
        print("dialog._close()",self._exit)
        self.tk.destroy()

    def close(self):
        self._close()
        time.sleep(0.1)
        input_event_blocker.unlock()
        self._cb(None)
        return {} #self._exit

    def ok(self):
        _data = {}
        for k,e in self.data.items():
            #print(k,dir(e))
            if e is not None:
                _data[k] = e.get()
        if "Value" not in _data:
            _data["Value"] = None


        #t=self.e_txt.get()#[:-1]
        #if "=" in t:
        #    t = t.split("=")[0]
        #self._exit = t
        self._exit = _data
        self._close()
        time.sleep(0.1)
        input_event_blocker.unlock()
        print(self,"ok()",self._exit)
        self._cb(self._exit)

    def _event(self,event,**args):
        print(self,"_event",event)
        if 0:#else:
            input_event_blocker.set( self.e , self.e_txt)
            input_event_blocker.event(event) #,args)
        if "keysym" in dir(event):
            if event.keysym == "Return":# or event.keysym == "Tab" or event.keysym == "ISO_Left_Tab":
                self.ok()

            if 1: # MAIN._global_short_key == 0:
                if event.keysym == "Escape":
                    self.close()

    def event(self,event,**args):
        print(self,"event",event)


        if 1:#else:
            input_event_blocker.set( self.e , self.e_txt)
            input_event_blocker.event(event) #,args)
        if "keysym" in dir(event):
            if event.keysym == "Return":# or event.keysym == "Tab" or event.keysym == "ISO_Left_Tab":
                self.ok()

            if 1: # MAIN._global_short_key == 0:
                if event.keysym == "Escape":
                    self.close()

    def ask_exec_config(self,prompt="",_cb=None,**args):
        print(self,"ask_exec_config()")
        print([prompt,args])
        self.data = {"Value:":None}
        self._exit = None

        try:
            self.close()
        except Exception as e:print(e)

        #self.tk = tkinter.Tk()
        self.tk = tkinter.Toplevel()
        #self.tk.withdraw() # do not draw
        self.tk.iconify()
        self.tk.geometry("500x200") #.format(120+c))
        self.tk.title("{} EXEC-CONFIG".format(prompt) )#+" "+":"+str(rnd_id))
        self.tk.attributes('-topmost',True)
        self.tk.protocol("WM_DELETE_WINDOW", self.close)
        self.tk.resizable(0,0)
        bg = "#e0e"
        bg = "#cd5"
        bg = "lightgrey"
        bg = "#bbb"
        self.tk["bg"] = bg
        #self.tk.overrideredirect(1)
        #self.tk.attributes('-toolwindow', True)
        #self.tk.state(newstate='iconic')



        self.fo = tk.Frame(self.tk,bd=1) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fo["bg"] = "red"
        self.fo["bg"] = "#eee"#lightgrey"
        self.fo.pack(side="top")
    

        self.fl = tk.Frame(self.fo,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fl["bg"] = "green"
        self.fl["bg"] = "#eee"#lightgrey"
        self.fl.pack(side="left")

        self.fm = tk.Frame(self.fo,width=20,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fm["bg"] = "#eee"#lightgrey"
        self.fm.pack(side="left",expand=1,fill="y")

        self.fr = tk.Frame(self.fo,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fr["bg"] = "blue"
        self.fr["bg"] = "#eee"#lightgrey"
        self.fr.pack(side="left")


        # ------------------------- frame right
        from_= 255
        to   = 0

        self.ff = tk.Frame(self.fr,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.ff["bg"] = "#99a"
        self.ff.pack(side="left")
        self.b = tk.Scale(self.ff,bg="lightblue", width=28,from_=from_,to=to,command=self._event)
        self.data["Master"] = self.b
        self.data["Master"].set(100)
        k = "HTP-MASTER"
        if "cfg" in args and k in args["cfg"]:
            #self.data["Master"].config(state="active")
            self.data["Master"].set(int(args["cfg"][k])) 
            self.data["Master"].config(state="disable")
        self.b.pack(side="top") #fill=tk.Y, side=tk.TOP)
        self.el = tk.Button(self.ff,text="Master",bg="lightblue",width=4)
        myTip = Hovertip(self.el,'HTP-MASTER')
        self.el.pack(side="top")


        from_= 200
        self.ff = tk.Frame(self.fr,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.ff["bg"] = "#99a"
        self.ff.pack(side="left")
        self.b = tk.Scale(self.ff,bg="lightblue",width=28,from_=from_,to=to,command=self._event)
        self.data["Size"] = self.b
        k = "SIZE-MASTER"
        if "cfg" in args and k in args["cfg"]:
            #self.data["Size"].config(state="active")
            self.data["Size"].set(int(args["cfg"][k])) 
            self.data["Size"].config(state="disable")
        self.b.pack(side="top") #fill=tk.Y, side=tk.TOP)
        self.el = tk.Button(self.ff,text="Size",bg="lightblue",width=4)
        myTip = Hovertip(self.el,'SIZE-MASTER')
        self.el.pack(side="top")

        from_= 400
        self.ff = tk.Frame(self.fr,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.ff["bg"] = "#99a"
        self.ff.pack(side="left")
        self.b = tk.Scale(self.ff,bg="lightblue", width=28,from_=from_,to=to,command=self._event)
        self.data["Speed"] = self.b
        k = "SPEED-MASTER"
        if "cfg" in args and k in args["cfg"]:
            self.data["Speed"].set(int(args["cfg"][k])) 
            self.data["Speed"].config(state="disable")
        self.b.pack(side="top") #fill=tk.Y, side=tk.TOP)
        self.el = tk.Button(self.ff,text="Speed",bg="lightblue",width=4)
        myTip = Hovertip(self.el,'SPEED-MASTER')
        self.el.pack(side="top")

        from_= 400
        self.ff = tk.Frame(self.fr,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.ff["bg"] = "#99a"
        self.ff.pack(side="left")
        self.b = tk.Scale(self.ff,bg="lightblue", width=28,from_=from_,to=to,command=self._event)
        self.data["Offset"] = self.b
        k = "OFFSET-MASTER"
        if "cfg" in args and k in args["cfg"]:
            #self.data["Offset"].config(state="active")
            self.data["Offset"].set(int(args["cfg"][k])) 
            self.data["Offset"].config(state="disable")
        self.b.pack(side="top") #fill=tk.Y, side=tk.TOP)

        self.el = tk.Button(self.ff,text="Offset",bg="lightblue",width=4)
        myTip = Hovertip(self.el,'OFFSET-MASTER')
        self.el.pack(side="top")
        #self.f = tk.Frame(self.fl) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        #self.f.pack(side="top")
        #self.elx = tk.Label(self.f,text="")
        #self.elx["bg"] = bg
        #self.elx.pack(side="left")

        # ----------------------------------- frame left

        self.f = tk.Frame(self.fl) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top",expand=1,fill="y")

        self.el = tk.Label(self.f,text=str("  "),anchor="e",width=7)
        self.el["bg"] = "#aaa"
        self.el.pack(side="left",expand=1,fill="y")

        #self.el = tk.Label(self.f,text=str(prompt),anchor="e",width=4)
        self.el = tk.Label(self.f,text="   ATTR  P/T",anchor="c",width=12)
        self.el["bg"] = "#aaa"
        self.el.pack(side="left",expand=1,fill="y")

        self.el2 = tk.Label(self.f,text="",anchor="w",width=10)
        self.el2.config(fg="#aaa")
        self.el2["bg"] = "#aaa"
        self.el2.pack(side="left")


        self.f2 = tk.Frame(self.fl) 
        self.f2.pack(side="top",expand=1,fill="y")
        self.data["in-Fade"] = tk.StringVar()
        self.el = tk.Label(self.f2,text="in-Fade",anchor="e",width=8)
        self.el.pack(side="left")
        self.e = tk.Entry(self.f2,textvariable=self.data["in-Fade"],width=4)
        print("---",self.data["in-Fade"].get())
        if "cfg" in args and "FADE" in args["cfg"]:
            self.data["in-Fade"].set(str(args["cfg"]["FADE"])) 
        print("---",self.data["in-Fade"].get())
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        self.e.bind("<Key>",self._event)
        self.e.bind("<Button>",self._event)
        self.e.pack(side="left")

        self.e7 = tk.Entry(self.f2,state="disable",textvariable="x",width=4)#self.data["in-Fade"],width=4)
        print("---",self.data["in-Fade"].get())
        #if "cfg" in args and "FADE" in args["cfg"]:
        #    self.data["in-Fade"].set(str(args["cfg"]["FADE"])) 
        print("---",self.data["in-Fade"].get())
        self.e7.config(highlightthickness=2)
        self.e7.config(highlightcolor= "red")
        self.e7.bind("<Key>",self._event)
        self.e7.bind("<Button>",self._event)
        self.e7.pack(side="left")
        self.el2 = tk.Label(self.f2,text="* only GO",anchor="w",width=9)
        self.el2.config(fg="#aaa")
        self.el2.pack(side="left")

        #self.el2 = tk.Label(self.f2,text="",anchor="w",width=9)
        #self.el2.config(fg="#aaa")
        #self.el2.pack(side="left")
        self.e1 = self.e
 

        
        self.f2 = tk.Frame(self.fl) 
        self.f2.pack(side="top",expand=1)
        self.data["out-Fade"] = tk.StringVar()
        self.data["out-Fade"].set("0.0")
        self.el = tk.Label(self.f2,text="out-Fade",anchor="e",width=8)
        self.el.pack(side="left")
        self.e   = tk.Entry(self.f2,textvariable=self.data["out-Fade"],width=4)
        print("---",self.data["out-Fade"].get())
        if "cfg" in args and "OUT-FADE" in args["cfg"]:
            self.data["out-Fade"].set(str(args["cfg"]["OUT-FADE"])) 
        print("---",self.data["out-Fade"].get())
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        self.e.bind("<Key>",self._event)
        self.e.bind("<Button>",self._event)
        self.e.pack(side="left")

        # P/T MOVE
        self.e7 = tk.Entry(self.f2,state="disable",textvariable="x",width=4)#self.data["in-Fade"],width=4)
        print("---",self.data["in-Fade"].get())
        #if "cfg" in args and "FADE" in args["cfg"]:
        #    self.data["in-Fade"].set(str(args["cfg"]["FADE"])) 
        print("---",self.data["in-Fade"].get())
        self.e7.config(highlightthickness=2)
        self.e7.config(highlightcolor= "red")
        self.e7.bind("<Key>",self._event)
        self.e7.bind("<Button>",self._event)
        self.e7.pack(side="left")

        self.el2 = tk.Label(self.f2,text="* only FL",anchor="w",width=9)
        self.el2.config(fg="#aaa")
        self.el2.pack(side="left")
        self.e1 = self.e



        self.f2 = tk.Frame(self.fl) 
        self.f2.pack(side="top",expand=1,fill="y")
        self.data["Delay"] = tk.StringVar()
        self.el = tk.Label(self.f2,text="Delay",anchor="e",width=8)
        self.el.pack(side="left")
        self.e = tk.Entry(self.f2,textvariable=self.data["Delay"],width=4)
        if "cfg" in args and "DELAY" in args["cfg"]:
            self.data["Delay"].set(str(args["cfg"]["DELAY"])) 
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        self.e.bind("<Key>",self._event)
        self.e.bind("<Button>",self._event)
        self.e.pack(side="left")
        self.el2 = tk.Label(self.f2,text="",anchor="w",width=15)
        self.el2.config(fg="#aaa")
        self.el2.pack(side="left")
        self.e2 = self.e
        
        self.f2 = tk.Frame(self.fl) 
        self.f2.pack(side="top",expand=1,fill="y")
        self.el = tk.Label(self.f2,text="Button",anchor="e",width=12)
        self.el.pack(side="left")

        self.e_txt = tk.StringVar()
        self.e = tk.OptionMenu(self.f2,self.e_txt,"FL", "SEL", "GO","ON") #,width=6)
        self.data["Button"] = self.e_txt
        self.e["width"] = 4
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        self.e_txt.set(str(""))

        ev1 = DialogEvent()
        ev1.e = self.e
        ev1.master = self
        ev1.e_txt = self.data["Button"]
        
        self.e.bind("<Key>",ev1._event)
        self.e.bind("<Button>",ev1._event)
        self.e.pack(side="left")
        if "button" in args and type(args["button"]) is str:
            self.e_txt.set(args["button"]) # default value
        self.e3 = self.e
        self.el2 = tk.Label(self.f2,text="",anchor="w",width=6)
        self.el2.config(fg="#aaa")
        self.el2.pack(side="left")
        del self.e_txt
        del ev1



        self.f = tk.Frame(self.fl) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")

        self.f2 = tk.Frame(self.f) 
        self.f2.pack(side="top",expand=1,fill="y")
        self.data["Label"] = tk.StringVar()
        self.el = tk.Label(self.f2,text="Label",anchor="e",width=8)
        self.el.pack(side="left")
        self.e = tk.Entry(self.f2,textvariable=self.data["Label"],width=15) #,command=ev._event)
        if "label" in args and type(args["label"]) is str:
            self.data["Label"].set(args["label"]) 

        #self.e["bg"] = "#eee"
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        self.e.icursor(999)
        #self.e.selection_range(0, 999)#"end")

        self.el2 = tk.Label(self.f2,text="",anchor="w",width=2)
        self.el2.config(fg="#aaa")
        self.el2.pack(side="left")
        
        ev = DialogEvent()
        ev.e = self.e
        ev.master = self
        ev.e_txt = self.data["Label"]


        self.e.bind("<Key>",ev._event)
        self.e.bind("<Button>",ev._event)
        self.e.pack(side="left")
        self.e1 = self.e
        del ev
        # ---------------------- frame bottom [ok,cancel]

        self.fu = tk.Frame(self.tk,bd=2) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fu["bg"] = "lightgrey"##eee"
        self.fu["bg"] = "#bbb"
        self.fu.pack(side="top")
        # --- Spacer ---- OK,Cancle
        self.f = tk.Frame(self.fu) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")
        self.elx = tk.Label(self.f,text="")
        self.elx["bg"] = bg
        self.elx["bg"] = "#bbb"
        self.elx.pack(side="left")

        self.f = tk.Frame(self.fu) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f["bg"] = "#bbb"
        self.f.pack(side="top")

        self.b = tk.Button(self.f,bg="lightgrey", text="OK",width=10,command=self.ok)
        self.b.config(padx=1)
        #self.b.bind("<Button>",tkevent.tk_event(fix=fix,mode="D-SELECT",elem=b).cb)
        self.b.pack(side="left")

        self.fxx = tk.Frame(self.f,width=20) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.fxx["bg"] = "#bbb"
        self.fxx.pack(side="left")

        self.b = tk.Button(self.f,bg="lightgrey", text="Cancel",width=10,command=self.close)
        self.b.config(padx=1)
        self.b.pack(side="left")

        self.f = tk.Frame(self.fu) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        #self.f["bg"] = "#bbb"
        self.f.pack(side="top")
        self.elx = tk.Label(self.f,text="")
        self.elx["bg"] = bg
        self.elx.pack(side="left")

        self.e.focus()
        #time.sleep(3)
        self.tk.deiconify()
    def askstring_new(self,title="title",prompt="prompt:",initialvalue=""):
        self.data = {}
        self._exit = None
        try:
            self.close()
        except Exception as e:print(e)
        #try:
        #    #self.tk.quit()
        #    print(dir(self.tk))
        #    self.close()
        #except Exception as e:print(e)

        #self.tk = tkinter.Tk()
        self.tk = tkinter.Toplevel()
        #self.tk.withdraw() # do not draw
        self.tk.iconify()
        c = prompt.count("\n") * 15
        self.tk.geometry("200x{}".format(120+c))
        self.tk.title(""+str(title) )#+" "+":"+str(rnd_id))
        self.tk.attributes('-topmost',True)
        self.tk.protocol("WM_DELETE_WINDOW", self.close)
        self.tk.resizable(0,0)
        bg = "#e0e"
        bg = "#aaa"
        self.tk["bg"] = bg
        #self.tk.overrideredirect(1)
        #self.tk.attributes('-toolwindow', True)
        #self.tk.state(newstate='iconic')

        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")
        self.elx = tk.Label(self.f,text="")
        self.elx["bg"] = bg
        self.elx.pack(side="left")

        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")

        self.el = tk.Label(self.f,text=prompt,anchor="w")
        self.el["bg"] = bg
        self.el.pack(side="left")
        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")
        self.e_txt = tk.StringVar()
        self.data["Value"] = self.e_txt
        #self.e = tk.Entry(self.f,state="readonly",textvariable=self.e_txt)
        self.e = tk.Entry(self.f,textvariable=self.e_txt)
        #self.e = tk.Button(self.f,textvariable=self.e_txt,relief="sunken",width=20)
        self.e["bg"] = "#fff"
        self.e.config(highlightthickness=2)
        self.e.config(highlightcolor= "red")
        #self.e_txt.set(str(initialvalue)+"<")
        self.e_txt.set(str(initialvalue))
        self.e.icursor(999)
        self.e.selection_range(0, 999)#"end")
        
        self.e.bind("<Key>",self.event)
        self.e.bind("<Button>",self.event)
        self.e.pack(side="top")

        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")
        self.elx = tk.Label(self.f,text="")
        self.elx["bg"] = bg
        self.elx.pack(side="left")

        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")

        self.b = tk.Button(self.f,bg="lightgrey", text="OK",width=10,command=self.ok)
        self.b.config(padx=1)
        #self.b.bind("<Button>",tkevent.tk_event(fix=fix,mode="D-SELECT",elem=b).cb)
        self.b.pack(side="left")

        self.b = tk.Button(self.f,bg="lightgrey", text="Cancel",width=10,command=self.close)
        self.b.config(padx=1)
        self.b.pack(side="left")

        self.f = tk.Frame(self.tk) #, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.f.pack(side="top")
        self.elx = tk.Label(self.f,text="")
        self.elx["bg"] = bg
        self.elx.pack(side="left")

        self.e.focus()
        #time.sleep(3)
        self.tk.deiconify()

