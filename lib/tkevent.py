#!/usr/bin/python3

import sys
import time

import traceback

from lib.cprint import cprint
import __main__ as MAIN

import lib.showlib as showlib
import lib.fxlib as fxlib
import lib.libtk as libtk
import tkgui.dialog as dialoglib
import lib.tkrefresh as tkrefresh

dialog = dialoglib.Dialog()

class tk_event():
    """ global input event Handeler for short cut's ... etc
    """
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data=data
        self.attr = attr
        self.elem = elem
        self.mode = mode

    def setup(self,event):       
        cprint("tk_event.SETUP",[self.mode,self.attr],color="red")
        if self.mode != "SETUP":
            return 0

        if self.attr == "SAVE\nSHOW":
            self.elem["bg"] = "orange"
            self.elem["text"] = "SAVING..."
            self.elem["bg"] = "red"
            self.elem.config(activebackground="orange")

            MAIN.modes.val(self.attr,1)

            MAIN.save_show()

            self.elem["bg"] = "lightgrey"
            self.elem.config(activebackground="lightgrey")
            b = libtk.BLINKI(self.elem)
            b.blink()
            self.elem["text"] = "SAVE\nSHOW"

        elif self.attr == "LOAD\nSHOW":
            name = "LOAD-SHOW"
            line1 = "PATH: " + showlib.current_show_path()
            line2 = "DATE: " + time.strftime("%Y-%m-%d %X",  time.localtime(time.time()))

            class cb():
                def __init__(self,name=""):
                    self.name=name
                    cprint("   LOAD-SHOW.init",name)
                def cb(self,event=None,**args):
                    cprint("   LOAD-SHOW.cdb",self.name,event,args)
                    if self.name != "<exit>":
                        cprint("-----------------------:")
                        MAIN.LOAD_SHOW_AND_RESTART(self.name).cb()

            pw = libtk.PopupList(name,cb=cb)
            print(line1,line2)
            frame = pw.sframe(line1=line1,line2=line2)
            r = libtk.frame_of_show_list(frame,cb=cb)

        elif self.attr == "NEW\nSHOW":

            def _cb(data):
                if not data:
                    cprint("err443",self,"_cb",data)
                    return None
                fname = data["Value"]
                fpath = showlib.generate_show_path(fname)
                cprint("SAVE NEW SHOW",fpath,fname)

                if MAIN.save_show_as(fname,new=1):
                    MAIN.LOAD_SHOW_AND_RESTART(fname).cb() 

            dialog._cb = _cb
            dialog.askstring("CREATE NEW SHOW","CREATE NEW SHOW:")

        elif self.attr == "SAVE\nSHOW AS":

            #def _cb(fname):
            def _cb(data):
                if not data:
                    cprint("err443",self,"_cb",data)
                    return None
                fname = data["Value"]

                if MAIN.save_show_as(fname):
                    MAIN.LOAD_SHOW_AND_RESTART(fname).cb() 


            dialog._cb = _cb
            dialog.askstring("SAVE SHOW AS","SAVE SHOW AS:")

        elif self.attr == "SAVE &\nRESTART":
            self.elem["bg"] = "orange"
            self.elem["text"] = "SAVING..."
            self.elem["bg"] = "red"
            self.elem.config(activebackground="orange")
            MAIN.modes.val(self.attr,1)

            MAIN.save_show()

            self.elem["text"] = "RESTARTING..."
            self.elem["bg"] = "lightgrey"
            self.elem.config(activebackground="lightgrey")
            MAIN.LOAD_SHOW_AND_RESTART("").cb(force=1)

        elif self.attr == "DRAW\nGUI":
            old_text = self.elem["text"]
            window_manager.top("PATCH")
            gui_patch.draw(MAIN.FIXTURES)
            gui_fix.draw(MAIN.FIXTURES)
            window_manager.top("MAIN.FIXTURES")
            MAIN.master._refresh_exec()
            self.elem["text"] = old_text  

        elif self.attr == "PRO\nMODE":
            MAIN.save_show()
            import lib.restart as restart
            restart.pro()

        elif self.attr == "EASY\nMODE":
            MAIN.save_show()
            import lib.restart as restart
            restart.easy()
        else:
            if IS_GUI:
                msg="{}\nnot implemented".format(self.attr.replace("\n"," "))
                r=tkinter.messagebox.showwarning(message=msg,parent=None)
        return 1

    def live(self,event):       
        if self.mode != "LIVE":
            return 0
                
        if "FADE" in self.attr or "DELAY" in self.attr:
           
            if self.attr == "FADE":
                ct = MAIN.FADE
            if self.attr == "DELAY":
                ct = MAIN.DELAY
            if "PAN/TILT\nFADE" in self.attr:
                ct = MAIN.FADE_move

            value = ct.val()
            #print("EVENT CHANGE ",[self.attr])
            cprint("EVENT CHANGE:",self.mode,value,self.attr)
            if value < 0:
                value = 1
            if event.num == 4:
                value += 0.1 
            elif event.num == 5:
                value -= 0.1
            elif event.num == 1:
                if ct._is():
                    ct.off()# = 0
                    self.data.commands.elem[self.attr]["bg"] = "grey"
                    self.elem.config(activebackground="grey")
                else:
                    ct.on()# = 1
                    self.data.commands.elem[self.attr]["bg"] = "green"
                    self.elem.config(activebackground="lightgreen")
            elif event.num == 2:
                value += 1

            if value > 10:
                value = 1
            value = round(value,1)
            value = ct.val(value)

            if self.attr == "FADE":
                self.data.commands.elem[self.attr]["text"] = "FADE:\n{:0.2f}".format(value)
            if self.attr == "DELAY":
                self.data.commands.elem[self.attr]["text"] = "DELAY:\n{:0.3f}".format(value)
            if "PAN/TILT\nFADE" in self.attr:
                self.data.commands.elem[self.attr]["text"] = "PAN/TILT\nFADE:{:0.2f}".format(value)



    def command(self,event):       
        if self.mode != "COMMAND":
            return 0

        if self.attr == "CLEAR":
            if event.num == 1:
                ok = MAIN.FIXTURES.clear()
                if ok:
                    MAIN.master._refresh_fix()
                MAIN.modes.val(self.attr,0)

        elif self.attr == "SAVE":
            MAIN.modes.val(self.attr,1)
            MAIN.save_show()
            #MAIN.EXEC.backup_exec()
            #MAIN.FIXTURES.backup_patch()
            #time.sleep(1)
            MAIN.modes.val(self.attr,0)

        elif self.attr == "S-KEY":
            if MAIN._global_short_key:
                MAIN._global_short_key = 0
                MAIN.master.commands.elem["S-KEY"]["bg"] = "red"
                MAIN.master.commands.elem["S-KEY"]["activebackground"] = "red"
            else:
                MAIN._global_short_key = 1
                MAIN.master.commands.elem["S-KEY"]["bg"] = "green"
                MAIN.master.commands.elem["S-KEY"]["activebackground"] = "green"
            cprint("s-key",MAIN._global_short_key)

        else:
            if event.num == 1:
                cprint("ELSE",self.attr)
                MAIN.modes.val(self.attr,1)

        return 0


    def encoder(self,event):
        cprint("tk_event","ENC",self.fix,self.attr,self.mode)
        cprint("SHIFT_KEY",MAIN._shift_key,"??????????")

        if self.mode == "ENCODER":
            if self._encoder(event):
                MAIN.master.refresh_fix() # delayed
                MAIN.refresher_fix.reset() # = tkrefresh.Refresher()

        if self.mode == "ENCODER2":
            if self._encoder(event):
                MAIN.master.refresh_fix() # delayed
                MAIN.refresher_fix.reset() # = tkrefresh.Refresher()

        if self.mode == "INVERT":
            cprint("INVERT",event)
            if self._encoder(event):
                MAIN.master.refresh_fix() # delayed
                MAIN.refresher_fix.reset() # = tkrefresh.Refresher()

    def _encoder(self,event):

        cprint("-- tk_event","_ENC",self.fix,self.attr,self.mode)
        cprint("-- SHIFT_KEY",MAIN._shift_key,"??????????")
        val=""
        if event.num == 1:
            val ="click"
        elif event.num == 4:
            val ="++"
            if MAIN._shift_key:
                val = "+"
        elif event.num == 5:
            val ="--"
            if MAIN._shift_key:
                val = "-"
        #print("SHIFT",val,MAIN._shift_key)
        if val:
            MAIN.FIXTURES.encoder(fix=self.fix,attr=self.attr,xval=val)
            return 1       


            
    def cb(self,event):
        cprint("EVENT cb",self.attr,self.mode,event,color='yellow')
        cprint(["type",event.type,"num",event.num])

        MAIN.INIT_OK = 1
        try:
            change = 0
            if "keysym" in dir(event):
                if "Escape" == event.keysym:
                    ok = MAIN.FIXTURES.clear()
                    MAIN.master._refresh_fix()
                    cprint()
                    return 0

            if self.mode == "SETUP":
                self.setup(event)
            elif self.mode == "COMMAND":
                self.command(event)
            elif self.mode == "LIVE":
                self.live(event)
            elif self.mode == "ENCODER":
                self.encoder(event)
                MAIN.master.refresh_fix()

            elif self.mode == "ENCODER2":
                self.encoder(event)
            elif self.mode == "INVERT":
                self.encoder(event)
            elif self.mode == "FX":
                cprint("tk_event CALLING FX WRONG EVENT OBJECT !!",color="red")
            elif self.mode == "ROOT":
                if event.keysym=="Escape":
                    pass

            elif self.mode == "INPUT":
                cprint("INP",self.data.entry.get())
                if event.keycode == 36:
                    x=self.data.entry.get()
                    #client.send(x)

            elif self.mode == "INPUT2":
                cprint("INP2",self.data.entry2.get())
                if event.keycode == 36:
                    x=self.data.entry2.get()
                    #client.send(x)

            elif self.mode == "INPUT3":
                cprint("INP3",self.data.entry3.get())
                if event.keycode == 36:
                    x=self.data.entry3.get()
                    #client.send(x)

            elif self.mode == "EXEC":
                nr = self.attr #int(self.attr.split(":")[1])-1

                if event.num == 3: # right click for testing
                    if str(event.type) == '4': #4 ButtonPress
                        if MAIN.modes.val("CFG-BTN"):
                            MAIN.master.btn_cfg(nr,testing=1)

                if event.num == 1:
                    if str(event.type) == '4': #4 ButtonPress
                        if MAIN.modes.val("REC"):
                            self.data.exec_rec(nr)
                            MAIN.modes.val("REC",0)
                            time.sleep(0.05)
                            MAIN.master._refresh_exec(nr=nr)
                        elif MAIN.modes.val("DEL"):
                            ok=MAIN.EXEC.delete(nr)
                            if ok:
                                MAIN.modes.val("DEL",0)
                                #MAIN.master.refresh_exec()
                                MAIN.master._refresh_exec(nr=nr)
                        elif MAIN.modes.val("COPY"):
                            ok=MAIN.EXEC.copy(nr)
                            if ok:
                                MAIN.modes.val("COPY",0)
                                MAIN.master._refresh_exec(nr=nr)
                        elif MAIN.modes.val("MOVE"):
                            ok,cnr,bnr=MAIN.EXEC.move(nr)
                            if ok:
                                #MAIN.modes.val("MOVE",0) # keep MOVE on
                                MAIN.master._refresh_exec(nr=nr)
                                MAIN.master._refresh_exec(nr=bnr)
                        elif MAIN.modes.val("CFG-BTN"):
                            MAIN.master.btn_cfg(nr)
                            #MAIN.master._refresh_exec(nr=nr)
                        elif MAIN.modes.val("LABEL"):#else:
                            MAIN.master.label(nr)
                            #MAIN.master._refresh_exec(nr=nr)

                        elif MAIN.modes.val("EDIT"):
                            MAIN.FIXTURES.clear()
                            self.data.exec_select(nr)
                            self.data.exec_go(nr,xfade=0,event=event,val=255,button="go")
                            MAIN.modes.val("EDIT", 0)
                            MAIN.master.refresh_fix()
                            MAIN.refresher_fix.reset() # = tkrefresh.Refresher()

                        elif MAIN.modes.val("SELECT"):
                            self.data.exec_select(nr)
                        else:
                            self.data.exec_go(nr,event=event,val=255)
                    else:
                        self.data.exec_go(nr,xfade=0,event=event,val=0)
                        #cprint(" == "*10)
                        MAIN.master.refresh_fix()
                        MAIN.refresher_fix.reset() # = tkrefresh.Refresher()

                        
                if event.num == 3:
                    if not MAIN.modes.val("REC"):
                        if str(event.type) == '4': #4 ButtonPress
                            self.data.exec_go(nr,xfade=0,ptfade=0,event=event,val=255)
                        else:
                            self.data.exec_go(nr,xfade=0,ptfade=0,event=event,val=0)
                        
                cprint()
                return 0
            elif self.mode == "INPUT":
                cprint()
                return 0

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        cprint()
        return 1 

class tk_event_fx():
    """ global input event Handeler for short cut's ... etc
    """
    def __init__(self,fix,elem,attr=None,data=None,mode=None):
        self.fix = fix
        self.data = data
        self.attr = attr
        self.elem = elem
        self.mode = mode

    def fx(self,event):
        cprint("Xevent.fx",self.attr,self.fix,event)
        fx2 = {}

        if self.attr == "FX:RED":
            if event.num == 4:
                cprint("FX:COLOR CHANGE",MAIN.fx_prm,color="red")
                txt = "FX:RED" 
                MAIN.fx_prm["MODE"] += 1
                if MAIN.fx_prm["MODE"] >= len(MAIN.fx_modes):
                    MAIN.fx_prm["MODE"]=0
                txt = "FX:\n"+MAIN.fx_modes[MAIN.fx_prm["MODE"]]

                MAIN.master.fx_color.elem["FX:RED"]["text"] = txt
            elif event.num == 5:
                cprint("FX:COLOR CHANGE",MAIN.fx_prm,color="red")
                txt = "FX:RED" 
                MAIN.fx_prm["MODE"] -= 1
                if MAIN.fx_prm["MODE"] < 0:
                    MAIN.fx_prm["MODE"]= len(MAIN.fx_modes)-1
                txt = "FX:\n"+MAIN.fx_modes[MAIN.fx_prm["MODE"]]
                MAIN.master.fx_color.elem["FX:RED"]["text"] = txt

        if self.attr.startswith("2D"):
            if event.num == 4:
                cprint("2D-X: CHANGE",MAIN.fx_prm,color="red")
                txt = "2D-X:" 
                MAIN.fx_prm["2D:MODE"] += 1
                if MAIN.fx_prm["2D:MODE"] >= len(fx_x_modes):
                    MAIN.fx_prm["2D:MODE"]=0
                txt = "2D:MODE\n"+fx_x_modes[MAIN.fx_prm["2D:MODE"]]

                MAIN.master.fx.elem["2D:MODE"]["text"] = txt
            elif event.num == 5:
                cprint("2D-X: CHANGE",MAIN.fx_prm,color="red")
                txt = "2D-X:" 
                MAIN.fx_prm["2D:MODE"] -= 1
                if MAIN.fx_prm["2D:MODE"] < 0:
                    MAIN.fx_prm["2D:MODE"]= len(fx_x_modes)-1
                txt = "2D:MODE\n"+fx_x_modes[MAIN.fx_prm["2D:MODE"]]
                MAIN.master.fx.elem["2D:MODE"]["text"] = txt

        elif event.num == 1:
            xfixtures = []
            fix_active =MAIN.FIXTURES.get_active() 
            for fix in fix_active:
                if fix == "CFG":
                    continue
                xfixtures.append(fix)

            if not xfixtures:
                cprint("470 fx() ... init no fixture selected",color="red")
                return 0
            
            
            xfixtures   = MAIN.process_matrix(xfixtures)
            wing_buffer = fxlib.process_wings(xfixtures,MAIN.fx_prm)
            fxlib.process_effect(
                        wing_buffer,MAIN.fx_prm,MAIN.fx_prm_move,MAIN.modes,
                        MAIN.jclient_send,MAIN.master,
                        MAIN.FIXTURES,fx_name=self.attr
                        )




    def command(self,event,mode=""):       
        cprint("fx_command",self.mode)
        if self.mode == "FX":
            prm = MAIN.fx_prm
            ct = self.data.fx 
        if self.mode == "FX-MOVE":
            prm = MAIN.fx_prm_move
            ct = self.data.fx_moves 

        if 1:
            if self.attr.startswith("SIZE:"):#SIN":
                #global MAIN.fx_prm
                k = "SIZE"
                if event.num == 1:
                    _stats = [0,30,100,255]
                    if prm[k] in _stats:
                        idx = _stats.index(prm[k])+1
                        if idx > len(_stats)-1: #rotate
                            idx = 0
                        prm[k] = _stats[idx]
                    else:
                        prm[k] = _stats[1]
                elif event.num == 3:
                    prm[k] =100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] +=5
                elif event.num == 5:
                    prm[k] -=5
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 0:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5
                ct.elem[self.attr]["text"] = "SIZE:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("SPEED:"):#SIN":
                #global prm
                k = "SPEED"
                if event.num == 1:
                    _stats = [0,5,25,30,100,255]
                    if prm[k] in _stats:
                        idx = _stats.index(prm[k])+1
                        if idx > len(_stats)-1: #rotate
                            idx = 0
                        prm[k] = _stats[idx]
                    else:
                        prm[k] = 0
                elif event.num == 3:
                    prm[k] = 10
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 0.06
                    elif prm[k] < 5:
                        prm[k] *=1.2
                    else:
                       prm[k] +=5 #1.1
                elif event.num == 5:
                    if prm[k] <= 5:
                        prm[k] *=0.8
                    else:
                        prm[k] -= 5 #1.1
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 0.05:
                    prm[k] =0
                if prm[k] > 5 and prm[k] < 10: #bug
                    prm[k] =5

                if prm[k] < 0:
                    ct.elem[self.attr]["text"] = "SPEED:\noff".format(prm[k])
                else:
                    ct.elem[self.attr]["text"] = "SPEED:\n{:0.02f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("START:"):#SIN":
                #global prm
                k = "START"
                if event.num == 1:
                    pass
                elif event.num == 2:
                    pass
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] += 5 #1.1
                elif event.num == 5:
                    prm[k] -= 5 #1.1
                #prm[k] =int(prm[k])
                
                if prm[k] > 4000:
                    prm[k] = 4000
                if prm[k] < 5:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5

                ct.elem[self.attr]["text"] = "START:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("WIDTH:"):#SIN":
                #global prm
                k = "WIDTH"
                if event.num == 1:
                    _stats = [0,25,50,75,10]
                    if prm[k] in _stats:
                        idx = _stats.index(prm[k])+1
                        if idx > len(_stats)-1: #rotate
                            idx = 0
                        prm[k] = _stats[idx]
                    else:
                        prm[k] = 25
                elif event.num == 2:
                    prm[k] = 50
                elif event.num == 3:
                    prm[k] = 100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    elif prm[k] == 50:
                        prm[k] = 100
                    elif prm[k] == 5:
                        prm[k] = 25
                    elif prm[k] == 25:
                        prm[k] = 50
                    else:
                        prm[k] += 5 #*=1.1
                elif event.num == 5:
                    if prm[k] == 10:
                        prm[k] = 5
                    elif prm[k] == 25:
                        prm[k] = 10
                    elif prm[k] == 50:
                        prm[k] = 25
                    elif prm[k] == 100:
                        prm[k] = 50
                    #else:
                    #    prm[k] -=5 #/=1.1
                    
                #prm[k] =int(prm[k])
                
                if prm[k] < 0:
                    prm[k] = 0
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] == 6: #bug
                    prm[k] =5
                if prm[k] > 25 and prm[k] < 50: #bug
                    prm[k] =50
                if prm[k] > 50 and prm[k] < 75: #bug
                    prm[k] =75
                if prm[k] > 75 and prm[k] < 100: #bug
                    prm[k] =100

                ct.elem[self.attr]["text"] = "WIDTH:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("DIR:"):#SIN":
                #global prm
                k = "DIR"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = -1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =-1
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "DIR:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("SHUFFLE:"):#SIN":
                #global prm
                k = "SHUFFLE"
                if event.num == 1:
                    prm[k] = 0
                elif event.num == 3:
                    prm[k] = 1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =0
                if prm[k] == 6: #bug ?
                    prm[k] =5
                ct.elem[self.attr]["text"] = k+":\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("INVERT:"):#SIN":
                #global prm
                k = "INVERT"
                if event.num == 1:
                    prm[k] = 0
                elif event.num == 3:
                    prm[k] = 1
                elif event.num == 4:
                    prm[k] = 1
                elif event.num == 5:
                    prm[k] =0
                if prm[k] == 6: #bug ?
                    prm[k] =5
                ct.elem[self.attr]["text"] = k+":\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("2D-X:"):#SIN":
                #global prm
                k = "2D-X"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = 2
                elif event.num == 4:
                    prm[k] += 1
                elif event.num == 5:
                    prm[k] -=1
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] < 1:
                    prm[k] =1
                    
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "2D-X:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("WING:"):#SIN":
                #global prm
                k = "WING"
                if event.num == 1:
                    prm[k] = 1
                elif event.num == 3:
                    prm[k] = 2
                elif event.num == 4:
                    prm[k] += 1
                elif event.num == 5:
                    prm[k] -=1
                if prm[k] > 100:
                    prm[k] = 100
                if prm[k] < 1:
                    prm[k] =1
                    
                txt = prm[k] 
                ct.elem[self.attr]["text"] = "WING:\n{}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("OFFSET:"):#SIN":
                #global prm
                k = "OFFSET"
                if event.num == 1:
                    prm[k] = 50
                elif event.num == 2:
                    prm[k] *= 2
                elif event.num == 3:
                    prm[k] = 100
                elif event.num == 4:
                    if prm[k] <= 0:
                        prm[k] = 1
                    prm[k] +=5 #*=1.1
                elif event.num == 5:
                    prm[k] -=5 #/=1.1
                #prm[k] =int(prm[k])
                
                #if prm[k] > 512:
                #    prm[k] = 512
                if prm[k] < 5:
                    prm[k] =0
                if prm[k] == 6: #bug
                    prm[k] =5

                ct.elem[self.attr]["text"] = "OFFSET:\n{:0.0f}".format(prm[k])
                cprint(prm)
            elif self.attr.startswith("BASE:"):
                k = "BASE"
                if event.num == 1:
                    prm[k] = "-"
                elif event.num == 3:
                    prm[k] = "0"
                elif event.num == 4:
                    prm[k] = "+"
                elif event.num == 5:
                    prm[k] = "0"
                ct.elem[self.attr]["text"] = "BASE:\n{}".format(prm[k])
            elif self.attr.startswith("2D:"):#SIN":
                self.fx(event)
            elif self.attr.startswith("FX:"):#SIN":
                self.fx(event)

            elif self.attr == "FX OFF":
                if event.num == 1:
                    MAIN.FIXTURES.fx_off("all")
                    MAIN.CONSOLE.fx_off("all")
                    MAIN.CONSOLE.flash_off("all")
                    MAIN.master._refresh_fix()
                    return 0

                #if event.num == 1:
            elif self.attr == "REC-FX":
                cprint("ELSE",self.attr)
                MAIN.modes.val(self.attr,1)

            return 0
            
    def cb(self,event):
        cprint("EVENT_fx cb",self.attr,self.mode,event,color='yellow')
        cprint(["type",event.type,"num",event.num])
        try:
            change = 0

            if self.mode.startswith("FX"):
                self.command(event)
                return 0

        except Exception as e:
            cprint("== cb EXCEPT",e,color="red")
            cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
            cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")
        return 1 

