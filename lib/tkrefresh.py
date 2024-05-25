#!/usr/bin/python3

import time
import sys
from lib.cprint import cprint
import traceback

import __main__ as MAIN
    



class Refresher():
    def __init__(self):
        self.time = time.time()
        self.time_max = time.time()
        self.time_delta = 15
        self.update = 1
        self.name = "name" # exec
        self.cb = None #self.dummy_cb
    def dummy_cb(self):
        cprint("dummy_cd()",time.time()-self.time)

    def reset(self):
        self.time = time.time() 
        self.update = 1

    def refresh(self):
        if self.update: 
            if self.time+self.time_delta < time.time():
                self._refresh()
        else:
            self.time = time.time() 

    def _refresh(self):
        cprint("_refresh()",self.name,self)
        if not MAIN.INIT_OK:
            return

        self.time_max = time.time()
        self.time     = time.time()
        self.update = 0
        try:
            if self.cb:
                self.cb()
            else:
                self.dummy_cb()
        except Exception as e:
            cprint("_refresh except:",e,"cb:",self.cb,color="red")
            traceback.print_exc()
            cprint()
        cprint("t=",self.time_max- time.time())

    def loop(self,args={}):
        while 1:
            try:
                if MAIN.INIT_OK:
                    self.refresh()
                    #tkinter.Tk.update_idletasks(gui_menu_gui.tk)
            except Exception as e:
                traceback.print_exc()
                cprint("== cb EXCEPT",e,color="red")
                cprint("Error on line {}".format(sys.exc_info()[-1].tb_lineno),color="red")
                cprint(''.join(traceback.format_exception(None, e, e.__traceback__)),color="red")

            time.sleep(0.2)
