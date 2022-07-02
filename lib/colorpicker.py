
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
    def __init__(self,win,cb=None,scale=None):
        self.scale=scale
        self.win = win
        self.int_color = [255,255,255]
        if cb:
            self.cb = cb
        else:
            self.cb = _cb 
    def _callback(self,event):
        clobj=event.widget
        ## undermouse=find_withtag(master.CURRENT)
        undermouse=self.win.find_closest(self.win.CURRENT)
        print( "colorpicker._callback",repr(undermouse))
    def callback(self,event):
        cnv = self.win

        try:
            item = cnv.find_closest(cnv.canvasx(event.x), cnv.canvasy(event.y))[0]
            tags = cnv.gettags(item)
            #cnv.itemconfigure(self.tag, text=tags[0])
            print("colorpicker callback",tags,item)
            color = cnv.itemcget(item, "fill")
            cnv.itemconfig("all", width=1)#filla="green")
            cnv.itemconfig(item, width=3)#filla="green")
            print("picker",color)
            self.int_color= hex_to_rgb(color[1:])
        except AttributeError as e:
            print("except colorpicker ",e)
            print("take old last",self.int_color)
        print("picker",self.int_color)
        int_color2 = []
        for c in self.int_color:
            if self.scale is not None:
                x = int(c *self.scale.get()/99)
                print(c,x)
                int_color2.append(x)
            else:
                int_color2.append(c)


        self.cb(event,{"canvas":cnv,"color":int_color2})


def colorpicker(xframe,width=500,height=100,xcb=None):
    canvas=tk.Canvas(xframe,width=width,height=height)
    canvas["bg"] = "grey" #"green"
    _scale = tk.Scale(xframe,repeatdelay=1000,resolution=5,showvalue=0,bg="black", width=10,length=110,from_=99,to=0)##,command=self.event)
    _scale.set(255)
    _callback = cb(canvas,xcb,_scale)

    #canvas.bind("<Key>", key)
    canvas.bind("<Key>", _callback.callback)
    canvas.bind("<Button-1>", _callback.callback)
    canvas.bind("<Button-2>", _callback.callback)
    canvas.bind("<Button-3>", _callback.callback)
    canvas.bind("<Button-4>", _callback.callback)
    canvas.bind("<Button-5>", _callback.callback)
    canvas.bind("<B1-Motion>", _callback.callback)
    canvas.bind("<B2-Motion>", _callback.callback)
    canvas.bind("<B3-Motion>", _callback.callback)
    canvas.bind("<B4-Motion>", _callback.callback)
    canvas.bind("<B5-Motion>", _callback.callback)
    canvas.pack(side="left")
    def scale_callback(data=[]):
        #_last_scale = time.time()
        print("scale_callback",data)
        _callback.callback(None) #data)
    #_scale.config(command=_callback.callback)
    _scale.config(command=scale_callback) 
    _scale.pack(side="left")

    x=2
    y=2
    d = 3
    r=0
    g=1
    b=1
    mode = 0
    count = 0
    grey = 0
    while 1:
        #print("-",[r,g,b],mode)
        for xx in range(d,0,-1):
            fi = int(xx*255/d)
            #print(xx,y)
            #print(fi,end=" ")
            color = '#%02x%02x%02x' % (int(255-r*fi),int(255-g*fi),int(255-b*fi)) 
            canvas.create_rectangle(x, y, x+20, y+20, fill=color)
            
            y+=22
        color = '#%02x%02x%02x' % (255,255,255) 
        canvas.create_rectangle(x, y, x+20, y+20, fill=color)
        
        y+=22
        if grey <= 255:
            color = '#%02x%02x%02x' % (grey,grey,grey) 
            canvas.create_rectangle(x, y, x+20, y+20, fill=color)
        grey +=255//25
        #print()
        if count == 1 and mode == 3:
            #print("-------")
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

    #print(dir(_b))
    #input()
    #b.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    #b = canvas.create_window(10, 10, anchor="nw", window=f)

    #self.b.pack(fill=tk.Y, side=tk.TOP)
    #self.elem.append(self.b)
    
if __name__ == "__main__":
    xframe = tk.Tk() 
    xframe.geometry("1600x600")
    r()
    colorpicker(xframe)
    xframe.mainloop()
