#!/usr/bin/python3

import os
import time
import json
from collections import OrderedDict

from lib.cprint import *
import lib.fixlib as fixlib

import string

import tkinter
tk = tkinter


HOME = os.getenv('HOME')

def _clean_path(fpath):
    _path=[]
    for i in fpath:
        fpath = fpath.replace(" ","_")
        if i in string.ascii_letters+string.digits+"äöüßÖÄÜ_-":
            _path.append(i)
    path = "".join(_path)
    return path

def _read_init_txt(show_path):
    fname = show_path+"init.txt"
    show_name = None
    msg = ""

    if not os.path.isfile( fname ):
        msg = "_read_init_txt Errror: " +fname +"\n NOT FOUND !"
        return [None,msg]

    try:
        f = open(fname,"r")
        for line in f.readlines():
            line = line.strip()
            print("  init.txt:",[line])
            if line.startswith("#"):
                continue
            if not line:
                continue

            show_name = line
            show_name = show_name.replace(".","")
            show_name = show_name.replace("\\","")
            show_name = show_name.replace("/","")
    except Exception as e:
        cprint("show name exception",color="red")
        msg="read_init_txt Error:{}".format(e)
    finally:
        f.close()

    return [show_name,msg]

def _read_sav_file(xfname):
    cprint("load",xfname)
    lines = []
    if not os.path.isfile(xfname):
        return []

    f = open(xfname,"r")
    lines = f.readlines()
    f.close()    

    data   = OrderedDict()
    labels = OrderedDict()
    i=0
    for line in lines:
        r = fixlib._fixture_decode_sav_line(line)
        if r:
            key,label,jdata = r
            fixlib._fixture_repair_nr0(jdata)
            data[key]   = jdata
            labels[key] = label
        
    return data,labels


def _listdir(show_path):
    #self._check()
    show_list =  list(os.listdir( show_path ))
    out = []
    for fname in show_list:
        if fname == "EASY": #hidde EASY show in list !
            continue
        #print(fname)
        ctime = os.path.getmtime(show_path+fname)
        ctime = time.strftime("%Y-%m-%d %X",  time.localtime(ctime)) #1650748726.6604707))
        try:
            mtime = os.path.getmtime(show_path+fname+"/patch.sav")
            mtime = time.strftime("%Y-%m-%d %X",  time.localtime(mtime)) #1650748726.6604707))
        except:
            mtime = 0

        if mtime:
            out.append([fname,mtime])#,ctime])

    from operator import itemgetter
    out=sorted(out, key=itemgetter(1))
    out.reverse()
    return out


class Base():
    def __init__(self):
        cprint("Base.init()",color="red")
        self._init()

    def _init(self):
        show_name = "" #DemoShow #"ErrorRead-init.txt"
        self.show_path0 = HOME +"/LibreLight/"
        self.show_path  = self.show_path0 
        self.show_path1 = self.show_path0 + "show/"
        
        msg = " X "
        self.show_name,msg = _read_init_txt(self.show_path)
        if not self.show_name:
            #r=tkinter.messagebox.showwarning(message=msg,parent=None)
            r=tkinter.messagebox.showwarning(message=msg,title="Error",parent=None)
            sys.exit()
        
        fpath = self.show_path1 +show_name 
        if not os.path.isdir(fpath):
            cprint(fpath)
            cprint( os.path.isdir(fpath))

            msg="'{}'\n Show Does Not Exist\n\n".format(show_name)
            msg += "please check\n"
            msg += "-{}init.txt\n".format(self.show_path0)
            msg += "-{}".format(self.show_path1)

            #showwarning(msg=msg,title="Show Error")
            r=tkinter.messagebox.showwarning(message=msg,title="Show Error",parent=None)
            exit()

        self._check()
    def _set(self,fname):
        ok= os.path.isdir(self.show_path1+"/"+fname)
        ini = self.show_path0+"init.txt"
        cprint("SET SHOW NAME",fname,ok,ini)
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
        
    def _check(self):
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/show/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        self.show_path += "/" +self.show_name +"/"
        if not os.path.isdir(self.show_path):
            os.mkdir(self.show_path)
        pass
    def _list(self):
        cprint("BASE._list()")
        out = _listdir(self.show_path1)
        return out

    def _load(self,filename):
        xpath = self.show_path+"/"+str(filename)+".sav"
        if not os.path.isfile(xpath):
            msg = ""#"Exception: {}".format(e)
            msg += "\n\ncheck\n-init.txt"
            cprint(msg,color="red")
            #showwarning(msg=msg,title="load Error")
            r=tkinter.messagebox.showwarning(message=msg,title="Error",parent=None)
            return
        return _read_sav_file(xpath)



    def build_path(self,save_as):
        save_as = _clean_path(save_as)
        path = self.show_path.split("/")
        path = "/".join(path[:-2])
        fpath = path+"/"+save_as
        return fpath,save_as

    def _create_path(self,fpath):
        if os.path.isdir(fpath):
            msg="STOP SHOW EXIST !"
            cprint(msg,color="red")
            #showwarning(msg=msg,title="Error")
            r=tkinter.messagebox.showwarning(message=msg,title="Error",parent=None)
            #r=tkinter.messagebox.showwarning(message=msg,parent=None)
            return 0
        else:
            cprint("CREATE DIR ",fpath,color="green")
            os.mkdir(fpath)
        #self._set(save_as)
        return fpath

    def _backup(self,filename,data,labels,save_as):

        if save_as:
            xfname = save_as +"/"+str(filename)+".sav"
        else:
            xfname = self.show_path+"/"+str(filename)+".sav"

        cprint("backup",xfname)
        f = open(xfname,"w")
        for key in data:
            line = data[key]
            #print(line)
            label = "label" 
            if key in labels:
                label = labels[key]
            if label == "Name-"+str(key):
                label = ""
            #print(xfname,"load",key,label,len(line))

            f.write( "{}\t{}\t{}\n".format( key,label,json.dumps(line) ) )
        f.close()

        return 1

