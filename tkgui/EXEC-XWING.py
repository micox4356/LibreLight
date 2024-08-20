

import sys
import time
import json

_file_path = "/opt/LibreLight/Xdesk/"
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

import tkgui.GUI as tkgui
import tool.git as git
#CAPTION += git.get_all()

CAPTION = "EXEC-XWING"
title = CAPTION
title += git.get_all()

INIT_OK = 1
IS_GUI = 0
from lib.cprint import cprint


import lib.libtk as libtk
import lib.libtk2 as libtk2

import lib.zchat as chat
console = chat.Client() #port=50001)

import lib.mytklib as mytklib
import lib.tkevent as tkevent


def set_exec_fader_cfg(nr,val,label="",color=""):
    #exec_wing = window_manager.get_obj(name="EXEC-WING") 
    if not exec_wing: 
        return
    try:
        if len(exec_wing.fader_elem) > nr:
            exec_wing.fader_elem[nr].attr["text"] =  label
            cfg = get_exec_btn_cfg(nr+80)
            exec_wing.fader_elem[nr].attr["bg"] = cfg["bg"]
            exec_wing.fader_elem[nr].attr["fg"] = cfg["fg"]

            #exec_wing.fader_elem[nr].attr["fx"] = cfg["fx"]

    except Exception as e:
        cprint("  set_exec_fader_cfg err:",e,color="red")
        print("  ",nr,val,label)
        raise e

def set_exec_fader(nr,val,label="",color="",info="info",change=0):
    #exec_wing = window_manager.get_obj(name="EXEC-WING") 
    if not exec_wing: 
        return

    try:
        exec_wing.set_fader(nr,val,color=color,info=info,change=change)
    except Exception as e:
        cprint(" - set_exec_fader err:",e,color="red")
        print("    ",nr,val,label)
        raise e
   

def set_exec_fader_all():
    print()
    cprint( "set_exec_fader_all()",color="green")
    for nr in range(10):
        _label = EXEC.label_exec[nr+80] # = label
        print("  set_exec_fader_all._label =",_label)
        set_exec_fader(nr,0,label=_label) 
        set_exec_fader_cfg(nr,0,label=_label)

def refresh_exec_fader_cfg():
    cprint( "set_exec_fader_all()",color="green")
    for nr in range(10):
        _label = EXEC.label_exec[nr+80] # = label
        #print("_label",_label)
        set_exec_fader_cfg(nr,0,label=_label)



def jclient_send(data):
    t_start = time.time()
    jtxt = data
    jdatas = []
    for jdata in data:
        if "CMD" in jdata:
            try:
                jdatas.append(jdata)
            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint("-----",color="red")

        elif "DMX" in jdata:

            try:
                jdata["DMX"] = int(jdata["DMX"])
                dmx = jdata["DMX"]

                if "ATTR" not in jdata:
                    # for fx off
                    jdatas.append(jdata)

                else: 
                    fix = "00000"
                    attr = "00000"
                    if "FIX" in jdata:    
                        fix  = jdata["FIX"]
                    if "ATTR" in jdata:    
                        attr = jdata["ATTR"]

                    dmx_fine = fixlib.get_dmx(FIXTURES.fixtures,fix,attr+"-FINE")
                    if jdata["DMX"] != dmx_fine and dmx > 0 and dmx_fine > 0:
                        jdata["DMX-FINE"] = dmx_fine
                    if "DMX-FINE" in jdata:
                        if jdata["DMX-FINE"] <= 0:
                            del jdata["DMX-FINE"] 
                       
                        

                    if jdata["ATTR"].startswith("_"):
                        pass # ignore attr._ACTIVE 
                    else:#
                        jdata["time"] = t_start
                        jdatas.append(jdata)
                
                #cprint("-- ",jdata,color="red")

            except Exception as e:
                cprint("jclient_send, Exception DMX ",color="red")
                cprint("",jdata,color="red")
                cprint(e,color="red")
                cprint("-----",color="red")
            
    jtxt = jdatas
    jtxt = json.dumps(jtxt)
    jtxt = jtxt.encode()
    console.send( jtxt ) #b"\00 ")
    cprint("{:0.04} sec.".format(time.time()-t_start),color="yellow")
    cprint("{:0.04} tick".format(time.time()),color="yellow")


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
            e= tkgui.EXEC_FADER(frameS,nr=j+1,fader_cb=self.event_cb)
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


class Command():
    def __init__(self):
        self.elem = {}

_global_key_lock = 0

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

class Modes(): # DUMMY
    def __init__(self,*arg,**args):
        print("Modes.__init__",arg,args)
        self.modes = {}
    def val(self,*arg,**args):
        #print("Modes.val",arg,args)
        pass

master = MASTER() #{}
modes = Modes()


import tool.movewin as movewin
#movewin.check_is_started(CAPTION,_file_path)
movewin.check_is_started("EXEC-XWING","/opt/LibreLight/Xdesk/tkgui/EXEC-XWING.py")

_global_short_key = 1
root = None


cmd_client = chat.Client(port=30003)

try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None






import lib.libwin as libwin
name="EXEC"
pos_list = libwin.read_window_position()
geo = libwin.split_window_position(pos_list,name)
args = {"title":name,"master":0,"width":600,"height":113,"left":30+5,"top":30+5+400*2+10}
if geo:
   args.update(geo)

import tkinter as tk
root = tk.Tk()

root.bind("<Button>",libtk2.tk_event)#
root.bind("<Key>",libtk2.tk_event)#,self.callback)
root.bind("<KeyRelease>",libtk2.tk_event)#,self.callback)

win_title="EXEC-XWING"
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
#draw_exec(gui,xframe,EXEC)
root.title(title) #"TK-EXEC")









#args = {"title":name,"master":0,"width":600,"height":415,"left":L1,"top":TOP+H1+HTB*2,"H1":H1,"W1":W1}
geo = libwin.split_window_position(pos_list,name)
if geo:
    args.update(geo)
data=[]
for i in range(10*3):
    data.append({"EXEC"+str(i):"EXEC"})

exec_wing = GUI_ExecWingLayout(root,xframe,data)
#def __init__(self,root,frame,data,title="tilte",width=800,start=81):

root.mainloop()




