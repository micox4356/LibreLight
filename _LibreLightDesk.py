#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
(c) 2012 micha@librelight.de

SPDX-License-Identifier: GPL-2.0-only
"""
import random
import subprocess
import string
import copy
import traceback

import json
import time
import sys
import os 

import _thread as thread

for i in range(30):
    print() # boot space

IS_GUI = 0
if __name__ == "__main__":
    IS_GUI = 1

import tool.movewin as movewin
import lib.fixlib as  fixlib
import lib.libwin as libwin
import lib.libtk as libtk
import lib.libconfig as libconfig

rnd_id  = str(random.randint(100,900))
rnd_id += " beta"
rnd_id2 = ""
rnd_id3 = ""
_ENCODER_WINDOW = None


__run_main = 0
if __name__ == "__main__":
    __run_main = 1
else:
    import __main__ 
    if "unittest" not in dir(__main__):
        __run_main = 1

import tool.git as git
rnd_id += git.get_all()


try:
    xtitle = __file__
except:
    xtitle = "__file__"

if "/" in xtitle:
    xtitle = xtitle.split("/")[-1]

sys.stdout.write("\x1b]2;"+str(xtitle)+" "+str(rnd_id)+"\x07") # terminal title


HOME = os.getenv('HOME')

space_font = None

INIT_OK = 0
_global_short_key = 1


path = "/home/user/LibreLight/"
#os.chdir(path)
f = open(path+"init.txt","r")
lines=f.readlines()
f.close()
out = []
for line in lines:
    if line != "EASY\n":
        out.append(line)
f = open(path+"init.txt","w")
f.writelines(out)
f.close()
if "--easy" in sys.argv:
    f = open(path+"init.txt","a")
    f.write("EASY\n")
    f.close()
    if not os.path.isdir(path+"show/EASY"):
        cmd = "cp -vrf '/opt/LibreLight/Xdesk/home/LibreLight/show/EASY' '{}/show/EASY' ".format(path)
        print(cmd)
        #input()
        os.system(cmd)
    # check if EASY show exist !

from lib.cprint import cprint
cprint("________________________________")
 
def cb(**args):
    cprint("MAIN.cb DUMMY",**args,color="red")


import lib.zchat as chat
import lib.motion as motion

from collections import OrderedDict

_FIX_FADE_ATTR = ["PAN","TILT","DIM","RED","GREEN","BLUE","WHITE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]




CUES    = OrderedDict()
groups  = OrderedDict()

class Modes():
    def __init__(self):
        self.modes = {}
        self.__cfg = {}
        self.__cb = None
    def val(self,mode,value=None): #like jquery
        if value is not None:
            return self.set(mode,value)
        elif mode in self.modes:
            return self.modes[mode]
    def list(self,_filter="all"): # actvie
        _modes = []
        for m in self.modes:
            v = self.val(m)
            if _filter == "active" and v:
                _modes.append(m)
            if _filter == "all": 
                _modes.append(m)
        return _modes
    def info(self):
        for m in self.modes:
            print("modes",m,self.val(m))
    def get(self,mode,value=None):
        return self.val(mode,value)
    def __check(self,mode):
        if mode not in self.modes:
            self.modes[mode] = 0
            self.__cfg[mode] = 0
    def cfg(self,mode,data={}):
        self.__check(mode)
        if type(data) is dict:
            for k in data:
                v = data[k]
                if v not in self.__cfg:
                    self.__cfg[k] = v
            return 1
        elif type(data) is str:
            if data in self.__cfg:
                return self.__cfg[data]
    def clear(self,protect=[]):
        protected = ["BLIND"]
        protected.extend(protect)
        for m in self.modes:
            if m in protected:
                continue
            self.modes[m] = 0

    def set(self,mode,value):
        protected = ["BLIND","CLEAR","REC-FX"]
        self.__check(mode)
        if mode == "CLEAR":
            return 1
        elif mode == "ESC":
            for m in self.modes:
                cprint("ESC",m)
                if m == "COPY":
                    EXEC.clear_copy()
                if m == "MOVE":
                    EXEC.clear_move()
                if m != "BLIND":
                    self.modes[m] = 0
                    self.callback(m)
            return 1

        if value:
            for m in self.modes:
                if m not in protected and mode not in protected and m != mode:
                    #cprint("-#-# clear mode",mode,m,value,color="red")
                    if self.modes[m]:
                        self.modes[m]= 0
                        self.callback(m)
            if self.modes[mode] and value == 1:
                if modes == "MOVE":
                    EXEC.clear_move()
                if modes == "COPY":
                    EXEC.clear_copy()
                self.modes[mode] = 0 # value
            else:
                self.modes[mode] = value #1 #value
        else:
            self.modes[mode] = 0 #value
            if modes == "COPY":
                EXEC.clear_copy()
            if modes == "MOVE":
                EXEC.clear_move()
        self.callback(mode)
        return value
    def set_cb(self,cb):
        if cb:
            self.__cb = cb
    def callback(self,mode):
        if self.__cb is not None and mode in self.modes:
            value = self.modes[mode]
            self.__cb(mode=mode,value=value)


modes = Modes()

#modes.val("BLIND", 0)
#modes.modes["BLIND"] = 0
modes.modes["ESC"] = 0
modes.modes["REC"] = 0
modes.modes["EDIT"] = 0
modes.modes["MOVE"] = 0
modes.modes["FLASH"] = 0
modes.modes["GO"] = 0
modes.modes["DEL"] = 0
modes.modes["REC-FX"] = 0
modes.modes["SELECT"] = 0
modes.modes["CFG-BTN"] = 0
modes.modes["LABEL"] = 0


POS   = ["PAN","TILT","MOTION"]
COLOR = ["RED","GREEN","BLUE","COLOR"]
BEAM  = ["GOBO","G-ROT","PRISMA","P-ROT","FOCUS","SPEED"]
INT   = ["DIM","SHUTTER","STROBE","FUNC"]

#client = chat.tcp_sender(port=50001)

def set_exec_fader_cfg(nr,val,label="",color=""):
    exec_wing = window_manager.get_obj(name="EXEC-WING") 
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
    exec_wing = window_manager.get_obj(name="EXEC-WING") 
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

# remote input - start (memcached)
def JCB(x,sock=None):
    for i in x:
        jv = x[i]

        try:
            jv = json.loads(jv)
            jv = jv[0]
            #print(jv)
            v = jv["iVAL"]
            #exec_wing.set_fader(0,v)
            set_exec_fader(0,v)
            set_exec_fader(1,200-v)
            set_exec_fader(2,int(v/2+10))
        except Exception as e:
            cprint("exception",e)
            print(sys.exc_info()[2])
        #print("remote in:",round(time.time(),0),"x",i,v)


if __name__ == "__main__":
    r1_server = chat.Server(port=30002)
    def server1_loop():
        while 1:
            r1_server.poll(cb=JCB)
            time.sleep(1/90)
    thread.start_new_thread(server1_loop,()) # SERVER


import lib.jsbc as JSBC

if __name__ == "__main__":
    r_server = chat.Server(port=30003,cb=JSBC.JSCB)
    def server_loop():
        while 1:
            r_server.poll(cb=JSBC.JSCB)
    thread.start_new_thread(server_loop,()) # SERVER


import lib.fifo as FIFO

if __name__ == "__main__":
    f_server = FIFO.read_loop() #chat.Server(port=30003,cb=JSBC.JSCB)
    f_server.loop(sleep=1)

    def f_server_read_loop():
        time.sleep(10)
        print("FIFO read_loop() __ ")
        while 1:
            try:
                data = f_server.read()
                for jdata in data:
                    # JSCB [{'event': 'EXEC', 'EXEC': 161, 'VAL': 0, 'NR-KEY': 1}]
                    print("FIFO:",jdata)
                    ok=1
                    for i in ["event","VAL","EXEC"]:
                        if i not in jdata:
                            ok=0
                    if ok:
                        if jdata["event"] != "EXEC":
                            continue

                        if "EXEC" in jdata:
                            exec_nr = jdata["EXEC"]
                        if "VAL" in jdata:
                            val = jdata["VAL"]

                        master.exec_go(exec_nr-1,xfade=None,val=val)
                else:
                    time.sleep(0.02)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("FIFO ERR1",e)
    
    thread.start_new_thread(f_server_read_loop,()) # SERVER


# read memcachd
memcache = None
try:
    import memcache
except Exception as e:
    cprint("Exception IMPORT ERROR",e)
        
class MC_FIX():
    def __init__(self,server="127.0.0.1",port=11211):
        cprint("MC.init() ----------" ,server,port,color="red")
        try:
            self.mc = memcache.Client(['{}:{}'.format(server,port)], debug=0)
        except Exception as e:
            cprint("-- Exception",e)

    def set(self,index="fix",data=[]):
        index = self.mc.get("index")
        self.mc.set("fix", data)


class MC():
    def __init__(self,server="127.0.0.1",port=11211):
        cprint("MC.init() ----------" ,server,port,color="red")
        try:
            #self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            self.mc = memcache.Client(['{}:{}'.format(server,port)], debug=0)
            #self.init()
        except Exception as e:
            cprint("-- Exception",e)

        # def init(self):
        data = {}
        start = time.time()
        delta = start
        index = self.mc.get("index")
        if index:
            for i in index:
                print("  key",i)
        self.last_fader_val = [-1]*512
        self.fader_map = []
        for i in range(30+1):
            self.fader_map.append({"UNIV":0,"DMX":0})

        try:
            fname = HOME + "/LibreLight/fader.json"
            f = open(fname)
            lines = f.readlines()
            cprint("FADER MAP",fname)

            for i,line in enumerate(lines):
                jdata = json.loads(line)
                print("  fader_map ->>",i,jdata)
                self.fader_map[i] = jdata

        except Exception as e:
            cprint("-- Except Fader_map",e)
        #exit()

    def ok(self):
        if self.mc: 
            return 1
        return 0

    def test(self):
        if not self.ok():
            return 
        self.mc.set("some_key", "Some value")
        self.value = mc.get("some_key")

        self.mc.set("another_key", 3)
        self.mc.delete("another_key")

    def loop(self):
        thread.start_new_thread(self._loop,())
        if not self.ok():
            return 

    def _exec_fader_loop(self,x):
        for i, line in enumerate(self.fader_map):
            try:
                #print(i,line)
                dmx = int(line["DMX"])
                if dmx > 0:
                    val = x[dmx-1]
                    #print("mc val",val)
                    #print("dmx_in change:",[i,val])
                    change = 0
                    if i < len(self.last_fader_val):
                        if self.last_fader_val[i] != val:
                            self.last_fader_val[i] = val
                            print("dmx_in change:",[i,val])
                            change = 1
                    set_exec_fader(nr=i,val=val,color="#aaa",info="dmx_in",change=change)
            except Exception as e:
                cprint("MC exc:",e,color="red")
                traceback.print_exc()
                pass

    def _loop(self):
        time.sleep(6)
        cprint("++++++++++ start.memcachd read loop",self )
        
        ip = libconfig.load_remote_ip()

        print("IP:",ip)
        #input()
        while 1:
            send = 0
            #print("+")
            try:
                #ip="10.10.10.13:0"
                #ip="ltp-out:0"
                x=self.mc.get(ip)
                #print(ip,len(x))
                   
                if x:
                    #print(ip,x)
                    #val = x[501-1]
                    #val = x[141-1]
                    self._exec_fader_loop(x)

                time.sleep(1/10)
            except Exception as e:
                cprint("exc", e)
                time.sleep(1)

_mc=MC()
_mc.loop()


def message_buss_loop():
    while 1:
        try:
            mc = memcache.Client(['127.0.0.1:11211'], debug=0)
            break
        except Exception as e:
            cprint("--1 message_buss_loop Exc",[e])
        time.sleep(2)

    while 1:
        try:
            key="MODES" 
            cfg = {}
            for k,v in modes.modes.items():
                if v:
                    cfg[k] = v

            cfg["S-KEY"] = _global_short_key
            mc.set(key,json.dumps(cfg))

        except Exception as e:
            cprint("--2 message_buss_loop Exc:",[e])
            time.sleep(2)
        time.sleep(0.2)

thread.start_new_thread(message_buss_loop,())

console = chat.Client() #port=50001)

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


def _highlight(fix,_attr="DIM"): 
    " patch test button "
    cprint("highlight",fix,"1")

    if fix not in FIXTURES.fixtures:
        return None

    d = FIXTURES.fixtures[fix]

    #for k,v in d.items():
    #    cprint("-",k,v)
    DMX = d["DMX"] + d["UNIVERS"]*512
    if "ATTRIBUT" in d:
        ATTR= d["ATTRIBUT"]
        data = {"VALUE":200,"DMX":1}
        attr = ""

        if _attr in ATTR:
            attr = _attr
        else:
            return #stop
        
    
        cprint(attr,ATTR[attr])
        old_val = ATTR[attr]["VALUE"]
        data["DMX"] = DMX + ATTR[attr]["NR"]-1
        cprint(attr,ATTR[attr])
        cprint(data)
        for i in range(3):
            cprint("highlight",fix,"0")
            data["VALUE"] = 100
            jclient_send([data])
            time.sleep(0.1)

            cprint("highlight",fix,"1")
            data["VALUE"] = 234
            jclient_send([data])
            time.sleep(0.3)

        
        cprint("highlight",fix,"0")
        data["VALUE"] = old_val 
        jclient_send([data])

def highlight2(fix,attr="DIM"):
    def x():
        highlight(fix,attr=attr)
    return x

def highlight(fix):
    cprint("highlight",fix)
    thread.start_new_thread(_highlight,(fix,"DIM"))
    thread.start_new_thread(_highlight,(fix,"RED"))
    thread.start_new_thread(_highlight,(fix,"GREEN"))
    thread.start_new_thread(_highlight,(fix,"BLUE"))

class ValueBuffer():
    def __init__(self,_min=0,_max=255):
        self._value = 2
        self._on = 1
        self._min=_min
        self._max=_max
    def check(self):
        if self._value < self._min:
            self._value = self._min
        elif self._value > self._max:
            self._value = self._max

    def inc(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value += round(value,4)
            else:
                self._value += value
        self.check()
        return self._value
    def val(self,value=None):
        if value is not None:
            if type(value) is float:
                self._value = round(value,4)
            else:
                self._value = value
        self.check()
        return self._value
    def on(self):
        self._on = 1
    def off(self):
        self._on = 0
    def _is(self):
        if self._on:
            return 1
        return 0

FADE = ValueBuffer()  #2 #0.1 #1.13
FADE.val(2.0)
FADE_move = ValueBuffer()  #2 #0.1 #1.13
FADE_move.val(4.0)

DELAY = ValueBuffer()  #2 #0.1 #1.13
DELAY.off()
DELAY.val(0.2)

fx_prm_main = {}
fx_prm_move = {"SIZE":40,"SPEED":8,"OFFSET":100,"BASE":"0","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":0,"WING":2,"WIDTH":100}

fx_color = {"A":"red","B":"blue"} 
fx_prm = {"SIZE":255,"SPEED":10,"OFFSET":100,"BASE":"-","START":0,"MODE":0,"MO":0,"DIR":1,"INVERT":1,"SHUFFLE":0,"WING":2,"WIDTH":25,"2D-X":1,"2D:MODE":0}
fx_x_modes = ["spiral","left","right","up","down","left_right","up_down"]

fx_modes = ["RED","GREEN","BLUE","MAG","YELLOW","CYAN"]
fx_mo    = ["fade","on","rnd","ramp","ramp2","cosinus","sinus","static"]

class FX_handler():
    def __init__():
        pass




class dummy_event():
    def __init__(self):
        self.num =0
        self.type = 4 #press 5 release
        self.set_value=-1


from lib import matrix
import lib.fxlib as fxlib


def process_matrix(xfixtures):
    fx_x = fx_prm["2D-X"]
    fx_mod = fx_x_modes[fx_prm["2D:MODE"]]

    r = _process_matrix(xfixtures,fx_x,fx_mod)
    return r 

def _process_matrix(xfixtures,fx_x,fx_mod):
    fix_count = len(xfixtures)
    cprint("----",fx_x,fx_mod)
    if fx_x > 1 and fix_count > fx_x:
        try: 
            w=fx_x
            h=int(fix_count/fx_x)

            if fx_mod == "spiral":
                _map = matrix.spiral(w,h)
            elif fx_mod == "up_down":
                _map = matrix.up_down(w,h)
            elif fx_mod == "left_right":
                _map = matrix.left_right(w,h)
            elif fx_mod == "left":
                _map = matrix.left(w,h)
            elif fx_mod == "right":
                _map = matrix.right(w,h)
            elif fx_mod == "up":
                _map = matrix.up(w,h)
            elif fx_mod == "down":
                _map = matrix.down(w,h)
            else:
                return xfixtures # do nothing

            matrix.mprint(xfixtures,w,h)
            out = ["0"]*(w*h)
            for i,f in enumerate(xfixtures):
                if i < w*h:
                    j = int(_map[i])
                    cprint(["i:",i,"f:",f,"j:",j])
                    out[j] = f

            matrix.mprint(out,w,h)
            xfixtures = out
        except Exception as e:
            cprint("matrix exception",e)

    return xfixtures

def check_backup_path():
    pass

def save_show_to_backup():
    pass

def check_save_path(basepath="",show_name=""):
    if basepath and show_name:
        cwd = os.getcwd()
        try:
            print("cwd:",cwd)
            cd = "/".join(basepath.split("/")[:-3])
            os.chdir(cd)

            mkdir = "/".join(basepath.split("/")[-3:])
            mkdir += str(show_name)
            CMD="mkdir -p '{}'".format(mkdir)
            print("CMD:",cd,";",CMD)
            os.system(CMD)

        finally:
            os.chdir(cwd)
    return True

def show_path_list():
    print()
    print("libwin  ", libwin.showlib.SHOW_DIR)
    print("movewin ", movewin.SHOW_PATH) 
    print("EXEC    ", EXEC.base.show_path)   
    print("FIXTURES", FIXTURES.base.show_path)
    print()

def show_path_reset():
    print("show_path_reset()")
    name = showlib.current_show_name() 
    SHOW_DIR  = showlib.BASE_PATH+"/show/"
    show_path_set(SHOW_DIR,name)

def show_path_set(path,name):
    SHOW_PATH = path + str(name) 
    SHOW_DIR = path

    libwin.showlib.SHOW_DIR = SHOW_DIR
    #movewin.showlib.SHOW_DIR = SHOW_DIR

    movewin.SHOW_PATH       = SHOW_PATH
    EXEC.base.show_path     = SHOW_PATH 
    FIXTURES.base.show_path = SHOW_PATH

def save_show_to_usb():
    cprint("*** "*20,color="yellow")
    CMD = "df | grep /media/$USER"
    CMD = "ls /media/$USER/"
    CMD = "mount  | grep /media/$USER | cut -d ' ' -f 3"
    r = os.popen(CMD)
    usbs = r.readlines()
    print("USB's:",usbs)
    for usb in usbs:
        usb = usb.strip()
        print(usb)
        
        cwd = os.getcwd()

        _show_name = showlib.current_show_name() 
        #_usbstick_path = "/media/user/"+str(usb)+"/LibreLight/show/" 
        _usbstick_path = ""+str(usb)+"/LibreLight/show/" 
        SHOW_DIR = libwin.showlib.SHOW_DIR 
        

        try: 
            if check_save_path(basepath=_usbstick_path,show_name=_show_name):
                
                #show_path_list()
                show_path_set(path=_usbstick_path,name=_show_name)

                a=EXEC.backup_exec()
                b=FIXTURES.backup_patch()
                c=libwin.save_window_position() 
                d=movewin.store_all_sdl()
        except FileNotFoundError as e:
            cprint("EXC",e,color="red")
        finally:
            show_path_reset()
            print(SHOW_DIR,showlib.current_show_path())
            cprint("   ","*** "*20,color="yellow")

        if a and b and d: # and c
            #show_path_list()
            cprint("SAVE SHOW OK",[a,b,c,d],_usbstick_path,color="green")

        cprint("--- "*20,color="yellow")


def save_show(fpath=None,new=0):
                
    # show_path_list()

    if fpath:
        a=EXEC.backup_exec(save_as=fpath,new=new)
        b=FIXTURES.backup_patch(save_as=fpath,new=new)
        c=libwin.save_window_position(save_as=fpath)
        d=movewin.store_all_sdl()
    else:
        print()
        print()
        cprint("SAVE SHOW ..",color="yellow")
        a=EXEC.backup_exec()
        b=FIXTURES.backup_patch()
        c=libwin.save_window_position() 
        d=movewin.store_all_sdl()

    if 1:
        save_show_to_usb()

    if a and b and d: # and c
        #show_path_list()
        cprint("SAVE SHOW OK",[fpath,new],[a,b,c,d],color="green")
        print()
        print()
        print()
        return 1
    cprint("SAVE SHOW FAIL",[fpath,new],[a,b,c,d],color="red")
    print()
    print()
    print()

def save_show_as(fname,new=0):
    print()
    print()
    fpath = showlib.generate_show_path(fname)

    info = "SAVE SHOW AS"
    if new:
        info = "SAVE (NEW) SHOW AS"

    cprint(info,fpath,fname,color="green")

    if showlib.create_new_show_path(fpath):
        return save_show(fpath,new)



import lib.showlib as showlib

class cb():
    def __init__(self,win):
        self.win = win
    def _callback(self,event):
        clobj=event.widget
        ## undermouse=find_withtag(master.CURRENT)
        undermouse=self.win.find_closest(self.win.CURRENT)
        cprint( repr(undermouse))
    def callback(self,event):
        cprint(__file__,self,"callback",event)
        cnv = self.win
        item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
        tags = cnv.gettags(item)
        #cnv.itemconfigure(self.tag, text=tags[0])
        cprint(tags,item)
        color = cnv.itemcget(item, "fill")
        cnv.itemconfig("all", width=1)#filla="green")
        cnv.itemconfig(item, width=3)#filla="green")
        cprint(color)
        cprint( hex_to_rgb(color[1:]))


import copy

def get_exec_btn_cfg(nr):
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
            have_fx  = 0
            have_val = 0
            fix_count = 0

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

                    fix_count += 1

                    for attr in sdata[fix]:
                        if attr.startswith("_"):
                            continue
                        if "FX2" in sdata[fix][attr]:
                            if sdata[fix][attr]["FX2"]:
                                fx_color = 1
                                have_fx  += 1
                        if "FX" in sdata[fix][attr]:
                            if sdata[fix][attr]["FX"]:
                                fx_color = 1
                                have_fx  += 1
                        if "VALUE" in sdata[fix][attr]:
                            if sdata[fix][attr]["VALUE"] is not None:
                                val_color = 1
                                have_val += 1
                    
                #if val_color:
                #    have_val += 1
                #if fx_color:
                #    have_fx  += 1


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

            sdata["CFG"]["HAVE-FX"]   = have_fx  
            sdata["CFG"]["HAVE-VAL"]  = have_val 
            sdata["CFG"]["FIX-COUNT"] = fix_count 


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

class Elem_Container():
    def __init__(self):
        self.commands = []
        self.val = {}
        self.elem = {}


import lib.execlib as execlib


class MASTER():
    def __init__(self):
        self.base = showlib.Base ()
        self.load()
        self._XX = 0

        self.all_attr =["DIM","PAN","TILT"]
        self.elem_attr = {}
        
        self.setup_elem = {} # Elem_Container()
        self.setup_cmd  = ["SAVE\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS","SAVE &\nRESTART","DRAW\nGUI","PRO\nMODE"]
        self.setup_cmd  = ["SAVE\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS","SAVE &\nRESTART","PRO\nMODE"]

        self.fx_main = Elem_Container()
        self.fx_main.commands =["REC-FX","FX OFF","\n"]
        self.fx_moves = Elem_Container()
        self.fx_moves.commands =[
                "FX:CIR","FX:PAN","FX:TILT", "WIDTH:\n100","DIR:\n0","INVERT:\n0","\n",
                "SHUFFLE:\n0","SIZE:\n","SPEED:\n","START:\n","OFFSET:\n","\n"
                ]
                #, "FX:SIN","FX:COS","FX:RAMP","FX:RAMP2","FX:FD","FX:ON","BASE:\n-"] #,"FX:RND" ]

        self.fx = Elem_Container()
        self.fx.commands =[
                "FX:DIM"," ", "WIDTH:\n25","WING:\n2","DIR:\n1","INVERT:\n1","\n","SHUFFLE:\n0"
                ,"SIZE:\n","SPEED:\n","START:\n","OFFSET:\n","BASE:\n-","2D-X:\n-","2D:MODE"
                ]
        self.fx_generic = Elem_Container()
        self.fx_generic.commands =["FX:SIN","FX:COS","FX:RAMP","FX:RAMP2","FX:FD","FX:ON","FX:STATIC"]

        self.fx_color = Elem_Container()
        self.fx_color.commands =["FX:RED","FX-C:A","FX-C:B"] 

        self.commands = Elem_Container()
        self.commands.commands =["\n","ESC","CFG-BTN","LABEL","-","DEL","-","\n"
                ,"SELECT","FLASH","GO","-","MOVE","S-KEY","\n"
                ,"BLIND","CLEAR","REC","EDIT","COPY",".","\n" 
                ]
        
        for i in range(8*8*8):
            if i not in EXEC.val_exec:
                name = "Preset:"+str(i+1)+":\nXYZ"
                #self.exec[i] = [i]
                EXEC.val_exec[i] = OrderedDict() # FIX 
                EXEC.val_exec[i]["CFG"] =  OrderedDict() # CONFIG 
                EXEC.label_exec[i] = "-"

        modes.set_cb(self.xcb)


    def jclient_send(self,data):
        # namespace wraper
        if not modes.val("BLIND"):
            jclient_send(data)

    def button_refresh(self,name,color,color2=None,text="",fg=None):
        #cprint("button_refresh",name,color)

        if color2 is None:
            color2 = color
        if text:
            text = "\n"+str(text)

        elem=None
        for elem in [self.commands.elem,self.fx.elem,self.fx_main.elem,self.fx_moves.elem]:
            try:
                if name in elem:
                    #print(" in xx.elem OK ",[name,color,name,text,color2])
                    if name in ["BLIND","CLEAR"] and color == "lightgrey":
                        color = "grey"
                        color2 = "grey"

                    elem[name]["bg"] = color
                    elem[name]["text"] = name+ text
                    elem[name].config(activebackground=color2)
                    if fg:
                        elem[name]["fg"] = fg

            except Exception as e:
                cprint(" master.button_refresh",self,e)
                cprint("  ",elem)

    def dialog_cfg_return(self,nr):
        # buffer nr
        def _cb(data):
            cfg    = EXEC._btn_cfg(nr) 
            button = EXEC.btn_cfg(nr) 
            label  = EXEC.label(nr) 
            if not data:
                cprint("err443",self,"_cb",data)
                return None
            cprint("btn_cfg._cb()",data)
            print( "dialog_cfg_retrun",data)
            if data:

                if "Button" in  data and type(data["Button"]) is str:
                    txt = data["Button"]
                    EXEC.btn_cfg(nr,txt)

                if "Label" in  data and type(data["Label"]) is str:
                    txt = data["Label"]
                    EXEC.label(nr,txt) 

                if "Delay" in  data and type(data["Delay"]) is str:
                    txt = data["Delay"]
                    try:
                        txt = float(txt) 
                        if "DELAY" in cfg:
                            cfg["DELAY"] = round(txt,2)
                    except e as Exception:
                        print("DELAY Exception",e)

                if "in-Fade" in  data and type(data["in-Fade"]) is str:
                    txt = data["in-Fade"]
                    try:
                        txt = float(txt) 
                        if "FADE" in cfg:
                            cfg["FADE"] = round(txt,2)
                    except e as Exception:
                        print("in-Fade Exception",e)

                if "out-Fade" in  data and type(data["out-Fade"]) is str:
                    txt = data["out-Fade"]
                    try:
                        txt = float(txt) 
                        cfg["OUT-FADE"] = round(txt,2)
                    except e as Exception:
                        print("out-Fade Exception",e)

            modes.val("CFG-BTN",0)
            master._refresh_exec(nr=nr)
        return _cb

    def btn_cfg(self,nr,testing=0):
        cfg    = EXEC._btn_cfg(nr) 
        button = EXEC.btn_cfg(nr) 
        label  = EXEC.label(nr) 

        dialog._cb = self.dialog_cfg_return(nr) # return cb()

        if 1: # testing:
            dialog.ask_exec_config(str(nr+1),button=button,label=label,cfg=cfg)
        else:
            dialog.askstring("CFG-BTN","GO=GO FL=FLASH\nSEL=SELECT EXE:"+str(nr+1),initialvalue=txt)

    def label(self,nr):
        txt = EXEC.label(nr) 
        def _cb(data):
            if not data:
                cprint("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            cprint("label._cb()",nr,txt)
            if txt:
                EXEC.label(nr,txt) 
            modes.val("LABEL", 0)

            master._refresh_exec(nr=nr)

        dialog._cb= _cb #_x(nr)
        dialog.askstring("LABEL","EXE:"+str(nr+1),initialvalue=txt)

    def button_clear(self):
        modes.clear()
        txt=""
        for m in modes.modes:
            if not modes.modes[m]:
                self.button_refresh(m,color="lightgrey",text=txt)

    def xcb(self,mode,value=None):
        cprint("  Master.xcb mode:",str(mode).rjust(10," "),value,color="yellow",end="")
        if value:
            cprint("===== ON  ======",color="green")
            txt = ""
            if mode == "REC-FX":
                modes.modes["REC"] = 1 # HACK !
                self.button_refresh("REC",color="red",text=txt)#,fg="blue")
                self.button_refresh(mode,color="red",text=txt)#,fg="blue")
            if value == 2:
                if mode in ["MOVE","COPY"]:
                    txt="to"
                self.button_refresh(mode,color="orange",text=txt)#,fg="blue")
            else:
                if mode in ["MOVE","COPY"]:
                    txt="from"
                self.button_refresh(mode,color="red",text=txt)#,fg="blue",text="from")
        else:
            cprint("===== OFF ======",color="red")
            if mode == "REC":
                modes.val("REC-FX",0)
            if mode == "REC-FX":
                modes.modes["REC"] = 0 # HACK !
                self.button_refresh("REC",color="lightgrey")#,fg="black")
            self.button_refresh(mode,color="lightgrey")#,fg="black")
        #modes.info()

    def load(self,fname=""):
        pass

    def exit(self):
        cprint("__del__",self)
        
    def refresh_exec(self):
        refresher_exec.reset() # = tkrefresh.Refresher()

    def _refresh_exec(self,nr=-1):
        s = time.time()
        cprint("EXEC.refresh_exec()")
        refresher_exec.reset() # = tkrefresh.Refresher()
        
        self._XX +=1
        self._nr_ok = 0
        ERR=""
        for nr in EXEC.val_exec: 
            cfg = get_exec_btn_cfg(nr)
        time.sleep(0.01)

    def refresh_fix(self):
        refresher_fix.reset() # = tkrefresh.Refresher()
    def _refresh_fix(self):
        cprint("_refresh_fix")
        s=time.time(); _XXX=0

        menu_buff = {"DIM":0,"DIM-SUB":0,"FIX":0,"FIX-SUB":0}

        elem_buffer = []

        for fix in FIXTURES.fixtures:                            
            sdata = FIXTURES.fixtures[fix]                            

            elem_attr_fix = None
            if fix in self.elem_attr:
                elem_attr_fix = self.elem_attr[fix]

            if "DIM" in sdata["ATTRIBUT"] and "_ACTIVE" in sdata["ATTRIBUT"] and len(sdata["ATTRIBUT"]) == 2:
                KEY = "DIM-SUB"
            else:
                KEY = "FIX-SUB"
            FIX = 0
            DIM = 0
            for attr in sdata["ATTRIBUT"]:
                _buff = {}
                row = sdata["ATTRIBUT"][attr]

                if attr.endswith("-FINE"):
                    continue

                b_attr = attr
                if b_attr == "_ACTIVE":
                    b_attr = "S"

                elem = None
                if elem_attr_fix:
                    if b_attr not in elem_attr_fix:
                        continue

                    elem = elem_attr_fix[b_attr]
                    if not elem:
                        continue
                

                
                if "elem" not in _buff:
                    _buff["elem"] = elem

                if not attr.startswith("_"):
                    v2 = row["VALUE"]
                    #_text  = "{} {}".format(str(attr).rjust(4,"0"),str(v2).rjust(4,"0")) # ~0.2 sec
                    _text  = "{} {}".format(attr,v2) 
                    _buff["text"] = _text

                if row["ACTIVE"]:
                    _buff["bg"] = "yellow"
                    _buff["abg"] = "yellow"

                    menu_buff[KEY] += 1
                    if b_attr == "S":
                        if KEY == "DIM-SUB":
                            DIM =1
                        else:
                            FIX =1
                else:
                    _buff["bg"] = "grey"
                    _buff["abg"] = "grey"

                if "FX" not in row: # insert FX2 excetption
                    row["FX"] = "" #OrderedDict()
                if "FX2" not in row: # insert FX2 excetption
                    row["FX2"] = {} #OrderedDict()
                #print("row",fix,row)    
                if row["FX"]:
                    _buff["fg"] = "blue"
                elif row["FX2"]:
                    _buff["fg"] = "red"
                else:
                    _buff["fg"] = "black"

                elem_buffer.append(_buff)

            menu_buff["FIX"] += FIX
            menu_buff["DIM"] += DIM

        try:
            for row in elem_buffer:
                elem = row["elem"]
                if not elem:
                     continue
                for e in row:
                    if e == "elem":
                        continue
                    v = row[e]

                    if e == "abg":
                        elem.config(activebackground=v)
                    else:
                        elem[e] = v
            w = window_manager.get_win("FIXTURES")
            if w:
                w.update_idle_task()
        except Exception as e:
            cprint("exc434",e,color="red")

        cprint("fix:",_XXX,round(time.time()-s,2),color="red");_XXX += 1
        cprint(gui_menu)

        menu_buff["FIX-SUB"] -= menu_buff["FIX"]
        if menu_buff["FIX-SUB"]:
            gui_menu.config("FIXTURES","bg","yellow")
            gui_menu.config("FIXTURES","activebackground","yellow")
        elif menu_buff["FIX"]:
            gui_menu.config("FIXTURES","bg","orange")
            gui_menu.config("FIXTURES","activebackground","orange")
        else:
            gui_menu.config("FIXTURES","bg","")
            gui_menu.config("FIXTURES","activebackground","")

        gui_menu.update("FIXTURES","{} : {}".format(menu_buff["FIX"],menu_buff["FIX-SUB"]))

        menu_buff["DIM-SUB"] -= menu_buff["DIM"]
        if menu_buff["DIM-SUB"]:
            gui_menu.config("DIMMER","bg","yellow")
            gui_menu.config("DIMMER","activebackground","yellow")
        elif menu_buff["DIM"]:
            gui_menu.config("DIMMER","bg","orange")
            gui_menu.config("DIMMER","activebackground","orange")
        else:
            gui_menu.config("DIMMER","bg","")
            gui_menu.config("DIMMER","activebackground","")


        gui_menu.update("DIMMER","{} : {}".format(menu_buff["DIM"],menu_buff["DIM-SUB"]))

        cprint("fix:",_XXX,round(time.time()-s),color="red"); _XXX += 1

    def exec_rec(self,nr):
        cprint("Master.exec_rec","-- EXEC RECORD ------------------------------")
        _filter=""
        if modes.val("REC-FX"):
            _filter="ONLY-FX"

        data = fixlib.get_active(FIXTURES.fixtures,_filter=_filter)
        EXEC.rec(nr,data)
            
        sdata=data
        EXEC.val_exec[nr] = sdata
        
        modes.val("REC-FX",0)
        modes.val("REC",0)
        
        cfg = get_exec_btn_cfg(nr)
        #master._refresh_exec()
        return 1
    def exec_edit(self,nr):
        cprint("Master.exec_edit","-- EXEC EDIT ------------------------------")
        fixlib.clear(MAIN.FIXTURES.fixtures)
        self.exec_select(nr)
        event=None
        self.exec_go(nr,xfade=0,event=event,val=255,button="go")
        modes.val("EDIT", 0)
        master.refresh_fix()
        refresher_fix.reset() # = tkrefresh.Refresher()

    def exec_select(self,nr):
        cprint("Master.exec_select","-- EXEC SELECT ------------------------------")
        sdata = EXEC.val_exec[nr]
        cmd = ""
        for fix in sdata:
            if fix == "CFG":
                continue
            for attr in sdata[fix]:
                #v2 = sdata[fix][attr]["VALUE"]
                #v2_fx = sdata[fix][attr]["FX"]
                #print( self.data.elem_attr)
                #if fix in self.elem_attr:
                #    if attr in self.elem_attr[fix]:
                #        elem = self.elem_attr[fix][attr]
                FIXTURES.fixtures[fix]["ATTRIBUT"][attr]["ACTIVE"] = 1
                FIXTURES.fixtures[fix]["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
                #elem["bg"] = "yellow"

    def exec_go(self,nr,val=None,xfade=None,event=None,button="",ptfade=None):
        s=time.time()
        t_start = time.time()
        if xfade is None and FADE._is():
            xfade = FADE.val()
        
        if ptfade is None and FADE_move._is():
            ptfade = FADE_move.val()

        print()
        cprint("Master.exec_go","-- EXEC GO FADE -----",nr,val)

        rdata = EXEC.get_raw_map(nr)
        if not rdata:
            return 0

        cfg   = EXEC.get_cfg(nr)
        if not cfg:
            cprint(" NO CFG",cfg,nr)
            return 0

        xFLASH = 0
        value=None
        cprint(" exec_go",nr,cfg)
        if modes.val("SELECT") or ( "BUTTON" in cfg and cfg["BUTTON"] == "SEL") and val and not button: #FLASH
            self.exec_select(nr)
        elif modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL") and not button: #FLASH
            xFLASH = 1
            xfade = 0
            if type(val) is not type(None) and val == 0 :
                value = "off"
                xfade=0
                if "OUT-FADE" in cfg:
                    xfade=cfg["OUT-FADE"]
            if event:
                if str(event.type) == "ButtonRelease" or event.type == '5' :
                    value = "off"
                    xfade=0
                    if "OUT-FADE" in cfg:
                        xfade=cfg["OUT-FADE"]


            cprint(" exec_go() FLUSH",value,color="red")
            #print(";",rdata)
            print(" cfg:",cfg)
            fcmd  = FIXTURES.update_raw(rdata,update=0)
            #print(":",fcmd) # raw dmx
            self._exec_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH,nr=nr)
                
        elif not val:
            cprint("exec_go() STOP",value,color="red")
        elif button == "on" or ( modes.val("ON") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["on","ON"])):
            fcmd  = FIXTURES.update_raw(rdata)
            self._exec_go(rdata,cfg,fcmd,value,xfade=0,xFLASH=xFLASH)
        elif button == "go" or ( modes.val("GO") or ( "BUTTON" in cfg and cfg["BUTTON"] in ["go","GO"])): 
            fcmd  = FIXTURES.update_raw(rdata)
            e=time.time()
            #print("_GO TIME:","{:0.02f}".format(e-s),int(e*10)/10)
            self._exec_go(rdata,cfg,fcmd,value,xfade=xfade,xFLASH=xFLASH,ptfade=ptfade,nr=nr)
            e=time.time()
            #print("GO TIME:","{:0.02f}".format(e-s),int(e*10)/10)
        return

        if not (modes.val("FLASH") or ( "BUTTON" in cfg and cfg["BUTTON"] == "FL")): #FLASH
            self.refresh_exec()
            self.refresh_fix()

        cprint("exec_go",time.time()-t_start)

    def _exec_go(self,rdata,cfg,fcmd,value=None,xfade=None,event=None,xFLASH=0,ptfade=0,nr=None):
        if xfade is None and FADE._is():
            xfade = FADE.val()

        if ptfade is None and FADE_move._is():
            ptfade = FADE_move.val()
        cprint("EXEC._exec_go() len=",len(rdata),cfg)
        if xfade is None:
            xfade = cfg["FADE"]
        if ptfade is None:
            ptfade = cfg["FADE"]
        #vcmd = reshape_exec( rdata ,value,[],xfade=xfade,fx=1) 
        #cprint(rdata,color="red")
        vcmd = execlib.reshape_exec( rdata ,value,xfade=xfade,ptfade=ptfade) 

        cmd = []
        delay=0
        for i,v in enumerate(fcmd):
            #print("go",i,v)
            if xFLASH:
                vcmd[i]["FLASH"] = 1

            DMX = fcmd[i]["DMX"]
            
            if "VALUE" in vcmd[i] and type(vcmd[i]["VALUE"]) is type(float):
                vcmd[i]["VALUE"] = round(vcmd[i]["VALUE"],3)
            if value is not None:
                vcmd[i]["VALUE"] = value 
            if value == "off":
                if "FX2" in vcmd:
                    vcmd[i]["FX2"]["TYPE"] = value
            if "FIX" in fcmd:
                vcmd[i]["FIX"] = fcmd["FIX"]

            if DMX and vcmd[i]:
                vcmd[i]["DMX"] = DMX

            if type(nr) is not type(None):
                vcmd[i]["EXEC"] = str(int(nr)+1)

            cmd.append(vcmd[i])

        if cmd and not modes.val("BLIND"):
            jclient_send(cmd)

    def render(self):
        #Xroot.bind("<Key>",tk_event(fix=0,elem=None,attr="ROOT",data=self,mode="ROOT").cb)
        #self.draw_input()
        pass
        


##draw_sub_dim


import tkgui.dialog as dialoglib
dialog = dialoglib.Dialog()


from tkgui.draw import *
from tkgui.GUI import *



class LOAD_SHOW_AND_RESTART():
    def __init__(self,fname=""):
        self.fname=fname
        self.base = showlib.Base()

    def cb(self,event=None,force=0):
        print()
        print()
        print()


        cprint("LOAD_SHOW_AND_RESTART.cb force={} name={}".format(force,self.fname),color="red" )
        if not self.fname and not force:
            return 0
        if self.base.show_name == self.fname and not force:
            cprint("filename is the same",self.fname)
            return 0
        if not force:
            self.base._set(self.fname)

        cprint("LOAD SHOW:",event,self.fname)

        BASE_PATH = "/opt/LibreLight/Xdesk/"
        cmd="_LibreLightDesk.py"
        arg = ""
        print("fork",[BASE_PATH,cmd,arg])
        if "--easy" in sys.argv:
            arg = "--easy"
        
        movewin.process_kill(BASE_PATH+"tksdl/")
        os.execl("/usr/bin/python3", BASE_PATH, cmd,arg)
        sys.exit()
                





lf_nr = 0


        
from tkinter import PhotoImage 

_shift_key = 0

class WindowManager():
    def __init__(self):
        self.windows = {}
        self.obj = {}
        self.nr= 0
        self.first=""
        self.window_init_buffer = {}

    def update(self,w,name="",obj=None):
        name = str(name)

        for k in self.windows:
            if k == name:
                self.windows[str(name)] = w
                self.obj[str(name)] = obj

    def new(self,w,name="",obj=None,wcb=None):
        name = str(name)

        if wcb and name:
            self.window_init_buffer[name] = wcb

        if not self.first:
            if name:
                self.first = name
            else:
                self.first = str(self.nr)

            if w:
                w.tk.state(newstate='normal')
                w.tk.attributes('-topmost',True)

        if name:
            self.windows[str(name)] = w
            self.obj[str(name)] = obj
        else:
            self.windows[str(self.nr)] = w
            self.obj[str(self.nr)] = obj
            self.nr+=1

    def mainloop(self):
        self.windows[self.first].mainloop()

    def get_win(self,name):
        #cprint(".get_win(name) =",name)
        name = str(name)
        if name in self.windows:
            out = self.windows[name]
            #cprint(out)
            return out

    def get(self,name):
        return get_win(name)

    def get_obj(self,name):
        name = str(name)
        if name in self.windows:
            out = self.obj[name]
            return out

    def create(self,name):
        #cprint( "create WindowContainer",name)

        if name in self.window_init_buffer:
            c = self.window_init_buffer[name] 
            w,obj,cb_ok = c.create()
            window_manager.update(w,name,obj)

            if cb_ok:
                cb_ok()

            resize = 1
            if "resize" in c.args:
                if not c.args["resize"]:
                    resize = 0
            #if resize:
            libwin.get_window_position(_filter=name,win=w) 

            if name in ["ENCODER"]:
                global _ENCODER_WINDOW 
                _ENCODER_WINDOW = w
            if name in ["DIMMER","FIXTURES"]:
                refresher_fix.reset() # = tkrefresh.Refresher()

    def _check_window_is_open(self,name):
        try:
            win = self.windows[name]
            if "tk" not in dir(win):
                return 0
            return win.tk.winfo_exists()
        except Exception as e:
            cprint("_check_window_is_open err",e,color="red")

    def top(self,name):
        name = str(name)
        if name not in self.windows:
            cprint(name," not in self.windows",self.windows.keys())
            return 

        if not self._check_window_is_open(name):
            cprint(" ",name," window is closed ! ")
            self.create(name)
        
        w = self.windows[name]

        if not str(type(w)).startswith("<class 'function'>"): 
            w.tk.attributes('-topmost',True)
            w.tk.attributes('-topmost',False)
            w.tk.update_idletasks()
        else:
            print(" 2.2-",w)
            w()


class Console():
    def __init__(self):
        pass

    def flash_off(self,fix):
        pass

    def fx_off(self,fix):
        cprint("Console.fx_off()",fix)
        if not fix or fix == "all":
            j = []
            if 0:
                jdata = {'VALUE': None, 'args': [], 'FX': 'alloff::::', 'FADE': 2, 'DMX': '0'}
                j.append(jdata)
                jdata = {'VALUE': None, 'args': [], 'FX': 'alloff::::', 'FADE': 2,'FLASH':1, 'DMX': '0'}
                j.append(jdata)
            else:
                jdata = {'VALUE': None, 'args': [], 'FX2': {"TYPE":"alloff"}, 'FADE': 2,'FLASH':1, 'DMX': '1'}
                j.append(jdata)

            if not modes.val("BLIND"):
                jclient_send(j)
            return 0




window_manager = WindowManager()

CONSOLE = Console()
EXEC = execlib.EXEC()
     
def refresh_exec_mc():
    time.sleep(10)
    while 1:
        try:
            pass#
            execlib.exec_set_mc(EXEC.label_exec,EXEC.val_exec)
        except Exception as e:
            print("refresh_exec_mc ERR",e)
            time.sleep(5) # extra time
        time.sleep(3) # refresh time

thread.start_new_thread(refresh_exec_mc,())

FIXTURES = fixlib.Fixtures()
FIXTURES.gui = GUIHandler()

def LOAD_SHOW():
    EXEC.load_exec()
    FIXTURES.load_patch()
LOAD_SHOW()

master = MASTER()



print("main",__name__)

import lib.tkrefresh as tkrefresh


refresher_fix = tkrefresh.Refresher()
refresher_fix.time_delta = 0.50 
refresher_fix.name = "fix"
refresher_fix.reset() 
refresher_fix.cb = master._refresh_fix

refresher_exec = tkrefresh.Refresher()
refresher_exec.time_delta = 10 #0
refresher_exec.name = "exec"
refresher_exec.reset() 
refresher_exec.cb = master._refresh_exec

refresher_exec = tkrefresh.Refresher()
refresher_exec.time_delta = 10 #0
refresher_exec.name = "exec-fader"
refresher_exec.reset() 
refresher_exec.cb = refresh_exec_fader_cfg

def loops(**args):
    time.sleep(5) # wait until draw all window's 
    cprint("-> run loops")
    thread.start_new_thread(refresher_fix.loop,())
    thread.start_new_thread(refresher_exec.loop,())

thread.start_new_thread(loops,())

class window_create_sdl_buffer():
    def __init__(self,args,cls,data,cb_ok=None,scroll=0,gui=None):
        self.args   = args.copy()
        self.cls    = cls
        self.cb_ok  = cb_ok
        self.data   = data
        self.scroll = scroll
        self.gui    = gui

    def create(self,hidde=0):
        cprint()
        return [self.cls,self.cls,None] #w,obj,cb_ok


def open_sdl_window():
    cprint("open_sdl_window ... delay 1sec",color="yellow")
    time.sleep(1)
    if "--easy" not in sys.argv:
        movewin.startup_all_sdl()

thread.start_new_thread(open_sdl_window,())

mc_fix = MC_FIX()
def mc_fix_loop():
    global master
    time.sleep(5)
    c=0
    while 1:
        try:
            if c >= 1:
                #master._refresh_exec()
                c=0
                for nr in EXEC.val_exec: 
                    cfg = get_exec_btn_cfg(nr)
        except Exception as e:
            print("MC_FIX EXCEPTION",e)
            #raise e
        c+=1
        try:
            data = FIXTURES.fixtures 
            mc_fix.set(index="fix",data=data)
        except Exception as e:
            print("MC_FIX EXCEPTION",e)
        time.sleep(1/10)

thread.start_new_thread(mc_fix_loop,())


if __run_main:
    cprint("main")

    TOP = libtk._POS_TOP + 15
    L0 = libtk._POS_LEFT 
    L1 = libtk._POS_LEFT + 95
    L2 = libtk._POS_LEFT + 920 
    W1 = 810
    H1 = 550
    HTB = 23 # hight of the titlebar from window manager

    pos_list = libwin.read_window_position()
    #geo = libwin.split_window_position(pos_list,name)
    #args = {"title":name,"master":0,"width":600,"height":113,"left":L1+5,"top":TOP+5+HTB*2+H1}
    #geo = libwin.split_window_position(pos_list,name)
    #if geo:
    #   args.update(geo)
    

    data = []
    #data.append({"text":"COMMAND"})
    #data.append({"text":"CONFIG"})

    data.append({"text":"PATCH"})
    data.append({"text":"DIMMER"})
    data.append({"text":"FIXTURES"})
    data.append({"text":"FIX-LIST"})
    #data.append({"text":"EXEC-BTN","name":"EXEC-BTN"})
    data.append({"text":"EXEC-BTN","name":"EXEC-BTN"})
    data.append({"text":"EXEC-WING"})
    data.append({"text":"---"})
    data.append({"text":"SETUP"})
    data.append({"text":"COMMAND"})
    data.append({"text":"LIVE"})
    data.append({"text":"FX"})
    data.append({"text":"ENCODER"})
    data.append({"text":"COLORPICKER","name":"COLOR"})
    data.append({"text":"---"})
    data.append({"text":"FIXTURE-EDITOR","name":"FIX-EDIT"})
    data.append({"text":"CONFIG"})
    data.append({"text":"SDL-MIDI"})
    data.append({"text":"CLOCK"})
    data.append({"text":"RAY-DMX"})
    data.append({"text":"SDL-DMX"})
    data.append({"text":"SDL-VPU"})
    data.append({"text":"SDL-OSZI"})
    data.append({"text":"Nodescanner","name":"NodeScan"})
    data.append({"text":"---"})
    data.append({"text":"---"})
    data.append({"text":"- DEMO -"})
    data.append({"text":"---"})
    data.append({"text":"XWING"})
    #data.append({"text":"TK-EXEC"})
    #data.append({"text":"EXEC-BTN","name":"EXEC-BTN"})
    data.append({"text":"SDL-STAGE"})
    data.append({"text":"SDL-Shader"})
    data.append({"text":"TABLE"})

    #data.append({"text":"MASTER-WING"})

    name="MAIN"
    args = {"title":"MAIN","master":1,"width":80,"height":H1,"left":L0,"top":TOP,"resize":1}

    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_menu 
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    window_manager.top(name)

    gui_menu_gui = window_manager.get_win(name)
    gui_menu = window_manager.get_obj(name)
    master._refresh_fix()








    # =======================================================================
    if 0:
        name="EXEC-BTN"
        args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
        geo = libwin.split_window_position(pos_list,name)
        if geo:
            args.update(geo)

        data  = EXEC
        cls   = draw_exec #GUI_ExecWingLayout
        cb_ok = None #set_exec_fader_all
        

        c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
        window_manager.new(None,name,wcb=c)
        if libwin.split_window_show(pos_list,_filter=name):
            window_manager.top(name)


        #print(dir(cls))
        #print(cls)
        #sys.exit()
    # =======================================================================
    name="SDL-MIDI"
    def sdl_config():
        cmd="nohup /usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/midi.py &"
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/midi.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="SDL-VPU"
    def sdl_config():
        cmd="python3 /opt/LibreLight/Xdesk/vpu/watchdog_vpu.py -single"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="SDL-OSZI"
    def sdl_config():
        cmd="python3 /opt/LibreLight/ASP/monitor/oszi_grid.py" 
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="SDL-DMX"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/dmx.py " #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="RAY-DMX"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tkray/dmx.py " #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="EXEC-BTN" #"TK-EXEC"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tkgui/EXEC-BTN.py " #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    # =======================================================================
    name="Nodescanner" #"TK-EXEC"
    def sdl_config():
        cmd="nohup /usr/bin/python3 /opt/LibreLight/Xdesk/tool/TK-Nodescanner.py" #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    # =======================================================================
    name="XWING" #"TK-EXEC"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tkgui/EXEC-XWING.py " #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="SDL-STAGE"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk//3d/stage_3d.py " #&"
        print(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="SDL-Shader"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk//3d/demo_shaders.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="FIX-LIST"
    def sdl_config():
        cmd="/usr/bin/python3 /opt/LibreLight/Xdesk/tksdl/fix.py " #&"
        print(cmd)
        #os.popen(cmd)

        def xyz123(cmd):
            os.system(cmd)
        thread.start_new_thread(xyz123,(cmd,))
        return [None,None,None]
    #class window_create_sdl_buffer():
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = sdl_config #: None #GUI_CONF
    cb_ok = None

    c = window_create_sdl_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="CONFIG"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data = []
    cls = GUI_CONF
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="DIMMER"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_DIM
    data = FIXTURES
    ok_cb=None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="FIXTURES"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    cls = GUI_FIX
    ok_cb=None
    data = FIXTURES

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="FIXTURE-EDITOR"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data=[]
    for i in range(12*6):
        data.append({"text"+str(i):"test"})

    import tkgui.fix as guifix

    cls = guifix.GUI_FixtureEditor
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)

    
    # =======================================================================
    name="MASTER-WING"
    args = {"title":name,"master":0,"width":75,"height":405,"left":L0,"top":TOP+H1-220,"resize":0}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)

    data=[]
    for i in range(2):
        data.append({"MASTER"+str(i):"MASTER"})

    cls = GUI_MasterWingLayout #(w1,data)
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="EXEC-WING"
    args = {"title":name,"master":0,"width":600,"height":415,"left":L1,"top":TOP+H1+HTB*2,"H1":H1,"W1":W1}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    data=[]
    for i in range(10*3):
        data.append({"EXEC"+str(i):"EXEC"})

    cls   = GUI_ExecWingLayout
    cb_ok = set_exec_fader_all

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="ENCODER"
    args = {"title":name,"master":0,"width":620,"height":113,"left":L0+710,"top":TOP+H1+15+HTB*2}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_enc #(master,w.tk)#Xroot)
    cb_ok = None
    data = FIXTURES #master

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name = "SETUP"
    args = {"title":name +" SHOW:"+master.base.show_name,
                "master":0,"width":445,"height":42,"left":L1+10+W1,"top":TOP,"resize":10}
    args["title"]  = "SETUP SHOW:"+master.base.show_name
    geo = libwin.split_window_position(pos_list,name)
    try:
        geo["width"] = args["width"]
        geo["height"] = args["height"]
    except:pass

    if geo:
        args.update(geo)

    cls = draw_setup #(master,w.tk)
    data = []
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name = "COMMAND"
    args = {"title":name,"master":0,"width":415,"height":130,"left":L1+10+W1,"top":TOP+81,"resize":10}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_command #(master,w.tk)
    data = []
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name = "LIVE"
    args = {"title":name,"master":0,"width":415,"height":42,"left":L1+10+W1,"top":TOP+235,"resize":10}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_live #(master,w.tk)
    data = []
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name = "CLOCK"
    args = {"title":name,"master":0,"width":335,"height":102,"left":L1+10+W1+80,"top":TOP+H1+HTB+160,"resize":0}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cclock = X_CLOCK()
    cls = cclock.draw_clock 
    data = []
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="FX"
    args = {"title":name,"master":0,"width":415,"height":297+30,"left":L1+10+W1,"top":TOP+302,"resize":1}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_fx #(master,w.tk)
    data = []
    cb_ok = None

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="PATCH"
    args = {"title":name,"master":0,"width":W1,"height":H1,"left":L1,"top":TOP,"foot":1,"head":1}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = GUI_PATCH
    data = FIXTURES

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=1)
    window_manager.new(None,name,wcb=c) #,obj)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)


    # =======================================================================
    name="COLORPICKER"
    args = {"title":name,"master":0,"width":600,"height":113,"left":L1+5,"top":TOP+5+HTB*2+H1}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    cls = draw_colorpicker #(master,w.tk,FIXTURES,master)
    data = [FIXTURES,master]
    cb_ok = None #FIXTURES

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)

    # =======================================================================
    name="TABLE"
    args = {"title":name,"master":0,"width":600,"height":113,"left":L1+5,"top":TOP+5+HTB*2+H1}
    geo = libwin.split_window_position(pos_list,name)
    if geo:
        args.update(geo)
    #cls = draw_colorpicker #(master,w.tk,FIXTURES,master)
    cls = TableFrame #(root=w.tk)#,left=80,top=620)
    data = [FIXTURES,master]
    cb_ok = None #FIXTURES

    c = libtk.window_create_buffer(args=args,cls=cls,data=data,cb_ok=cb_ok,gui=master,scroll=0)
    window_manager.new(None,name,wcb=c)
    if libwin.split_window_show(pos_list,_filter=name):
        window_manager.top(name)



    def wm_mainloop():
        try:
            window_manager.mainloop()
        finally:
            print()
            print()
            cmd="xset -display :0.0 r rate 240 20"
            os.system(cmd)
            cprint(" - EXIT -",color="red")
            BASE_PATH = "/opt/LibreLight/Xdesk/"
            movewin.process_kill(BASE_PATH+"tksdl/")
            master.exit()
            sys.exit()

    wm_mainloop() #window_manager.mainloop()
    # thread.start_new_thread(wm_mainloop,()) # break TKINTER !!!
    
    while 1:
        print("loop..")
        time.sleep(1)


