import pygame
import pygame.gfxdraw
import math
import random

import os


os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,184)
os.environ['SDL_VIDEO_CENTERED'] = '0'

pg = pygame
pygame.init()

main_size=(600,300)
main_size=(1600,900)
main_size=(300,300)

#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.RESIZABLE|pygame.DOUBLEBUF,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
# pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))) ,pygame.FULLSCREEN)
#pg.display.set_mode(window,pg.DOUBLEBUF) #|pg.OPENGL)
pg.display.set_caption('LibreLight Animation')


import pygame
import pygame.gfxdraw
import math
import random

import os

def event_read():

    inc = 1

    for event in pg.event.get():
        print("event",event)
        move_x = 0
        move_y = 0
        move_z = 0

        rot_x = 0
        rot_y = 0
        rot_z = 0
        if event.type== pg.QUIT:
            print("quit")
            pg.quit()
            quit()
            sys.exit()
        if "key" in dir(event):
            if event.key == 27: #ESC pg.KEYDOWN:
                print("quit")
                pg.quit()
                quit()
                sys.exit()





pg = pygame
pygame.init()

main_size=(600,300)
main_size=(1600,900)
main_size=(600,300)
main_size=(280,200)
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.RESIZABLE|pygame.DOUBLEBUF,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
# pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))) ,pygame.FULLSCREEN)
#pg.display.set_mode(window,pg.DOUBLEBUF) #|pg.OPENGL)
pg.display.set_caption('LibreLight Animation')

class FIX():
    def __init__(self,pos=[10,10]):
        self.rgb = [255,255,255]
        self.pos = pos
    def draw(self):
        pygame.draw.rect(window,self.rgb,[self.pos[0],self.pos[1],15,15])

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)


import time
s=time.time()
import math
while 1:
    x=mc.get("index")#cmd)
    if x is None:
        x = ["127.0.0.1"]
    for ip in x:
        #print( ip)
        ok = 0
        if "ltp-out" in ip:
            ok = 1
        if "2.0.0." in ip:
            ok = 1
        if ":2" not in ip:
            continue
        
        if not ok:
            continue

        t = int(math.sin(time.time() - s)*10)
        event_read()
        r = mc.get(ip) #"2.0.0.13:2")
        rr = [0]*512
        for i,v in enumerate(r):
            try: #cleanup ltp-out to int
                v = int(v)
                rr[i] = v
            except:pass
        r = rr


        if not r:
            c = 0
            time.sleep(0.1)
            r = [0] *512
            for i in range(12*8+1):
                dmx = i*4
                #print(dmx)
                r[dmx:dmx+4] = [255,10,10,40] 

        #print(r)
        ch = 4
        dmx = 1-1
        rgb = [255,255,255]
        for y in range(8):
            for x in range(12):
                #f = FIX(pos=[x*16,y*16])
                if dmx+ch < len(r):
                    dim = r[dmx]/255
                    rgb = [r[dmx+1]*dim,r[dmx+2]*dim,r[dmx+3]*dim]
                    #print(rgb)
                pos=[x*16,y*16]
                pygame.draw.rect(window,rgb,[40+pos[0],40+pos[1],16,16])
                dmx += ch

        pygame.display.flip()
        pg.time.wait(10)


