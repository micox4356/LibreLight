#!/usr/bin/python3

import time
import traceback
import json

import __main__ as MAIN
from lib.cprint import *

def JSCB(x,sock=None):
    i = ""
    msg = ""
    msgs = []
    try:
        #print("JSCB",sock)
        for i in x:
            #print("i",[i])
            msgs = json.loads(i)
            print(" JSCB",msgs) #,sock)
            if type(msgs) is not list:
                continue

            for msg in msgs:
                print("  ",msg)
                # MAIN.FIXTURES.encoder
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
                    #MAIN.FIXTURES.encoder(str(FIX),ATTR,xval="click",xfade=0,xdelay=0)#,blind=0)
                    MAIN.FIXTURES.encoder(str(FIX),ATTR,xval=VAL,xfade=0,xdelay=0)#,blind=0)

                    #print(dir(cb))
                    #event.num = enum

                    #MAIN.master.refresh_fix() # delayed
                    #refresher_fix.reset() # = Refresher()
                    #cb.cb(event)
                if "CLEAR" == msg["event"]:
                    MAIN.FIXTURES.clear()
                    MAIN.modes.val("REC",0)
                    #MAIN.master.xcb("CLEAR",1)
                elif "REC" == msg["event"]:
                    MAIN.modes.val("REC",1)
                elif "EDIT" == msg["event"]:
                    MAIN.modes.val("EDIT",1)
                elif "BLIND" == msg["event"]:
                    MAIN.modes.val("BLIND",1)
                elif "FLASH" == msg["event"]:
                    MAIN.modes.val("FLASH",1)
                elif "CFG-BTN" == msg["event"]:
                    MAIN.modes.val("CFG-BTN",1)
                elif "LABEL" == msg["event"]:
                    MAIN.modes.val("LABEL",1)
                elif "REC" == msg["event"]:
                    MAIN.modes.val("REC",1)
                elif "SAVE\nSHOW" == msg["event"]:
                    MAIN.save_show()
                elif "RESTART" == msg["event"]:
                    print("OK OK")
                    MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)
                elif "REC-FX" == msg["event"]:
                    MAIN.modes.val("REC-FX",1)
                elif "EXEC" == msg["event"]:
                    print("  EXEC EXEC")
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
                            #print("time:",e-s,e)
                            #print("TIME:",int((e-s)*1000),int(e*10)-1_703_800_000)
                            #print("TIME:",int((e-s)*1000),int(e*10)/10)
                            print("EXE TIME:","{:0.02f}".format(e-s),int(e*100)/100)
                            print()

                    except Exception as e:
                        print("EXEC ERR:",e)
            
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
