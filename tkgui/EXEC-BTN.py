
import json
import time
import sys

import tkinter as tk
from tkinter import font

import traceback
import _thread as thread


import dialog
DIALOG = dialog.Dialog()

gui=None
GLOBAL_old_btn_nr = -1
def Dcb(exec_nr): #DAILOG CONFIG CALLBACK
    def _Dcb(*args):
        print("Dcb:",args)
        msg=json.dumps([{"event":"EXEC-CFG","EXEC":exec_nr,"VALUE":255,"DATA":args[0]}]).encode("utf-8")
        cprint("SEND DIALOG.cb",msg,color="green")
        cmd_client.send(msg)
        def _X_refresh():
            global GLOBAL_old_btn_nr 
            if 1:#REFRESH:
                btn_nr = exec_nr
                time.sleep(1.2)
                print()
                print("CFG CB REFRESH !?",btn_nr)
                nr = btn_nr-1
                b = gui.elem_exec[nr]

                gui._refresh_exec_single(nr,b) #,METAS):
                time.sleep(0.2)
                nr2= GLOBAL_old_btn_nr
                if nr2 >= 0 and nr2 != nr:
                    gui._refresh_exec_single(nr2,b) #,METAS):
                    print("CFG CB2 REFRESH ",nr,nr2)
                if 1:
                    GLOBAL_old_btn_nr = nr
        thread.start_new_thread(_X_refresh,())
    return _Dcb

def Dcb_label(exec_nr): #DAILOG CONFIG CALLBACK
    def _Dcb(*args):
        print("Dcb_label:",args)
        if "Value" in args[0]:
            DATA = {"Label":args[0]["Value"]}
        #msg=json.dumps([{"event":"LABEL","EXEC":exec_nr,"VALUE":255,"DATA":args[0]}]).encode("utf-8")
        msg=json.dumps([{"event":"EXEC-LABEL","EXEC":exec_nr,"VALUE":255,"DATA":DATA}]).encode("utf-8")
        cprint("SEND DIALOG.cb",msg,color="green")
        cmd_client.send(msg)
        msg=json.dumps([{"event":"LABEL","EXEC":exec_nr,"VALUE":255,"DATA":{}}]).encode("utf-8")
        cmd_client.send(msg)
        def _X_refresh():
            global GLOBAL_old_btn_nr 
            if 1:#REFRESH:
                btn_nr = exec_nr
                time.sleep(1.2)
                print()
                print("CFG CB REFRESH !?",btn_nr)
                nr = btn_nr-1
                b = gui.elem_exec[nr]

                gui._refresh_exec_single(nr,b) #,METAS):
                time.sleep(0.2)
                nr2= GLOBAL_old_btn_nr
                if nr2 >= 0 and nr2 != nr:
                    gui._refresh_exec_single(nr2,b) #,METAS):
                    print("CFG CB2 REFRESH ",nr,nr2)
                if 1:
                    GLOBAL_old_btn_nr = nr
        thread.start_new_thread(_X_refresh,())
    return _Dcb

DIALOG._cb = Dcb(-3)
#d = dialog.Dialog()
#d.ask_exec_config(str(nr+1),button=button,label=label,cfg=cfg)


import __main__ as MAIN

_file_path = "/opt/LibreLight/Xdesk/"
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

import tool.git as git
#CAPTION += git.get_all()

CAPTION = "EXEC-BTN"
title = CAPTION
title += git.get_all()

INIT_OK = 1
IS_GUI = 0
from lib.cprint import cprint


import lib.libtk as libtk
import lib.libtk2 as libtk2
import lib.zchat as chat

import lib.mytklib as mytklib
import lib.tkevent as tkevent

#import tkgui.draw as draw

def draw_exec(gui,xframe,EXEC):
    
    i=0
    c=0
    r=0
    root = xframe
    
    frame = tk.Frame(root,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)

    gui.elem_exec = {}
    i=0
    for k in EXEC.val_exec:
        if i%(10*8)==0 or i ==0:
            c=0
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
            c+=7
            if i == 0:
                b = tk.Button(frame,bg="darkgrey", text="HELP",command=libtk.online_help("librelight:20-exec")) #"0&do=index"))
                b.grid(row=r, column=c, sticky=tk.W+tk.E)
            r+=1
            c=0
        i+=1
        v=0
        label = ""

        sdata=EXEC.val_exec[k]
        BTN="go"
        if "CFG" in sdata:#["BUTTON"] = "GO"
            if "BUTTON" in sdata["CFG"]:
                BTN = sdata["CFG"]["BUTTON"]


        txt=str(k+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label

        b = mytklib.ExecButton(frame,text=txt)

        b.bind("<Button>",       tkevent.tk_event(fix=0,elem=b,attr=k,data=gui,mode="EXEC").cb)
        b.bind("<ButtonRelease>",tkevent.tk_event(fix=0,elem=b,attr=k,data=gui,mode="EXEC").cb)
        
        if k not in gui.elem_exec:
            gui.elem_exec[k] = b
        b.grid(row=r, column=c, sticky=tk.W+tk.E)

        b.config(text="xx"+str(i))
        c+=1
        if c >=10:
            c=0
            r+=1
    time.sleep(0.1)
    gui._refresh_exec()
    print("##################################")

import tool.movewin as movewin
#movewin.check_is_started(CAPTION,_file_path)
movewin.check_is_started("EXEC-BTN","/opt/LibreLight/Xdesk/tkgui/EXEC-BTN.py")

_global_short_key = 1
root = None

cmd_client = chat.Client(port=30003)

try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None



class Refresher(): # DUMMY
    def __init__(self,*arg,**args):
        print(self,"__init__",arg,args)
    def reset(*arg,**args):
        print(self,"reset",arg,args)

class Command():
    def __init__(self):
        self.elem = {}

class MASTER(): # DUMMY
    def __init__(self,*arg,**args):
        print(self,"__init__",arg,args)
        #self.refresh_fix = Refresher()
        self.commands = Command()
    def refresh_fix(self,*arg,**args):# = Refresher()
        print(self,"refresh_fix",arg,args)
    def exec_go(self,nr,*arg,**args): #val=None,xfade=None,event=None,button="",ptfade=None):
        if _global_key_lock:
            return
        #def exec_go(nr,xfade=None,val=0):
        print(self,"MASTER",nr,arg,args)
        btn_nr = nr
        v = args["val"]
        
        msg=json.dumps([{"event":"EXEC","EXEC":btn_nr+1,"VAL":v,"NR-KEY":btn_nr}]).encode("utf-8")
        cprint("SEND MASTER.EXEC_GO:",msg,color="green")
        cmd_client.send(msg)

def refresh_fix(*arg,**args): # DUMMY
    print("refresh_fix",arg,args)

class Refresher_fix(): # DUMMY
    def __init__(self,*arg,**args):
        print(self,"init",arg,args)
    def reset(self,*arg,**args):
        print(self,"reset",arg,args)

refresher_fix =  Refresher_fix()

class Modes(): # DUMMY
    def __init__(self,*arg,**args):
        print("Modes.__init__",arg,args)
        self.modes = {}
    def val(self,*arg,**args):
        #print("Modes.val",arg,args)
        pass

master = MASTER() #{}
modes = Modes()

import tkinter as tk
class Exec(): # DUMMY
    def __init__(self):
        self.val_exec = {}
        for i in range(512):
            k=i #"ABC-{}".format(i+1)
            self.val_exec[k] = {"NAME":"XX"}
EXEC = Exec()
class Gui(): # DUMMY
    def __init__(self):
        self.elem_exec = []
        self.elem_meta = [None]*512
        self.old_btn_nr = -1
        self.METAS = []
        for i in range(512):
            self.METAS.append({})

    def _refresh_exec(self,*arg,**args):
        #print("EXEC_Gui._refresh_exec",arg,args)

        nr = 14-1

        METAS = []
        for i in range(512):
            nr = i #+1
            try:
                data = mc.get("EXEC-META-"+str(nr)) #,json.dumps(index))
                data = json.loads(data)
                METAS.append(data)
            except Exception as e:
                print("  ER1R mc...",e)

        self.METAS = METAS

        for nr,b in enumerate( self.elem_exec): #[nr]
            self._refresh_exec_single(nr,b,METAS)
            #time.sleep(0.001)

    def _refresh_exec_single(self,nr,b,METAS=None):
            if not METAS:
                try:
                    data = mc.get("EXEC-META-"+str(nr)) #,json.dumps(index))
                    data = json.loads(data)
                    self.METAS[nr] = data #.append(data)
                    print(time.time())
                    print(" _REFRESH_EXEC_SINGLE",nr,b,data)
                except Exception as e:
                    print("  ER1R mc...",e)

                METAS = self.METAS
            _bg = "grey"
            _ba = "grey"
            _bg = "grey"
            _fg = "#555" #darkgrey"
            _text = "0 N/V 0\n N/V"

            txt = "None/nNone"
            txt1 = "None/nNone"

            out = {} # default
            out["fx"] = ""
            out["bg"] = _bg # "grey"
            out["ba"] = _ba #"grey"
            out["fg"] = _fg
            out["text"] = _text #"? "+str(nr+1)

            META = {'LABEL': 'ERR',  'CFG': {}}
            META["CFG"] = {'FADE': 3.0, 'DEALY': 0, 'DELAY': 4.0, 'BUTTON': 'ON', 'HTP-MASTER': 100
                           ,'SIZE-MASTER': 100, 'SPEED-MASTER': 100, 'OFFSET-MASTER': 100, 'OUT-FADE': 10.0
                           ,'FIX-COUNT':0 ,'HAVE-FX':0,'HAVE-VAL':0
                         }
            
            try: 
                META = METAS[nr]
                label = "{} {} {}\n{}".format(nr+1,META["CFG"]["BUTTON"],META["CFG"]["FIX-COUNT"],META["LABEL"])
                out["text"] = str(label)

            except Exception as e:
                print("  ER4R",e,nr)
                time.sleep(0.001)
            try:
                txt1 = META["CFG"]["BUTTON"]
            except:
                pass

            if  META["CFG"]["FIX-COUNT"]: 
                _fg = "black"
                
            if  META["CFG"]["HAVE-VAL"]: 
                _fg = "black"
                _bg = "yellow"
                _ba = "#ffaa55"
                if "SEL" in txt1:
                    #_bg = "blue"
                    #_fg = "blue"
                    _bg = "gold"
                    _bg = "#77f"
                elif "ON" in txt1:
                    _bg = "gold"
                    _fg = "#040"
                    _fg = "black"
                elif "GO" in txt1:
                    _bg = "gold"
                    _fg = "#555"
                    _fg = "black"
                elif "FL" in txt1:
                    _bg = "gold"

            out["fx"] = ""
            if  META["CFG"]["HAVE-FX"] >= 1:
                out["fx"] = META["CFG"]["HAVE-FX"] # show FX on EXEC-BTN

            if  META["CFG"]["HAVE-FX"] >= 1 and META["CFG"]["HAVE-VAL"] == 0:
                _bg = "cyan"

            if "FL" in txt1:
                _fg = "#00e"
            
            out["fg"] = _fg #= "#00e"
            out["bg"] = _bg #= "#00e"
            cfg = out 
            
            self.elem_meta[nr] = META

            b = self.elem_exec[nr]
            b.configure(fg=cfg["fg"],bg=cfg["bg"],activebackground=cfg["ba"],text=cfg["text"],fx=cfg["fx"])

    def exec_go(self,*arg,**args):
        print("Gui.exec_go",arg,args)

        btn_nr = arg[0]
        v=args["val"]
        if "CFG-BTN" in modes.modes:
            button = self.elem_exec[btn_nr]
            label = str(btn_nr) #self.elem_meta[nr] = META
            
            if v:
                META = self.elem_meta[btn_nr] 
                print("META",META)
                cfg = META["CFG"]
                label = META["LABEL"]
                button = cfg["BUTTON"]
                DIALOG._cb = Dcb(btn_nr+1)
                DIALOG.ask_exec_config(str(btn_nr+1),button=button,label=label,cfg=cfg)
                #print("INFO",master.commands.elem)

            return #STOP

        if "LABEL" in modes.modes:
            button = self.elem_exec[btn_nr]
            label = str(btn_nr) #self.elem_meta[nr] = META
            
            if v:
                META = self.elem_meta[btn_nr] 
                print("META",META)
                cfg = META["CFG"]
                label = META["LABEL"]
                button = cfg["BUTTON"]
                DIALOG._cb = Dcb_label(btn_nr+1)
                #DIALOG.ask_exec_config(str(btn_nr+1),button=button,label=label,cfg=cfg)
                DIALOG.askstring("LABEL","LABEL EXE:"+str(btn_nr+1),initialvalue=label)
                #print("INFO",master.commands.elem)

            return #STOP

        PREFIX = ""
        REFRESH = 0
        for k in ["REC","EDIT","COPY","MOVE","DEL","REC-FX"]:#,"SELECT","FLASH","GO","EDIT"]:
            if k in modes.modes:
                PREFIX = str(k) #+"-"

        for k in ["REC","COPY","MOVE","DEL","REC-FX"]:
            if k in modes.modes:
                REFRESH = 1

        print(" ",[arg,args])
        edata={}
        if "event" in args:
            edata =  libtk2.serialize_event(args["event"])
        print(" ",edata)
        num = -1
        MOUSE = ""
        out={"event": "EXEC","EXEC":btn_nr+1,"VAL":v,"NR-KEY":btn_nr}
        if "num" in edata:
            num = edata["num"]
            if num == 1:
                out["MOUSE"]="LEFT"
            if num == 3:
                out["MOUSE"]="RIGHT"

        msg=json.dumps([out]).encode("utf-8")

        if not _global_key_lock:
            cmd_client.send(msg)
        cprint("SEND GUI.EXEC_GO",msg,color="green")


        def _X_refresh():
            #if 1:#REFRESH:
            time.sleep(0.2)
            print()
            print("REC REFRESH !?",PREFIX)
            nr = btn_nr
            b = self.elem_exec[nr]
            
            refresh_both = 0
            if self.old_btn_nr >= 0 and self.old_btn_nr  != nr:
                self.old_btn_nr = nr
                refresh_both = 1
                
            time.sleep(0.4)
            self._refresh_exec_single(nr,b) #,METAS):
            time.sleep(0.4)
            if refresh_both:
                self._refresh_exec_single(self.old_btn_nr,b) #,METAS):

            time.sleep(2.)
            self._refresh_exec_single(nr,b) #,METAS):
            if refresh_both:
                self._refresh_exec_single(self.old_btn_nr,b) #,METAS):

        thread.start_new_thread(_X_refresh,())

gui  = Gui()
 



import lib.libwin as libwin
name="EXEC"
pos_list = libwin.read_window_position()
geo = libwin.split_window_position(pos_list,name)
args = {"title":name,"master":0,"width":600,"height":113,"left":30+5,"top":30+5+400*2+10}
if geo:
   args.update(geo)

root = tk.Tk()

win_title="EXEC-BTN"
store = movewin.load_all_sdl(win_title)
print(store)
W=850
H=460
POS=[10,10]
if store:
    W = store[-4]
    H = store[-3]
    POS=[store[-2],store[-1]]


root.geometry('%dx%d+%d+%d' % (W, H, POS[0],POS[1]))
root.tk_setPalette(background='#bbb', foreground='black', activeBackground='#aaa', activeForeground="black")
defaultFont = tk.font.nametofont("TkDefaultFont")
defaultFont.configure(family="FreeSans",
                       size=10,
                       weight="bold")
# MAIN MENUE
try:
    ico_path = "/opt/LibreLight/Xdesk/icon/"
    root.iconphoto(False, tk.PhotoImage(file=ico_path+"exec.png"))
except Exception as e:
    print(" Exception GUIWindowContainer.__init__",e)

xframe = libtk.ScrollFrame(root,width=820,height=400,bd=1,bg="black",head=None,foot=None)
draw_exec(gui,xframe,EXEC)
root.title(title) #"TK-EXEC")

root.bind("<Button>",libtk2.tk_event)#
root.bind("<Key>",libtk2.tk_event)#,self.callback)
root.bind("<KeyRelease>",libtk2.tk_event)#,self.callback)
#root.bind("<FocusIn>",libtk2.tk_event)#, on_focus(self.args["title"],"In").cb)
#root.bind("<FocusOut>",libtk2.tk_event)#, on_focus(self.args["title"],"Out").cb)

import os

_global_key_lock = 0
def focus_in(event=None):
    _global_short_key = 0 # protect key-press-repeat
    cmd = "xset -display :0.0 r off"
    print("FOCUS_IN1", cmd)
    os.system(cmd)
    time.sleep(0.3)
    print("FOCUS_IN2", cmd)
    os.system(cmd)
    _global_short_key = 1 # protect key-press-repeat
    time.sleep(0.3)
    _global_key_lock = 0

def focus_out(event=None):
    _global_key_lock = 1
    _global_short_key = 0
    cmd="xset -display :0.0 r rate 240 20"
    print("FOCUS_OUT", cmd)
    #os.system(cmd) # DISABLED 

root.bind("<FocusIn>", focus_in)
root.bind("<FocusOut>", focus_out)


def _refr_loop():
    time.sleep(3)
    while 1:
        gui._refresh_exec()
        time.sleep(10)

thread.start_new_thread(_refr_loop,())

def _refr_loop2():
    time.sleep(3)
    while 1:
        try:
            global root,title
            data = mc.get("MODES")
            title2 = title +"  "+str(data)
            data = json.loads(data)
            #print("MODES",data)
            modes.modes = data
            if "S-KEY" in data:
                _global_short_key = 0
                if data["S-KEY"]:
                    _global_short_key = 1
            if root:
                root.title(title2)
        except Exception as e:
            print("  ER7R mc...",e)
            time.sleep(3)
        time.sleep(0.1)

thread.start_new_thread(_refr_loop2,())

root.mainloop()
