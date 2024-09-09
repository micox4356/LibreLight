#!/usr/bin/python3
import os
import json
import time

import __main__  as MAIN

from collections import OrderedDict
from lib.cprint import *

HOME = os.getenv('HOME')

def _fixture_decode_sav_line(line):
    out = None
    out = [0,"none",{}]

    if line.count("\t") < 2:
        cprint("Error line.count('\\t') < 2  (is:{})".format(line.count("\t")),color="red",end=" ")
        cprint("file:{}".format(line),color="red")
    else:
        key,label,rdata = line.split("\t",2)
        jdata = json.loads(rdata,object_pairs_hook=OrderedDict)
        key = int(key)
        #label += " dsav"
        #label = label.replace(" dsav","")
        out = [key,label,jdata]

    #if not out:
    #print(line)
    #sys.exit()
    return out

def _fixture_repair_nr0(jdata):
    nrnull = 0
    if "ATTRIBUT" in jdata:  # translate old Fixtures.fixtures start with 0 to 1          
        if nrnull:
            cprint("DMX NR IS NULL",attr,"CHANGE +1")
            for attr in jdata["ATTRIBUT"]:
                if "NR" in jdata["ATTRIBUT"][attr]:
                    nr = jdata["ATTRIBUT"][attr]["NR"]
                    if nr >= 0:
                        jdata["ATTRIBUT"][attr]["NR"] +=1
    #return jdata

def FIXTURE_CHECK_SDATA(ID,sdata):
    #print("FIXTURE_CHECK_SDATA",ID)
    new_f = OrderedDict()
    #print("++++")
    for k,j in sdata.items():
        overide=0 # only for repair
        if overide:
            if k in ["TYPE","VENDOR"]: #ignor
                continue
        new_f[k] = j
        if k =="NAME":
            #print("AAAADDDDDD")
            if "TYPE" not in sdata and not overide:
                if len( sdata["ATTRIBUT"]) == 1:
                    new_f["TYPE"] = "DIMMER"
                elif "PAN" in sdata["ATTRIBUT"]:
                    new_f["TYPE"] = "MOVER"
                elif "RED" in sdata["ATTRIBUT"] and len(sdata["ATTRIBUT"]) == 3:
                    new_f["TYPE"] = "RGB"
                elif "RED" in sdata["ATTRIBUT"]:
                    new_f["TYPE"] = "LED"
                elif "CYAN" in sdata["ATTRIBUT"]:
                    new_f["TYPE"] = "COLOR"
                else:
                    new_f["TYPE"] = ""
            if "VENDOR" not in sdata and not overide:
                new_f["VENDOR"] = ""

        #print(k,j)#,sdata)
    sdata = new_f
    if "ACTIVE" not in sdata:
        sdata["ACTIVE"] = 0

    sdata["ATTRIBUT"]["_ACTIVE"] = OrderedDict()
    sdata["ATTRIBUT"]["_ACTIVE"]["NR"] = 0
    sdata["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
    sdata["ATTRIBUT"]["_ACTIVE"]["VALUE"] = 0
    sdata["ATTRIBUT"]["_ACTIVE"]["FX2"] = {}
    sdata["ATTRIBUT"]["_ACTIVE"]["FX"] = ""

    DEL = []
    for ATTR in list(sdata["ATTRIBUT"].keys()):
        if ATTR.startswith("_"):
            continue

        if ATTR.endswith(" FINE"):
            ATTR2 = ATTR.replace(" FINE","-FINE")
            ATTR2 = ATTR2.replace(" -","-")
            ATTR2 = ATTR2.replace("  "," ")
            ATTR2 = ATTR2.replace("  "," ")
            ATTR2 = ATTR2.replace("  "," ")
            if ATTR2 not in sdata["ATTRIBUT"]:
                print("  CHECK_SDATA REPAIR",[ATTR,ATTR2])
                sdata["ATTRIBUT"][ATTR2]  = sdata["ATTRIBUT"][ATTR] 
                DEL.append(ATTR)
    for d in DEL:
        if d in sdata["ATTRIBUT"]:
            print("  CHECK_SDATA DEL   ",[d],"!")
            del sdata["ATTRIBUT"][d]

    if "DIM" not in sdata["ATTRIBUT"]:
        _tmp = None
        #print(sdata)
        vdim_count = 0
        for a in ["RED","GREEN","BLUE"]:#,"WHITE","AMBER"]:
            if a in sdata["ATTRIBUT"]:
                vdim_count +=1

        if vdim_count == 3:
            _tmp =  {"NR": 0, "MASTER": "0", "MODE": "F", "VALUE": 255, "ACTIVE": 0, "FX": "", "FX2": {}}
            _tmp = OrderedDict(_tmp)
            sdata["ATTRIBUT"]["DIM"] =_tmp 
        print("   ADD ---- VDIM",vdim_count,_tmp)
        #input("STOP")

    for attr in sdata["ATTRIBUT"]:
        row = sdata["ATTRIBUT"][attr]
        row["ACTIVE"] = 0

        if "FX" not in row:
            row["FX"] =""
        if "FX2" not in row:
            row["FX2"] = {}
        if "MASTER" not in row:
            row["MASTER"] = 0


    if "ID" not in sdata:
        sdata["ID"] = str(ID)
    return sdata


def _parse_fixture_name(name):
    out = []
    #{"FIX","MAN","CH","PATH":""}
    if name.count(".") == 2:
        m,n,e = name.split(".")
        #out = [n,m,"0",name]
        out = {"name":n,"manufactor":m,"fname":name}
    elif name.count("_") == 2:
        name,e = name.split(".")
        m,n,c = name.split("_")
        out = {"name":n,"ch":c,"manufactor":m,"name":name}
        #out = [n,m,c,name]
    else:
        out = {"name":name}
    return out




def index_fixtures():
    p="/opt/LibreLight/Xdesk/fixtures/"
    ls = os.listdir(p )
    ls.sort()
    blist = []
    
    for l in ls:
        b = _parse_fixture_name(l)
        b.append(p)
        b.insert(0,"base")
        blist.append(b)
    return blist



#def _fixture_create_import_list(path=None):
def _fixture_load_import_list(path=None):
    if not path:
        path = "/home/user/LibreLight/show"

    blist = []
    lsd = os.listdir(path)
    lsd.sort()
    fname_buffer = []
    for sname in lsd:
        #print("   ",sname)
        ok = 0
        try:
            fname = path+"/"+sname+"/patch.sav"
            if os.path.isfile(fname):
                ok = 1
            else:
                fname = path+"/"+sname
                if os.path.isfile(fname):
                    ok = 1
            #fname_buffer = []
            if not ok:
                continue

            f = open(fname)
            lines = f.readlines()
            f.close()

            for line in lines:
                ok2 = 0
                _key = ""
                line = line.split("\t")
                if len(line) < 2:
                    continue
                jdata = json.loads(line[2])

                fixture = jdata
                _len = str(fixture_get_ch_count(fixture))
                if "ATTRIBUT" in jdata:
                    #_len = len(jdata["ATTRIBUT"])
                    #if "_ACTIVE" in jdata["ATTRIBUT"]:
                    #    _len -= 1
                    _key = list(jdata["ATTRIBUT"].keys()) 
                    _key.sort()
                    _key = str(_key)
                    if _key not in fname_buffer:
                        fname_buffer.append(_key) # group same fixtures by ATTR
                        ok2 = 1
                if ok2:
                    name = jdata["NAME"]
                    #row = [name,fname+":"+name,path])
                    xfname = fname.replace(path,"")
                    row = {"xfname":xfname ,"name":name,"ch":_len, "xpath":path,"d":_key} #,"b":jdata}
                    blist.append(row)
        except Exception as e:
            print("exception",e)
            raise e
    return blist


def fixture_get_ch_count(fixture):
    _len = [0,0]
    if "ATTRIBUT" not in fixture:
        return [-1,-1]

    for at in fixture["ATTRIBUT"]:
        #print(at,_len)
        #print(" ",fixture["ATTRIBUT"][at])
        if not at.startswith("_") and not at.startswith("EMPTY"):
            _len[1] += 1

        if "NR" in fixture["ATTRIBUT"][at]:
            NR = fixture["ATTRIBUT"][at]["NR"]
            if NR > _len[0]:
                _len[0] = NR
        #print("-",at,_len)

    return _len

def fixture_get_attr_data(fixture,attr):
    if "ATTRIBUT" in fixture:
        if attr in fixture["ATTRIBUT"]:
            return fixture["ATTRIBUT"][attr]

    if "NAME" in fixture:
        print("  NO fixture_get_attr_data A",fixture["NAME"],attr)
    else:
        print("  NO fixture_get_attr_data B",fixture,attr)

def fixture_order_attr_by_nr(fixture):
    out1 = []
    max_nr = 0
    if "ATTRIBUT" not in fixture:
        return []

    nrs = {}
    for at in fixture["ATTRIBUT"]:
        #print("+   ",at)
        atd = fixture_get_attr_data(fixture,at)
        #print("+   ",atd)
        if not atd:
            continue

        k = atd["NR"]
        v = at
        nrs[k] = v
        if k > max_nr:
            max_nr = k

    for i in range(1,max_nr+1):
        if i not in nrs:
            v = "EMPTY" #-{}".format(i)
            nrs[i] = v
            #print("-: ",v)


    nrs_key = list(nrs.keys())
    nrs_key.sort()
    #print(nrs_key)

    for k in nrs_key:
        v = nrs[k]
        #print("-: ",k,v)
        out1.append(v)

    #print()
    return out1 

def _load_fixture_list(mode="None"):
    blist = []

    if mode == "USER":
        path = HOME+"/LibreLight/fixtures/"

    elif mode == "GLOBAL":
        path="/opt/LibreLight/Xdesk/fixtures/"

    elif mode == "IMPORT":
        path=None 

    _r =  _fixture_load_import_list(path=path)
    blist.extend( _r )
    return blist

def get_attr(fixtures,fix,attr):
    if fix in fixtures:
        data = fixtures[fix]
        if "ATTRIBUT" in data:
            if attr in data["ATTRIBUT"]:
                return data["ATTRIBUT"][attr]


def get_dmx(fixtures,fix,attr):
    #cprint("get_dmx",[fix,attr], fix in self.fixtures)
    DMX = -99
    if attr.startswith("_"):
        return -88

    if fix in fixtures:
        data = fixtures[fix]
        if "DMX" in data:
            DMX = int(data["DMX"])
        
        if DMX <= 0:
            return DMX # VIRTUAL FIX

        if "UNIVERS" in data:
            DMX += int(data["UNIVERS"])*512

        #adata = self.get_attr(fix,attr)
        adata = get_attr(fixtures,fix,attr)

        if adata:
            if "NR" in adata:
                NR = adata["NR"] 
                if NR <= 0:
                    return -12 # not a VIRTUAL ATTR
                else:
                    DMX+=NR-1
                return DMX
    return -199

def get_active(fixtures,_filter=""): #_filter only-fx
    cprint("fixlib.get_active",_filter)
    CFG = OrderedDict()

    sdata = OrderedDict()
    sdata["CFG"] = CFG # OrderedDict()
    sdata["CFG"]["FADE"] = MAIN.FADE.val()
    sdata["CFG"]["DEALY"] = 0

    for fix in fixtures:                            
        data = fixtures[fix]

        for attr in data["ATTRIBUT"]:
            if not data["ATTRIBUT"][attr]["ACTIVE"]:
                continue

            if fix not in sdata:
                sdata[fix] = {}

            if attr not in sdata[fix]:
                sdata[fix][attr] = OrderedDict()

                if "ONLY-FX" in _filter:
                    #cprint( "          ONLY FX !!!     -------------------- ")
                    sdata[fix][attr]["VALUE"] = None 
                else:
                    sdata[fix][attr]["VALUE"] = data["ATTRIBUT"][attr]["VALUE"]

                if "FX" not in data["ATTRIBUT"][attr]: 
                     data["ATTRIBUT"][attr]["FX"] = ""

                if "FX2" not in data["ATTRIBUT"][attr]: 
                     data["ATTRIBUT"][attr]["FX2"] = {}
                
                sdata[fix][attr]["FX"] = data["ATTRIBUT"][attr]["FX"] 
                sdata[fix][attr]["FX2"] = data["ATTRIBUT"][attr]["FX2"] 

    return sdata

def _deselect_all(fixtures,fix=None):
    cprint("fixlib._deselect_all()",fix,"ALL",color="yellow")
    c=0
    if fix in fixtures:
        data = fixtures[fix]

        for attr in data["ATTRIBUT"]:
            #print("SELECT ALL",fix,attr)
            if "-FINE" in attr.upper():
                pass
            else:
                c+=select(fixtures,fix,attr,mode="off",mute=1)
    
    return c

def _select_all(fixtures,fix=None,mode="toggle",mute=0):
    if not mute:
        cprint("fixlib._select_all()",fix,"ALL",mode,color="yellow")
    c=0
    if fix in fixtures:
        data = fixtures[fix]
        for attr in data["ATTRIBUT"]:
            #print("SELECT ALL",fix,attr)
            if "-FINE" in attr.upper():
                continue
            
            if mode == "toggle":
                c+=select(fixtures,fix,attr,mode="on",mute=mute)
            elif mode == "swap":
                if not attr.startswith("_"):
                    c+=select(fixtures,fix,attr,mode="toggle",mute=mute)

        if not c and mode == "toggle": # unselect all
            c= _deselect_all(fixtures,fix=fix)
    return c 

def select(fixtures,fix=None,attr=None,mode="on",mute=0):
    if not mute:
        cprint("fixlib.select() >>",fix,attr,mode,color="yellow")
    out = 0

    if fix == "SEL":
        if attr.upper() == "INV-ATTR":
            fixs = get_active(fixtures)
            cprint("selected:",len(fixs))
            for fix in fixs:
                x=_select_all(fixtures,fix=fix,mode=mode,mute=1)
            return None 

    if fix in fixtures:
        if attr.upper() == "ALL":
            x=_select_all(fixtures,fix=fix,mode=mode)
            return x

        data = fixtures[fix]
        if attr in data["ATTRIBUT"]:
            if mode == "on":
                if not data["ATTRIBUT"][attr]["ACTIVE"]:
                    data["ATTRIBUT"][attr]["ACTIVE"] = 1
                    data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
                    out = 1
            elif mode == "off":
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    data["ATTRIBUT"][attr]["ACTIVE"] = 0
                    out = 1
            elif mode == "toggle":
                if data["ATTRIBUT"][attr]["ACTIVE"]:
                    data["ATTRIBUT"][attr]["ACTIVE"] = 0
                else:
                    data["ATTRIBUT"][attr]["ACTIVE"] = 1
                    data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
                out = 1
    return out

def clear(fixtures):
    out = 0
    for fix in fixtures:
        data = fixtures[fix]
        for attr in data["ATTRIBUT"]:
            #if attr.endswith("-FINE"):
            #    continue
            if data["ATTRIBUT"][attr]["ACTIVE"]:
                out +=1
            data["ATTRIBUT"][attr]["ACTIVE"] = 0
    return out



def encoder(fixtures,fix,attr,xval="",xfade=0,xdelay=0,blind=0):

    _blind = 0
    if MAIN.modes.val("BLIND"):
        _blind = 1 
    if blind:
        _blind = 1
    
    if not _blind:
        cprint("fixlib.encoder",fix,attr,xval,xfade,color="yellow")

    if attr == "CLEAR":
        clear(fixtures)
        return 0

    if attr == "ALL":
        x=select(fixtures,fix,attr,mode="toggle")
        return x

    if attr == "INV-ATTR":
        cprint("-x-x-x-x-x-x-x-X-")
        x=select(fixtures,fix,attr,mode="swap")
        master.refresh_fix()
        return x
    if attr == "INV-FIX":
        cprint("-x-x-x-x-x-x-x-x-")
        x=select(fixtures,fix,attr,mode="swap")
        return x
    out = []

    #cprint("Fixture.Encoder(...)",fix,attr)
    if fix not in fixtures: 
        #cprint(" activate Fixture in fixture list on encoder click ")

        ii =0
        delay=0
        sstart = time.time()
        #cprint("  encoder fix  <--")
        sub_data = []
        for _fix in fixtures:
            #print([fix,"_fix",_fix])
            #print(fixtures)
            #print(type(fixtures),len(fixtures))
            ii+=1
            data = fixtures[_fix]
            if "-FINE" in attr.upper():
                continue

            elif (attr in data["ATTRIBUT"] ) and "-FINE" not in attr.upper()   :
                if xval == "click":
                    select(fixtures,_fix,attr,mode="on")
                elif data["ATTRIBUT"][attr]["ACTIVE"]:
                    if _fix:
                        sub_data.append([_fix,attr,xval,xfade,delay])
            if MAIN.DELAY._is():
                delay += MAIN.DELAY.val()/100

        sub_jdata = []
        for dd in sub_data:
            #print("---",len(sub_data),end="")
            #encoder(fix,attr,xval,xfade,delay)
            _x123 = encoder(fixtures,dd[0],dd[1],dd[2],dd[3],dd[4],blind=1)
            sub_jdata.append(_x123)

        if sub_jdata:
            cprint("  SEND MASTER ENCODER:",len(sub_data),sub_data[0],"... _blind:",_blind)#,end="")
            if not _blind:
                MAIN.jclient_send(sub_jdata) 

        jdata=[{"MODE":ii}]
        #cprint("  ENCODER j send <--")

        if not _blind:
           MAIN.jclient_send(jdata)
        return sub_jdata  #len(sub_data)

    data = fixtures[fix]

    if xval == "click":
        #cprint(data)
        return select(fixtures,fix,attr,mode="toggle")


    v2=data["ATTRIBUT"][attr]["VALUE"]
    change=0
    increment = 5 #4.11
    jdata = {"MODE":"ENC"}
    if xval == "++":
        v2+= increment
        jdata["INC"] = increment
        change=1
    elif xval == "--":
        jdata["INC"] = increment*-1
        v2-= increment
        change=1
    elif xval == "+":
        increment = 0.25 #.5
        v2+= increment
        jdata["INC"] = increment
        change=1
    elif xval == "-":
        increment = 0.25 #.5
        jdata["INC"] = increment*-1
        v2-= increment
        change=1
    elif type(xval) is int or type(xval) is float:
        v2 = xval 
        change=1

        
    if v2 < 0:
        v2=0
    elif v2 > 256:
        v2=256

    jdata["VALUE"]    = round(v2,4)
    jdata["FIX"]      = fix
    jdata["FADE"]     = 0
    jdata["DELAY"]    = 0
    jdata["ATTR"]     = attr
    dmx               = get_dmx(fixtures,fix,attr)
    jdata["DMX"]      = dmx

    dmx_fine = get_dmx(fixtures,fix,attr+"-FINE")
    if dmx_fine != jdata["DMX"] and dmx > 0:
        jdata["DMX-FINE"] = dmx_fine

    out = {} 
    if 1: #change:
        data["ATTRIBUT"][attr]["ACTIVE"] = 1
        data["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] = 1
        data["ATTRIBUT"][attr]["VALUE"] = round(v2,4)

        if xfade:
            jdata["FADE"] = xfade

        if xdelay:
            #if attr not in ["PAN","TILT"] and 1:
            jdata["DELAY"] = xdelay

        if not _blind:
            jdata = [jdata]
            MAIN.jclient_send(jdata)
            time.sleep(0.001)

    return jdata




import lib.showlib as showlib

class Fixtures():
    def __init__(self):
        #super().__init__() 
        self.base=showlib.Base()
        #self.load()
        self.fixtures = OrderedDict()
        self.gui = None # GUIHandler()


    def load_patch(self):
        cprint("Fixtures.load_patch ..")
        filename="patch"
        d,l = self.base._load(filename)
        self.fixtures = OrderedDict()
        for i in l:
            sdata = d[i]
            #sdata = self._repair_sdata(sdata)
            sdata = FIXTURE_CHECK_SDATA(i,sdata)

            self.fixtures[str(i)] = sdata
        self._re_sort()
        self.fx_off("all")

    def _re_sort(self):
        keys = list(self.fixtures.keys())
        keys2=[]
        for k in keys:
            #k = "{:0>5}".format(k)
            k = int(k)
            keys2.append(k)
        keys2.sort()
        fixtures2 = OrderedDict()
        for k in keys2:
            k = str(k)
            fixtures2[k] = self.fixtures[k]


        self.fixtures = fixtures2

    def backup_patch(self,save_as="",new=0):
        filename = "patch"
        #self.fx_off("all")
        data  = self.fixtures
        labels = {}
        for k in data:
            labels[k] = k
        if new:
            data = []
            labels = {}
        return self.base._backup(filename,data,labels,save_as)

    def fx_get(self,fix=None):
        out={}
        if not fix or fix == "all":
            #self.data.fx.elem[self.attr]["bg"] = "magenta"
            for fix in self.fixtures:
                data = self.fixtures[fix]
                for attr in data["ATTRIBUT"]:
                    out[str(fix)+"."+str(attr)+".fx"] =  data["ATTRIBUT"][attr]["FX"] 
                    out[str(fix)+"."+str(attr)+".fx"] =  data["ATTRIBUT"][attr]["FX2"]

        return out
    def fx_off(self,fix=None):
        if not fix or fix == "all":
            #self.data.fx.elem[self.attr]["bg"] = "magenta"
            for fix in self.fixtures:
                data = self.fixtures[fix]
                for attr in data["ATTRIBUT"]:
                    data["ATTRIBUT"][attr]["FX"] = ""
                    data["ATTRIBUT"][attr]["FX2"] = OrderedDict()

    def get_max_dmx_nr(self,fix):
        max_dmx = 0
        used_dmx = 0
        if fix not in self.fixtures:
            return (used_dmx,max_dmx)

        data = self.fixtures[fix]
        used_dmx = len(data["ATTRIBUT"])
        for a in data["ATTRIBUT"]:
            attr = data["ATTRIBUT"][a]
            if "NR" in attr:
                try:
                    _n = int(attr["NR"])
                    if _n > max_dmx:
                        max_dmx=_n
                except ValueError:pass
        return (used_dmx,max_dmx)


    def update_raw(self,rdata,update=1):
        #cprint("update_raw",len(rdata))
        cmd = []
        for i,d in enumerate(rdata):
            xcmd = {"DMX":""}
            fix   = d["FIX"]
            attr  = d["ATTR"]
            v2    = d["VALUE"]
            v2_fx = d["FX"]

            if fix not in self.fixtures:
                continue 

            sdata = self.fixtures[fix] #shortcat

            ATTR  = sdata["ATTRIBUT"] 
            if attr not in ATTR:
                continue

            sDMX = get_dmx(self.fixtures,fix,attr)
            #print(sDMX)
            xcmd["DMX"] = str(sDMX)

            cmd.append(xcmd)

            v=ATTR[attr]["VALUE"]
            if v2 is not None and update:
                ATTR[attr]["VALUE"] = v2
            
            if d["FX2"] and update:
                ATTR[attr]["FX2"] = d["FX2"] 

            text = str(attr)+' '+str(round(v,2))
        return cmd






