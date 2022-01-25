
import tkinter as tk

def r():
    canvas=tk.Canvas(xframe,width=600,height=100)
    canvas["bg"] = "yellow" #"green"
    canvas.pack()
    # RGB
    x=0
    y=0
    j=0
    d = 20
    f = 255 #255-fi
    e = 5
    for r in range(0,d+1):
        fi = int(r*255/d)
        color = '#%02x%02x%02x' % (f, fi, fi) 
        print( "farbe", r*10, j, f,fi,fi,color)
        r = canvas.create_rectangle(x, y, x+20, y+20, fill=color)
        x+=20


def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) 

def _cb(event,data={}):
    print("dummy cb",event)

class cb():
    def __init__(self,win,cb=None):
        self.win = win
        if cb:
            self.cb = cb
        else:
            self.cb = _cb 
    def _callback(self,event):
        clobj=event.widget
        ## undermouse=find_withtag(master.CURRENT)
        undermouse=self.win.find_closest(self.win.CURRENT)
        print( repr(undermouse))
    def callback(self,event):
        cnv = self.win
        item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
        tags = cnv.gettags(item)
        #cnv.itemconfigure(self.tag, text=tags[0])
        print(tags,item)
        color = cnv.itemcget(item, "fill")
        cnv.itemconfig("all", width=1)#filla="green")
        cnv.itemconfig(item, width=3)#filla="green")
        print(color)
        int_color= hex_to_rgb(color[1:])
        print(int_color)
        self.cb(event,{"canvas":cnv,"color":int_color})


def colorpicker(xframe,width=600,height=100,xcb=None):
    canvas=tk.Canvas(xframe,width=width,height=height)
    canvas["bg"] = "grey" #"green"
    _callback = cb(canvas,xcb)

    #canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", _callback.callback)
    canvas.pack()

    x=2
    y=2
    d = 3
    r=0
    g=1
    b=1
    mode = 0
    count = 0
    while 1:
        print("-",[r,g,b],mode)
        for xx in range(d,0,-1):
            fi = int(xx*255/d)
            print(xx,y)
            print(fi,end=" ")
            color = '#%02x%02x%02x' % (int(255-r*fi),int(255-g*fi),int(255-b*fi)) 
            canvas.create_rectangle(x, y, x+20, y+20, fill=color)
            
            y+=22
        color = '#%02x%02x%02x' % (255,255,255) 
        canvas.create_rectangle(x, y, x+20, y+20, fill=color)
        print()
        if count == 1 and mode == 3:
            print("-------")
            break
        y=2
        x+=22
        if r >= 1 and g >= 1 and b <= 0:
            mode = 1
        elif r <= 0 and g >= 1 and b <= 0:
            mode = 2
        elif r <= 0 and g >= 1 and b >= 1:
            mode = 3
        elif r <= 0 and g <= 0 and b >= 1:
            mode = 4
        elif r >= 1 and g <= 0 and b >= 1:
            mode = 5
        elif r >= 1 and g <= 0 and b <= 0:
            mode = 6
            count +=1

        s = 0.25 # 1/d #0.25
        if mode == 1:
            r -= s#0.25
        if mode == 2:
            b += s#0.25
        if mode == 3:
            g -= s#0.25
        if mode == 4:
            r += s#0.25
        if mode == 5:
            b -= s#0.25
        if mode == 6:
            g += s#0.25

        if r > 1:
            r=1
        if g > 1:
            g=1
        if b > 1:
            b=1

        if r < 0:
            r=0
        if g < 0:
            g=0
        if b < 0:
            b=0
    
if __name__ == "__main__":
    xframe = tk.Tk() 
    xframe.geometry("1600x600")
    r()
    colorpicker(xframe)
    xframe.mainloop()
