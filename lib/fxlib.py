#/usr/bin/python3

import random

import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import lib.fixlib as fixlib

def cprint(*args):
    print(args)

def process_wings(xfixtures,fx_prm):
    """process the wing's of selected fixtures
    input: [1,2,3,4,10,12,13,14]
    if WING = 2 return: [[1,2,3,4][14,13,12,10]]
    """
    wing_buffer = []
    fix_count = len(xfixtures)
    prm = fx_prm # ToDo:  global WING for PAN/TILE !? ATTRIBUT is not availible in this moment 

    if prm["WING"] > 1 and fix_count > 1:
        wing_count = fix_count // prm["WING"]
        number_of_fix_in_wing = fix_count // wing_count

        if number_of_fix_in_wing < 2:
            number_of_fix_in_wing = 2

        for i in range(number_of_fix_in_wing):
            j = i*wing_count
            wing = xfixtures[j:j+wing_count]
            if i%2!=0:
                wing = wing[::-1]
            cprint("wing",i,"j",j,"wing_count:",wing_count,"wing",wing)
            wing_buffer.append(wing)

        if fix_count > j+wing_count: # append Fixtures Left over
            wing = xfixtures[j+wing_count:]
            wing_buffer.append(wing)
    else:
        wing_buffer.append(xfixtures)

    if prm["SHUFFLE"]:
        _wing_buffer = []
        for wing in wing_buffer:
            wing = wing[:]
            random.seed(9300) # sync random
            random.shuffle(wing)
            _wing_buffer.append(wing)
        wing_buffer = _wing_buffer
    return wing_buffer

def process_effect(wing_buffer,fx_prm,fx_prm_move,modes,jclient_send,master,FIXTURES,fx_name=""):
    jdatas = []
    offset = 0
    offset_move = 0
    start = fx_prm["START"]
    base  = fx_prm["BASE"]

    for wi, wing in enumerate(wing_buffer):
        count_of_fix_in_wing = len(wing)
        coffset= 0 # 1024/count_of_fix_in_wing * (offset/255)
        coffset_move=0
    
        for fix in wing:
            if fix not in FIXTURES.fixtures:
                continue
            data = FIXTURES.fixtures[fix]
            for attr in data["ATTRIBUT"]:

                if attr.startswith("_"):
                    continue
                if attr.endswith("-FINE"):
                    continue

                jdata = {"MODE":"FX"}
                jdata["WING"] = wi
                jdata["VALUE"]    = None
                jdata["FIX"]      = fix
                dmx               = fixlib.get_dmx(FIXTURES.fixtures,fix,attr)
                jdata["DMX"]      = dmx

                dmx_fine = fixlib.get_dmx(FIXTURES.fixtures,fix,attr+"-FINE")
                if dmx_fine != jdata["DMX"] and dmx > 0:
                    jdata["DMX-FINE"] = dmx_fine

                jdata["ATTR"]     = attr

                tmp_fx_prm = fx_prm
                coffset= round(offset,1)

                if attr in ["PAN","TILT"]:
                    tmp_fx_prm = fx_prm_move
                    coffset_move= round(offset_move,1)

                csize  = tmp_fx_prm["SIZE"]
                cspeed = tmp_fx_prm["SPEED"]
                cstart = tmp_fx_prm["START"]
                cbase  = tmp_fx_prm["BASE"]
                width  = tmp_fx_prm["WIDTH"]
                invert = tmp_fx_prm["INVERT"]

                fx=""
                if "SIN" in fx_name:
                    fx = "sinus"
                elif "FD" in fx_name:
                    fx = "fade"
                elif "RND" in fx_name:
                    fx = "rnd"
                elif "STATIC" in fx_name:
                    fx = "static"
                elif "ON" in fx_name:
                    fx = "on"
                elif "RAMP2" in fx_name:
                    fx = "bump2"
                    fx = "ramp2"
                elif "RAMP" in fx_name:
                    fx = "ramp"
                elif "COS" in fx_name:
                    fx = "cosinus"

                if fx:
                    if attr in ["PAN","TILT"]:
                        cprint("SKIP FX attr:{} fix:{} " .format(attr,fix) )
                        continue

                if fx:
                    if cspeed < 0:
                        fx = "off"
                else:
                    if ":DIM" in fx_name:
                        base=""
                        ffxb=fx_mo[fx_prm["MO"]] 

                        if attr == "DIM":
                            if cspeed < 0:
                                fx = "off"
                            else:
                                fx = ffxb #"fade"
                    elif ":TILT" in fx_name:
                        base=""
                        if attr == "PAN":
                            fx = "off"
                        if attr == "TILT":
                            if cspeed < 0:
                                fx = "off"
                            else:
                                fx = "sinus"
                    elif ":PAN" in fx_name:
                        base=""
                        if attr == "PAN":
                            if cspeed < 0:
                                fx = "off"
                            else:
                                fx = "cosinus" 
                        if attr == "TILT":
                           fx = "off"
                    elif ":CIR" in fx_name:
                        base=""
                        if attr == "PAN":
                            if cspeed < 0:
                                fx = "off"
                            else:

                                fx = "cosinus" 
                        if attr == "TILT":
                            if cspeed < 0:
                                fx = "off"
                            else:
                                fx = "sinus"

                    elif ":RED" in f_name:
                        fxon  = "on" 
                        fxoff = "static" #"off" 
                        MODE = fx_modes[fx_prm["MODE"]]
                        
                        if "RED" in MODE:
                            base="-"
                            if attr == "RED":
                                fx = fxon # ON ---- 
                                #csize *=-1
                            if attr == "GREEN":
                                fx = "static"
                                csize = 0
                            if attr == "BLUE":
                                fx = "static"
                                csize = 0
                        elif "GREEN" in MODE:
                            base="-"
                            if attr == "RED":
                                fx = "static"
                                csize = 0
                            if attr == "GREEN":
                                fx = fxon # ON ----
                                csize *=-1
                            if attr == "BLUE":
                                fx = "static"
                                csize = 0
                        elif "BLUE" in MODE:
                            base="-"
                            if attr == "RED":
                                fx = "static"
                                csize = 0
                            if attr == "GREEN":
                                fx = "static"
                                csize = 0
                            if attr == "BLUE":
                                fx = fxon # ON ----
                                csize *=-1
                        elif "YELLOW" in MODE:
                            base="-"
                            if attr == "RED":
                                fx = fxon
                                csize *=-1
                            if attr == "GREEN":
                                fx = fxon
                                csize *=-1
                            if attr == "BLUE":
                                fx = "static"
                                csize = 0
                        elif "CYAN" in MODE: 
                            base="-"
                            if attr == "RED":
                                fx = fxoff
                                invert *= -1
                                csize = 0
                                fx = fxon
                            if attr == "GREEN":
                                fx = fxon
                                csize=0
                            if attr == "BLUE":
                                fx = fxon
                                csize=0
                        elif "MAG" in MODE: 
                            base="-"
                            if attr == "RED":
                                fx = fxon
                                csize=0
                            if attr == "GREEN":
                                fx = fxoff
                                invert *= -1
                                csize = 0
                                fx = fxon
                            if attr == "BLUE":
                                fx = fxon
                                csize=0
                        else:
                            cprint("FX: unbekant",fx_modes[fx_prm["MODE"]],color="red")

                    fxtype = fx

                fxtype = fx

                if "FX" not in data["ATTRIBUT"][attr]:
                    data["ATTRIBUT"][attr]["FX"] =""
                if "FX2" not in data["ATTRIBUT"][attr]:
                    data["ATTRIBUT"][attr]["FX2"] ={}

                if data["ATTRIBUT"][attr]["ACTIVE"] and fxtype:
                    fjdata = {}
                    if cspeed < 0.1:
                        fjdata["TYPE"]  = "off"
                    else:
                        fjdata["TYPE"]  = fxtype
                    fjdata["SIZE"]  = round(csize,2)
                    fjdata["SPEED"] = round(cspeed,2)
                    fjdata["WIDTH"] = int(width)
                    fjdata["START"] = cstart
                    if attr in ["PAN","TILT"]:
                        fjdata["OFFSET"]= round(coffset_move,2)
                    else:
                        fjdata["OFFSET"]= round(coffset,2)
                    fjdata["INVERT"]= int(invert)
                    fjdata["BASE"]  = cbase
                    jdata["FX2"]    = fjdata
                    data["ATTRIBUT"][attr]["FX2"] = fjdata
                    jdatas.append(jdata)
                    #print("GOO FX:",jdata)

            
            if fx_prm_move["OFFSET"] > 0.5: # and 
                aoffset_move = (100/count_of_fix_in_wing) * (fx_prm_move["OFFSET"]/100) 
                if fx_prm_move["DIR"] <= 0:
                    offset_move -= aoffset_move 
                else:
                    offset_move += aoffset_move 
                offset_move = round(offset_move,2)

            if fx_prm["OFFSET"] > 0.5: # and 
                aoffset = (100/count_of_fix_in_wing) * (fx_prm["OFFSET"]/100) 
                if fx_prm["DIR"] <= 0:
                    offset -= aoffset 
                else:
                    offset += aoffset 
                offset = round(offset,2)

    #exit()
    if jdatas and not modes.val("BLIND"):
        jclient_send(jdatas)
    master._refresh_fix()

    return jdatas

