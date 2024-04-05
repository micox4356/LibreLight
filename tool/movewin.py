#!/usr/bin/python3
import os
import sys
import time
import psutil
import json    

# python3 movewin.py window-title x y
# python3 movewin.py COMMA 723 943

class Control():
    def __init__(self):
        self.title = "WinfoWinName"
        self.winid = ""
    def winfo(self):
        winid = winfo(self.title)
        if type(winid) == list:
            if len(winid) >= 1:
                self.winid = winid[0]
    def winfo2(self):
        winid = winfo2(self.title)
        #if type(winid) == list:
        #    if len(winid) >= 1:
        #        self.winid = winid[0]
    def move(self,x=None,y=None):
        if self.winid:
            cmd=movewin(_id=self.winid,x=x,y=y)
            system(cmd)
    def size(self,x=None,y=None):
        if self.winid:
            cmd = sizewin(_id=self.winid,x=x,y=y)
            system(cmd)
    def activate(self):
        if self.winid:
            cmd=activate(_id=self.winid)
            system(cmd)

def winfo(name="WinfoWinName"):
    search = name
    cmd = "xwininfo -root -children -all | grep '{}'"
    cmd = cmd.format(search)
    print(cmd)

    r = os.popen(cmd)
    lines = r.readlines()
    _id = [] #"xxxx"
    if lines and lines[0]:
        _id.append( lines[0].split()[0] )
    print("ID:",_id)
    for line in lines:
        line = line.strip()
        print("-",line)
    return _id

def parse_winfo_line(line):
    a1 = 0
    a2 = 0

    ps_name  = ""
    ps_title = ""
    ps_id    = ""
    ps_pos   = ""
    ps_size  = ""

    if line: # in lines:
        a1 = line.index(' ("')+2   
        a2 = line.index('") ')+1   
        ps_id   = line.split()[0]
        ps_id   = ps_id.replace(" ","")
        ps_pos  = line.split()[-1]
        ps_size = line.split()[-2]

        ps_pos  = ps_pos.replace("+"," ").replace("x"," ")
        ps_size = ps_size.replace("+"," ").replace("x"," ")

        ps_pos = ps_pos.strip().split()
        ps_size = ps_size.strip().split()
        for i in range(len(ps_pos)):
            ps_pos[i] = int(ps_pos[i])
        for i in range(len(ps_size)):
            ps_size[i] = int(ps_size[i])
        
        ps_pos[-2] -= ps_size[-2]
        ps_pos[-1] -= ps_size[-1]

        #ps_pos_x1 = int(ps_apos.split("+")[-2])
        #ps_pos_y1 = int(ps_pos.split("+")[-1])

        if a1 >= 0 and a2 >= 0:
            ps_name = line[a1:a2]
            line = line[:a1]+line[a2:]
            if ' "' in line and '":' in line:
                a1 = line.index(' "')+2
                a2 = line.index('":')
                ps_title = line[a1:a2]
                _line = [ps_id,ps_name,ps_title,ps_size,ps_pos]
                print("   ",_line)
                return _line 

def winfo2(name="WinfoWinName"):
    print("--------------")
    search = name
    cmd = "xwininfo -root -children -all | grep '{}'"
    cmd = cmd.format(search)
    print(cmd)

    r = os.popen(cmd)
    lines = r.readlines()
    _data = [] 
    for line in lines:
        a = parse_winfo_line(line)
        if a:
            _data.append(a)

    print("--------------")
    return _data

def get_store_line():
    lines = winfo2(name="SDL-")
    out_lines=[]
    for line in lines:
        #print(" ##",line)
        t=line[2].split()
        for k in t:
            k = k.replace(" ", "_")
            if "SDL-" in k:
                s=line[-2]
                p=line[-1]

                # info: b x h + x + y
                #out = "{} {} {} {} {} {}\n".format(1,k, s[0],s[1],p[0],p[1] )
                out = [1,k, s[0],s[1],p[0],p[1] ]
                #print("  --",k,out)
                out_lines.append(out)
    return out_lines


def store_all_sdl():
    fname ="/home/user/gui-sdl.txt"
    if os.path.isfile(fname):
        f=open(fname,"r")
        xlines = f.readlines()
        f.close()

        in_lines = []
        print("  read",fname)
        for line in xlines:
            line = line.strip()
            if not line.startswith("#") and line:
                #print(" ++",[line])
                in_lines.append(line)
        in_lines.append("[0,0,00,0,0,0]")

    print("Öö"*20)
    lines = get_store_line()
    ap_line = []
    for line in lines:
        ok = 0
        iline = ""
        for iline in in_lines:
            if line[1] in iline:
                ok = 1 
        if not ok and iline:
           ap_line.append(iline)


    f=open(fname,"w")
    f.write("#"+json.dumps(["on","title","w","h","x","y"])+"\n")
    for line in lines:
        f.write(json.dumps(line)+"\n")

    for line in ap_line:
        print("+++>",line)
        f.write(line+"\n")
    f.write("\n")
    f.close()

def movewin(_id="0xWinId",x=None,y=None):
    cmd="xdotool windowmove {} {} {}".format(_id,x,y)
    return cmd

def sizewin(_id="0xWinId",x=None,y=None):
    cmd="xdotool windowsize {} {} {}".format(_id,x,y)
    return cmd

def activate(_id="0xWinId"):
    cmd="xdotool windowactivate {}".format(_id)
    return cmd

def system(cmd):
    print(cmd)
    os.system(cmd)

def search_process(_file_path,exact=1):
    print("search_process",_file_path)
    pids = psutil.pids()
    count = 0
    out = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            break

        ps = p.cmdline()

        if len(ps) < 2:
            continue

        if "python" not in ps[0]:
            continue

        print(" ",[ps[1]])
        print("exact_search",exact)
        if exact:
            if str(_file_path) == str(ps[1]):
                print(ps)
                count += 1
                out.append(pid)
        else:
            if str(_file_path) in str(ps[1]):
                print(ps)
                count += 1
                out.append(pid)

    print("search_process",count)
    return out

def process_kill(path):
    pids = search_process(path,exact=0)
    for pid in pids:
        print("process_kill:",pid)
        p = psutil.Process(pid)   
        #p.name()
        #p.cmdline()
        p.terminate()
        p.wait()

import inspect
def get_lineno():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  #print(info.filename)                      # __FILE__     -> Test.py
  #print(info.function)                      # __FUNCTION__ -> Main
  #print(info.lineno)                        # __LINE__     -> 13
  return info.lineno

if __name__ == "__main__":
    print("# python3 movewin.py window-title x y")
    print("# python3 movewin.py COMMA 723 943")
    import random

    a=random.randint(100,400)
    b=random.randint(100,400)
    
    search = "ASD"
    try:
        search = sys.argv[1]
        search = search.replace("'","")
    except:pass


    try:
        a = sys.argv[2]
    except:pass
    try:
        b = sys.argv[3]
    except:pass

    _ids = winfo(search)
    for _id in _ids:
        c1 = sizewin(_id,a,b)
        c2 = movewin(_id,a,b)
        c3 = activate(_id)
        system(c1)
        time.sleep(0.1)
        system(c2)
        time.sleep(0.1)
        system(c3)

def check_is_started(CAPTION,_file_path,sleep=0):
    if sleep:
        time.sleep(sleep)

    pids = search_process(_file_path)
    if len(pids) >= 2:
        search = CAPTION[:]
        _ids = winfo(search)
        for _id in _ids:
            c3  = activate(_id)
            print("check_is_started CMD:",c3)
            os.system(c3)
        time.sleep(1)
        sys.exit()
