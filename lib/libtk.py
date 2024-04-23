#!/usr/bin/python3

import os
import time

import tkinter
tk = tkinter

import __main__ as MAIN
from lib.cprint import *

import lib.libwin as libwin


class on_focus():
    def __init__(self,name,mode):
        self.name = name
        self.mode = mode
    def cb(self,event=None):
        print("on_focus",event,self.name,self.mode)
        try:
            e = MAIN.master.commands.elem["."]
        except:pass

        if self.mode == "Out":
            cmd="xset -display :0.0 r rate 240 20"
            print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#aaa"
                e["activebackground"] = "#aaa"
            except:pass
        if self.mode == "In":
            cmd = "xset -display :0.0 r off"
            print(cmd)
            os.system(cmd)
            try:
                e["bg"] = "#fff"
                e["activebackground"] = "#fff"
            except:pass

class DummyCallback():
    def __init__(self,name="name"):
        self.name = name
    def cb(self,event=None):
        cprint("DummyCallback.cb",[self.name,event])

class Window():
    def __init__(self,args): #title="title",master=0,width=100,height=100,left=None,top=None,exit=0,cb=None,resize=1):
        global lf_nr
        self.args = {"title":"title","master":0,"width":100,"height":100,"left":None,"top":None,"exit":0,"cb":None,"resize":1}
        self.args.update(args)
        
        cprint("Window.init()",id(self.args),color="yellow")
        cprint("  ",self.args,color="yellow")

        ico_path="./icon/"
        self.cb = MAIN.cb

        if self.args["master"]: 
            self.tk = tkinter.Tk()
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.withdraw() # do not draw
            self.tk.resizable(self.args["resize"],self.args["resize"])
            self.tk.tk_setPalette(background='#bbb', foreground='black', activeBackground='#aaa', activeForeground="black")

            defaultFont = tkinter.font.nametofont("TkDefaultFont")
            cprint(defaultFont)
            defaultFont.configure(family="FreeSans",
                                   size=10,
                                   weight="bold")
            # MAIN MENUE
            try:
                self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"main.png"))
            except Exception as e:
                cprint("Exception GUIWindow.__init__",e)
        else:
            # addtional WINDOW
            self.tk = tkinter.Toplevel()
            self.tk.iconify()
            #self.tk.withdraw() # do not draw
            self.tk.protocol("WM_DELETE_WINDOW", self.close_app_win)
            self.tk.resizable(self.args["resize"],self.args["resize"])
            
            try:
                if "COLORPICKER" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"picker.png"))
                elif "ENCODER" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"enc.png"))
                elif "EXEC" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"exec.png"))
                elif "FX" in self.args["title"]:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"fx.png"))
                else:
                    self.tk.iconphoto(False, tk.PhotoImage(file=ico_path+"scribble.png"))
            except Exception as e:
                cprint("Exception on load window icon",self.args["title"])
                cprint("Exception:",e)
            #time.sleep(3)
            self.tk.deiconify()



        self.tk["bg"] = "black"
        self.tk.bind("<Button>",self.callback)
        self.tk.bind("<Key>",self.callback)
        self.tk.bind("<KeyRelease>",self.callback)
        self.tk.bind("<FocusIn>", on_focus(self.args["title"],"In").cb)
        self.tk.bind("<FocusOut>", on_focus(self.args["title"],"Out").cb)

        self.tk.title(""+str(self.args["title"])+" "+str(MAIN.lf_nr)+":"+str(MAIN.rnd_id))
        MAIN.lf_nr+=1
        #self.tk.geometry("270x600+0+65")
        geo ="{}x{}".format(self.args["width"],self.args["height"])
        if self.args["left"] is not None:
            geo += "+{}".format(self.args["left"])
            if self.args["top"] is not None:
                geo += "+{}".format(self.args["top"])

        #self._event_clear = Xevent(fix=0,elem=None,attr="CLEAR",data=self,mode="ROOT").cb
        self.tk.geometry(geo)
        self.show()
    def update_idle_task(self):
        if INIT_OK:
            tkinter.Tk.update_idletasks(gui_menu_gui.tk)
        pass
    def close_app_win(self,event=None):
        cprint("close_app_win",self,event,self.args["title"],color="red")
        if exit:
            if self.title == "MAIN":
               libwib.save_window_position()
            libwin.save_window_position()
            
            self.tk.destroy()
        try:
            self.cb("<exit>").cb()
        except Exception as e:
            cprint("EXCETPION: close_app_win",e,self,color="red")

    def title(self,title=None):
        if title is None:
            return self.tk.title()
        else:
            #return self.tk.title(title)
            self.args["title"] = title
            return self.tk.title(""+str(self.args["title"])+" "+str(lf_nr)+":"+str(rnd_id))
    def show(self):
        self.tk.deiconify()
        pass
    def mainloop(self):
        #save_window_position_loop() #like autosave
        try:
            self.tk.mainloop()
        finally:
            self.tk.quit()
            cmd="xset -display :0.0 r rate 240 15"
            print(cmd)
            os.system(cmd)

    def callback(self,event,data={}):#value=255):
        #global MAIN._global_short_key
        sstart = time.time()
        #time.sleep(0.1)
        if not MAIN._global_short_key:
            return 1

        global _shift_key
        #cprint("<GUI>",event,color="yellow")
        value = 255
        if "Release" in str(event.type) or str(event.type) == '5' or str(event.type) == '3':
            value = 0
        cprint("<GUI>",event.state,data,value,[event.type,event.keysym],color="yellow")
        #print(event)
        if "state" in dir(event) and "keysym" in dir(event):
            #print([event.state,event.keysym,event.type])
            if event.state == 4  and str(2) == str(event.type): # strg + s
                if str(event.keysym) == "s":
                    cprint("tTtT ReW "*20)
                    #print("numbersign !!")
                    MAIN.PRESETS.backup_presets()
                    MAIN.FIXTURES.backup_patch()
                    libwin.save_window_position()

                    e =  MAIN.master.setup_elem["SAVE\nSHOW"]
                    #print(e)
                    b = MAIN.BLINKI(e)
                    b.blink()
                if str(event.keysym) == "c":
                    MAIN.PRESETS.backup_presets()
                    MAIN.FIXTURES.backup_patch()

                    libwin.save_window_position()
                    #self.elem.config(activebackground="lightgrey")
                    MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)
                #cprint("oipo "*10,round(int(time.time()-sstart)*1000,2))
                return

        if "keysym" in dir(event):
            if "Escape" == event.keysym:
                MAIN.FIXTURES.clear()
                MAIN.modes.val("ESC",1)
                MAIN.master.refresh_fix()
            elif event.keysym in ["Shift_L","Shift_R"]:
                #cprint(event.type)
                if "KeyRelease" in str(event.type) or str(event.type) in ["3"]:
                    _shift_key = 0
                else:
                    _shift_key = 1
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                #cprint("SHIFT_KEY",_shift_key,"??????????")
                global _ENCODER_WINDOW
                try:
                    if _shift_key:
                        _ENCODER_WINDOW.title("SHIFT/FINE ")
                    else:
                        _ENCODER_WINDOW.title("ENCODER") 
                except Exception as e:
                    cprint("exc9800",e)

            elif event.keysym in "ebfclrmsRx" and value: 
                if "e" == event.keysym:
                    MAIN.modes.val("EDIT",1)
                elif "b" == event.keysym:
                    MAIN.modes.val("BLIND",1)
                elif "f" == event.keysym:
                    MAIN.modes.val("FLASH",1)
                elif "c" == event.keysym:
                    MAIN.modes.val("CFG-BTN",1)
                elif "l" == event.keysym:
                    MAIN.modes.val("LABEL",1)
                elif "r" == event.keysym:
                    MAIN.modes.val("REC",1)
                elif "R" == event.keysym:
                    MAIN.modes.val("REC-FX",1)
                elif "x" == event.keysym:
                    MAIN.modes.val("REC-FX",1)
                elif "m" == event.keysym:
                    x=MAIN.modes.val("MOVE",1)
                    if not x:
                        MAIN.PRESETS.clear_move()
                elif "s" == event.keysym:
                    MAIN.modes.val("SELECT",1)
            elif event.keysym in ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]:
                nr = int( event.keysym[1:]) # F:1-12
                nr = nr-1+81  
                cprint("F-KEY",value,nr,event.keysym)
                #print(event)
                MAIN.master.preset_go(nr-1,xfade=None,val=value)
            elif event.keysym in ["1","2","3","4","5","6","7","8","9","0"]:
                nr = int( event.keysym)
                if nr == 0:
                    nr = 10
                nr = nr-1+161  
                cprint("NUM-KEY",value,nr)
                MAIN.master.preset_go(nr-1,xfade=None,val=value)
            elif "numbersign" == event.keysym and value: # is char "#"
                cprint("numbersign !!")
                MAIN.PRESETS.backup_presets()
                MAIN.FIXTURES.backup_patch()

                libwin.save_window_position()

                for e in MAIN.master.setup_cmd:
                    cprint(e)
                e =  MAIN.master.setup_elem["SAVE\nSHOW"]
                cprint(e)
                b = MAIN.BLINKI(e)
                b.blink()
                #e = Xevent(fix=0,elem=None,attr="SAVE\nSHOW",mode="SETUP")
                #e.cb(event=event)
            elif "End" == event.keysym:
                MAIN.FIXTURES.fx_off("all")
                CONSOLE.fx_off("all")
                CONSOLE.flash_off("all")
            elif "Delete" == event.keysym:
                #MAIN.PRESETS.delete(nr)
                if value:
                    MAIN.modes.val("DEL",1)

        cprint("oipo "*10,round(int(time.time()-sstart)*1000,2))
 

class PopupList():
    def __init__(self,name="<NAME>",master=0,width=400,height=450,exit=1,left=MAIN._POS_LEFT+400,top=MAIN._POS_TOP+100,cb=None,bg="black"):
        self.name = name
        self.frame = None
        self.bg=bg
        self.cb = cb
        if cb is None: 
            cb = DummyCallback #("load_show_list.cb")
        #w = Window(self.name,master=master,width=width,height=height,exit=exit,left=left,top=top,cb=cb)
        args = {"title":self.name,"master":master,"width":width,"height":height,"exit":exit,"left":left,"top":top,"cb":cb}
        w = Window(args)
        self.w = w
        w.show()
    def sframe(self,line1="<line1>",line2="<line2>",data=[]):

        xframe=self.w.tk
        if self.bg:
            xframe.configure(bg=self.bg)
            self.w.tk.configure(bg=self.bg)
        c=0
        r=0

        b = tk.Label(xframe,bg="grey",text=line1,anchor="w")
        b.pack(side="top",expand=0,fill="x" ) 


        b = tk.Label(xframe,bg="grey",text=line2,anchor="w")
        b.pack(side="top",expand=0,fill="x" ) 

        b = tk.Label(xframe,bg="black",fg="black",text="")
        if self.bg:
            b.configure(fg=self.bg)
            b.configure(bg=self.bg)
        b.pack(side="top") 

        b = tk.Entry(xframe,width=10,text="")#,anchor="w")
        b.pack(side="top",expand=0,fill="x") 
        b["state"] = "readonly"
        b.focus()


        #frame = tk.Frame(xframe,heigh=2800)
        #frame.pack(fill=tk.BOTH,expand=1, side=tk.TOP)

        frame = MAIN.ScrollFrame(xframe,width=300,height=500,bd=1,bg=self.bg)
        #frame.pack(side="left") #fill=tk.BOTH,expand=1, side=tk.TOP) 
        #self.frame = frame
        self.w.tk.state(newstate='normal')
        self.w.tk.attributes('-topmost',True)
        return frame

def showwarning(msg="<ERROR>",title="<TITLE>"):
    cprint("showwarning","MSG:",msg,"tilte:",title)

    if IS_GUI:
        _main = tkinter.Tk()
        defaultFont = tkinter.font.nametofont("TkDefaultFont")

        cprint("showwarning",defaultFont)

    if IS_GUI:
        defaultFont.configure(family="FreeSans",
                               size=10,
                               weight="normal")
        
        geo ="{}x{}".format(20,20)
        _main.geometry(geo)
        def _quit():
            time.sleep(1/10)
            _main.quit()
        thread.start_new_thread(_main.mainloop,())
        #_main.quit()

        #msg="'{}'\n Show Does Not Exist\n\n".format(show_name)
        #msg += "please check\n"
        #msg += "-{}init.txt\n".format(self.show_path0)
        #msg += "-{}".format(self.show_path1)

        r=tkinter.messagebox.showwarning(message=msg,title=title,parent=None)
