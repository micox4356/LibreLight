#!/usr/bin/python3

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
                # FIXTURES.encoder
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
                    print("  Xevent",FIX,VAL,ATTR)
                    #cb = Xevent(fix=FIX,elem=None,attr=ATTR,mode="ENCODER",data=[]) #data)
                    #FIXTURES.encoder(str(FIX),ATTR,xval="click",xfade=0,xdelay=0)#,blind=0)
                    FIXTURES.encoder(str(FIX),ATTR,xval=VAL,xfade=0,xdelay=0)#,blind=0)

                    #print(dir(cb))
                    #event =  DEVENT()
                    #event.num = enum

                    #master.refresh_fix() # delayed
                    #refresher_fix.reset() # = Refresher()
                    #cb.cb(event)
                if "CLEAR" == msg["event"]:
                    FIXTURES.clear()
                if "EXEC" == msg["event"]:
                    print("  EXEC EXEC")
                    val = -1
                    exec_nr = -1
                    try:
                        if "VAL" in msg:
                            val = int(msg["VAL"])
                        if "EXEC" in msg:
                            exec_nr = int(msg["EXEC"])
                        if val >= 0 and exec_nr > 0:
                            print("PRESET_GOOO",exec_nr,val)
                            s = time.time()
                            master.preset_go(exec_nr-1,xfade=None,val=val)
                            e = time.time()
                            #print("time:",e-s,e)
                            #print("TIME:",int((e-s)*1000),int(e*10)-1_703_800_000)
                            #print("TIME:",int((e-s)*1000),int(e*10)/10)
                            print("EXE TIME:","{:0.02f}".format(e-s),int(e*100)/100)
                            print()

                    except Exception as e:
                        print("EXEC ERR:",e)
            
    except Exception as e:
        cprint("exception JSCB:",e)
        cprint("- i:",i)
        cprint("- msg:",msgs)
        cprint(traceback.format_exc(),color="red")
        if sock:
            msg = ["Notice: Exception on JSCB-SERVER: ",str(e)]
            msg = json.dumps(msg)
            msg = bytes(msg,"utf8")
            chat._send(sock,msg)

    #time.sleep(1/60)
