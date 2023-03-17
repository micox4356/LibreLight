
import math
import random
import time
import os
import sys

START = time.time()
_START = time.time()

from optparse import OptionParser
...
parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode",
                  help="pixel mode") #, metavar="FILE")

parser.add_option("-X", "--XX", dest="XX", #default=1,
                  help="x-split") #, metavar="FILE")

parser.add_option("-x", "--xx", dest="xsplit", #default=1,
                  help="x-split") #, metavar="FILE")
parser.add_option("-y", "--yy", dest="ysplit",#default=1,
                  help="y-split") #, metavar="FILE")

parser.add_option("-s", "--start-univ", dest="start_univ",#default=1,
                  help="set start-univers default=2") #, metavar="FILE")

parser.add_option("-g", "--gobo-ch", dest="gobo_ch",#default=1,
                  help="gobo ch univ on 1") #, metavar="FILE")

#parser.add_option("-f", "--file", dest="filename",
#                  help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()


# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,55)
os.environ['SDL_VIDEO_CENTERED'] = '0'

pg = pygame
pygame.init()
pygame.mixer.quit()


f = pygame.font.get_fonts()
f = list(f)
f.sort()
for i in f:
    if 1:# "mono" in i.lower():
        print(i)
    

font0 = pygame.font.SysFont("freesans",10)
font0b = pygame.font.SysFont("freesansbold",10)
font = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
font22 = pygame.font.SysFont("FreeSans",22)
#font = pygame.font.SysFont(None,30)

fr = font.render("hallo" ,1, (200,0,255))

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
        self.w = 20
        self.h = 10
        self.pos = pos
        self.on = 0
        self.bd = [0,255,0]
        self.on_bg = [255,255,0]
        self.rgb = (0xaa,0xaa,0xaa,127)
        self.__layout = Layout(self)
        self.pack = self.__layout.pack
        self.grid = self.__layout.grid
        self.bind = self.__layout.bind
        self.text = "line1\nline2"
        self.motion = 0

    def draw(self,text="GOBO1"):
        #pos = [160,100,70,60]
        #rgb = (0xdd,0xdd,0xdd,0)
        #rgb = (0xaa,0xaa,0xaa,0)
        pos = self.pos
        rgb = self.rgb
        window.set_alpha(128)  

        if self.on:
            rgb = self.on_bg 
        pygame.draw.rect(self.window,rgb,pos)

        r = pos[1]+6
        for i in self.text.split("\n"):
            fr = font0.render(i ,1, (0,0,0))
            #fr = font.render("You win!", True, BLACK)
            #text_rect = fr.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.window.blit(fr,(pos[0]+4,r))
            r += 10


        self._check_event()
        self._draw_bd(color=(0xaa,0xaa,0xaa))
        self._draw_bd(delta=-1)
        self._draw_bd(delta=-2,highlight=1,color=self.bd)

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
            pygame.draw.aaline(window,color,i[0],i[1],1)

    def event(self,event=None):
        #print(self.pos)
        if "pos" in event.dict:
            self.event_pos = event.pos
            self._check_event()

        if self.motion:
            #print(self,"Motion.event",event)

            if "button" in event.dict:
                print("-",self,"Button.event",event.dict)
                print(type(event))
                if event.type == 5:
                    if event.button == 1:
                        if self.on:
                            self.on = 0
                        else:
                            self.on = 1

def draw_box(pos1,pos2,color=[128,128,128],text=1):

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

main_size=(500,500)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
pg.display.set_caption('NEXTGEN GUI')

class Gevent():
    def __init__(self):
        self.drag = 0
        self.pos1 = [0,0]
        self.pos2 = [0,0]
        self.event_pos = [0,0]
        self.gain = 0

    def check_in(self,elem):
        print(self.event_pos)
        print(self.pos1)
        print(self.pos2)
        print(elem.pos)

    def draw(self,delta=0,highlight=0,color=[0,255,0]):
        if self.pos1 == [0,0]:
            return
        if self.pos2 == [0,0]:
            return
        #if not self.drag:
        #    return 

        pos1 = [self.pos1[0],self.pos1[1]]
        pos2 = [self.pos2[0],self.pos2[1]]
        #pygame.draw.aaline(window,color,pos1,pos2,1)
 

        color = [200,0,0,127]

        draw_box(self.pos1,self.pos2)
        return 0

        fr = font15.render("A" ,1, (200,200,200))
        window.blit(fr,self.pos1)

        fr = font15.render("B" ,1, (200,200,200))
        window.blit(fr,[self.pos2[0]-10,self.pos2[1]-10])
        

        # h unten
        pos1 = [self.pos1[0],self.pos2[1]]
        pos2 = [self.pos2[0],self.pos2[1]]
        pygame.draw.aaline(window,color,pos1,pos2,1)

        color = [255,255,0,127]
        # h rechts
        pos1 = [self.pos2[0],self.pos1[1]]
        pos2 = [self.pos2[0],self.pos2[1]]
        pygame.draw.aaline(window,color,pos1,pos2,1)


        color = [0,200,0,127]
        # h links
        pos1 = [self.pos1[0],self.pos1[1]]
        pos2 = [self.pos1[0],self.pos2[1]]
        pygame.draw.aaline(window,color,pos1,pos2,1)


        color = [0,0,200,127]
        # h oben
        pos1 = [self.pos1[0],self.pos1[1]]
        pos2 = [self.pos2[0],self.pos1[1]]
        pygame.draw.aaline(window,color,pos1,pos2,1)


    def event(self,event):
        print("GLOBAL",self,self.event_pos,event,event.type)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.VIDEORESIZE:
            scrsize = event.size
            width   = event.w
            hight   = event.h
            screen = pygame.display.set_mode(scrsize,pg.RESIZABLE)
            changed = True



        if "pos" in event.dict:
            self.event_pos = event.pos
            #self._check_event()

        if "button" in event.dict:
            if event.button == 1 and event.type == 5: # and self.drag:
                self.pos1 = self.event_pos
                self.drag = 0

        if "buttons" in event.dict:
            if event.buttons[0] == 1:
                self.pos2 = self.event_pos
                self.drag = 1
            else:
                self.drag = 0

        if "gain" in event.dict:
            self.gain = event.gain
global_event = Gevent()


def main():
    START = time.time()
    running = 1
    frame   = 0
    fps = 0

    b0 = Button(window,pos=[80,80,50,40])
    b1 = Button(window,pos=[100,100,60,40])
    b2 = Button(window,pos=[200,200,60,40])
    b2a = Button(window,pos=[260,200,60,40])
    b3 = Button(window,pos=[1500,800,60,40])

    table = []
    r = 0
    for i in range(20):
         bx = Button(window,pos=[20,150+r,60,20])
         bx.text = "FIX:{}".format(i+1)
         bx.on_bg = [255,0,255]
         table.append(bx)
         r+=20

    while running:
        pygame.display.flip()
        #event()
        pos = [160,10,70,60]
        rgb = (0xdd,0xdd,0xdd,0)
        rgb = (0xaa,0xaa,0xaa,0)
        
        window.fill((0,0,0))
        fr = font22.render("DEMO / TEST - MODE !"  ,1, (200,200,200))
        window.blit(fr,(10,30 ))


        fr = font15.render("{}".format(pos[1]) ,1, (200,200,200))
        window.blit(fr,(10,pos[1] ))
        fr = font15.render("{}".format(fps) ,1, (200,200,200))
        window.blit(fr,(30,pos[1] ))

        fr = font15.render("{}".format(frame) ,1, (200,200,200))
        window.blit(fr,(60,pos[1] ))

        fr = font15.render("{:03}".format(int((START+1-time.time())*100)) ,1, (200,200,200))
        window.blit(fr,(80,pos[1] ))
        #print(window,rgb,pos)
        #pygame.draw.rect(window,rgb,pos)
        #pygame.draw.rect(window,(255,0,0),(15,15,20,10))

        for event in pygame.event.get(): 
            global_event.event(event)
            b0.event(event)
            b1.event(event)
            b2.event(event)
            b2a.event(event)
            b3.event(event)
            for t in table:
                t.event(event)
        

        b0.draw()
        b1.draw()
        b2.draw()
        b2a.draw()
        b3.draw()

        c = (200,200,200)

        #for t in table:
        #    global_event.check_in(t)

        for t in table:
            t.draw()
        global_event.check_in(t)

        
        fr = font15.render("A:{}".format(str(global_event.pos1)) ,1, c)
        window.blit(fr,(200,pos[1] ))
        fr = font15.render("B:{}".format(str(global_event.pos2)) ,1, c)
        window.blit(fr,(200,pos[1]+10 ))

        if global_event.gain:
            c = (0,255,0)
        
        #blue box
        if global_event.pos1[0] > global_event.event_pos[0] and  global_event.pos2[0] < global_event.event_pos[0]:
            #c = (0,0,255)
            if global_event.pos1[1] > global_event.event_pos[1] and  global_event.pos2[1] < global_event.event_pos[1]:
                c = (0,0,255)
        # red box
        if global_event.pos1[0] < global_event.event_pos[0] and  global_event.pos2[0] > global_event.event_pos[0]:
            #c = (0,0,255)
            if global_event.pos1[1] < global_event.event_pos[1] and  global_event.pos2[1] > global_event.event_pos[1]:
                c = (255,0,0)
        fr = font15.render("{:03}/{:03}".format(global_event.event_pos[0],global_event.event_pos[1]) ,1, c)
        window.blit(fr,(120,pos[1] ))


        global_event.draw()

        
        pygame.display.flip()
        pg.time.wait(30)
        pg.time.wait(30)
        #pg.time.wait(30)

        frame += 1
        if START+1 < time.time():
            fps = frame
            frame = 0
            START = time.time()


if __name__ == "__main__":
    main()
