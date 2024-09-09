#/usr/bin/python3

import copy

from collections import OrderedDict

import tkinter 
tk = tkinter 

from idlelib.tooltip import Hovertip

import tkgui.dialog  as dialoglib
dialog = dialoglib.Dialog()

import __main__ as MAIN

from lib.cprint import *


import lib.fixlib  as fixlib
import lib.showlib as showlib
import lib.libtk   as libtk



class BaseCallback():
    def __init__(self,cb=None,args={}):
        self._cb=cb
        self.args = args

    def cb(self,**args):
        print("BaseCallback.cb()")
        print("  ",self.args)
        print("  ",self._cb)
        if self._cb:
            if self.args:
                self._cb(args=self.args) 
            else:
                self._cb() 


def GUI_LOAD_FIXTURE_LIST(frame,data={"EMPTY":"None"},cb=None,bg="black"):
    #print("__func__",__func__)
    print("#",sys._getframe().f_code.co_name)
    blist = data
    blist = blist[:100]

    frame.configure(bg=bg)

    # table header
    c=0
    for r,row in enumerate(blist):
        bg="lightgrey"
        dbg="grey"
        dbg="lightgrey"
        c+=1
        b = tk.Label(frame,bg="grey",text=str("Nr."))
        b.grid(row=r, column=c, sticky=tk.W) #+tk.E)
        c+=1
        for k,v in row.items():
            b = tk.Label(frame,bg="grey",text=k)
            b.grid(row=r, column=c, sticky=tk.W) #+tk.E)
            c+=1
        break
    
    if not cb:
        cb = DummyCallback()

    # table data
    for r,row in enumerate(blist):
        c=1

        bg="lightgrey"
        #dbg="grey"
        b = tk.Button(frame,text=r+1,anchor="w",bg=dbg,width=6,height=1,relief="sunken")
        b.grid(row=r+1, column=c, sticky=tk.W ) #+tk.E)
        c+=1
        bg="lightgrey"
        dbg="lightgrey"
        for k,v in row.items():
            #if v > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*4)):
            #    dbg = "lightgreen"
            #elif v > time.strftime("%Y-%m-%d %X",  time.localtime(time.time()-3600*24*7)):
            #    dbg = "green"
            if "." in v:
                #v = v.split(".",-1)
                v = v[::1].split(".",1)[0]#[::-1]

            if c == 3:
                bg="grey"
                dbg="grey"
                _cb2 = BaseCallback(cb=cb,args={"key":k,"val":v,"data":row}).cb
                b = tk.Button(frame,text=v,anchor="w",height=1,bg=bg,command=_cb2)
            else: 
                b = tk.Button(frame,text=v,anchor="w",bg=dbg,relief="flat",height=1)
                b.config(activebackground=dbg)
            b.grid(row=r+1, column=c, sticky=tk.W+tk.E)
            c+=1
            bg="lightgrey"
            dbg="lightgrey"




class GUI_FixtureEditor():
    def __init__(self,root,frame,data,title="tilte",width=800):
        #xfont = tk.font.Font(family="FreeSans", size=5, weight="bold")
        self.font8 = ("FreeSans",8)
        self.dmx=1
        self.univ=0
        self.elem=[]
        self.fader_elem = []
        self.pw = None
        self.header=[]
        self.data = data
        self.fixture = []
        self.title = title
        self.width = width
        #cprint("GUI:",root,title)
        self.root = root
        self.frame = frame
        self.draw()
    def draw(self):
        root = self.frame

        title = self.title
        width = self.width
        data = self.data

        self.fader_elem = []

        #Head 1
        self.frame = tk.Frame(root,bg="grey",width=width)
        self.frame.pack(fill="both", side=tk.TOP)
        self.frame = tk.Frame(self.frame,bg="grey",width=width)
        self.frame.pack(fill="both", side=tk.RIGHT)#EFT)

        bg = "lightblue"
        self.b = tk.Button(self.frame,bg=bg,text="IMPORT FROM SHOW", width=20)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_import
        self.b.pack( side=tk.LEFT)

        self.b = tk.Button(self.frame,bg=bg,text="USER", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_user
        self.b.pack( side=tk.LEFT)

        self.b = tk.Button(self.frame,bg=bg,text="GLOBAL", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.open_fixture_list_global
        self.b.pack( side=tk.LEFT)


        self.b = tk.Label(self.frame,bg=bg ,text="")
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg=bg,text="SAVE", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.save_fixture
        #self.b.pack( side=tk.LEFT)
        

        #self.b = tk.Button(self.frame,bg=bg,text="SAVE AS", width=5)#,command=self.event) #bv.change_dmx)
        #self.b["command"] = self.save_as_fixture
        #self.b.pack( side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="black",text="") # spacer
        self.b.pack(fill=tk.Y, side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="grey",text="HELP", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = libtk.online_help("librelight:80-fixture-editor" ) #""fixture-editor")
        self.b.pack( side=tk.LEFT)

        self.b = tk.Button(self.frame,bg="grey",text="VDIM", width=5)#,command=self.event) #bv.change_dmx)
        self.b["command"] = libtk.online_help("librelight:05-virtueller-attribute" ) #""fixture-editor")
        self.b.pack( side=tk.LEFT)
        # HEAD 2
        



        r=0
        c=0
        self.frame = tk.Frame(root,bg="grey",width=width)
        self.frame.pack(fill="both", side=tk.TOP)

        #c+=1 ;r=0
        self.b = tk.Label(self.frame,bg="#ddd",text="FIX-ID:")
        self.b.grid(row=r,column=c) #,expand=1)

        r+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="3001", width=4)
        self.fixid=self.b
        self.b["command"] = self.set_fixid
        self.b.grid(row=r,column=c)

        c+=1 ;r=0
        self.b = tk.Label(self.frame,bg="#ddd",text="NAME:")
        self.b.grid(row=r,column=c) #,expand=1)

        r+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="FixName", width=13)
        self.name=self.b
        self.b["command"] = self.set_name
        self.b.grid(row=r,column=c)

        c+=1 ;r=0
        self.b = tk.Label(self.frame,bg="lightblue",text="UNIV:")
        self.b.grid(row=r,column=c)
        r+=1
        self.b_univ = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        self.entry_univ=self.b_univ
        self.b_univ["command"] = self.event_univ
        self.b_univ.grid(row=r,column=c)

        c+=1 ;r=0
        self.b = tk.Label(self.frame,bg="lightblue",text="DMX:")
        self.b.grid(row=r,column=c)

        r+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="1", width=4)#,command=self.event) #bv.change_dmx)
        self.entry_dmx=self.b
        self.b["command"] = self.event_dmx
        self.b.grid(row=r,column=c)

        c+=1 ;r=0
        self.b = tk.Label(self.frame,bg="lightblue",text="QTY:")
        self.b.grid(row=r,column=c)

        r+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="4", width=4)#,command=self.event) #bv.change_dmx)
        #self.entry_qty=self.b
        self.qty=self.b
        self.b["command"] = self.set_qty
        #self.b["command"] = self.event_dmx
        self.b.grid(row=r,column=c)

        c+=1 ;r=0
        r+=1
        self.b = tk.Button(self.frame,bg="lightblue",text="PATCH", width=6)#,command=self.event) #bv.change_dmx)
        self.b["command"] = self.do_patch
        self.b.grid(row=r,column=c)


        # HEAD 1
        
        #root = tk.Frame(root,bg="black",width=width)
        #root.pack(fill=tk.BOTH, side=tk.TOP)

        self.frame = tk.Frame(root,bg="grey",width=width)
        self.frame.pack(fill="x", side=tk.TOP)

        self.b = tk.Label(self.frame,bg="#fff",text="Fixture Editor") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#aaa",text="FILE:") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b_path = tk.Label(self.frame,bg="#fff",text="~/LibreLight/fixtures/lalla.json") #,font=self.font8 )
        self.b_path.pack(fill=None, side=tk.LEFT)

        self.b = tk.Label(self.frame,bg="#aaa",text="----") #,font=self.font8 )
        self.b.pack(fill=None, side=tk.LEFT)

        self.b_info = tk.Label(self.frame,bg="#fff",text="") #,font=self.font8 )
        self.b_info.pack(fill=None, side=tk.LEFT)
        # DATA
        self.frame = libtk.ScrollFrame(root,bg="#003",width=2000 ,height=1000,bd=2) # fader frame


        self.r=0
        self.c=0
        self.pb=10
        self.j = 0

        for page_nr in range(10):
            self.draw_bank(page_nr)

        self._event_redraw()

    def draw_bank(self,page_nr):
        title = self.title
        width = self.width

        idx = self.pb*page_nr
        data = self.data[idx:idx+self.pb]

        c = idx
        for j,row in enumerate(data):
            if c % self.pb == 0 or c==0:
                h=hex(j*10)[2:].rjust(2,"0")
                frameS = tk.Frame(self.frame,bg="#000",width=width,border=2)
                frameS.pack(fill=tk.BOTH, side=tk.TOP)
                bank_nr=j//self.pb+1
                txt="BANK:{} {}-{}".format(bank_nr,bank_nr*self.pb-self.pb+1,bank_nr*self.pb) 
                self.b = tk.Label(frameS,bg="lightblue",text=txt,width=15,font=self.font8 )
                self.header.append(self.b)

                self.b.pack(fill=None, side=tk.LEFT)
                self.b = tk.Label(frameS,bg="black",text="" ,width=11,font=self.font8 )
                self.b.pack(fill=tk.BOTH, side=tk.LEFT)

                try:
                    frameS = tk.Frame(self.frame,bg="#a000{}".format(h),width=width,border=2)
                except:
                    frameS = tk.Frame(self.frame,bg="#a0aadd",width=width,border=2)
                self.c=0

            e= libtk.ELEM_FADER(frameS,nr=j+1,cb=self._cb,fader_cb=self._fader_cb,width=14)
            e.pack()
            #e.attr["bg"] = "red"
            self.fader_elem.append(e)
            self.elem.append(e)
            frameS.pack(fill=tk.X, side=tk.TOP)
            c+=1

    def _fader_cb(self,arg,name="<name>",**args):
        print("   FixtureEditor._cb",args,arg,name)
        #print("    ",name,"_cb.args >>",args,arg[1:])
        self.count_ch()
    
        try:
            a1 = arg #arg[2]
            nr = args["nr"] #.nr
            j=[]
            e = self.fader_elem[args["nr"]-1]
            nr = int(e.elem_nr["text"]) 
            if not nr:
                nr = args["nr"]
                return
            nr_start = ( int(self.entry_dmx["text"])-1 + int(self.entry_univ["text"])*512 )
            nr += nr_start

            jdata = {'VALUE': int(a1), 'args': [] , 'FADE': 0,'DMX': str(nr)}
            print("   ",jdata)
            j.append(jdata)
            MAIN.jclient_send(j)
        except Exception as e:
            print("exec",arg,args,nr)
            print(e)
            raise e

    def _cb(self,arg,name="<name>",**args):
        #print(" FixtureEditor._cb")
        #print(" ",name,"_cb.args >>",args,arg[1:])
        self.count_ch()
        elm,mode,name = arg    
        #print("_cb",arg)
        if mode == "set_attr":
            #print(" ->")
            if name.endswith(" FINE"):
                name = name.replace(" FINE","-FINE")
                elm.label["text"] = name
    

    def count_ch(self):
        #print("FixtureEditor.count_ch:")
        #e._set_attr( "---")
        ch_s = []
        j=-1
        self.b_info["text"] = "xx"

        for i,elem in enumerate(self.elem):
            #print(dir(elem))
            txt = elem.attr["text"]
            if txt:
                #print("count_ch:",i,txt)
                if txt.startswith("EMPTY"):
                    elem.attr["bg"] = "#fa0"
                    elem.attr["activebackground"] = "#ff0"
                elif txt.endswith("-FINE"):
                    elem.attr["bg"] = "#0b0"
                    elem.attr["activebackground"] = "#ff0"
                else:
                    elem.attr["bg"] = "#0f0"
                    elem.attr["activebackground"] = "#ff0"
                ch_s.append([i,txt])
                j=i
            else:
                elem.attr["bg"] = "lightgrey"
                elem.attr["activebackground"] = "white"
        self.b_info["text"] = "CH's: {} USED: {}".format(j+1,len(ch_s))

    def set_qty(self,_event=None):
        txt = self.qty["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"._cb()",txt)
            self.qty["text"] = "{}".format(txt)
            print("set_qty",[_event,self])
        dialog._cb = _cb
        dialog.askstring("QTY:","QTY:",initialvalue=txt)

    def do_patch(self,_event=None):
        qty = int(self.qty["text"])
        ID = int(self.fixid["text"])
        univ = self.univ #int(self.univ["text"])
        dmx = self.dmx #int(self.dmx["text"])
        name = self.name["text"]
        name_nr = ""
        if "-" in name:
            try:
                name_nr = name.split("-")[-1]
                name_nr = int(name_nr)
                name = name.split("-")[:-1]
                name = "-".join(name)
            except:
                name_nr = ""
        
        if name_nr == '':
            if ID:
                name_nr = ID
            else:
                name_nr = 9000
        name_nr=int(name_nr)
        print("do_patch",dmx,univ,qty)
        DMX = dmx #univ*512 + dmx 
        fixture = {"DMX": DMX, "UNIVERS": univ, "NAME": "D1", "TYPE": "", "VENDOR": "", "ATTRIBUT": {} , "ACTIVE": 0}
        ATTR = []
        max_nr = 0
        for fader in self.fader_elem:
            #print("patch -",fader)
            attr = fader.attr["text"]
            nr = fader.elem_nr["text"]
            if nr == '':
                continue
            if nr == "off":
                nr = -1
            nr = int(nr)
            mode = fader.mode["text"]
            val = float(fader.elem_fader.get())
            if not attr:
                continue
            if attr.startswith("EMPTY"):
                continue
            ATTR = OrderedDict()
            ATTR["NR"] = nr
            ATTR["MASTER"] = "0"
            ATTR["MODE"] = mode
            ATTR["VALUE"] = val
            ATTR["ACTIVE"] = 0
            ATTR["FX"] = ""
            ATTR["FX2"] =  {}
            print("patch --",nr,mode,attr)

            fixture["ATTRIBUT"][attr] = ATTR
            if nr > max_nr:
                max_nr = nr

        ok = 1
        out=[]
        err = []
        msg=""
        err2 = []
        sucess = []
        _fixture = fixture 
        _dmx = _fixture["DMX"] 
        for i in range(qty):
            fixture = copy.deepcopy(_fixture)
            fixture["DMX"] = _dmx 
            print("i",i)
            fixture["NAME"] = name + "-{:0>4}".format(name_nr)
            fixture["ID"] = ID 
            print(fixture)
            fixture = fixlib.FIXTURE_CHECK_SDATA(ID,fixture)
            #out.append(sdata)
            out.append(fixture)
            #fixture = copy.deepcopy(fixture)
            if str(ID) in MAIN.FIXTURES.fixtures:
                ok = 0
                #err.append(" ID '{}' is in use ! ".format(ID))
                err.append("FIX-ID '{}' ".format(ID))

            if ATTR:
                sucess.append("ID '{}' DMX:{} UNIV:{}".format(ID,fixture["DMX"],fixture["UNIVERS"]))
            else:
                ok = 0
                err2.append(" NO 'attributes'  ID:'{}' ! ".format(ID))

            name_nr += 1
            ID += 1
            _dmx += max_nr # bug offset of one fixture
        print("OK:",ok)
        print()
        if err:
            #msg+="Name:'"+name+"'\n"
            msg+="FIX-ID is in use !\n"
            msg+="\n"
            msg+="\n".join(err)
            msg+="\n"
            msg+="\n"
            msg+="OVERWRITE ?\n"
            msg+="überschreiben ?\n"
            #msg+="\n "
            r=tkinter.messagebox.askyesno(message=msg,title="cancel/Abbruch",parent=None)
            print("err",r)
            if r: # if yes
                pass
            else:
                return

        if err2:
            r=tkinter.messagebox.showwarning(message="PATCH ERROR 2'"+name+"'\n\n"+"\n".join(err2)+"\n\n ",title="Error",parent=None)
            return

        if sucess:
            msg+="name:'"+name+"'\n\n"
            msg="PATCH OK ?\n"
            msg+="\n".join(sucess)
            msg+="\n"
            r=tkinter.messagebox.askyesno(message=msg,title="Execute/Ausführen",parent=None)
            print("yes no" ,r )
            if r:
                for fix in out:
                    print(";;",fix)
                    k = str(fix["ID"])
                    v = fix
                    MAIN.FIXTURES.fixtures[k] = v

                MAIN.FIXTURES._re_sort()


    def set_fixid(self,_event=None):
        txt = self.fixid["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"._cb()",txt)
            self.fixid["text"] = "{}".format(txt)
            print("set_fixid",[_event,self])
        dialog._cb = _cb
        dialog.askstring("FIXTURE ID:","ID:",initialvalue=txt)

    def set_name(self,_event=None):
        txt = self.name["text"]
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"._cb()",txt)
            self.name["text"] = "{}".format(txt)
            print("change_dmx",[_event,self])

        dialog._cb = _cb
        dialog.askstring("FIXTURE NAME:","NAME:",initialvalue=txt)


    def save_as_fixture(self,event=None):
        print("save_as_fix",self,event)
        self.count_ch()

    def save_fixture(self,event=None):
        print("save_fix",self,event)
        self.count_ch()


    def open_fixture_list_global(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="GLOBAL")
    def open_fixture_list_import(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="IMPORT")
    def open_fixture_list_user(self):
        self.close_fixture_list()
        self._open_fixture_list(mode="USER")
        
    def _open_fixture_list(self,mode=""):
        name = "FIXTURE-{}".format(mode)
        line1="Fixture Library"
        line2="CHOOS to EDIT >> DEMO MODUS"
        line3="CHOOS to EDIT >> DEMO MODUS"

        cb = None #LOAD_FIXTURE(self,"USER").cb 
        self.pw = libtk.PopupList(name,width=600,cb=cb,left=libtk._POS_LEFT+620,bg="#333")
        frame = self.pw.sframe(line1=line1,line2=line2) #,line3=line3)


        def cb(event=None,args={}):
            print("open_fixture_list.cb(")
            print("   ",args)
            if self.pw:
                self.pw.w.tk.destroy()
            data = args["data"]
            self.b_path["text"] = data["name"] #"load_MH2"
            self.name["text"] = data["name"] #"load_MH2"
            self.name["text"] = data["name"] #"load_MH2"
            xpath = data["xpath"] + "/" + data["xfname"]
            fdata = showlib._read_sav_file(xpath)
            n = []
            a = []
            m = []
            NR = 0
            for row in fdata:
                #print("row:  ",row.keys())
                #print("a-")
                for k,fixture in row.items():#keys():
                    #v = row[k]
                    if "NAME" not in fixture:
                        continue
                    if fixture["NAME"] != args["val"]:
                        continue
                    
                    self.fixture = fixture

                    print("a    :",k,str(fixture)[:220],"...")
                    #print("a    ::",type(k),":",type(fixture))


                    attr_by_nr = fixlib.fixture_order_attr_by_nr(fixture)

                    if "ATTRIBUT" in fixture:
                        for at in attr_by_nr: #fixture["ATTRIBUT"]:
                            print("   ",at)
                            if at.startswith("EMPTY"):
                                NR += 1
                                n.append(str(NR))
                                a.append(at)
                                m.append("-")
                                continue
                            print("       ",fixture["ATTRIBUT"][at])

                            if at.startswith("_"):
                                 continue
                            try:
                                NR = fixture["ATTRIBUT"][at]["NR"]
                                n.append(str(NR))
                            except:
                                n.append("-") 
                            
                            at2 = at
                            if at2.endswith(" FINE"):
                                at2 = at2.replace(" FINE","-FINE")
                            while " -" in at2:
                                at2 = at2.replace(" -","-")
                            at2 = at2.replace("  "," ")
                            a.append(at2 ) #+":"+ str(fixture["ATTRIBUT"][at]["NR"]))

                            if at.endswith("-FINE"):
                                m.append("-")
                            elif at in MAIN._FIX_FADE_ATTR: 
                                #["PAN","TILT","DIM","RED","GREEN","BLUE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]:
                                m.append("F")
                            else:
                                m.append("S")
                            #m.append("F")

                    break # only a single fixture #no sub fixture

            self._load_fix(None,n,a,m)
            self.close_fixture_list()
        #_x =dir(MAIN)
        #_x.sort()
        #for _a in _x:
        #    print(_a)
        blist = fixlib._load_fixture_list(mode=mode)
        
        r=GUI_LOAD_FIXTURE_LIST(frame,data=blist,cb=cb,bg="#333")

    def close_fixture_list(self):
        if self.pw:
            self.pw.w.tk.destroy()

    def clear(self,_event=None,attr=[]):
        attr = [""]*100
        mode = [""]*100
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "clean..."
        self.close_fixture_list()

    def load(self,_event=None,attr=[]):
        attr = ["LOAD"]*10
        mode = ["X"]*10
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "clean..."
        self.close_fixture_list()

    def load_EMPTY(self,_event=None,attr=[]):
        #attr = [,"RED","GREEN","BLUE"]
        #mode = ["F","F","F","F"]
        self._load_mh(None)#,attr,mode)
    def load_DIM(self,_event=None,attr=[]):
        attr = ["DIM"]
        mode = ["F"]
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_DIM"
        self.close_fixture_list()
    def load_LED(self,_event=None,attr=[]):
        attr = ["DIM","RED","GREEN","BLUE"]
        mode = ["F","F","F","F"]
        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_LED"
        self.close_fixture_list()
    def load_MH(self,_event=None,attr=[]):
        if not attr:
            attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO"]
        mode = []
        for a in attr:
            if a.endswith("-FINE"):
                mode.append("-")
            elif a in MAIN._FIX_FADE_ATTR: #["PAN","TILT","DIM","RED","GREEN","BLUE","CYAN","YELLOW","MAGENTA","FOCUS","ZOOM","FROST"]:
                mode.append("F")
            else:
                mode.append("S")

        self._load_fix(None,attr,mode)
        self.b_path["text"] = "load_MH"
        self.close_fixture_list()
    def load_MH2(self,_event=None,attr=[]):
        attr = ["PAN","PAN-FINE","TILT","TILT-FINE","SHUTTER","DIM","RED","GREEN","BLUE","GOBO","G-ROT","PRISM","P-ROT","ZOOM","CONTR"]
        mode = ["F","F","F","F","S","F","F","F","F","S","S","S","S","F","S"]
        self.b_path["text"] = "load_MH2"
        self._load_fix(None,attr,mode)
        self.close_fixture_list()

    def _load_fix(self,_event=None,nrs=[],attr=[],mode=[]):
        print("load_fixture",[_event,self])
        #for i,e in enumerate(self.elem):
        for i,e in enumerate(self.elem):
            #print(self,"event",_event,e)
            #print("event",_event,e)
            if len(attr) > i:
                e._set_nr( nrs[i])
            else:
                e._set_nr( "")

            if len(attr) > i:
                e._set_attr( attr[i])
            else:
                e._set_attr( "")

            if len(mode) > i:
                e._set_mode( mode[i]+"'")
            else:
                e._set_mode( "---")
        self.count_ch() 

    def event_univ(self,_event=None):
        nr=self.univ
        txt= self.entry_univ["text"]
        #def _cb(txt):
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"event_univ._cb()",txt)
            try:
                nr = int(txt)
            except TypeError:
                print("--- abort ---")
                return 0
            self.univ = nr
            self._event_redraw(_event)
        dialog._cb = _cb
        dialog.askstring("Universe","Univ 0-15",initialvalue=txt)

    def event_dmx(self,_event=None):
        nr=self.dmx
        txt= self.entry_dmx["text"]
        #txt = dialog.askstring("DMX","ArtNet 1-512 (7680 max)",initialvalue=txt)
        #def _cb(txt):
        def _cb(data):
            if not data:
                print("err443",self,"_cb",data)
                return None
            txt = data["Value"]
            print(self,"event_dmx._cb()",txt)
            try:
                nr = int(txt)
            except TypeError:
                print("--- abort ---")
                return 0
            self.dmx = nr
            if self.dmx <= 0:
                self.dmx = 1
            if self.dmx > 512:
                self.univ = (self.dmx-1)//512
                self.dmx = (self.dmx-1)%512+1
            self._event_redraw(_event)
        dialog._cb = _cb
        dialog.askstring("DMX","ArtNet 1-512 (7680 max)",initialvalue=txt)

        
    def _event_redraw(self,_event=None):
        self.entry_dmx["text"] = "{}".format(self.dmx)
        self.entry_univ["text"] = "{}".format(self.univ)
        nr = 1 # self.univ*(512)+self.dmx # multiplay fader nr with dmx...
        # self.b_xdmx["text"] = " {}  ".format(nr)

        print("change_dmx",[_event,self])
        for i,btn in enumerate(self.elem):
            #print("event",_event,btn)
            #print("btn",btn)
            dmx=nr+i
            nr2 = dmx%512 
            btn.set_label("{} {}.{}\n D:{}".format(i+1,self.univ,nr2,dmx))
            btn.nr = nr+i

        pb=self.pb
        for j,e in enumerate(self.header):
            p=j+1
            #p=nr/pb
            txt="BANK:{} {}-{}".format(p,p*pb-pb+nr,(p*pb+nr)-1) 
            print("---",j,txt,e)
            e["text"] = txt
        self.count_ch() 
