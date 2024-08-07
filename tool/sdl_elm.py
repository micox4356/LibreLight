#!/usr/bin/python3 
import pygame
import pygame.gfxdraw
import pygame.font
from lib.xcolor import *

font0 = pygame.font.SysFont("freesans",10)

font0b = pygame.font.SysFont("freesansbold",10)
font = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
font22 = pygame.font.SysFont("FreeSans",22)
#font = pygame.font.SysFont(None,30)

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


class ELEM_KILLGROUP():
    def __init__(self):
        self.data = []
    def insert(self,elm):
        if elm not in self.data:
            self.data.append(elm)
            return 1
        return 0
    def clean(self,elm):
        v = elm.val
        for i in self.data:
            i.clear()
        #elm.set(v)
        return v

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

class Layout():
    def __init__(self,master):
        self.master = master
    def pack(self,**args):
        pass
    def grid(self,**args):
        pass
    def bind(self,**args):
        pass

def get_font_hight(font):
    fr = font.render("test_font_hight" ,1, (0,0,0))
    r = fr.get_rect()
    h = r[3]
    return h



def draw_bd(pos=[0,0,10,10],delta=0):
    d = delta
    xpos = ( 
            (pos[0]-d          ,pos[1]-d),
            (pos[0]+pos[2]+d-1 ,pos[1]-d),
            (pos[0]+pos[2]+d-1 ,pos[1]+pos[3]+d-1),
            (pos[0]-d          ,pos[1]+pos[3]+d-1)
            )
    i_old = None
    ypos = []
    for i in xpos:
        if i_old:
            ypos.append( (i_old,i)   )
        i_old = i

    ypos.append( (i_old,xpos[0])   )
    return ypos

def check_area_v(v1,v2,event_v):#elm_pos,event_pos):
    if event_v < v1+1: 
        return 0
    if event_v > v2-1: 
        return 0
    return 1

def check_area(pos,event_pos):
    v2 = pos[0]+pos[2]
    x = check_area_v(pos[0],v2,event_pos[0])
    v2 = pos[1]+pos[3]
    y = check_area_v(pos[1],v2,event_pos[1])
    if x and y:
        return 1


def check_area2_dir(R1,R2):
    r2 = R2[:] #mouse_box
    xd = 1
    yd = 1
    if r2[0] > r2[2]:
        r2[0],r2[2] = r2[2],r2[0]
        xd=-1
    if r2[1] > r2[3]:
        r2[1],r2[3] = r2[3],r2[1]
        yd=-1
    #print("check_area2_dir",xd,yd)
    return xd,yd,r2


def check_area2(R1,R2): #pos,mouse_box
    xd,yd,r2 = check_area2_dir(R1,R2)

    btn_box = R1[:] #btn_box
    w=btn_box[2]
    h=btn_box[3]

    p1 = [btn_box[0],btn_box[1]]
    p4 = [btn_box[0]+w,btn_box[1]+h]

    x=0
    if r2[2] > p1[0] and r2[0] < p4[0]:
        x+=1
    y=0
    if r2[3] > p1[1] and r2[1] < p4[1]:
        y+=1

    if x and y:#> 4:
        #print("btn",R1,"mouse",R2)
        #print("btn",btn_box,"mouse",r2)
        #print("area2",x,y)
        return 1 


class Button():
    def __init__(self,window,pos):
        self.window = window
        self.event_pos = [0,0]
        self.font0 = pygame.font.SysFont("freesans-bold",16)
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

        self.window.set_alpha(128)  

        self._draw_bg()
        self._draw_fader()
        self._draw_font(text="")
            
        rgb = self.btn2.get_color()

        self._draw_bd(color=rgb) 
        self._draw_bd(delta=-1)

        rgb = self.btn3.get_color()
        self._draw_bd(delta=-2,color=rgb)

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
        pygame.draw.rect(self.window,rgb,pos)

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
            pygame.draw.rect(self.window,rgb,pos2)
        elif self.fader == "v":
            if v > 0: 
                pos2[1] += int((hight-20)* v/_max_val)
                pos2[3] = 20
            else:
                pos2[3] = 20 
            pos2[0] += 6
            pos2[2] -= 12 
            pygame.draw.rect(self.window,rgb,pos2)

    def _draw_font(self,text=""):
        pos = self.pos

        a = pos[0]+4
        r = pos[1]+4
        v = "{:4.02f}".format(self.btn4.val.get()) 

        lines = self.text.split("\n")
        lines.extend(self.text2)

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
            fr = self.font0.render(i ,1, (0,0,0))

            fr_r=fr.get_rect()
            p2 = [pos[0]+4,r,fr_r[2],fr_r[3]]
            if 0:# dbg # bg highlight
                pygame.draw.rect(self.window,[0,0,255],p2)

            self.window.blit(fr,(a,r))
            r+=fr_r[3]+1

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
                if event.type in [5,1025]:
                    mode = "press"
                if event.type in [6,1026]: 
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


def draw_mouse_box(window,pos1,pos2,color=[128,128,128],text=1):
    color = [200,0,0,127]
    
    if text:
        fr = font15.render("A" ,1, (200,200,200))
        window.blit(fr,pos1)

        fr = font15.render("B" ,1, (200,200,200))
        window.blit(fr,[pos2[0]-10,pos2[1]-10])

    # h unten
    _pos1 = [pos1[0],pos2[1]]
    _pos2 = [pos2[0],pos2[1]]
    pygame.draw.aaline(window,color,_pos1,_pos2,1)

    color = [255,255,0,127]
    # h rechts
    _pos1 = [pos2[0],pos1[1]]
    _pos2 = [pos2[0],pos2[1]]
    pygame.draw.aaline(window,color,_pos1,_pos2,1)


    color = [0,200,0,127]
    # h links
    _pos1 = [pos1[0],pos1[1]]
    _pos2 = [pos1[0],pos2[1]]
    pygame.draw.aaline(window,color,_pos1,_pos2,1)


    color = [0,0,200,127]
    # h oben
    _pos1 = [pos1[0],pos1[1]]
    _pos2 = [pos2[0],pos1[1]]
    pygame.draw.aaline(window,color,_pos1,_pos2,1)

