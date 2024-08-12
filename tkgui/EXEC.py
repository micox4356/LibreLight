
import json
import time
import sys

import tkinter as tk
import traceback
import _thread as thread



import __main__ as MAIN

sys.path.insert(0,"/opt/LibreLight/Xdesk/")

INIT_OK = 1
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
        self.A_refresh_exec(arg,args)
        #self.B_refresh_exec(arg,args)

    def A_refresh_exec(self,*arg,**args):
        print("Gui",arg,args)


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


        #try:
        #    y = mc.get("EXEC-"+str(nr)) #,json.dumps(index))
        #    _jdata = json.loads(y)
        #    keys  = _jdata.keys()
        #except Exception as e:
        #    print("  ER2R mc...",e,nr)



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

            if "FL" in txt1:
                _fg = "#00e"
            
            out["fg"] = _fg #= "#00e"
            out["bg"] = _bg #= "#00e"
            cfg = out 

            b = self.elem_exec[nr]
            b.configure(fg=cfg["fg"],bg=cfg["bg"],activebackground=cfg["ba"],text=cfg["text"],fx=cfg["fx"])

    def B_refresh_exec(self,*arg,**args):
        #def OLD_get_exec_btn_cfg(nr):
        k = nr
        if 1:
            
            _bg = "grey"
            _ba = "grey"
            _fg = "lightgrey"
            _text = "N/V"
            txt = "None/nNone"
            txt1 = "None/nNone"

            if nr >= 0:
                if nr != k:
                    return #continue


            label = ""

            if k in EXEC.label_exec:
                label = EXEC.label_exec[k]
            
            ifval = 0
            fx_only = 0
            fx_color = 0
            if k in EXEC.val_exec and len(EXEC.val_exec[k]) :
                sdata = EXEC.val_exec[k]

                BTN="go"
                if "CFG" in sdata:#["BUTTON"] = "GO"
                    if "BUTTON" in sdata["CFG"]:
                        BTN = sdata["CFG"]["BUTTON"]
                txt="{} {} {}\n{}".format(k+1,BTN,len(sdata)-1,label)
                _text = txt

                if len(sdata) > 1:
                    ifval = 1
                    val_color = 0
                    for fix in sdata:
                        if fix == "CFG":
                            continue
                        for attr in sdata[fix]:
                            if "FX2" in sdata[fix][attr]:
                                if sdata[fix][attr]["FX2"]:
                                    fx_color = 1
                            if "FX" in sdata[fix][attr]:
                                if sdata[fix][attr]["FX"]:
                                    fx_color = 1
                            if "VALUE" in sdata[fix][attr]:
                                if sdata[fix][attr]["VALUE"] is not None:
                                    val_color = 1

                    if val_color:
                        _bg = "gold"
                        _ba = "#ffaa55"
                        if fx_color:
                            _fg = "blue"
                    else:   
                        if fx_color:
                            fx_only = 1
                else:
                    _bg = "grey"
                    _ba = "#aaa"


            if "\n" in txt:
                txt1 = txt.split("\n")[0]

            _fg = "black"
            if ifval:
                if fx_only:
                    _bg = "cyan"
                    _ba = "#55d4ff"

                if "SEL" in txt1:
                    _bg = "#77f"
            else: 
                _bg = "grey"
                _fg = "darkgrey"

                if "SEL" in txt1:
                    _fg = "blue"
                elif "ON" in txt1:
                    _fg = "#040"
                elif "GO" in txt1:
                    _fg = "#555"

            if "FL" in txt1:
                _fg = "#00e"
            
            out = {} # default
            out["fx"] = ""
            out["bg"] = "lightgrey"
            out["ba"] = "grey"
            out["fg"] = "grey"
            out["text"] = "?"
            
            out["fx"] = fx_color
            out["bg"] = _bg
            out["ba"] = _ba
            out["fg"] = _fg
            out["text"] = _text
            
            return out
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


def _refr_loop():
    time.sleep(3)
    while 1:
        gui._refresh_exec()
        time.sleep(3)
thread.start_new_thread(_refr_loop,())



root.mainloop()
