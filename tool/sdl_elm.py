#!/usr/bin/python3 
import pygame
import pygame.gfxdraw
import pygame.font

font0 = pygame.font.SysFont("freesans",10)

font0b = pygame.font.SysFont("freesansbold",10)
font = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
font22 = pygame.font.SysFont("FreeSans",22)
#font = pygame.font.SysFont(None,30)


class VALUE():
    def __init__(self,v,_min=0,_max=255):
        self._val = v
        self._max = _max
        self._min = _min
    def set(self,val):
        if val <= self.max and val >= self.min:
            self._val = val
    def _check(self):
        if self._val > self._max:
            self._val = self._max
        if self._val < self._min:
            self._val = self._min

    def inc(self,v):
        self._val += v
        self._check()

    def get(self):
        self._check()
        return self._val

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
        

class ELEM_BUF():
    def __init__(self,kill=None):
        self.val = 0
        self.color = [0,255,0]
        self.color_on = [255,255,0]
        self.type="toggle" #"flash"
        self.killgroup = kill 

    def get(self):
        return self.val

    def get_color(self):
        if self.val:
            return self.color_on
        return self.color

    def clean(self):
        self.val = 0

    def press(self):
        if self.type == "toggle":
            if self.val:
                self.val = 0
            else:
                self.val = 1

        if self.type == "flash":
            self.val = 1

    def release(self):
        if self.type == "flash":
            self.val = 0

class Layout():
    def __init__(self,master):
        self.master = master
    def pack(self,**args):
        pass
    def grid(self,**args):
        pass
    def bind(self,**args):
        pass

class Button():
    def __init__(self,window,pos):
        self.window = window
        self.event_pos = [0,0]
        self.font0 = pygame.font.SysFont("freesans",10)
        self.w = 20
        self.h = 10
        self.pos = pos

        self.btn1 = ELEM_BUF() #btn
        #self.btn1.type = "flash"
        self.btn1.color = [140,140,140]
        self.btn1.color_on = [255,0,0]
        self.btn2 = ELEM_BUF() #sel
        self.btn2.color = [120,120,120]

        self.val = VALUE(0,0,256)
        self.val_inc = 10

        self.__layout = Layout(self)
        self.pack = self.__layout.pack
        self.grid = self.__layout.grid
        self.bind = self.__layout.bind
        self.text = "line1\nline2"
        self.motion = 0
        self.type = "toggle" # flash, kill

        self.text2 = []

    def check(self):
        if 10:#dbg:
            self.text2 = []
            #self.text2.append(self.val)
            self.text2.append([self.btn1.get(),self.btn2.get()])
            self.text2.append(self.btn1.type)

        self._check_event()
        self._check_min_hight()

    def draw(self,text="GOBO1"):
        self.check()

        self.window.set_alpha(128)  

        self._draw_bg()
        self._draw_font(text="")
            
        rgb = self.btn2.get_color()

        self._draw_bd(color=rgb) 
        self._draw_bd(delta=-1)
        self._draw_bd(delta=-2,highlight=1,color=rgb)

    def get_rect(self):
        self.check()
        return self.pos[:]

    def _check_min_hight(self):
        c = 1+ self.text.count("\n") #+1
        c += len(self.text2)

        fr = self.font0.render("test_font_hight" ,1, (0,0,0))
        #self.window.blit(fr,(pos[0]+4,r))
        fr_r =fr.get_rect()
        h = (fr_r[3]+1)*c +6#8 #+8
        #print("-.",c,h,fr_r,self.pos,self.text)
        #input()
        if self.pos[3] < h:
            self.pos[3] = h #ah+20
            #self.bg = (0xff,0xaa,0xaa,127)

    def _get_surface_center(self):
        #text_rect = fr.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        pass

    def _draw_bg(self):
        pos = self.pos
        #rgb = self.bg

        rgb = self.btn1.get_color()
        pygame.draw.rect(self.window,rgb,pos)

    def _draw_font(self,text=""):
        pos = self.pos

        a = pos[0]+4
        r = pos[1]+4
        v = "{:4.02f}".format(self.val.get()) 

        lines = self.text.split("\n")
        lines.extend(self.text2)

        for i in lines:
            i = str(i)
            if "<val>" in i:
                i = i.replace("<val>",v)
            fr = self.font0.render(i ,1, (0,0,0))

            fr_r=fr.get_rect()
            p2 = [pos[0]+4,r,fr_r[2],fr_r[3]]
            if 0:# dbg # bg highlight
                pygame.draw.rect(self.window,[0,0,255],p2)

            self.window.blit(fr,(a,r))
            r+=fr_r[3]+1


    def _check_event(self):
        self.bd = [125,125,125]
        self.motion = 0
        if self.event_pos[0] < self.pos[0]+1: 
            return #continue
        if self.event_pos[0] > self.pos[0]+self.pos[2]-1: 
            return #continue
        
        if self.event_pos[1] < self.pos[1]+1: 
            return #continue
        if self.event_pos[1] > self.pos[1]+self.pos[3]-1: 
            return #continue

        #print(">>",self.event_pos)
        self.bd = [200,200,200]
        self.motion = 1

    def _draw_bd(self,delta=0,highlight=0,color=[0,0,0]):
        pos = self.pos
        d = delta
        xpos = ( 
                (pos[0]-d        ,pos[1]-d),
                (pos[0]+pos[2]+d-1 ,pos[1]-d),
                (pos[0]+pos[2]+d-1 ,pos[1]+pos[3]+d-1),
                (pos[0]-d        ,pos[1]+pos[3]+d-1)
                )
        i_old = None
        ypos = []
        for i in xpos:
            if i_old:
                ypos.append( (i_old,i)   )
            i_old = i

        ypos.append( (i_old,xpos[0])   )

        for i in ypos:
            #print("ypos",i)
            #pygame.draw.aaline(self.window,color,i[0],i[1],1)
            pygame.draw.aaline(self.window,color,i[0],i[1],1)

    def event(self,event=None):
        #print(self.pos)
        if "pos" in event.dict:
            self.event_pos = event.pos
            self._check_event()

        if self.motion:
            #print(self,"Motion.event",event)

            if "button" in event.dict:
                #print()
                #print("-","Button.event",event.dict,event.type,event.button,self.type)
                #print(type(event))
                mode = ""
                if event.type == 5:
                    mode = "press"
                if event.type == 6: 
                    mode = "release"

                e = [event.button,mode]
                print("e",e)

                if e[0] in [1,3] and e[1] == "press":
                    self.btn1.press()
                if e[0] in [1,3] and e[1] == "release":
                    self.btn1.release()

                if e[0] in [2] and e[1] == "press":
                        self.btn2.press()
                if e[0] in [2] and e[1] == "release":
                        self.btn2.release()

                if e[0] in [4]: #mouse encoder 
                    self.val.inc(self.val_inc)
                if e[0] in [5]: #mouse encoder 
                    self.val.inc(-self.val_inc)

def draw_box(window,pos1,pos2,color=[128,128,128],text=1):

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

