

import json
from collections import OrderedDict

f_out = open("patch.sav","w") 


nr=0
dmx=1
def add(jdata,att):
    global nr,dmx,name,fix,sub
    print("======", "{}_{} {:03}".format( name,fix,sub) )
    #for i in jdata:
    #    print(i )

    
    if "ATTRIBUT" in jdata:
        for a in att:
            if a == "":
                print("---",nr+dmx-1,nr,"")
                nr+=1
                continue
            rdata = '{"NR": 1, "MASTER": "0", "MODE": "S", "VALUE": 0, "ACTIVE": 0, "FX": "", "FX2": {}}'
            rdata = '{"NR": 1, "MASTER": "0", "MODE": "S", "VALUE": 0, "ACTIVE": 0, "FX": "", "FX2": {}}'
            jattr = json.loads(rdata,object_pairs_hook=OrderedDict)
            jattr["NR"] = nr
            if a in ["DIM","RED","GREEN","BLUE"]: #,"PAN","TILT","ZOOM","IRIS"]:
                jattr["MODE"] = "F"

            jdata["ATTRIBUT"][a] = jattr
            print("add",nr+dmx-1,nr,a)
            nr+=1
    print()


fix = 1
sub =1
name="VPU"
dmx=1
univ=2
#for i in range(9*13): # fixtures
#for i in range(8+1*12+1): # fixtures
#for i in range((8*2)+1*(12*2)+1): # fixtures
for i in range(96): # fixtures
    print("====================================")
    rdata='{"DMX": 1, "UNIVERS": 2, "NAME": "VPU_01", "TYPE": "MOVER", "VENDOR": "AYERTON", "ATTRIBUT":{}}'
    jdata = json.loads(rdata,object_pairs_hook=OrderedDict)

    jdata["NAME"] = "{}_{}{:02}".format( name,fix,sub)
    jdata["NAME"] = "{}_{:03}".format( name,fix)#,sub)
    nr=1

    jdata["UNIVERS"] = univ
    jdata["DMX"] = dmx

    att = []
    #att.append("PAN")
    #att.append("PAN-FINE")
    #att.append("TITL")
    #att.append("TILT-FINE")
    #att.append("")
    #att.append("SHUTTER")
    #att.append("DIM")
    #att.append("ZOOM")
    #att.append("GOBO")
    #att.append("")
    #att.append("GOBO2")
    #att.append("G-ROT")
    #att.append("")
    #att.append("PRISMA")
    #att.append("P-ROT")
    #att.append("")
    #att.append("")
    att.append("DIM")
    att.append("RED")
    att.append("GREEN")
    
    att.append("BLUE")

    add(jdata,att)
    fnr="{}{:02}".format(fix,sub)
    fnr="{}".format(fix,sub)
    fnr="{:04}".format(fix,sub)
    f_out.write("{}\t{}\t{}\n".format(fnr,fnr,json.dumps(jdata) ) )
    f_out.flush()   

    rdata='{"DMX": 1, "UNIVERS": 2, "NAME": "SPX7_01", "TYPE": "MOVER", "VENDOR": "JB", "ATTRIBUT":{}}'
    jdata = json.loads(rdata,object_pairs_hook=OrderedDict)


    if 0:#for i in range(3):
        sub+=1
        jdata["NAME"] = "{}_{:03}{:03}".format( name,fix,sub)

        dmx+=nr-1
        univ=2
        nr=1

        jdata["UNIVERS"] = univ
        jdata["DMX"] = dmx

        att = []
        att.append("RED")
        att.append("GREEN")
        att.append("BLUE")
        att.append("WHITE")

        add(jdata,att)
        fnr="{}{:02}".format(fix,sub)
        fnr="{:04}".format(fix,sub)
        f_out.write("{}\t{}\t{}\n".format(fnr,fnr,json.dumps(jdata) ) )
        f_out.flush()
    fix += 1
    sub=1
    dmx+=nr-1
    if dmx >= 512:
        univ +=1
        dmx = 1

