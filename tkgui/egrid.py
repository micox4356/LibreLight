#!/usr/bin/python3

import sys
import os

event_que = []
print( os.getcwd())
try:
    import lib.zchat as chat
    print(sys.path)
except ModuleNotFoundError:
    sys.path.insert(0,os.path.dirname(__file__)+"/.." )
    print(sys.path)
    import lib.zchat as chat

import tkinter as tk
value = 1
data = []

class Event():
    def __init__(self,name):
        self.name=name
        print("init",self)
    def event(self,event):
        global value
        global event_que
        print(self.name,event)
        print("event:",[int(event.type),event.num])

        lock.acquire_lock()
        print(lock.locked())
        event_que.append([self,event])
        lock.release()

        if int(event.type) == 4:
            if event.num == 4:
                value +=1
            if event.num == 5:
                value -=1
            print(value)

        for e in data:
            t = e["text"]
            if ":" in t:
                t = t.split(":")[0]
            e["text"] = t +": "+ str(value)
                

class scroll():
    def __init__(self,canvas):
        self.canvas=canvas
    def config(self,event):
        canvas = self.canvas
        canvas.configure(scrollregion=canvas.bbox("all"))#,width=400,height=200)



def ScrollFrame(root,width=50,height=100,bd=1,bg="black",scrollbar="xy"):
    _scrollbar = scrollbar 
    #print("ScrollFrame init",width,height)
    aframe=tk.Frame(root,relief=tk.GROOVE)#,width=width,height=height,bd=bd)
    #aframe.place(x=0,y=0)
    aframe.pack(side="top",fill="both",expand=1) #x=0,y=0)

    canvas=tk.Canvas(aframe,width=width-24,height=10)#height)
    if bg == "":
        bg="orange"
    canvas["bg"] = bg # "black" #"green"
    bframe=tk.Frame(canvas,width=width,height=height)
    bframe["bg"] = "blue"
    scrollbar_y=tk.Scrollbar(aframe,orient="vertical",command=canvas.yview,width=20)
    canvas.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x=tk.Scrollbar(aframe,orient="horizontal",command=canvas.xview,width=20)
    canvas.configure(xscrollcommand=scrollbar_x.set)
    if "x" in _scrollbar:
        scrollbar_x.pack(side="bottom",fill="x")
    if "y" in _scrollbar:
        scrollbar_y.pack(side="right",fill="y")
    canvas.pack(side="left",expand=1,fill="both")
    canvas.create_window((0,0),window=bframe,anchor='nw')

    bframe.bind("<Configure>",scroll(canvas).config)

    canvas.bind("<Button>",Event("XXX").event)
    canvas.bind("<Key>",Event("XXX").event)
    canvas.bind("<KeyRelease>",Event("XXX").event)
    return bframe
#frame = ScrollFrame(root)



root = tk.Tk()
# set window title
root.wm_title("Fixture Editor")
i=0
#root.bind("<Button>",Event("M:{}".format(i)).event)
#root.bind("<Key>"   ,Event("M:{}".format(i)).event)
#root.bind("<KeyRelease>",Event("M:{}".format(i)).event)

aframe = tk.Frame(root,height=10) #,bg="#fff")
aframe.pack(side="top",expand=0,fill="both")
aframe.bind("<Button>",Event("H:{}".format(i)).event)
aframe.bind("<Key>"   ,Event("H:{}".format(i)).event)
aframe.bind("<KeyRelease>",Event("H:{}".format(i)).event)
i=0
l = tk.Button(aframe,text="MENUE ".format(i+1))
l.grid(row=i,column=0)

aframe = tk.Frame(root,height=5,bg="#333")
aframe.pack(side="top",expand=0,fill="x")

#xframe = ScrollFrame(root,width=300,height=300)
xframe = ScrollFrame(root,width=300,height=300,scrollbar="xy")
i=0
for x in range(40):
    for y in range(10):
        l = tk.Button(xframe,text="Eintrag {}: 0".format(i+1),width=12)
        l.bind("<Button>",Event("  B1:{}".format(i)).event)
        #l.bind("<Key>",Event("B2:{}".format(i)).event)
        #l.bind("<KeyRelease>",Event("B3:{}".format(i)).event)
        data.append(l)
        l.grid(row=x,column=y)
        i+=1

aframe = tk.Frame(root,height=5,bg="#333")
aframe.pack(side="top",expand=0,fill="x")

bframe = tk.Frame(root ) #,bg="#fff")
bframe.pack(side="top",expand=0,fill="both")
bframe.bind("<Button>",Event("B:{}".format(i)).event)
bframe.bind("<Key>"   ,Event("B:{}".format(i)).event)
bframe.bind("<KeyRelease>",Event("B:{}".format(i)).event)

i=1
l = tk.Button(bframe,text="STATUS BAR {}".format(i+1))
l.grid(row=i,column=0)



import _thread as thread
import time



def loop():
    global event_que 
    time.sleep(3)
    c = chat.Client(port=51111)
    i=0
    while 1:
        lock.acquire_lock()
        #print(lock.locked())
        _event_que = event_que[:]
        event_que = []
        lock.release()
        #print(_event_que)

        for i in _event_que:
            print(i)
            c.send(str(i[1]).encode("ascii"))
        
        #c.send(s.encode("ascii"))
        #s = "hi {}".format(i)
        #print(s)
        #c.send(s.encode("ascii"))
        #i+=1
        #time.sleep(1)
        #r=c.read()
        #print(r)
        time.sleep(0.02)

thread.start_new_thread(loop,())
lock = thread.allocate_lock()

if 1:
    # lock example
    print(lock.locked())
    lock.acquire_lock()
    print(lock.locked())
    lock.release()
    print(lock.locked())

# show window
root.geometry("400x500")
#root.width=400
#root.config({"height":400})
#root.config(width=360, height=315)
#root.itemconfigure(height=400)
#root["height"] = 400
root.mainloop()


