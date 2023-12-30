#!/usr/bin/python3
import os
import sys
import time
import psutil

# python3 movewin.py window-title x y
# python3 movewin.py COMMA 723 943

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
