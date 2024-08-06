#/usr/bin/python3

import time
from pyray import *
import pyray 

for i in dir(pyray):
    if "path" in i.lower():
        print(i)
print()
print(pyray.FilePathList)
print(pyray.get_directory_path)
input()


ConfigFlags(FLAG_MSAA_4X_HINT) #|FLAG_WINDOW_RESIZABLE  )
ConfigFlags(FLAG_WINDOW_HIGHDPI )
init_window(800, 450, "TITLE",10,10,10,10)

import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import tool.tk_elm as tk_elm

img = "/opt/LibreLight/Xdesk/icon/scribble.png"
IMG = load_image(img)
print(set_window_icon(IMG)) 

a = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
a = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
a = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
a = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"

k=200
i= 40 
i= 140 
#font1 = load_font_ex(a, i, None, 0);
font1 = load_font_ex(a, i, None, 0);

input()


start = time.time()
frame_count = 0
fps_count = 0

GRAY   = [127,127,127,255] 
RED    = [255,0,0,255]
YELLOW = [255,255,0,255]  
WHITHE = [255,255,255,255] 

def get_font_hight(x):
    return 10

class Layout():
    def __init__(self,master):
        self.master = master
    def pack(self,**args):
        pass
    def grid(self,**args):
        pass
    def bind(self,**args):
        pass


class CALLBACK():
    def __init__(self):
        self._cb  = self.dummy
        self.ok = 0
    def cb(self,*args):
        if self.ok:
            print("CALLBACK.cb",args)
            #try:
            self._cb(args)
            #except Exception as e:
            #    print(" Exception CALLBACK.cb",args)
    def dummy(self,arg):
        print("CALLBACK.dummy",arg)
    def set(self,cb):
        self._cb = cb
        self.ok = 1
        print("CALLBACK",cb)

def check_rgb(rgb):
    rgb_out = [127,127,127,127]
    try:    
        for i,v in enumerate(rgb):
            if v > 255:
                v = 255
            if v < 0:
                v = 0
            rgb_out[i] = v

    except Exception as e:
        print("rgb exception ",e)

    return rgb_out

class ELEM_BUF():
    def __init__(self,kill=None,name="ELEM_BUF"):
        self.val = VALUE() #0
        self.increment = 10 
        self.name = name
        self.cb_on  = CALLBACK()
        self.cb_off = CALLBACK()
        self.nr_on  = [0]
        self.nr_off = [0]
        self.color = [0,255,0]
        self.color_on = [255,255,0]
        self.type="flash" #"toggle" #"flash",fade
        self.killgroup = kill 
        self.events = []
    def _rep__(self):
        x="<ELEM_BUF name:{} val:{} id:{}>".format(self.name,self.val.get(), id(self))
    def get_event(self):
        out = self.events[:]
        self.events = []
        return out

    def get(self):
        return self.val.get()

    def get_color(self):
        if self.val.get():
            return self.color_on
        return self.color

    def clean(self):
        self.val.set(0)

    def press(self):
        #print("ELEM_BUF.press",[self.name,self.type,self.val.get()])
        if self.type == "fader":
            self.inc(self.increment)

        if self.type == "toggle":
            if self.val.get():
                self.val.set(0)
            else:
                self.val.set(1)

        if self.type == "flash":
            self.val.set(1)
        
        self.events.append("press")
        self.cb_on.cb("ho")

    def release(self):
        if self.type == "fader":
            self.inc(-self.increment)
        if self.type == "flash":
            self.val.set(0)
        self.events.append("release")

    def inc(self,v):
        self.val.inc(v)

class VALUE():
    def __init__(self,v=0,_min=0,_max=255):
        self._val = v
        self._max = _max
        self._min = _min

    def _check(self):
        if self._val > self._max:
            self._val = self._max
        if self._val < self._min:
            self._val = self._min

    def get(self):
        self._check()
        return self._val

    def set(self,val):
        if val <= self._max and val >= self._min:
            self._val = val

    def inc(self,v):
        self._val += v
        self._check()


def draw_rect(rgb,pos):
    #pygame.draw.rect(self.window,rgb,pos2)
    xpos = pos[:]
    xpos = [pos[0],pos[0],pos[0],pos[0]]
    xpos = pos[:]
    xpos = [pos[0],pos[0],pos[0],pos[0]]
    x1 = pos[0]
    y1 = pos[1]
    w = pos[2]
    h = pos[3]
    x2 = pos[0]+w
    y2 = pos[1]+h

    #draw_line(x1, y1, x1+200, x2+200, rgb)
    #draw_line(30, 300, 30, 900, [255,255,255])
    #draw_line(pos[0], pos[1], pos[2], pos[3], rgb)
    #draw_line(pos[0], pos[1], pos[2], pos[3], rgb)
    #draw_line(pos[0], pos[1], pos[2], pos[3], rgb)

class Button():
    def __init__(self,window,pos):
        self.window = window
        self.event_pos = [0,0]
        self.font0 = font1 #pygame.font.SysFont("freesans-bold",16)
        self.w = 20
        self.h = 10
        self.pos = pos
        self.rel_pos = [0,0]
        self.fader = "h" #v
        self.ATTR = "XX"
        self.ID = "0"

        self.btn1 = ELEM_BUF() 
        self.btn1.name = "BUTTON"
        self.btn1.nr_on  = [1,3]
        self.btn1.nr_off = [1,3]
        #self.btn1.color = LIGHTGRAY 
        self.btn1.color = GRAY 
        self.btn1.color_on = RED 

        self.btn2 = ELEM_BUF() # sel elem
        self.btn2.name = "SELECT BUF"
        self.btn2.nr_on  = [2]
        self.btn2.nr_off = [0]
        self.btn2.color = GRAY 
        self.btn2.color_on = YELLOW
        self.btn2.type = "toggle"

        self.btn3 = ELEM_BUF() 
        self.btn3.name = "MOUSE FOCUS"
        self.btn3.color = GRAY 
        self.btn3.color_on = WHITHE

        self.btn4 = ELEM_BUF() 
        self.btn4.name = "MOUSE ENCODER"
        self.btn4.increment = 4.4
        self.btn4.type = "fader"
        self.btn4.nr_on  = [4]
        self.btn4.nr_off = [5]
        self.btn4.color = GRAY 
        self.btn4.color_on = WHITHE

        self.btns = []
        self.btns.append(self.btn1)
        self.btns.append(self.btn2)
        self.btns.append(self.btn3)
        self.btns.append(self.btn4)

        self.__layout = Layout(self)
        self.pack = self.__layout.pack
        self.grid = self.__layout.grid
        self.bind = self.__layout.bind
        self.text = "line1\nline2"
        self.type = "toggle" # flash, kill
        self.dbg = 0
        self.text2 = []

    def __repr__(self):
        x="<sdl.BUTTON name:{} ID:{}-{:8} btn1:{:03} val2:{:03} id at {}>"
        x=x.format(self.btn1.name,self.ID,self.ATTR,self.btn1.val.get(),self.btn4.val.get(), id(self))
        return x
    def check(self):
        if self.dbg:
            self.text2 = []
            #self.text2.append(self.val)
            b = []
            for btn in self.btns:
                b.append(btn.get())
            self.text2.append(b)
            self.text2.append(self.btn1.type)

        self._check_event()
        self._check_min_hight()

    def draw(self,text="GOBO1"):
        self.check()

        #self.window.set_alpha(128)  

        self._draw_bg()
        self._draw_fader()
        self._draw_font(text="")
            
        #rgb = self.btn2.get_color()

        #self._draw_bd(color=rgb) 
        #self._draw_bd(delta=-1)

        #rgb = self.btn3.get_color()
        #self._draw_bd(delta=-2,color=rgb)

    def get_rect(self):
        self.check()
        return self.pos[:]


    def _check_min_hight(self):
        c = 1+ self.text.count("\n") #+1
        c += len(self.text2)

        fh = get_font_hight(self.font0)
        h = (fh+1)*c +6#8 #+8
        
        if self.pos[3] < h:
            self.pos[3] = h #ah+20

    def _draw_bg(self):
        pos = self.pos

        rgb = self.btn1.get_color()
        rgb = check_rgb(rgb)
        #pygame.draw.rect(self.window,rgb,pos)
        #draw_line(pos[0], pos[1], pos[0]+pos[2], pos[1]+pos[3], (255,225,0,220))
        draw_rectangle(int(pos[0]),int(pos[1]),pos[2],pos[3],rgb)

    def _draw_fader(self):
        rgb = [0,200,0]
        rgb = self.btn4.color_on
        pos2 = self.pos[:]
        hight = pos2[3] 
        v = self.btn4.val.get() #self.val.get()
        fh = get_font_hight(self.font0)
        _max_val = self.btn4.val._max
        if self.fader == "h":
            pos2[1] += 2 #fh+2
            pos2[3] = 4 #fh+2
            if v > 0: 
                pos2[2] = int(pos2[2]* v/_max_val)
            else:
                pos2[2] = 4
            #pygame.draw.rect(self.window,rgb,pos2)
            draw_line(pos2[0], pos2[1], pos2[0]+pos2[2], pos2[1], rgb)
        elif self.fader == "v":
            if v > 0: 
                pos2[1] += int((hight-20)* v/_max_val)
                pos2[3] = 20
            else:
                pos2[3] = 20 
            pos2[0] += 6
            pos2[2] -= 12 
            # pygame.draw.rect(self.window,rgb,pos2)
            draw_line(pos2[0], pos2[1], pos2[0]+pos2[2], pos2[1], rgb)

    def _draw_font(self,text=""):
        pos = self.pos

        a = pos[0]+4
        r = pos[1]+2
        v = "{:4.02f}".format(self.btn4.val.get()) 

        lines = self.text.split("\n")
        lines.extend(self.text2)

        draw_rect([255,0,0],pos)

        for i in lines:
            i = str(i)
            if "<ival%>" in i:
                v=float(v)
                v=v/self.btn4.val._max*100
                v=int(v)
                i = i.replace("<ival%>",str(v))
            if "<ival>" in i:
                i = i.replace("<ival>",str(int(float(v))))
            if "<val>" in i:
                i = i.replace("<val>",v)
            #fr = self.font0.render(i ,1, (0,0,0))
            draw_text_ex(self.font0,i, [a,r], font_size, 0, YELLOW)
            #draw_rectangle(int(pos[0]+1),int(pos[1]+1),pos[2]-2,pos[3]-2,[250,0,255])
            #draw_rect([255,0,0],pos)

            #fr_r=fr.get_rect()
            #p2 = [pos[0]+4,r,fr_r[2],fr_r[3]]
            #if 0:# dbg # bg highlight
            #    pygame.draw.rect(self.window,[0,0,255],p2)

            #self.window.blit(fr,(a,r))
            #r+=fr_r[3]+1
            r+=int(pos[3]/2)

    def _set_mouse_focus(self,state):
        if state:
            self.btn3.press() # mouse focus on
        else:
            self.btn3.release()

    def _check_event(self):
        pass
    def _draw_bd(self,delta=0,color=GRAY):#BLACK):
        l_pos = draw_bd(pos=self.pos,delta=delta)
        for i in l_pos:
            pygame.draw.aaline(self.window,color,i[0],i[1],1)


    def event(self,event=None):
        r_event = {}
        if "pos" in event.dict:
            self.event_pos = event.pos[:]

            
            update_rel_pos = 0
            if "buttons" in event.dict:
                if event.dict["buttons"][0]:
                    update_rel_pos = 1

            if "button" in event.dict:
                if event.dict["button"] == 1:
                    update_rel_pos = 1

            if update_rel_pos:
                    rel = [0,0]
                    rel[0] = self.event_pos[0] -self.pos[0]-4
                    rel[0] = rel[0]/(self.pos[2]-8)
                    rel[1] = self.event_pos[1] -self.pos[1]-4
                    rel[1] = rel[1]/(self.pos[3]-8)

                    if rel[0] < 0:
                        rel[0] = 0
                    if rel[0] > 1:
                        rel[0] = 1

                    if rel[1] < 0:
                        rel[1] = 0
                    if rel[1] > 1:
                        rel[1] = 1

                    #print("RELPOS",rel)
                    self.rel_pos = rel
            self._check_event()

        self._set_mouse_focus(0)
        if check_area(self.pos,self.event_pos):
            self._set_mouse_focus(1)


            if "button" in event.dict:
                mode = ""
                if event.type == 5:
                    mode = "press"
                if event.type == 6: 
                    mode = "release"

                e = [event.button,mode]
                #print("e",e)
                for btn in self.btns: 
                    if e[0] in btn.nr_on  and e[1] == "press":
                        btn.press()
                    if e[0] in btn.nr_off and e[1] == "release":
                        btn.release()
                    re = btn.get_event()
                    if re and btn.name not in ['MOUSE FOCUS']:
                        #print("----------------",btn.name,re)
                        r_event[btn.name] = re
        return r_event





pyray.TextureFilter(3)

old_x =10 # m.x
old_y =10 # m.y
c=0
cd = 1
cc=0
import string
while not window_should_close():
    begin_drawing()

    clear_background(BLACK)
    Color(255,0,0,0)
    rl_enable_smooth_lines()
    font_size = 14

    try:
        GREY = [122,122,122,255]
        p=0
        txt=string.printable
        v=10

        x2 = 10
        y2 = 10

        txt2 = str(c)
        draw_text_ex(font1,txt, [20,320], 22, 0, [255,120,0,123]) #YELLOW)

        draw_text_ex(font1,txt2, [140,60], font_size, 0, YELLOW)

        draw_text("free fonts included with raylib", 250, 20, 20, GRAY);

        draw_rectangle(x2-1, y2,24,13,[255,255,255,int(v)])
        draw_text("FPS:{}".format(fps_count), 3, 3, 3, VIOLET)

        fonts = [None]*10
        #fonts[0] = load_font("resources/fonts/alagard.png");
        #fonts[0] = load_font("alagard.png");
        font2 = load_font("alagard.ttf");
        draw_text_ex(font2,"asdlkjaskjdalksjd", [140,160], font_size, 0, YELLOW)


        m=get_mouse_position()
        if m.x != old_x or m.y != old_y:
            old_x = m.x
            old_y = m.y
            print(m.x,m.y)
        draw_text("X:"+str(m.x), 50, 120, 20, GRAY);
        draw_text("Y:"+str(m.y), 50, 140, 20, GRAY);
        draw_rectangle(int(old_x-10),int(old_y-1),20,2,[255,0,255,255])
        draw_rectangle(int(old_x-1),int(old_y-10),2,20,[255,0,255,255])

        draw_line(5, 16, 40, 16, (255,225,0,220))

        btn = Button(None,[200,200,80,30])
        btn.text = "a\n{}".format(c)
        btn.btn4.val.set(c) #self.val.get()
        if c % 10 == 0:
            if cc:
                cc=0
            else:
                cc=1

        if cc: #=0
            pass#btn.btn1.color = [255,0,0]
        else:
            pass #btn.btn1.color = [220,221,220]
        btn.draw()
            
        #draw_fps(30,10)

        end_drawing()

        #time.sleep(1/11) # FPS RATE
        time.sleep(1/31) # FPS RATE

        frame_count += 1
        if time.time()-start > 1:
            start = time.time()
            fps_count = frame_count
            frame_count = 0

        if cd:
            c+=1
        else:
            c-=1

        if c<0:
            cd = 1
        if c >= 255:
            cd = 0

    except KeyboardInterrupt as e:
        raise e
    except Exception as e:# KeyInterupt
        print("err",e)
        raise e
        time.sleep(1)

close_window()

