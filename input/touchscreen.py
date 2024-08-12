#!/usr/bin/python3

#cat touchscreen_pointer_mapping_5.py 

# xte is in part of xautomation
# apt install xautomation

import os, tempfile
import time
import subprocess
from _thread import start_new_thread

import sys
sys.stdout.write("\x1b]2;TOUCHSCREEN EVENT\x07")

debug = 0

def mapFromTo_(x,a,b,c,d):
    y=(x-a)/(b-a)*(d-c)+c
    return y

def mapFromTo(value,in_min,in_max,out_min,out_max):
    #out_max -= 10
    #out_min += 10
    #y=(value-in_min)/(in_max-in_min)*(out_max-out_min)+out_min
    y= (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

    padding = 8 #px
    if y < out_min+padding:
        y = out_min+padding
    if y > out_max-padding:
        y = out_max-padding
    return y
   
class PIPE():
    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()
        try:os.mkdir(self.tmpdir)
        except:pass
        self.filename = os.path.join(self.tmpdir, 'myfifo')
    def init(self):
        print()
        print( "create ifio file")
        
        print( self.filename)
        try:
            os.mkfifo(self.filename)
        except OSError as e:
            print( "Failed to create FIFO: %s" % e)
        print( "ende")
        return self.filename

    def __del__(self):
        print( "PIPE DESTRUKTOR")
        #self.fifo.close()
        os.remove(self.filename)
        os.rmdir(self.tmpdir)



def get_touch_id():
    cmd = ["xinput"]

    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = sub.communicate()[0]

    #print( output)
    data = output.split("\n")

    odata = []
    pattern = "TouchController"
    print( "GET INPUT TUCHSCREEN ID")
    for line in data:
        if pattern in line:
            print( line,end="")
            if "id=" in line:
                 idx = line.index("id=")
                 idx = line.index("id=")
                 line = line[idx+3:]
                 line = line.split(" ")[0]
                 line = line.split("\t")[0]
            print( [line])
            odata.append(line)
    return odata



def enabel_xinput_touch(name,output):
    # not implemented
    # cmd = "xinput map-to-output {} VGA1".format( i )
    # cmd = "xinput test {} > {} ".format(str(i),filename)
    pass

def disable_xinput_touch(name):
    cmd="xinput list"
    print("cmd",cmd)
    r=os.popen(cmd)
    lines = r.readlines()
    for line in lines:
        if name in line:
            line = line.strip()
            line = line.split("\t")
            print("DISABLE !!",[line])
            _id =""
            for l in line:
                if "id=" in l:
                    _id = l.replace("id=","")
            if _id:
                cmd="xinput disable {}".format(_id) # disable touch as normal input 
                print("cmd:",cmd)
                os.system(cmd)
    #exit()

                     
def cleanup_multipointer(prefix="multipointer_"):
    import os
    cmd="xinput list | grep '{}'".format(prefix)
    print(" cleanup multipointer:", cmd)
    r=os.popen(cmd )

    lines = r.readlines()

    for line in lines:
        line = line.strip()
        line = line.replace("\t"," " )
        if "  " in line:
            line = line.replace("  "," ")
        
        if "id=" in line and "pointer" in line:
            line = line.split()
            print(" LINE",[line])
            _id = line[-4]
            _id = _id.replace("id=","")
            cmd= "xinput remove-master '{}'".format(_id)
            print(" ",cmd)
            print("  kill X11 ")
            os.system(cmd)
        """traps: xfce4-terminal[283904] trap int3 ip:7f784386cabb sp:7ffebb961c10 error:0 in libglib-2.0.so.0.6600.8[7f784382e000+88000]
         [24187.974998] xfce4-terminal[306138]: segfault at 90 ip 00007f1b725ac838 sp 00007ffd8e83b940 error 4 in libgdk-3.so.0.2404.20[7f1b72573000+7f000]
        [24187.975015] Code: 41 0f 10 4f 60 48 89 5d 38 f2 0f 5e c8 f2 0f 11 4d 48 e8 8b 72 fd ff 48 89 df e8 93 fb fc ff 48 89 ef 48 89 c6 e8 38 7f fd ff <49> 8b b5 90 00 00 00 48 89 ef e8 89 7f fd ff 49 8d 97 b8 00 00 00
        """


class Action():
    def __init__(self, output=""):
        self._X = 0
        self._Y = 0
        self._Xmin = 10000000000
        self._Ymin = 10000000000
        self._Xmax = 0
        self._Ymax = 0
        self.touch_config= {"x_max":1024,"y_max":"768"}
        self.touch = ""
        self.screen_config = {}
        self.screen = output # "DP-2"
        self.timer = time.time() 
        self.motion_changeX =0
        self.motion_changeY =0
        self.motion_change = 0
        self.btn_cmd = ""
        self.btn_timer = time.time()                   
        self.btn_down = 0
        self.btn_up = 0
        self._btn_timer = 0
        
        self._config_ok = 0
        self._config_data = []
            
        self.pointer_config = []
        self.pointer_create_count = 0
        self.MT_SLOT = 0 #int(ix)

        self.mode = "touchpad" # or touchscreen
        self.refresh_screen_config()

        self.refresh_multipointer_config(cleanup=1)

    def check_monitor(self):
        if self.screen not in self.screen_config:
            #for k,v in self.screen_config.items():
            #    print(k,v)
            #print("x() key ",self.screen," not in CONFIG")
            return 0
        return 1 
    def system(self,cmd):
        if self.check_monitor():
            #print("my_system CMD:",cmd)
            os.system(cmd)
        else:
            pass
            #print("my_system CMD:",cmd ,"NO MONITOR:",self.screen,"!!!!!")
    def refresh_multipointer_config(self,cleanup=0):
        print()
        print("refresh_multipointer_config")

        self.pointer_config = []
        prefix = "multipointer_"
        prefix = "librelight_pointer_z"
        if cleanup:
             cleanup_multipointer(prefix=prefix)

        cmd = "xinput list | grep '{}' | grep 'XTEST pointer'".format(prefix)
        print(" CMD:",cmd)
        r = os.popen(cmd)
        lines = r.readlines()

        for line in lines:
            cfg = {}
            line = line.strip().split()
            print([line])
            _id = line[5]
            _id = _id.replace(")","")
            _id = _id.replace("(","")
            _id = _id.replace("id=","")
            cfg["id"] = _id
            cfg["name"] = line[2]
            self.pointer_config.append( cfg )


        multipointer_off = 1
        # error with window manager  
        # - window-ontop not working properly
        # - window-focus not working properly
        # error !!! ??? 


        # creat 5 pointer on screen for Mutlitouch input
        # pointer jump's around on X11 
        #print()
        create = []
        for i in [1]: #range(1,5+1):
            ok = 0
            n = "{}{}".format(prefix,i)
            for j in self.pointer_config:
                print(" pt",i,j)
                print(" pt",n, j["name"]) 
                if n == j["name"]: 
                    ok = 1
                    if multipointer_off:
                        j["id"] = "xx"
                    cmd = "xte -i {} 'mousemove {:8} {:8}' ".format(j["id"],4000,4000)
                    print(" ",cmd)
                    self.system(cmd)
                    #cmd = "xinput list-props {} ".format(j["id"])
                    #print(cmd)
                    #self.system(cmd)
                    #cmd = "xinput set-prop {} \"Device Enabled\" 1".format(j["id"])
                    #print(cmd)
                    #self.system(cmd)
                    break


            if not ok:
                 create.append(n)

        
        for i in create:
            if not multipointer_off:
                cmd = "xinput create-master '{}'".format(i)
                print(" CMD:",cmd)
                self.system(cmd)

        if multipointer_off:
            print(" multipointer ist OFF !")
            #return

        if len(create) and self.pointer_create_count < 10: # recursion !!
            print(" self.refresh_multipointer_config() # recursion !!!")
            self.pointer_create_count += 1
            #print(self.pointer_create_count)

            self.refresh_multipointer_config()

        #for p in range(12):
        #for p in self.pointer_config:
        #     cmd = "xte -i {} 'mousemove {:8} {:8}' ".format(p,10,20)
        #     self.system(cmd)


    def refresh_screen_config(self):
        #self.screen_config = {}
        cmd = "xrandr --listmonitors"
        r = os.popen(cmd)
        lines = r.readlines()
        lines = lines[1:] # remove header
        for line in lines:
            cfg = {}
            line = line.strip().split()
            #print("scr_cfg",[line])
            cfg["id"] = line[0]
            cfg["name"] = line[1]
            cfg["res"] = line[2]
            output = line[3]
            cfg["output"] = output

            if "*" in cfg["name"]:
                cfg["primary"] = 1
            else:
                cfg["primary"] = 0

            x,y = cfg["res"].split("x")
            cfg["x"] = x.split("/")[0]
            cfg["y"] = y.split("/")[0]
            pos = y.split("/")
            pos = pos[-1]
            pos = pos.split("+")
            cfg["x_pos"] = pos[1]
            cfg["y_pos"] = pos[2]

            for k in cfg:
                v = cfg[k]
                try:
                    cfg[k] = int(v)
                except ValueError:
                    pass
            print("  cfg:",cfg)

            self.screen_config[ output] = cfg 
        #exit()


    def x(self):
        v = self._X
        if not self.check_monitor():
            return v


        if self.mode == "touchpad":
            scr = self.screen_config[self.screen]
            v = mapFromTo(self._X,0,self.touch_config["ABS_X"]["Max"],scr["x_pos"],scr["x_pos"]+scr["x"])
        elif self.mode == "touchscreen":
            v = mapFromTo(self._X,10,4000,0,1600)
        return round(v,2)

    def y(self):
        v = self._Y
        if not self.check_monitor():
            return v

        if self.mode == "touchpad":
            scr = self.screen_config[self.screen]
            v = mapFromTo(self._Y,0,self.touch_config["ABS_Y"]["Max"],scr["y_pos"],scr["y_pos"]+scr["y"])
        elif self.mode == "touchscreen":
            v = mapFromTo(self._Y,0,1400,0,1600)

        return round(v,2)
                                 

    def _parse_config(self):
        print()
        print("_parse_config",[self.screen,self.touch])
        code = ""
        lines = self._config_data
        for i,line in enumerate(lines):
            #print(i,[line])
            cfg = {}
            if "Event code" in line:
                line = line.strip()
                if "  " in line:
                    line = line.replace("  "," ")
                tmp = line.split()
                key = tmp[3]
                key = key.replace("(","").replace(")","")
                cfg["key"] = key
                cfg["code"] = tmp[2]
                for j in range(1,10):
                    tmp = lines[i+j]
                    if not tmp.startswith("      "): #sub config
                        break
                    tmp = tmp.strip()
                    if "  " in tmp:
                        tmp = tmp.replace("  "," ")
                    tmp = tmp.split()
                    k = tmp[0]
                    v = tmp[1]
                    try:
                        v = int(v)
                    except ValueError:
                        pass
                    cfg[k] = v
                    #print("  ADD CFG",key,[k,v])
                print(" t_cfg",cfg)
                self.touch_config[key] = cfg

        
    def check_config(self,line):

        if not self._config_ok:
            self._config_data.append( line)
            #print("CONFIG:",[line])
            if "Testing ... (interrupt to exit)" in line:
                self._config_ok = 1
                self._parse_config()
            return 0
            
        else: #init touch screen config
            if "Input driver version is" in line:
                self._config_ok = 0
            elif "Input device ID:" in line:
                self._config_ok = 0
        return 1

    def cur_pointer_id(self):
        i =  self.MT_SLOT
        #return "xxx"
        #print("cur_pointer_id:", self.pointer_config,i)
        if i < len(self.pointer_config):
            return self.pointer_config[i]["id"]
        return "xxx"


    def _check_ABS(self,line):
        #print([line])

        if "ABS_MT_SLOT" in line:
            key =", value "
            #print("ABS_MT_SLOT", line)
            line = line.strip()
            if key in line:
                ix = line.split()[-1] #.index(key)
                
                try:
                    ix = int(ix)
                    if ix > 5:
                        ix = 5
                    self.MT_SLOT = ix
                    #print("++++++++++++++++++++++++++++++++++++++++++++++++++++ NEW SLOT",ix)
                    #self.cur_pointer_id()
                except ValueError:
                    pass

        if "ABS_X" in line or "ABS_Y" in line:# or "ABS_MT_POSITION_X" in line or "ABS_MT_POSITION_Y" in line:
            key =", value "
            #print("ABS", [line])
            if key in line:
                ix = line.index(key)
                try:
                    c = line[ix+len(key):]
                    c = int(c)
                    if "_X" in line:
                        self._X =c
                        if c > self._Xmax:
                            self._Xmax = c
                        if c < self._Xmin:
                            self._Xmin = c
                        self.motion_changeX += 1
                            
                    else:
                        self._Y =c
                        
                        if debug:print( [c , self._Ymin,c < self._Ymin])
                        if c > self._Ymax:
                            self._Ymax = c
                        if c < self._Ymin:
                            self._Ymin = c
                        self.motion_changeY += 1
                    
                    #cmd = "xdotool mousemove {} {}".format(self.x(),self.y())
                    
                    # 3 position changes to acept position
                    if self.motion_changeX >0 and self.motion_changeY >0:
                        self.motion_changeX =0
                        self.motion_changeY =0
                        self.motion_change = 1
                
                    
                    if debug:
                        print( line)
                        print( cmd)
                        print( self._Xmin,self._Xmax,self._Ymin,self._Ymax)
                    
                    #self.system(cmd)
                except Exception as e:
                    print( "ERR:",e)
                    print( "E:", [line])
    def action(self,line):
        """GET DEVICE INPUT LINE AND DECODE IT
        
        xinput test  
        motion a[0]=366 a[1]=558
        
        evtestEvent: 
        time 1556826444.499763, type 2 (EV_REL), code 0 (REL_X), value 8
        """
        if "motion" in line: #xinput test id
            if "a[2]=1" in line:
                #cmd = "xdotool click 1"
                cmd = "xdotool mouseup 1"
                p = self.cur_pointer_id()
                cmd = "xte -i {} mouseup 1  # Monitor:{}".format(p,self.screen)
                print("\033[92m{}\033[0m".format( cmd))
                #print( line,cmd)
                self.system(cmd)
                #self.system("ls -l")
            if "a[2]=0" in line:
                #cmd = "xdotool click 1"
                cmd = "xdotool mousedown 1"
                print("\033[95m{}\033[0m".format( cmd))
                #print( line,cmd)
                #self.system(cmd)
                #self.system("ls -l")
        if "BTN_LEFT" in line or "BTN_TOUCH" in line: #evtest /dev/input/eventX
            " Mouse Button Click "
            
            key =", value "
            if key in line:
                ix = line.index(key)
                try:
                    c = line[ix+len(key):]
                    c = int(c)
                    if c:
                        self.btn_down = 1                        
                    else:
                        self.btn_up = 1
                    
                    #RESET MOTION CHANGE
                    self.motion_changeX =0
                    self.motion_changeY =0
                    self.motion_change = 0
                    self.btn_timer = time.time()
                    #print( line)
                    #print( self.btn_cmd )                   
                    
                except Exception as e:
                    print( "ERR:",e)
                    print( "E:", [line])

        if not self.check_config(line):
            return 

        self._check_ABS(line)
                    
        self.run()
        
    def btn(self,val):
        if val:
            #time.sleep(0.01)
            cmd = "xdotool mousedown 1"                        
            p = self.cur_pointer_id()
            cmd = "xte -i {} 'mousedown 1' # MONITOR:{} OK:{}".format(p,self.screen,self.check_monitor())                        
            msg =""
            if self.check_monitor():
                msg = "\033[95m{:33}\033[0m {:8} {:8} "
            else:
                msg = "\033[41m{:33}\033[0m {:8} {:8} "

            print(msg.format(cmd,self.x(),self.y()) , self.screen ,"MT_SLOT", self.MT_SLOT)
            #print("\033[92m{:30}\033[0m".format( cmd),"{:8} {:8} "
            #.format(self.x(),self.y()) , self.screen ,"MT_SLOT",self.MT_SLOT)

            if self.MT_SLOT == 0:
                pass 
                self.system(cmd)
            self.btn_down = 0
            self._btn_timer = time.time()
        else:            
            cmd = "xdotool mouseup 1"                        
            p = self.cur_pointer_id()
            cmd = "xte -i {} 'mouseup 1' #MONITOR:{} OK:{}".format(p,self.screen,self.check_monitor())                        
            #print( cmd)
            t = time.time() - self._btn_timer
            msg =""
            if self.check_monitor():
                msg = "\033[95m{:33}\033[0m {:8} {:8} "
            else:
                msg = "\033[41m{:33}\033[0m {:8} {:8} "

            print(msg.format(cmd,self.x(),self.y()) , self.screen ,"MT_SLOT", self.MT_SLOT,"t:",round(t,2))
            self.system(cmd)
            self.btn_up = 0            
            self._btn_timer = time.time()
        time.sleep(0.001)           
        
    def set_pointer(self):
        #cmd = "xdotool mousemove {:8} {:8} ".format(self.x(),self.y())

        p = self.cur_pointer_id()
        cmd = "xte -i {} 'mousemove {:8} {:8}' # MONITOR:{}".format(p,int(self.x()),int(self.y()),self.screen)

        t = int((time.time() - self._btn_timer)*10)/10.
        #print(t,"\033[95m{}\033[0m".format( cmd),self.mode)
        
        if self.MT_SLOT == 0:
            self.system(cmd)
            #self.system(cmd)
            self.motion_changeX =0
            self.motion_changeY =0
            self.motion_change = 0
            self.timer = time.time()            
        #time.sleep(0.000001)           
        
                    
    def run(self):
        #print "RUN"
        
        if self.btn_up:
            if time.time() - self._btn_timer > 0.05: # long press
                self.set_pointer()
            self.btn(0)
            #self.btn(0)
            
            
        if self.motion_change and self.timer+0.01 < time.time():
            if self.btn_down:
                #self.btn(0)
                self.set_pointer()
                self.btn(1)
        
            
            if self.motion_change and self.timer+0.01 < time.time():
                if time.time() - self._btn_timer > 0.05: # long press
                    self.set_pointer()
            
            
            
    


def get_touch_list():
    cmd = 'echo "\n" | evtest 2>&1 | grep event'
    print("cmd", [cmd])
    r = os.popen(cmd)
    lines = r.readlines()
    out = []
    for line in lines:
        line = line.strip()
        #line = line.replace("\t"," ")
        line = line.split("\t")
        if len(line) >= 2:
            path = line[0][:-1]
            name = line[1]
            out.append([name,path])
    return out

def touch_filter(name,lines):
    out = []
    for line in lines:
        if name == line[0]:
            out = line
    return out
    



def loop(cmd="",output="",name=""):
    a = Action(output)
    line = ""
    #cmd="evtest /dev/input/event5"
    #cmd="evtest /dev/input/event24"
    while 1:
        print()
        print("="*40)
        print("loop cmd: ",cmd)
        r = os.popen(cmd)
        while 1:
            line = r.readline() 
            if not line:
                print("loop cmd r.readline return NONE !",int(time.time()))
                print("losst touchscteen connection",output)
                print()
                break
            try:
                a.action(line)
            except Exception as e:
                print("ERROR:a.action EXCEPTION:",[e])
                print("ERROR: >>",output,name)
                print("ERROR: >>",line)

        time.sleep(1)

        # rescan touch input's 
        touch_list =  get_touch_list()
        x= touch_filter(name,touch_list)
        print(x)
        if len(x):   
            disable_xinput_touch(name)
            #cmd="evtest /dev/input/event5"
            cmd="evtest {}".format(x[1])
    
if __name__ == "__main__":
    
    cmd="xset -display :0.0 r rate 240 15"
    os.system(cmd)

    touch_list =  get_touch_list()
    touch_ok = []

    touchscreen_count = 0

    #TOUCH 1 a
    print()
    name = "iSolution multitouch"
    x= touch_filter(name,touch_list)
    print(x)
    
    print("TOUCH 0",x)
    touch_ok.append(x)
    if len(x):
        disable_xinput_touch(name)
        #cmd="evtest /dev/input/event24"
        cmd="evtest {}".format(x[1])
        #start_new_thread(loop,(cmd,"DP-2"))
        start_new_thread(loop,(cmd,"HDMI-1",name))#),name)
        touchscreen_count +=1

    #TOUCH 1
    print()
    name = "iSolution multitouch"
    x= touch_filter(name,touch_list)
    print("TOUCH 1",x)
    touch_ok.append(x)

    if len(x):
        disable_xinput_touch(name)
        #cmd="evtest /dev/input/event24"
        cmd="evtest {}".format(x[1])
        start_new_thread(loop,(cmd,"DP-2",name))#),name)
        #start_new_thread(loop,(cmd,"HDMI-1"))
        touchscreen_count +=1



    #TOUCH 1
    print()
    name="ELAN Touchscreen"
    x= touch_filter(name,touch_list)
    print("TOUCH 2",x)
    touch_ok.append(x)
    if len(x):   
        disable_xinput_touch(name)
        #cmd="evtest /dev/input/event5"
        cmd="evtest {}".format(x[1])
        start_new_thread(loop,(cmd,"eDP-1",name))#),name)
        #start_new_thread(loop,(cmd,"HDMI-1"))
        touchscreen_count +=1


    time.sleep(1)
    print()
    print("touch_ok",touch_ok)
    while 1:
        time.sleep(1)
