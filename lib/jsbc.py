#!/usr/bin/python3

import time
import traceback
import json

import __main__ as MAIN
from lib.cprint import *
import lib.fixlib as fixlib


def JSCB(x,sock=None):
    # REMOTE KEY EVENT's
    i = ""
    msg = ""
    msgs = []
    try:
        #print("JSCB",sock)
        for i in x:
            #print("i",[i])
            msgs = json.loads(i)
            #print(" JSCB",msgs) #,sock)
            if type(msgs) is not list:
                continue

            for msg in msgs:
                OK = 0
                #print("  msg",msg)
                if "event" not in msg:
                    continue

                if "FIXTURES" == msg["event"]:
                    FIX=0
                    VAL=""
                    ATTR=""
                    if "FIX" in msg:
                        FIX=msg["FIX"]
                    if "VAL" in msg:
                        VAL=msg["VAL"]
                    if "ATTR" in msg:
                        ATTR=msg["ATTR"]
                    print("  MAIN.tk_event",FIX,VAL,ATTR)
                    #cb = MAIN.tk_event(fix=FIX,elem=None,attr=ATTR,mode="ENCODER",data=[]) #data)
                    fixlib.encoder(MAIN.FIXTURES.fixtures,str(FIX),ATTR,xval=VAL,xfade=0,xdelay=0)#,blind=0)

                    #print(dir(cb))
                    #event.num = enum

                    #cb.cb(event)
                    OK = 1
                if "CLEAR" == msg["event"]:
                    #MAIN.FIXTURES.clear()
                    fixlib.clear(MAIN.FIXTURES.fixtures)
                    MAIN.modes.val("REC",0)
                    #MAIN.master.xcb("CLEAR",1)
                    OK = 1
                elif "REC" == msg["event"]:
                    MAIN.modes.val("REC",1)
                    OK = 1
                elif "EDIT" == msg["event"]:
                    MAIN.modes.val("EDIT",1)
                    OK = 1
                elif "BLIND" == msg["event"]:
                    MAIN.modes.val("BLIND",1)
                    OK = 1
                elif "FLASH" == msg["event"]:
                    MAIN.modes.val("FLASH",1)
                    OK = 1
                elif "CFG-BTN" == msg["event"]:
                    MAIN.modes.val("CFG-BTN",1)
                    OK = 1
                elif "LABEL" == msg["event"]:
                    MAIN.modes.val("LABEL",1)
                    OK = 1
                elif "REC" == msg["event"]:
                    MAIN.modes.val("REC",1)
                    OK = 1
                elif "FX-OFF" == msg["event"]:
                    #MAIN.modes.val("FX-OFF",1)
                    MAIN.CONSOLE.fx_off("all") #"FX-OFF",1)
                    #OK = 1
                elif "SAVE\nSHOW" == msg["event"]:
                    MAIN.save_show()
                    OK = 1
                elif "RESTART" == msg["event"]:
                    print("OK OK")
                    MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)
                    OK = 1
                elif "REC-FX" == msg["event"]:
                    MAIN.modes.val("REC-FX",1)
                    OK = 1
                elif "REC-EXEC" == msg["event"]:
                    print("  JSCB.REC-EXEC")
                    val = -1
                    exec_nr = -1
                    try:
                        if "VAL" in msg:
                            val = int(msg["VAL"])
                        if "EXEC" in msg:
                            exec_nr = int(msg["EXEC"])

                        if val >= 1 and exec_nr > 0: # VAL >=1 !!!
                            print(" EXEC_GOOO",exec_nr)
                            s = time.time()
                            MAIN.master.exec_rec(exec_nr-1)
                            e = time.time()
                            print("EXE TIME:","{:0.02f}".format(e-s),int(e*100)/100)
                            print()
                            OK = 1
                    except Exception as e:
                        print("REC-EXEC ERR:",[e])
                        raise e
                elif "EXEC" == msg["event"]:
                    print("  JSCB.EXEC")
                    val = -1
                    exec_nr = -1
                    try:
                        if "VAL" in msg:
                            val = int(msg["VAL"])
                        if "EXEC" in msg:
                            exec_nr = int(msg["EXEC"])
                        if val >= 0 and exec_nr > 0:
                            print("EXEC_GOOO",exec_nr,val)
                            s = time.time()
                            MAIN.master.exec_go(exec_nr-1,xfade=None,val=val)
                            e = time.time()
                            print("EXE TIME:","{:0.02f}".format(e-s),int(e*100)/100)
                            print()
                            OK = 1
                    except Exception as e:
                        print("EXEC ERR:",e)
            
                if OK:
                    cprint(" remote-key:",msg ,color="green")
                    if "REC-EXEC" in msg["event"]:
                        MAIN.execlib.exec_set_mc(MAIN.EXEC.label_exec,MAIN.EXEC.val_exec)
                else:
                    cprint(" remote-key:",msg ,color="red")
    except Exception as e:
        cprint("exception JSCB:",e,color="red")
        cprint("- i:",i,color="red")
        cprint("- msg:",msgs,color="red")
        cprint(traceback.format_exc(),color="red")
        if sock:
            msg = ["Notice: Exception on JSCB-SERVER: ",str(e)]
            msg = json.dumps(msg)
            msg = bytes(msg,"utf8")
            cprint(msg,color="red")
            #chat._send(sock,msg)

    #time.sleep(1/60)
