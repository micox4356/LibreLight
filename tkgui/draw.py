

import tkinter as tk
import traceback

from __main__ import *
import lib.mytklib as mytklib




def draw_command(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    # b = tk.Button(frame,bg="lightblue", text="COMM.",width=6)
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #r+=1
    c+=1
    for comm in gui.commands.commands:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0
        if comm == "BLIND":
            b["bg"] = "grey"
            myTip = Hovertip(b,'BLIND MODE\nNO CHANGE on DMX-OUTPUT')
        if comm == "CLEAR":
            b["bg"] = "grey"
            myTip = Hovertip(b,'CLEAR ALL SELECTED\nFIXTURES ATTRIBUTES')
        if comm == "REC-FX":
            b["bg"] = "grey"
            myTip = Hovertip(b,'RECORD ONLY FX\nINTO EXEC')
        if comm == "FADE":
            b["bg"] = "green"
            myTip = Hovertip(b,'adjust fade time')
        if comm == "S-KEY":
            b["bg"] = "green"
            myTip = Hovertip(b,'keyboard short-key\non or  off')
        if comm == "FX OFF":
            b["bg"] = "magenta"
        if comm == "SIZE:":
            b["text"] = "SIZE:{:0.0f}".format(fx_prm["SIZE"])
        if comm == "SPEED:":
            b["text"] = "SPEED:{:0.0f}".format(fx_prm["SPEED"])
        if comm == "DELAY":
            b["text"] = "FADE:\n{:0.02f}".format(DELAY.val())
        if comm == "FADE":
            b["text"] = "FADE:\n{:0.02f}".format(FADE.val())
        if comm == "START:":
            b["text"] = "START:{:0.0f}".format(fx_prm["START"])
        if comm == "OFFSET:":
            b["text"] = "OFFSET:{:0.0f}".format(fx_prm["OFFSET"])
        if comm == "FX-X:":
            b["text"] = "FX-X:{}".format(fx_prm["FX-X"])
        if comm == "BASE:":
            b["text"] = "BASE:{}".format(fx_prm["BASE"])

        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="COMMAND").cb)
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=8:
            c=0
            r+=1

def draw_exec(gui,xframe,PRESETS):
    draw_preset(gui,xframe,PRESETS)


def draw_preset(gui,xframe,PRESETS):
    
    i=0
    c=0
    r=0
    root = xframe
    
    frame = tk.Frame(root,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
    #time.sleep(0.1)
    gui.elem_presets = {}
    i=0
    for k in PRESETS.val_presets:
        if i%(10*8)==0 or i ==0:
            c=0
            #b = tk.Label(frame,bg="black", text="" )
            b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            r+=1
            c=0
            b = tk.Button(frame,bg="lightblue", text="EXEC " )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="lightblue", text="BANK " + str(int(i/(8*8))+1) )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            c+=1
            b = tk.Button(frame,bg="lightblue", text="NAME"  )
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
            r+=1
            c=0
        i+=1
        v=0
        label = ""
        #if k in PRESETS.label_presets:
        #    label = PRESETS.label_presets[k]
        #    #print([label])

        sdata=PRESETS.val_presets[k]
        BTN="go"
        if "CFG" in sdata:#["BUTTON"] = "GO"
            if "BUTTON" in sdata["CFG"]:
                BTN = sdata["CFG"]["BUTTON"]


        #bb = tk.Frame(frame, highlightbackground = "red", highlightthickness = 1, bd=0)
        #bb = tk.Canvas(frame, highlightbackground = "black", highlightthickness = 1, bd=1)
        #bb.configure(width=70, height=38)
        txt=str(k+1)+":"+str(BTN)+":"+str(len(sdata)-1)+"\n"+label

        b = mytklib.ExecButton(frame,text=txt)

        #b = tk.Button(bb,bg="grey", text=txt,width=7,height=2)
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
        b.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=gui,mode="PRESET").cb)
        
        if k not in gui.elem_presets:
            gui.elem_presets[k] = b
        #b.pack(expand=1)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)

        b.config(text="xx")
        c+=1
        if c >=10:
            c=0
            r+=1
    time.sleep(0.1)
    gui._refresh_exec()
    #gui.refresh_exec()
    #gui.refresh_exec()
    print("##################################")


def draw_input(gui,root2):

    i=0
    c=0
    r=0
    frame = tk.Frame(root2,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)

    b = tk.Label(frame,bg="black", text="------------------------ ---------------------------------------")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    r=0
    
    frame = tk.Frame(root2,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
    
    b = tk.Label(frame, text="send:")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    b = tk.Entry(frame,bg="grey", text="",width=50)
    gui.entry = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","d0:127,fx241:sinus:50:50:10,fx243:cosinus:50:50:10,d201:127,fx201:sinus:50:300:10")
    r+=1
    b = tk.Entry(frame,bg="grey", text="",width=20)
    gui.entry2 = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","d1:0:4")
    r+=1
    b = tk.Entry(frame,bg="grey", text="",width=20)
    gui.entry3 = b
    b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    #b.bind("<B1-Motion>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    b.insert("end","fx:alloff:::")


def draw_colorpicker(gui,xframe,FIXTURES,master):
    import lib.colorpicker as colp

    class _CB():
        def __init__(gui,FIXTURES,master):
            gui.old_color = (0,0,0)
        def cb(gui,event,data):
            print("CB.cb",gui,event,data)
            cprint("colorpicker CB")
            if "color" not in data:
                return 0
            if gui.old_color == data["color"]:
                pass #return 0
            
            #gui.old_color = data["color"]
            color = data["color"]
            
            print("e",event,data)
            print("e",dir(event))#.keys())
            try:
                print("e.state",event.state)
            except:pass
            set_fade = FADE.val() #fade

            event_ok = 0
            event_num = 0
            event_state = 0
            if event is None:
                event_ok = 1
                event_num = 3
            elif event.num == 1:
                event_ok = 1
                event_num = event.num 
            elif event.num == 3:
                event_ok = 1
                event_num = event.num 
            elif event.num==2:
                event_ok = 1
                event_num = event.num 
            elif event.state in [256,1024]:
                event_ok = 1
                event_state = event.state


            if "color" in data and event_ok:
                cr=None
                cg=None
                cb=None
                cw=0
                ca=0
                set_fade=0

                if event_num == 1: 
                    if FADE._is():
                        set_fade=FADE.val() #fade
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]
                elif event_num == 3: 
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]
                elif event_num == 2: 
                    cr= "click"
                    cg= "click"
                    cb= "click"
                    cw= "click"
                    ca= "click"
                elif event_state == 256:
                    cr = color[0]
                    cg = color[1]
                    cb = color[2]


                if cr is not None:
                    FIXTURES.encoder(fix=0,attr="RED",xval=cr,xfade=set_fade)
                if cg is not None:
                    FIXTURES.encoder(fix=0,attr="GREEN",xval=cg,xfade=set_fade)
                if cb is not None:
                    FIXTURES.encoder(fix=0,attr="BLUE",xval=cb,xfade=set_fade)
                FIXTURES.encoder(fix=0,attr="WHITE",xval=cw,xfade=set_fade)
                FIXTURES.encoder(fix=0,attr="AMBER",xval=ca,xfade=set_fade)
                master.refresh_fix()
                 
                print("PICK COLOR:",data["color"])
    _cb=_CB(FIXTURES,master)
    colp.colorpicker(xframe,width=580,height=113, xcb=_cb.cb)
    return 0

    canvas=tk.Canvas(xframe,width=600,height=113)
    canvas["bg"] = "yellow" #"green"
    canvas.pack()
    # RGB
    x=0
    y=0
    j=0
    d = 20
    for i in range(0,d+1):
        fi = int(i*255/d)
        f = 255-fi
        if i > d/2: 
            pass#break
        color = '#%02x%02x%02x' % (f, fi, fi)
        print( "farbe", i*10, j, f,fi,fi,color)
        r = canvas.create_rectangle(x, y, x+20, y+20, fill=color)
        x+=20




#def draw_config(gui,xframe):
class GUI_CONF():
    def __init__(self,gui,xframe,data):
        self.gui = gui
        self.data = data
        self.xframe = xframe
        self.draw()
    def draw(self):
        gui =self.gui
        xframe = self.xframe
        for widget in xframe.winfo_children():
            widget.destroy()

        i=0
        c=0
        r=0
        root2 = xframe

        frame = tk.Frame(root2,bg="#222")
        frame.pack(fill="both", expand=1,side=tk.TOP)


        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c=0
        r+=1
        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c=1
        r+=1
        
        
        b = tk.Label(frame, text="_________")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        b = tk.Entry(frame,bg="grey", text="",width=50)
        gui.entry = b
        #b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        #b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","" ) #d0:127,fx241:sinus:50:50:10,fx243:cosinus:50:50:10,d201:127,fx201:sinus:50:300:10")
        r+=1
        b = tk.Entry(frame,bg="grey", text="",width=20)
        gui.entry2 = b
        #b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
        #b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT2").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","d1:0:4")
        r+=1
        b = tk.Entry(frame,bg="grey", text="",width=20)
        gui.entry3 = b
        #b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
        ##b.bind("<B1-Motion>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
        #b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT3").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        b.insert("end","fx:alloff:::")

        r+=1

        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b = tk.Label(frame, text=" BATCH COMMAND ")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b1 = tk.Entry(frame,bg="grey", text="",width=50)
        #gui.entry = b
        #b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        #b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        b1.grid(row=r, column=c, sticky=tk.W+tk.E)
        b1.insert("end","fix 1-100 patch @ 2.120")
        r+=1

        b = tk.Label(frame, text="",bg="#222")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b = tk.Label(frame, text=" BATCH COMMAND ")
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=0
        r+=1
        b2 = tk.Entry(frame,bg="grey", text="",width=50)
        #gui.entry = b
        #b.bind("<Button>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        #b.bind("<Key>",Xevent(fix=0,elem=b,attr="INPUT",data=gui,mode="INPUT").cb)
        b2.grid(row=r, column=c, sticky=tk.W+tk.E)
        b2.insert("end","SELECT 33-61 PAN,TILT")

        root2.pack(fill="both",expand=1,side="top")



def draw_enc(gui,xframe):

    for widget in xframe.winfo_children():
        widget.destroy()

    root2 = xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(xframe,bg="black")
    frame.pack( side=tk.LEFT,expand=0,fill="both")

    
    b = tk.Button(frame,bg="lightblue", text="ENCODER",width=6)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)


    thread.start_new_thread(mytklib.tk_btn_bg_loop,(b,))

    c+=1
    eat = gui.all_attr

    if len(eat) < 24:
        for i in range(24-len(eat)):
            eat.append("")
    for attr in eat:
        if attr.endswith("-FINE"):
            continue
        v=0
        if attr.startswith("_"):
            continue

        b = tk.Button(frame,bg="#6e6e6e", text=str(attr)+'',width=7)#, anchor="w")
        if attr == "DIM":
            b = tk.Button(frame,bg="#ff7f00", text=str(attr)+'',width=7)#, anchor="w")
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=attr,data=gui,mode="ENCODER2").cb)
        b.grid(row=r, column=c, sticky=tk.W+tk.E ,ipadx=0,ipady=0,padx=0,pady=0)#,expand=True)
        c+=1
        if c >=8:
            c=0
            r+=1

    b = tk.Button(frame,bg="#bfff00", text="INV-ATTR",width=6)
    myTip = Hovertip(b,'INVERT ATTRIBUT SELECTION')
    b.bind("<Button>",Xevent(fix="SEL",elem=b,attr="INV-ATTR",data=gui,mode="INVERT").cb)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1

def _draw_fx(frame,c,r,gui,mode="FX"):
    ct  = gui.fx
    prm = fx_prm
    if mode=="FX-MOVE":
        ct  = gui.fx_moves
        prm = fx_prm_move
    elif mode=="FX-GENERIC":
        ct  = gui.fx_generic
        prm = fx_prm #_generic

    for comm in ct.commands:
        if comm == "\n\n":
            b = tk.Label(frame,bg="black", text="-",font=space_font)
            b.grid(row=r, column=c,pady=0,padx=0, sticky=tk.W+tk.E)
            c=0
            r+=1
            continue
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        if "PAN/TILT" in comm: 
            b = tk.Button(frame,bg="grey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in ct.elem:
            #comm = comm.replace("\n","")
            ct.elem[comm] = b
            ct.val[comm] = 0
        b.bind("<Button>",Xevent_fx(fix=0,elem=b,attr=comm,data=gui,mode=mode).cb)
        if comm == "REC-FX":
            b["bg"] = "grey"
        elif comm == "FX OFF":
            b["bg"] = "magenta"
        elif comm[:3] == "FX:":
            b["text"] = comm
            b["bg"] = "#ffbf00"
        elif comm[:3] == "MO:":
            b["text"] = comm 
            b["bg"] = "lightgreen"
        elif comm.startswith( "SIZE:"):
            b["text"] = "SIZE:\n{:0.0f}".format(prm["SIZE"])
            b["bg"] = "lightgreen"
        elif comm.startswith( "SPEED:"):
            b["text"] = "SPEED:\n{:0.0f}".format(prm["SPEED"])
            b["bg"] = "lightgreen"
        elif comm.startswith("START:"):
            b["bg"] = "lightgreen"
            b["text"] = "START:\n{:0.0f}".format(prm["START"])
        elif comm.startswith( "OFFSET:"):
            b["bg"] = "lightgreen"
            b["text"] = "OFFSET:\n{:0.0f}".format(prm["OFFSET"])
        elif comm[:3] == "BASE:":
            b["bg"] = "lightgreen"
            b["text"] = "BASE:\n{}".format(prm["BASE"])
        elif comm[0] == "M":
            b["text"] = comm 
            b["bg"] = "lightgrey"

        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=6:
            c=0
            r+=1
    return c,r



def draw_fx(gui,xframe):
    frame_fx=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_fx,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    b = tk.Button(frame,bg="lightblue", text="FX.",width=6)
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    c+=1
    thread.start_new_thread(mytklib.tk_btn_bg_loop,(b,))

    c,r = _draw_fx(frame,c,r,gui,mode="FX-MOVE")
    r+=1

    b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    r+=1
    c=0

    c,r = _draw_fx(frame,c,r,gui,mode="FX")

    b = tk.Canvas(frame,bg="black", height=4,bd=0,width=6,highlightthickness=0) #,bd="black")
    b.grid(row=r, column=c, sticky=tk.W+tk.E)
    r+=1
    c=0

    c,r = _draw_fx(frame,c,r,gui,mode="FX-GENERIC")


def draw_setup(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    #b = tk.Button(frame,bg="lightblue", text="SETUP",width=6)
    #b.bind("<Button>",Xevent(fix=fix,elem=b).cb)
    
    #b.grid(row=r, column=c, sticky=tk.W+tk.E)
    #r+=1
    c+=1
    for comm in ["SAVE\nSHOW","LOAD\nSHOW","NEW\nSHOW","SAVE\nSHOW AS","SAVE &\nRESTART","DRAW\nGUI"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        if comm == "SAVE\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=5,height=2)
        elif comm == "LOAD\nSHOW":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=5,height=2)
        elif comm == "SAVE\nSHOW AS":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        elif comm == "SAVE &\nRESTART":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        elif comm == "DRAW\nGUI":
            b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        else:
            b = tk.Button(frame,bg="grey", text=str(comm),width=5,height=2)

        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0

        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="SETUP").cb)

        if comm == "BASE:":
            b["text"] = "BASE:{}".format(prm["BASE"])
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=7:
            c=0
            r+=1













def draw_live(gui,xframe):
    frame_cmd=xframe
    i=0
    c=0
    r=0
    
    frame = tk.Frame(frame_cmd,bg="black")
    frame.pack(fill=tk.X, side=tk.TOP)
   
    c+=1
    for comm in ["FADE","DELAY","PAN/TILT\nFADE","PAN/TILT\nDELAY"]:
        if comm == "\n":
            c=0
            r+=1
            continue
        v=0
        
        b = tk.Button(frame,bg="lightgrey", text=str(comm),width=6,height=2)
        if comm not in gui.commands.elem:
            gui.commands.elem[comm] = b
            gui.commands.val[comm] = 0
        b.bind("<Button>",Xevent(fix=0,elem=b,attr=comm,data=gui,mode="LIVE").cb)

        if "FADE" == comm:
            b["text"] = "FADE:\n{:0.2}".format(FADE.val())
        if "DELAY" == comm:
            b["text"] = "DELAY:\n{:0.2}".format(DELAY.val())
        if "PAN/TILT\nFADE" == comm:
            b["text"] = "PAN/TILT\nFADE:{:0.2}".format(FADE_move.val())

        if "FADE" in comm:
            b["bg"] = "green"
            b.config(activebackground="lightgreen")
        if comm:
            b.grid(row=r, column=c, sticky=tk.W+tk.E)
        c+=1
        if c >=5:
            c=0
            r+=1

