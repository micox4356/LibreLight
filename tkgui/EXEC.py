
import json
import time
import sys

import tkinter as tk
import traceback
import _thread as thread



import __main__ as MAIN

sys.path.insert(0,"/opt/LibreLight/Xdesk/")


IS_GUI = 0
import tkgui.draw as draw

#import lib.mytklib as mytklib
import lib.libtk as libtk
#import lib.tkevent as tkevent
#import lib.fixlib as fixlib

from lib.cprint import cprint


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
        print("refresh_fix",arg,args)
    def val(self,*arg,**args):
        print("val",arg,args)

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
    def _refresh_exec(self,*arg,**args):
        print("Gui",arg,args)
        #_XX +=1
        # _nr_ok = 0

        nr = 14-1
        jdata = {}
        keys = []
        
        labels = []
        if 10:
            nr = 0
            for i in range(512):
                nr = i #+1
                label = "err-{}".format(nr)
                try:
                    label = mc.get("EXEC-LABEL-"+str(nr)) #,json.dumps(index))
                except Exception as e:
                    print("  ER1R mc...",e)
                labels.append(label)

            try:
                y = mc.get("EXEC-"+str(nr)) #,json.dumps(index))
                jdata = json.loads(y)
                keys  = jdata.keys()
            except Exception as e:
                print("  ER2R mc...",e,nr)
        
        #for nr in EXEC.val_exec: 
        #for nr in range(200):
        for nr,b in enumerate( self.elem_exec): #[nr]
            out = {} # default
            out["fx"] = ""
            out["bg"] = "grey"
            out["ba"] = "grey"
            out["fg"] = "#999" #black" #grey"
            out["text"] = "? "+str(nr+1)
            
        
            try: 
                out["text"] = "GO\n"+str(labels[nr])
                if len(labels[nr]) >= 3:
                    out["bg"] = "orange" #yellow"
                    out["fg"] = "black" #grey"
            except Exception as e:
                print("  ER4R",e,nr)
                time.sleep(0.001)
            #xout["fx"] = fx_color
            #xout["bg"] = _bg
            #xout["ba"] = _ba
            #xout["fg"] = _fg
            #out["text"] = _text
            
            #return out
            cfg = out #get_exec_btn_cfg(nr)

            b = self.elem_exec[nr]
            b.configure(fg=cfg["fg"],bg=cfg["bg"],activebackground=cfg["ba"],text=cfg["text"],fx=cfg["fx"])
    def exec_go(*arg,**args):
        print("Gui",arg,args)

gui  = Gui()


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
root.mainloop()
