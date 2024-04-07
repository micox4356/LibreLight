#!/usr/bin/python3

import os
HOME = os.getenv('HOME')

from lib.cprint import *
import lib.baselib as baselib
import __main__ as MAIN

window_list_buffer = {}

def save_window_position(save_as=""):
    global window_list_buffer
    cprint()
    cprint("save_window_position",[save_as])

    base = baselib.Base()
    fname = HOME+"/LibreLight"
    fname = base.show_path1 +base.show_name 
    if save_as:
        fname = save_as 
    fname +=  "/gui.txt"
    cprint("- fname",fname)

    for k in window_list_buffer:
        window_list_buffer[k][0] = 0   

    for k,win in MAIN.window_manager.windows.items():
        try:
            geo = win.tk.geometry()
            data = [1,k,geo]
            if k not in  window_list_buffer:
                cprint("-- new:win:pos",k.ljust(15," "),data)
            elif window_list_buffer[k][2] != geo:
                cprint("-- update:win:pos",k.ljust(15," "),data)
            window_list_buffer[k] = data

            if k in ["PATCH","FIXTURES","DIMMER","FIXTURE-EDITOR","CONFIG"]:
                window_list_buffer[k][0] = 0   

        except Exception as e:
            cprint("-A save_window_position Exception:",k,e,color="red")

    lines = ""
    for k,data in window_list_buffer.items():
        try:
            #print("-- save:win:pos",k.ljust(15," "),data)
            if not data[2]:
                continue
            line ="{} {} {}\n"
            line = line.format(data[0],k,data[2])
            lines += line
        except Exception as e:
            cprint("-A save_window_position Exception:",e,color="red")

    try:
        f = open(fname,"w")
        f.write( lines )
    except Exception as e:
        cprint("-B save_window_position Exception:",e,color="red")
    finally:
        f.close() #f.flush()



def save_window_position_loop(): # like autosave
    def loop():
        time.sleep(20)
        try:
            while 1:
                save_window_position()
                time.sleep(60)
        except Exception as e:
            cprint("save_loop",e)
    thread.start_new_thread(loop,())

def get_window_position(_filter="",win=None):
    global window_list_buffer
    cprint()
    show = None
    k = _filter
    geo = ""

    cprint("get_window_position",[_filter])
    if _filter in window_list_buffer:
        show,k,geo  = window_list_buffer[_filter]
        if win:
            win.tk.geometry(geo)
    return show,k,geo


def read_window_position():
    try:
        base = baselib.Base()
        fname = HOME+"/LibreLight"
        fname = base.show_path1 +base.show_name 
        fname +=  "/gui.txt"
        cprint("- fname:",fname)
        f = open(fname,"r")
        lines = f.readlines()
        f.close()
        out = []
        for line in lines:
            line = line.strip()
            #print(line)
            if " " in line:
                if line.count(" ") >= 2:
                    show,name,geo = line.split(" ",2)
                elif line.count(" ") == 1:
                    name,geo = line.split(" ",1)
                    show = 1

                if "--easy" in sys.argv:
                    if name not in ["MAIN","EXEC","SETUP"]:
                        show=0
            out.append([show,name,geo])

        return out
    except Exception as e:
        cprint("- load_window_position 345 Exception:",e,color="red")
        return 
    return []

def split_window_show(lines,_filter=""):
    try:
        for show,name,geo in lines:
            #print( "wwWww "*10,[show,name,geo] )
            if _filter in name:
                return int(show)
    except Exception as e:
        cprint("- split_window_show 345 Exception:",e,color="red")

def split_window_position(lines,_filter=""):
    try:
        for show,name,geo in lines:
            #print( "wwWww "*10,[show,name,geo] )
            if _filter in name:
                geo = geo.replace("+"," ")
                geo = geo.replace("x"," ")
                geo = geo.split()
                #print( "wwWww "*10,[show,name,geo] )
                if len(geo) == 4:
                    #print( [show,name,geo] )
                    args = {}
                    args["width"]  = int(geo[0])
                    args["height"] = int(geo[1])
                    args["left"]   = int(geo[2])
                    args["top"]    = int(geo[3])
                    return args
    except Exception as e:
        cprint("- split_window_position 345 Exception:",e,color="red")



def load_window_position(_filter=""):
    print()
    global window_list_buffer
    cprint()
    cprint("load_window_position",[_filter])
    try:
        lines = read_window_position()

        data = {}
        for show,name,geo in lines:
            data[name] = [show,name,geo]
            window_list_buffer[name] = [show,name,geo]

        for name,win in MAIN.window_manager.windows.items():
            if not win:
                continue

            if name not in data:
                continue

            if _filter:
                if _filter != name:
                    continue

            w = data[name][2] 

            print("  set_win_pos","filter:",[_filter],"Name: {:<20}".format(name),w,win)
            try:
                win.tk.geometry(w)
            except Exception as e:
                cprint("- load_window_position 544 Exception:",e,color="red")

    except Exception as e:
        cprint("- load_window_position 345 Exception:",e,color="red")
        return 
