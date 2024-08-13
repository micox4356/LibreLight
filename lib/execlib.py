#/usr/bin/python3

import copy
import __main__ as MAIN
from lib.cprint import cprint
from collections import OrderedDict
import json
try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None

def reshape_exec(data ,value=None,xfade=0,flash=0,ptfade=0,DELAY=None):

    f=0 #fade

    out = []
    delay=0
    for row in data:
        #cprint("reshape_exec in:",row)
        line = {}
        line["DELAY"]=delay
        if type(value) is float:
            line["VALUE"] = value #round(value,3)
        else:
            line["VALUE"] = value

        if "FX" not in row:
            cprint("698 FX not in row...",row,color="red")
            row["FX"] = ""
        else:
            if type(row["FX"]) is not str:
                cprint("702 FX is not str...",row,color="red")
                row["FX"] = ""

        if value is not None:
            line["FX"] = row["FX"].split(":",1)[-1]
        else:
            line["FX"] = row["FX"]

        if row["FX2"]:
            line["FX2"] = row["FX2"]

        if row["FIX"]:
            line["FIX"] = row["FIX"]
        if row["ATTR"]:
            line["ATTR"] = row["ATTR"]


        if row["VALUE"] is not None:
            if value is None: 
                v=row["VALUE"]
                if type(v) is float:
                    line["VALUE"]  = v #round(v,3)
                else:
                    line["VALUE"]  = v

        if row["ATTR"] in ["PAN","TILT"]:
            f = ptfade 

        for a in ["DIM","ZOOM","FOCUS","RED","GREEN","BLUE","WHITE","AMBER","IRIS","BLADE"]: 
            #FADE ATTRIBUTES
            if a in row["ATTR"]:
                f = xfade 
                break

        if flash:
            xfade = 0
        if type( f ) is float:
            line["FADE"] = round(f,4)
        else:
            line["FADE"] = f
        
        if 0:
            cprint("reshape_exec j",line,color="red") 
        #cprint("reshape_exec out:",line)
        out.append(line)

        if DELAY:
            if DELAY._is():
                delay+=DELAY.val()/100 #0.02
    return out


import lib.showlib as showlib



def EXEC_CFG_CHECKER(sdata):
    "repair CFG  "
    ok = 0
    if "CFG" not in sdata:
        sdata["CFG"] = OrderedDict()
        ok += 1
    if "FADE" not in sdata["CFG"]:
        sdata["CFG"]["FADE"] = 4
        ok += 1
    if "DELAY" not in sdata["CFG"]:
        sdata["CFG"]["DELAY"] = 0
        ok += 1
    if "BUTTON" not in sdata["CFG"]:
        sdata["CFG"]["BUTTON"] = "GO"
        ok += 1
    if "HTP-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["HTP-MASTER"] = 100 #%
        ok += 1
    if "SIZE-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["SIZE-MASTER"] = 100 #%
        ok += 1
    if "SPEED-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["SPEED-MASTER"] = 100 #%
        ok += 1
    if "OFFSET-MASTER" not in sdata["CFG"]:
        sdata["CFG"]["OFFSET-MASTER"] = 100 #%
        ok += 1
    if "HAVE-FX" not in sdata["CFG"]:
        sdata["CFG"]["HAVE-FX"] = 0  # yes/no
        ok += 1
    if "HAVE-VAL" not in sdata["CFG"]:
        sdata["CFG"]["HAVE-VAL"] = 0  # yes/no
        ok += 1
    if "FIX-COUNT" not in sdata["CFG"]:
        sdata["CFG"]["FIX-COUNT"] = 0  # yes/no
        ok += 1

    #try:del sdata["CFG"]["SPEED-MASTER"] #= 100 #%
    #except:pass

    return ok

import time
def exec_set_mc(excec_labels,exec_data):
    l = excec_labels
    d = exec_data
    
    if mc:
        index=[]
        for i,v in enumerate(l):
            key="EXEC-"+str(i) 
            mc.set(key,json.dumps(d[v]))
            index.append(key)

            key2="EXEC-META-"+str(i) 
            cfg = {'FADE': 3.0, 'DEALY': 0, 'DELAY': 4.0, 'BUTTON': 'ON', 'HTP-MASTER': 100
                    , 'SIZE-MASTER': 100, 'SPEED-MASTER': 100, 'OFFSET-MASTER': 100, 'OUT-FADE': 10.0}
            if "CFG" in d[v]:
                cfg = d[v]["CFG"]
            mc.set(key2,json.dumps({"LABEL":l[i],"LEN":len(d[v])-1,"CFG":cfg}) )
        mc.set("EXEC-INDEX",json.dumps(index))
        print("---------------------------------------")
        #,start - time.time())
        #

class EXEC(): #Presets():
    def __init__(self):
        self.base = showlib.Base()
        self._last_copy = None
        self._last_move = None
        self.fx_buffer = {}

    def load_exec(self): 
        filename="exec"
        filename="presets" # preset.sav
        d,l = self.base._load(filename)
        for i in d:
            sdata = d[i]
            ok = EXEC_CFG_CHECKER(sdata)
        start = time.time()


        self.val_exec = d
        self.label_exec = l

        exec_set_mc(self.label_exec,self.val_exec)

    def check_cfg(self,nr=None):
        cprint("EXEC.check_cfg()",nr)#,color="red")
        ok = 0
        if nr is not None:
            if nr in self.val_exec:
                sdata = self.val_exec[nr]
                ok += self._check_cfg(sdata)
            else:
                cprint("nr not in data ",nr,color="red")
        else:
            for nr in self.val_exec:
                sdata = self.val_exec[nr]
                ok += self._check_cfg(sdata)
        return ok

    def _check_cfg(self,sdata):
        cprint("EXEC._check_cfg()")#,color="red")

        ok = EXEC_CFG_CHECKER(sdata)

        if ok:
            cprint("REPAIR CFG's",ok,sdata["CFG"],color="red")
        return ok
        
    def backup_exec(self,save_as="",new=0):
        filename = "exec" # new
        filename = "presets" # preset.sav
        data   = self.val_exec
        labels = self.label_exec
        if new:
            data  = [] #*512
            labls = [""]*512
        r=self.base._backup(filename,data,labels,save_as)
        return r
        

    def get_cfg(self,nr):
        cprint("EXEC.get_cfg()",nr)
        self.check_cfg(nr)
        if nr not in self.val_exec:
            cprint("get_cfg",self,"error get_cfg no nr:",nr,color="red")
            return {}
        if "CFG" in self.val_exec[nr]:
            return self.val_exec[nr]["CFG"]

    def clean(self,nr):
        
        if nr not in self.val_exec:
            self.val_exec[nr] = OrderedDict()
            #self.val_exec[nr]["VALUE"] = 0
            #self.val_exec[nr]["FX"] = ""


        sdata = self.val_exec[nr]
        for fix in sdata:
            #print("exec.clear()",nr,fix,sdata[fix])
            for attr in sdata[fix]:
                row = sdata[fix][attr]
                if fix == "CFG":
                    continue

                if "VALUE" not in row:
                    row["VALUE"] = None
                if "FX" not in row:
                    row["FX"] = "" 
                if "FX2" not in row:
                    row["FX2"] = OrderedDict()
                elif row["FX2"]:
                    for k in ["SIZE","SPEED","START","OFFSET"]:
                        row["FX2"][k] = int( row["FX2"][k] )
                    row["FX"] = "" 


                if "FX" in row and row["FX"] and not row["FX2"]: # rebuild old FX to Dict-FX2
                    #"off:0:0:0:16909:-:"
                    x = row["FX"].split(":")
                    cprint("-fx",x,len(x))
                    #'FX2': {'TYPE': 'sinus', 'SIZE': 200, 'SPEED': 30, 'START': 0, 'OFFSET': 2805, 'BASE': '-'}}
                    if len(x) >= 6:
                        row["FX2"]["TYPE"] = x[0] 
                        row["FX2"]["SIZE"] =  int(x[1])
                        row["FX2"]["SPEED"] = int(x[2]) 
                        row["FX2"]["START"] = int(x[3]) 
                        row["FX2"]["OFFSET"] = int(x[4]) 
                        row["FX2"]["BASE"] = x[5] 
                    row["FXOLD"] = row["FX"]
                    row["FX"] = ""
                #cprint("exec.clear()",nr,fix,row)

            
    def get_raw_map(self,nr):
        self.clean(nr)

        cprint("get_raw_map",nr)
        sdata = self.val_exec[nr]
        cmd = ""
        out = []
        dmx=-1
        for fix in sdata:
            if fix == "CFG":
                #print("CFG",nr,sdata[fix])
                continue

            for attr in sdata[fix]:
                x = {}
                #print("RAW",attr)
                x["FIX"]   = fix
                x["ATTR"]  = attr

                x["VALUE"] = sdata[fix][attr]["VALUE"]
                x["FX"]    = sdata[fix][attr]["FX"]
                x["FX2"]    = sdata[fix][attr]["FX2"]
                #x["DMX"]  = sdata[fix][attr]["NR"] 

                out.append(x)
        return out

    def get_btn_txt(self,nr):
        sdata=self.val_exec[nr]
        BTN="go"
        if "CFG" in sdata:
            if "BUTTON" in sdata["CFG"]:
                BTN = sdata["CFG"]["BUTTON"]
        _label = self.label_exec[nr] # = label
        #txt=str(nr+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+_label
        #txt=str(nr+1)+" "+str(BTN)+" "+str(len(sdata)-1)+"\n"+_label
        txt="{} {} {}\n{}".format(nr+1,BTN,len(sdata)-1,_label)
        cprint("get_btn_txt",nr,[txt])
        return txt

    def _btn_cfg(self,nr,txt=None):
        if nr not in self.val_exec:
            return ""
        if "CFG" not in self.val_exec[nr]:
            self.val_exec[nr]["CFG"] = OrderedDict()
        return self.val_exec[nr]["CFG"]

    def btn_cfg(self,nr,txt=None):
        if nr not in self.val_exec:
            return ""
        if "CFG" not in self.val_exec[nr]:
            self.val_exec[nr]["CFG"] = OrderedDict()
        if "BUTTON" not in self.val_exec[nr]["CFG"]:
            self.val_exec[nr]["CFG"]["BUTTON"] = ""

        if type(txt) is str:
            self.val_exec[nr]["CFG"]["BUTTON"] = txt
        if self.val_exec[nr]["CFG"]["BUTTON"] is None:
            self.val_exec[nr]["CFG"]["BUTTON"] = ""

        MAIN.master._refresh_exec(nr=nr)
        cprint("EEE", self.val_exec[nr]["CFG"]["BUTTON"] )
        return self.val_exec[nr]["CFG"]["BUTTON"] 

    def label(self,nr,txt=None):
        if nr not in self.label_exec:
            return ""
        if type(txt) is str:
            self.label_exec[nr] = txt
            cprint("set label",nr,[txt])
        cprint("??? ?? set label",nr,[txt])
        return self.label_exec[nr] 

    def clear_move(self):
        cprint("EXEC.clear_move()",end=" ")
        self.clear_copy()
        
    def clear_copy(self):
        cprint("EXEC.clear_copy()",end=" ")
        if self._last_copy is not None:
            cprint("=OK=",color="red")
            self._last_copy = None
        else:
            cprint("=NONE=",color="green")

    def copy(self,nr,overwrite=1):
        cprint("EXEC._copy",nr,"last",self._last_copy)
        if nr >= 0:
            if self._last_copy is not None:
                if MAIN.modes.val("COPY"):
                    MAIN.modes.val("COPY",3)
                ok = self._copy(self._last_copy,nr,overwrite=overwrite)
                return ok #ok
            else:
                if MAIN.modes.val("COPY"):
                    MAIN.modes.val("COPY",2)
                self._last_copy = nr
                cprint("EXEC.copy START ",color="red")
                return 0
        return 1 # on error reset move
    def _copy(self,nr_from,nr_to,overwrite=1):
        cprint("EXEC._copy",nr_from,"to",nr_to)
        self.check_cfg(nr_from)
        if type(self._last_copy) is None:
            cprint("EXEC._copy last nr is None",color="red")
            return 0
        cprint("------ EXEC._copy", nr_from in self.val_exec , nr_to in self.val_exec)
        if nr_from in self.val_exec and nr_to in self.val_exec:
            fdata = self.val_exec[nr_from]
            tdata = self.val_exec[nr_to]
            #cprint(fdata)
            flabel = self.label_exec[nr_from]
            tlabel = self.label_exec[nr_to]
            self.val_exec[nr_to] = copy.deepcopy(fdata)
            self.label_exec[nr_to] = flabel
            if not overwrite: #default
                cprint("overwrite",overwrite)
                self.val_exec[nr_from] = copy.deepcopy(tdata)
                self.label_exec[nr_from] = tlabel
            #self.label_exec[nr_from] = "MOVE"
            self.clear_copy()
            cprint("EXEC.copy OK",color="green")
            return 1

    def move(self,nr):
        cprint("EXEC.move",self._last_copy,"to",nr)
        if nr >= 0: 
            last = self._last_copy

            if MAIN.modes.val("MOVE"):
                MAIN.modes.val("MOVE",2)
            ok= self.copy(nr,overwrite=0)
            if ok and last >= 0:
                if MAIN.modes.val("MOVE"):
                    MAIN.modes.val("MOVE",3)
                cprint("EXEC.move OK",color="red")
                #self.delete(last)
                return ok,nr,last #ok
            
        return 0,nr,last # on error reset move
    def delete(self,nr):
        cprint("EXEC.delete",nr)
        ok=0
        if nr in self.val_exec:
            self.val_exec[nr] = OrderedDict()
            self.label_exec[nr] = "-"
            ok = 1
        self.check_cfg(nr)
        return ok

    def rec(self,nr,data,arg=""):
        cprint("rec",self,"rec()",len(data),arg)
        self.check_cfg(nr)
        self._check_cfg(data) #by ref

        odata=self.val_exec[nr]
        #print("odata",odata)
        if "CFG" in odata:
            if "BUTTON" in odata["CFG"]:
                data["CFG"]["BUTTON"] = odata["CFG"]["BUTTON"]  
        self.val_exec[nr] = data
        return 1
           
