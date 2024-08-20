import __main__ as MAIN
import json 
import sys
import time

_file_path = "/opt/LibreLight/Xdesk/"
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

from lib.cprint import cprint
import lib.libtk as libtk


def serialize_event(event):
    data = {}
    for k in dir(event):
        if k.startswith("_"):
            continue
        v = event.__getattribute__(k)
        if v == '??':
            continue
        if type(v) not in [int,str,float]:
            continue
        data[k] = v

    data["event"] = str(event).split()[0][1:]
    if "state" in data:
        del data["state"]
    if "time" in data:
        del data["time"]
    if "serial" in data:
        del data["serial"]
    keys = list(data.keys())
    keys.sort()
    data2={}
    for k in keys:
        data2[k] = data[k] 
    return data2



Control_L = 0
Alt_L = 0
def tk_event(event,data={}):
    #print("tk_event",event,data)
    global Control_L,Alt_L
    if MAIN._global_key_lock:
        return
    #print("   ",dir(event)) #.dict())
    data =  serialize_event(event)

    if 'keysym' in data:
        keysym = data["keysym"]
        if keysym == 'Control_L':  
            if "Press" in data["event"]:
                Control_L = 1
            if "Release" in data["event"]:
                Control_L = 0
        if keysym == 'Alt_L':  
            if "Press" in data["event"]:
                Alt_L = 1
            if "Release" in data["event"]:
                Alt_L = 0

        data["Alt_L"] = Alt_L
        data["Control_L"] = Control_L
        
    print("tk_event",data)
    ok=0

    # CONTROL + KEY
    key_code = {"s":"SAVE\nSHOW","c":"RESTART" }
    if 'keysym' in data:
        keysym = data["keysym"]

        if keysym in key_code:
            if "Press" in data['event'] and data["Control_L"]:
                MOD = key_code[keysym]
                msg=json.dumps([{"event":MOD}]).encode("utf-8")
                cprint("SEND tk_event",msg,color="green")
                MAIN.cmd_client.send(msg)
                if MOD in ["RESTART"]:
                    time.sleep(2)
                    exit()
                ok = 1

        if ok:
            return

    # NORMAL KEY
    key_code = {"r":"REC","x":"REC-FX","e":"EDIT","c":"CFG-BTN"
                ,"m":"MOVE","Delete":"DEL","End":"FX-OFF"
                ,"Escape":"ESC","s":"SELECT","f":"FLASH"
                ,"C":"COPY","d":"DEL","b":"BLIND"
                }
    if 'keysym' in data:
        keysym = data["keysym"]

        if keysym in key_code:
            if "Press" in data['event']:
                MOD = key_code[keysym]
                msg=json.dumps([{"event":MOD}]).encode("utf-8")
                cprint("SEND tk_event",msg,color="green")
                MAIN.cmd_client.send(msg)
            ok = 1
    cprint("OK",ok)
    if not ok:
        libtk.tk_keyboard_callback(event,data=data)

