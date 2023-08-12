#!/usr/bin/python3

import tkinter as tk
import time
#import _thread as thread


def tk_btn_bg_loop(btn,c1="#00ff00",c2="#00f",stime=time.time()):
    while time.time() < stime+10:
        time.sleep(0.1)
    #time.sleep(10)
    print("tk_btn_loop",btn,c1,c2,"sleep 20")
    flip = 0
    change = 0
    t_last = time.time()
    try:
        while 1:
            #t = int(time.time()*1000)
            #if t % 500 == 0: 
            #    change = 1
            #    time.sleep(.001)
            #else: 
            #    time.sleep(.001)
            #    continue
            change = 1
            time.sleep(0.5)
            if change:
                #print(btn,"change",str(t)[:-3],btn["text"])

                if flip:flip = 0
                else:flip = 1

                if flip:c = c1
                else:c = c2

                btn["bg"] = c 
    except Exception as e:
        print(__file__,"loop() exception")
        print(e)
        time.sleep(3)

#usage
#thread.start_new_thread(tk_btn_bg_loop,(b,))



class MiniButton:
    def __init__(self,root,width=72,height=38,text="button"):
        self.text=text
        self.rb = tk.Frame(root, highlightbackground = "lightgrey", highlightthickness = 1, bd=0)
        self.bb = tk.Canvas(self.rb, highlightbackground = "black", highlightthickness = 1, bd=1,relief=tk.RAISED)
        self.bb.configure(width=width, height=height)
        self.fg = "#002"
        self.label = []
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        # !! BLOCK's other bindings like GO
        #self.bind("<Button-1>", self.on_b1)
        #self.bind("<ButtonPress>", self.on_press)
        #self.bind("<ButtonRelease>", self.on_release)
        #self.bind("<ButtonRelease-1>", self.on_release)
        self._last_label_id = 0
        self._label_ring = ["labelA","labelB"]
        self.activebackground="lightgrey"
        self.defaultBackground="grey"

    def on_b1(self, e):
        print("on_b1",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.SUNKEN)#abackground=self.activebackground)
        return 1
    def on_press(self, e):
        print("on_press",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.SUNKEN)#abackground=self.activebackground)
        return 1
    def on_release(self, e):
        print("on_release",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.RAISED)#abackground=self.activebackground)
        return 1
    def on_enter(self, e):
        #print("on_enter",e)
        #self.bb.config(background=self.activebackground)
        self.bb.config(relief=tk.FLAT)#abackground=self.activebackground)
        return 1

    def on_leave(self, e):
        #print("on_leave",e)
        self.bb.config(background=self.defaultBackground)
        self.bb.config(relief=tk.RAISED)#abackground=self.activebackground)
        return 1

    def _label(self,text="1\n2\n3\n"):
        z = 0
        tag = self._label_ring[self._last_label_id]
        #self.bb.delete("label")
        self.label = []
        for t in text.split("\n"):
            self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag)
            #self.l["color"] = self.fg
            self.label.append(self.l)
            
            z+=1
        self.delete_tag()
    def delete_tag(self):
        self._last_label_id += 1
        if self._last_label_id >=len(self._label_ring ):
            self._last_label_id = 0
        tag = self._label_ring[self._last_label_id]
        self.bb.delete(tag)

    def _configure(self,**args):
        if "text" in args:
            if self.text != args["text"]:
                self.text = args["text"]
                self._label(self.text)
        if "bg" in args:
            #print(dir(self.bb))
            self.bb.configure(bg=args["bg"])
            self.defaultBackground=args["bg"]
        if "fg" in args:
            #print(dir(self.bb))
            self.fg=args["fg"]
            #if len(self.label):
            #    self.label[0].configure(color="red") #args["fg"])
            #self.defaultBackground=args["fg"]
    def configure(self,**args):
        self._configure(**args)
    def config(self,**args):
        self._configure(**args)
    def bind(self,etype="<Button>",cb=None):
        #bb.bind("<ButtonRelease>",Xevent(fix=0,elem=b,attr=k,data=self,mode="PRESET").cb)
        if cb:
            self.bb.bind(etype,cb)
    def grid(self,row=0, column=0, sticky=""):
        self.bb.pack() #(row=row, column=column, sticky=sticky)
        self.rb.grid(row=row, column=column, sticky=sticky)
 


class ExecButton(MiniButton):
    def __init__(self,root,width=72,height=38,text="button"):
        #self.text = "1\n2\n3\n"
        super().__init__(root,width,height,text)
        self.x9font = tk.font.Font(family="FreeSans", size=9, weight="bold")
        self.x8font = tk.font.Font(family="FreeSans", size=8, weight="bold")
        self.x7font = tk.font.Font(family="FreeSans", size=7, weight="bold")
        self.x6font = tk.font.Font(family="FreeSans", size=6, weight="bold")
        self.x5font = tk.font.Font(family="FreeSans", size=5, weight="bold")
        #print(self,"init()",[self.text])
    def config(self,**args):
        self._configure(**args)
        self._label()
    def configure(self,**args):
        self._configure(**args)
        self._label()
    def dbg_info(self):
        print(self,"_label()",[self.text])
        for i in dir(self.bb):
            print("-",i)
    def _label(self,text=None):
        if type(text) is str:
            if self.text == text:
                return
            self.text = text
        else:
            text = self.text[:]
        
        tag = self._label_ring[self._last_label_id]
        #self.bb.delete("labelB")
        #self.bb.delete("labelA")
        txt2 = text
        try:
            text = text.split("\n")[1]
        except:pass


        if "grün" in text.lower() or "green" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="green",tag=tag)
        elif "purple" in text.lower() or "purple" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#800080",tag=tag)
        elif "lime" in text.lower() or "lime" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#00ff00",tag=tag)
        elif "blau" in text.lower() or "blue" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="blue",tag=tag)
        elif "rot" in text.lower() or "red" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="red",tag=tag)
        elif "orange" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="orange",tag=tag)
        elif "weiß" in text.lower() or "white" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="white",tag=tag)
        elif "cyan" in text.lower():# or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="cyan",tag=tag)
        elif "gelb" in text.lower() or "yellow" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="yellow",tag=tag)
        elif "pink" in text.lower() or "pink" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="#ff69b4",tag=tag)
        elif "mage" in text.lower() or "mage" in text.lower():
            self.l = self.bb.create_rectangle(10,29,20,39,fill="magenta",tag=tag)

        if "nebel" in text.lower()  or "smoke" in text.lower() or "haze" in text.lower():
            self.l = self.bb.create_rectangle(10,29,60,39,fill="white",tag=tag)
        if "mh " in text.lower() or " mh" in text.lower() :
            self.l = self.bb.create_rectangle(30,29,35,32,fill="black",tag=tag)
            self.l = self.bb.create_rectangle(28,34,37,39,fill="black",tag=tag)
        if "off" in text.lower(): 
            self.l = self.bb.create_rectangle(50,30,55,35,fill="black",tag=tag)
        if "dim" in text.lower() or "front" in text.lower()  or "on" in text.lower(): 
            #self.l = self.bb.create_line(56,30,60,28,fill="black",tag=tag)
            self.l = self.bb.create_rectangle(50,30,55,35,fill="white",tag=tag)
            #self.l = self.bb.create_line(56,36,58,36,fill="black",tag=tag)
        if "circle" in text.lower(): 
            self.l = self.bb.create_oval(30,29,40,39,fill="",tag=tag)
        if "pan" in text.lower(): 
            self.l = self.bb.create_line(20,34 ,45,34,fill="black",arrow=tk.BOTH,tag=tag)
        if "tilt" in text.lower(): 
            self.l = self.bb.create_line(30,25 ,30,43,fill="black",arrow=tk.BOTH,tag=tag)

        text = txt2
        z = 0
        for t in text.split("\n"):
            ts = 10
            _max = 7
            if z==1 and len(t) >= _max:
                ts = int(10 - (len(t)-_max)/1.5)
                if ts < 5:
                    ts = 5
                xfont = self.x9font
                if 1:
                    if ts == 9:
                        xfont = self.x9font
                    elif ts == 8:
                        xfont = self.x8font
                    elif ts == 7:
                        xfont = self.x7font
                    elif ts == 6:
                        xfont = self.x7font
                    elif ts == 5:
                        xfont = self.x7font

                if len(t) > 14:
                    t2 = t[:14]
                    t3 = t[14:]
                    self.l = self.bb.create_text(37,z*10+9-2,text=t2,anchor="c",tag=tag,fill=self.fg,font=xfont)
                    self.l = self.bb.create_text(37,z*10+9+6,text=t3,anchor="c",tag=tag,fill=self.fg,font=xfont)
                else:
                    self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg,font=xfont)
                #self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg)
            else:
                self.l = self.bb.create_text(37,z*10+9,text=t,anchor="c",tag=tag,fill=self.fg)
            z+=1
        #self.bb.update(0)
        #self.bb.after(0)

        self.delete_tag()
