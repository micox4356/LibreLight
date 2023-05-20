#!/usr/bin/python3
import os
import sys
import time

# python3 movewin.py window-title x y
# python3 movewin.py COMMA 723 943

def winfo(name="WinfoWinName"):
    search = name
    cmd = "xwininfo -root -children -all | grep '{}'"
    cmd = cmd.format(search)
    print(cmd)

    r = os.popen(cmd)
    lines = r.readlines()
    _id = "xxxx"
    if lines and lines[0]:
        _id = lines[0].split()[0]
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
    _id = winfo(search)
    c1 = sizewin(_id,a,b)
    c2 = movewin(_id,a,b)
    c3 = activate(_id)
    system(c1)
    time.sleep(0.1)
    system(c2)
    time.sleep(0.1)
    system(c3)

