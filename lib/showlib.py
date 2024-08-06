#!/usr/bin/python3

import os
import time
import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

import json
from collections import OrderedDict

from lib.cprint import *
import lib.fixlib as fixlib

import string

import tkinter
tk = tkinter

HOME      = os.getenv('HOME')
BASE_PATH = HOME+"/LibreLight/"
SHOW_DIR  = BASE_PATH+"/show/"

def _clean_path(fpath):
    _path=[]
    for i in fpath:
        fpath = fpath.replace(" ","_")
        if i in string.ascii_letters+string.digits+"äöüßÖÄÜ_-":
            _path.append(i)
    path = "".join(_path)
    return path



def current_show_name(base_path=""):
    if not base_path:
        base_path = BASE_PATH

    fname = base_path+"/init.txt"
    show_name = "null"
    msg = ""

    if not os.path.isfile( fname ):
        msg = "current_show_path Error: " +fname +"\n NOT FOUND !"
        cprint(msg,color="red")
        return show_name #,msg]

    try:
        f = open(fname,"r")
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.strip()
            #print("  init.txt:",[line])
            if line.startswith("#"):
                continue
            if not line:
                continue

            show_name = line
        show_name = show_name.replace(".","")
        show_name = show_name.replace("\\","")
        show_name = show_name.replace("/","")
    except Exception as e:
        msg="current_show_path \nError:{}".format(e)
        cprint(msg,color="red")

    #return [show_name,msg]
    return show_name

def current_show_path():
    SHOW_PATH = SHOW_DIR + current_show_name()
    while "//" in SHOW_PATH: 
        SHOW_PATH = SHOW_PATH.replace("//","/")
    return SHOW_PATH

def generate_show_path(show_name):
    show_name = _clean_path(show_name)
    SHOW_PATH = SHOW_DIR + show_name
    while "//" in SHOW_PATH: 
        SHOW_PATH = SHOW_PATH.replace("//","/")
    return SHOW_PATH


def build_path(fn):
    fn = _clean_path(fn)
    path = current_show_path().split("/")
    path = "/".join(path[:-2])
    fpath = path+"/show/"+fn
    cprint(fpath,fn,color="red")
    return fpath,fn

def create_new_show_path(fpath):
    if os.path.isdir(fpath):
        cprint("   CREATE DIR FAIL (exist)",[fpath],color="red")
        return 0
    os.mkdir(fpath)
    cprint("   CREATE DIR OK",[fpath],color="green")
    return 1


def _read_sav_file(xfname):
    cprint("load",xfname)
    lines = []
    data   = OrderedDict()
    labels = OrderedDict()

    if not os.path.isfile(xfname):
        return [] #data,labels

    f = open(xfname,"r")
    lines = f.readlines()
    f.close()    

    i=0
    for line in lines:
        r = fixlib._fixture_decode_sav_line(line)
        if r:
            key,label,jdata = r
            fixlib._fixture_repair_nr0(jdata)
            data[key]   = jdata
            labels[key] = label
        
    return data,labels

def list_shows(path=None):
    if not path:
        path = SHOW_DIR

    show_list =  list(os.listdir( path ))
    out = []
    for fname in show_list:
        fpath = path+fname
        if fname == "EASY": #hidde EASY show in list !
            continue
        ctime = os.path.getmtime(fpath)
        ctime = time.strftime("%Y-%m-%d %X",  time.localtime(ctime)) 
        try:
            mtime = os.path.getmtime(fpath+"/patch.sav")
            mtime = time.strftime("%Y-%m-%d %X",  time.localtime(mtime)) 
        except:
            mtime = 0

        if mtime:
            out.append([fname,mtime])#,ctime])

    from operator import itemgetter
    out=sorted(out, key=itemgetter(1))
    out.reverse()
    return out

def set_current_show_name(fname):
    ok= os.path.isdir(SHOW_DIR+"/"+fname)
    ini = BASE_PATH+"init.txt"
    print()
    print()
    cprint("SET SHOW NAME",fname,ok,ini,color="green")
    print()
    try:
        f = open( ini ,"r")
        lines = f.readlines()
        f.close()
        if len(lines) >= 10: # cut show history
            cprint("_set",ini,len(lines))
            lines = lines[-10:]
            f = open( ini ,"w")
            f.writelines(lines)
            f.close()
            exit()

    except:pass
    if ok:
        #self.show_name = fname
        f = open( ini ,"a")
        f.write(fname+"\n")
        f.close()
        return 1

class Base():
    def __init__(self):
        self.show_path = current_show_path() 
        self.show_name = current_show_name() 
        cprint("Base.init()",self.show_path,self.show_name,color="yellow")

        msg = "<msg>"


        if not self.show_name:
            r=tkinter.messagebox.showwarning(message=msg,title="444 Error",parent=None)
            sys.exit()
        
        if not os.path.isdir(self.show_path):
            msg += "Show does not exist\n\n"
            msg += "please check\n"
            msg += "-{} init.txt\n".format(BASE_PATH)
            msg += "-{}".format(self.show_path)
            cprint(msg,color="red")
            r=tkinter.messagebox.showwarning(message=msg,title="Show Error",parent=None)
            exit()

        self._check()

    def _set(self,fname):
        set_current_show_name(fname)

    def _check(self):
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)


    def _load(self,filename):
        xpath = self.show_path+"/"+str(filename)+".sav"
        if not os.path.isfile(xpath):
            msg = ""
            msg += "\n"*2
            msg += "check init.txt"
            msg += "\n"*2
            msg += xpath
            cprint(msg,color="red")
            r=tkinter.messagebox.showwarning(message=msg,title="123 Error",parent=None)
            return
        return _read_sav_file(xpath)


    def _create_path(self,fpath):
        if not create_new_show_path(fpath):
            msg="STOP SHOW EXIST !"
            cprint(msg,color="red")
            r=tkinter.messagebox.showwarning(message=msg,title="333 Error",parent=None)
            return 0
        return fpath

    def _backup(self,filename,data,labels,save_as):
        try:
            fpath = self.show_path
            if save_as:
                fpath = save_as 

            fpath += "/"+str(filename)+".sav"

            f = open(fpath,"w")
            for key in data:
                line = data[key]
                label = "label" 
                if key in labels:
                    label = labels[key]
                if label == "Name-"+str(key):
                    label = ""

                nline = "{}\t{}\t{}\n".format( key,label,json.dumps(line) ) 
                f.write( nline )

            f.close()
            cprint("  Base._backup",[fpath],len(data),"OK",color="green")
        except Exception as e:
            cprint("  Base._backup",[fpath],len(data),"FAIL !",color="red")
            raise e

        return 1

def test():
    print()
    print("-- "*40)
    print("HOME        ",HOME)
    print("BASE_PATH   ",BASE_PATH)
    print("SHOW_DIR    ",SHOW_DIR)
    print()

    print("-- "*20)
    print("TEST  ")
    print("current_show_path",current_show_path())
    print()

    print("-- "*20)
    dl = list_shows()
    for i in dl:
        print(" - ",i)

    print("-- "*20)
    xpath = SHOW_DIR + "/" + dl[0][1] +"/presets.sav" # exec.sav
    print(xpath)
    x= _read_sav_file(xpath)
    print("len.x",len(x))


    base = Base()
    print("::")
    #x=base.build_path("TOST")
    #print(x)

    x=build_path("TEST")
    print(x)

    show_name = "tEsT"
    x= generate_show_path(show_name)
    print("generate_show_path",x)

    #x=base.build_path(show_name)
    #print("build_path",[show_name,x])


if __name__ == "__main__":
    test()




