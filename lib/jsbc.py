#!/usr/bin/python3

import time
import traceback
import json
import _thread as thread

import __main__ as MAIN
from lib.cprint import *
import lib.fixlib as fixlib


GLOBAL_old_exec_nr = -1
def JSCB(x,sock=None):
    global GLOBAL_old_exec_nr 
    print()
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
                    val = msg["VAL"] # fix int MIDI
                    try:
                        val = int(msg["VAL"]) # fix int MIDI
                    except:pass

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
                    print("jsbc.RESTART")
                    MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)
                    OK = 1
                elif "EXEC-LABEL" == msg["event"]:
                    print("LABEL",msg)
                    if 1:#val >= 1: # only Press
                        if "DATA" in msg:
                            sdata = msg["DATA"]
                            print("EXEC-CFG",sdata)
                            if sdata:
                                MAIN.master.dialog_cfg_return(exec_nr-1)(sdata)
                                #MAIN.EXEC.set_cfg(exec_nr-1,sdata)
                                EXEC_REFRESH = 1
                    msg["OK"] = "EXEC-LABEL"
                    OK = 1
                elif "EXEC-CFG" == msg["event"]:
                    print("EXEC-CFG",msg)
                    if 1:#val >= 1: # only Press
                        if "DATA" in msg:
                            sdata = msg["DATA"]
                            print("EXEC-CFG",sdata)
                            if sdata:
                                MAIN.master.dialog_cfg_return(exec_nr-1)(sdata)
                                #MAIN.EXEC.set_cfg(exec_nr-1,sdata)
                                EXEC_REFRESH = 1
                    msg["OK"] = "SET-CFG"
                    OK = 1
                elif "EXEC" == msg["event"]:
                    print("jscb.JSCB:",msg["event"])
                    try:
                        if exec_nr > 0:

                            if MAIN.modes.val("REC"):
                                if val >= 1: # only Press
                                    MAIN.master.exec_rec(exec_nr-1)
                                    EXEC_REFRESH = 1
                                msg["OK"] = "REC"
                                OK = 1
                            elif MAIN.modes.val("EDIT"):
                                if val >= 1: # only Press
                                    MAIN.master.exec_edit(exec_nr-1)
                                    EXEC_REFRESH = 1
                                msg["OK"] = "EDIT"
                                OK = 1
                            elif MAIN.modes.val("COPY"):
                                if val >= 1: # only Press
                                    MAIN.EXEC.copy(exec_nr-1)
                                    if MAIN.modes.val("COPY") > 2:
                                        MAIN.modes.val("COPY",0)
                                    EXEC_REFRESH = 1
                                msg["OK"] = "COPY"
                                OK = 1
                            elif MAIN.modes.val("MOVE"):
                                if val >= 1: # only Press
                                    MAIN.EXEC.move(exec_nr-1)
                                    EXEC_REFRESH = 1
                                msg["OK"] = "MOVE"
                                OK = 1
                            elif MAIN.modes.val("DEL"):
                                if val >= 1: # only Press
                                    MAIN.EXEC.delete(exec_nr-1)
                                    MAIN.modes.val("DEL",0)
                                    EXEC_REFRESH = 1
                                msg["OK"] = "DEL"
                                OK = 1




                            if not OK:
                                print("MIDI?",val)
                                if val >= 0: #Press/Release
                                    if "MOUSE" in msg and msg["MOUSE"] == "RIGHT":
                                        MAIN.master.exec_go(exec_nr-1,xfade=0,val=val)
                                    else:
                                        MAIN.master.exec_go(exec_nr-1,xfade=None,val=val)
                                    OK = 1
                                    #EXEC_REFRESH = 1

                            msg["MODES"]=MAIN.modes.list("active")

                    except Exception as e:
                        print("EXEC ERR:",e)
                        raise e

            
                if OK:
                    cprint(" jsbc.remote-key:",msg ,color="green")
                    print()
                    if EXEC_REFRESH:
                        def xx():
                            #MAIN.execlib.exec_set_mc(MAIN.EXEC.label_exec,MAIN.EXEC.val_exec)
                            nr = exec_nr-1
                            label = MAIN.EXEC.label_exec[nr] #l[nr]
                            data  = MAIN.EXEC.val_exec[nr] #d[k]
                            print(" EXEC_REFRESH ? ",nr,label,"==================")
                            MAIN.execlib.exec_set_mc_single(nr,label,data)
                            print(time.time())

                            global GLOBAL_old_exec_nr
                            nr2 = GLOBAL_old_exec_nr
                            if nr2 != nr and nr2 >= 0:
                                label = MAIN.EXEC.label_exec[nr2] #l[nr]
                                cprint(" GLOBAL_OLD_EXEC_NR",nr2,nr,label,"==================")
                                data  = MAIN.EXEC.val_exec[nr2] #d[k]
                                MAIN.execlib.exec_set_mc_single(nr2,label,data)
                            GLOBAL_old_exec_nr = nr
                        thread.start_new_thread(xx,())
                else:
                    cprint(" jsbc.remote-key:",msg ,color="red")
                    print()
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
