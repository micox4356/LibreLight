
import json
import time
import sys

import tkinter as tk
import traceback
import _thread as thread

import dialog
DIALOG = dialog.Dialog()
#d = dialog.Dialog()
#d.ask_exec_config(str(nr+1),button=button,label=label,cfg=cfg)

import __main__ as MAIN

sys.path.insert(0,"/opt/LibreLight/Xdesk/")

INIT_OK = 1
IS_GUI = 0
from lib.cprint import cprint

import tkgui.draw as draw
import lib.libtk as libtk
import lib.zchat as chat

root = None

cmd_client = chat.Client(port=30003)

try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None



class Refresher():
    def __init__(self,*arg,**args):
        print(self,"__init__",arg,args)
    def reset(*arg,**args):
        print(self,"reset",arg,args)
    
class MASTER():
    def __init__(self,*arg,**args):
        print(self,"__init__",arg,args)
        #self.refresh_fix = Refresher()
    def refresh_fix(self,*arg,**args):# = Refresher()
        print(self,"refresh_fix",arg,args)

def refresh_fix(*arg,**args):
    print("refresh_fix",arg,args)

class Refresher_fix():
    def __init__(self,*arg,**args):
        print(self,"init",arg,args)
    def reset(self,*arg,**args):
        print(self,"reset",arg,args)

refresher_fix =  Refresher_fix()

class Modes():
    def __init__(self,*arg,**args):
        print("Modes.__init__",arg,args)
        self.modes = {}
    def val(self,*arg,**args):
        print("Modes.val",arg,args)

master = MASTER() #{}
modes = Modes()

import tkinter as tk
class Exec():
    def __init__(self):
        self.val_exec = {}
        for i in range(512):
            k=i #"ABC-{}".format(i+1)
            self.val_exec[k] = {"NAME":"XX"}
EXEC = Exec()
class Gui():
    def __init__(self):
        self.elem_exec = []
        self.elem_meta = [None]*512

    def _refresh_exec(self,*arg,**args):
        print("Gui._refresh_exec",arg,args)

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


        for nr,b in enumerate( self.elem_exec): #[nr]
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

            META = {'LABEL': 'ERR', 'LEN': 2, 'CFG': {}}
            META["CFG"] = {'FADE': 3.0, 'DEALY': 0, 'DELAY': 4.0, 'BUTTON': 'ON', 'HTP-MASTER': 100, 'SIZE-MASTER': 100, 'SPEED-MASTER': 100, 'OFFSET-MASTER': 100, 'OUT-FADE': 10.0}
            
            try: 
                META = METAS[nr]
                label = "{} {} {}\n{}".format(nr+1,META["CFG"]["BUTTON"],META["LEN"],META["LABEL"])
                out["text"] = str(label)
                LEN = META["LEN"] #int(label.split("\n")[0].split()[-1])
                if LEN: # >= 3:
                    _bg = "orange" #yellow"
                    _fg = "black" #grey"
            except Exception as e:
                print("  ER4R",e,nr)
                time.sleep(0.001)
            try:
                txt1 = META["CFG"]["BUTTON"]
            except:
                pass
                
            if META["LEN"]:
                _fg = "black"
                _bg = "gold"
                _ba = "#ffaa55"
                if "SEL" in txt1:
                    #_bg = "blue"
                    #_fg = "blue"
                    _bg = "#77f"
                elif "ON" in txt1:
                    _fg = "#040"
                    _fg = "black"
                elif "GO" in txt1:
                    _fg = "#555"
                    _fg = "black"

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
        #print(" ",dir(arg))
        #print(" ",self)
        btn_nr = arg[0]
        v=args["val"]
        if "CFG-BTN" in modes.modes:
            button = self.elem_exec[btn_nr]
            label = str(btn_nr) #self.elem_meta[nr] = META

            if v:
                cfg = self.elem_meta[btn_nr] 
                DIALOG.ask_exec_config(str(btn_nr+1),button=button,label=label,cfg=cfg)
            return 
        msg=json.dumps([{"event":"EXEC","EXEC":btn_nr,"VAL":v,"NR-KEY":btn_nr}]).encode("utf-8")
        print("SPCIAL-KEY",msg)
        cmd_client.send(msg)

gui  = Gui()
 


#import memcache
#mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#import time
#while 1:
#    x=mc.get("MODE")
#    print(x)
#    time.sleep(1)



root = tk.Tk()

#root.withdraw() # do not draw
#root.resizable(1,1)
root.tk_setPalette(background='#bbb', foreground='black', activeBackground='#aaa', activeForeground="black")

defaultFont = tk.font.nametofont("TkDefaultFont")
#cprint(defaultFont)
defaultFont.configure(family="FreeSans",
                       size=10,
                       weight="bold")
# MAIN MENUE
#try:
#    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"main.png"))
#except Exception as e:
#    print(" Exception GUIWindowContainer.__init__",e)

#xframe=root
xframe = libtk.ScrollFrame(root,width=820,height=400,bd=1,bg="black",head=None,foot=None)
draw.draw_exec(gui,xframe,EXEC)
#xframe.pack()
root.title("DEMO TK-EXEC 2")


def _refr_loop():
    time.sleep(3)
    while 1:
        gui._refresh_exec()
        time.sleep(3)
thread.start_new_thread(_refr_loop,())

def _refr_loop2():
    time.sleep(3)
    while 1:
        try:
            global root
            title = "DEMO TK-EXEC"
            data = mc.get("MODES")
            title += "  "+str(data)
            data = json.loads(data)
            #print("MODES",data)
            modes.modes = data
            if root:
                root.title(title)
        except Exception as e:
            print("  ER7R mc...",e)
            time.sleep(3)
        time.sleep(0.5)

thread.start_new_thread(_refr_loop2,())

root.mainloop()
