#!/usr/bin/python3

import time
import traceback
import json
import _thread as thread

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
                EXEC_REFRESH = 0
                val     = -1
                exec_nr = -1
                fix_nr  = -1
                attr    = ""
                if "event" not in msg:
                    continue
                if "EXEC" in msg:
                    try:
                        exec_nr = int(msg["EXEC"])
                    except:
                        exec_nr = -2
                if "VAL" in msg:
                    val = msg["VAL"]
                
                if "FIX" in msg:
                    fix_nr=msg["FIX"]
                if "ATTR" in msg:
                    attr=msg["ATTR"]

                print("  MAIN.tk_event","fix:",fix_nr,"exec_nr:",exec_nr,"val:",val,"attr",attr)

                if "FIXTURES" == msg["event"]:
                    fixlib.encoder(MAIN.FIXTURES.fixtures,str(fix_nr),attr,xval=val,xfade=0,xdelay=0)#,blind=0)
                    OK = 1
                elif "CLEAR" == msg["event"]:
                    fixlib.clear(MAIN.FIXTURES.fixtures)
                    OK = 1
                elif "ESC" == msg["event"]:
                    fixlib.clear(MAIN.FIXTURES.fixtures)
                    MAIN.modes.clear() # FIX
                    MAIN.master.button_clear() # REC,CFG-BTN ...
                    OK = 1
                elif msg["event"] in ["REC","REC-FX","EDIT","BLIND","FLASH","CFG-BTN","LABEL","MOVE","GO","SELECT","DEL","COPY"]:
                    if msg["event"] in ["REC-FX"]:
                        MAIN.modes.clear(protect=["REC-FX","REC",msg["event"]]) # FIX
                        MAIN.master.button_clear() # REC,CFG-BTN ...
                    MAIN.modes.val(msg["event"],1)
                    OK = 1
                elif "FX-OFF" == msg["event"]:
                    MAIN.CONSOLE.fx_off("all") 
                    OK = 1
                elif "SAVE\nSHOW" == msg["event"]:
                    MAIN.save_show()
                    OK = 1
                elif "RESTART" == msg["event"]:
                    print("OK OK")
                    MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)
                    OK = 1
                elif "EXEC" == msg["event"]:
                    print("  JSCB:",msg["event"])
                    try:
                        if exec_nr > 0:
                            if val >= 1: # only Press
                                pass
                                if MAIN.modes.val("REC"):
                                    MAIN.master.exec_rec(exec_nr-1)
                                    msg["OK"] = "REC"
                                    EXEC_REFRESH = 1
                                    OK = 1
                                elif MAIN.modes.val("COPY"):
                                    MAIN.EXEC.copy(exec_nr-1)
                                    msg["OK"] = "COPY"
                                    if MAIN.modes.val("COPY") > 2:
                                        MAIN.modes.val("COPY",0)
                                    EXEC_REFRESH = 1
                                    OK = 1
                                elif MAIN.modes.val("MOVE"):
                                    MAIN.EXEC.move(exec_nr-1)
                                    msg["OK"] = "MOVE"
                                    EXEC_REFRESH = 1
                                    OK = 1
                                elif MAIN.modes.val("DEL"):
                                    MAIN.EXEC.delete(exec_nr-1)
                                    MAIN.modes.val("DEL",0)
                                    msg["OK"] = "DEL"
                                    EXEC_REFRESH = 1
                                    OK = 1

                            if not OK:
                                if val >= 0: #Press/Release
                                    MAIN.master.exec_go(exec_nr-1,xfade=None,val=val)
                                    OK = 1
                                    EXEC_REFRESH = 1

                    except Exception as e:
                        print("EXEC ERR:",e)

            
                if OK:
                    cprint(" remote-key:",msg ,color="green")
                    if EXEC_REFRESH:
                        def xx():
                            MAIN.execlib.exec_set_mc(MAIN.EXEC.label_exec,MAIN.EXEC.val_exec)
                        thread.start_new_thread(xx,())
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
