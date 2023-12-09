#!/usr/bin/python3

import time
import random
import os
import tool.movewin as movewin

# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
pg = pygame

#os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,55)
#os.environ['SDL_VIDEO_CENTERED'] = '0'
main_size=(600,500)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom

pg = pygame
pygame.init()
pygame.mixer.quit()

import tool.sdl_elm as sdl_elm


CAPTION = 'LibreLight Start :{}'.format(random.randint(100,999))

_id = movewin.winfo(CAPTION)
c1 = movewin.movewin(_id,200,50)
os.system(c1)
c1 = movewin.activate(_id)
os.system(c1)

pg.display.set_caption(CAPTION)


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

start = time.time()

# init
table = []
i = 1
r = 150
bx = sdl_elm.Button(window,pos=[20,r,60,20])
bx.text = "FIX:{}".format(i+1)
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.bg_on = [255,0,255]
bx.btn1.color_on = [255,0,55]
bx.btn1.type = "flash"
#self.btn1.type = "flush"
table.append(bx)
i += 1
#r+=20
r+=bx.get_rect()[3]
bx = sdl_elm.Button(window,pos=[20,r,80,40])
bx.text = "FIX:{}".format(i+1)
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.bg_on = [255,0,255]
table.append(bx)
i += 1
#r+=60
r+=bx.get_rect()[3]
bx = sdl_elm.Button(window,pos=[20,r,80,40])
bx.text = "FIX:{}".format(i+1)
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.bg_on = [255,0,255]
bx.font0 = pygame.font.SysFont("freesans",20)
table.append(bx)
i += 1
#r+=60
r+=bx.get_rect()[3]
bx = sdl_elm.Button(window,pos=[30,r,190,60])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.bg_on = [255,0,255]
bx.font0 = pygame.font.SysFont("freesans",20)
bx.btn1.type = "flash"
table.append(bx)
i += 1
r+=bx.get_rect()[3]
bx = sdl_elm.Button(window,pos=[20,r,60,20])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.bg_on = [255,0,255]
bx.font0 = pygame.font.SysFont("freesans",12)
table.append(bx)

while 1:

    pygame.display.flip()
    #event()
    pos = [160,10,70,60]
    rgb = (0xdd,0xdd,0xdd,0)
    rgb = (0xaa,0xaa,0xaa,0)
    
    window.fill((5,5,5))
    pygame.draw.rect(window,(0,0,0),[0,0,main_size[0],main_size[1]])

    fr = font22.render("DEMO / TEST - MODE !"  ,1, (200,200,200))
    window.blit(fr,(10,30 ))

    pos = [160,110,70+80,20]
    pygame.draw.rect(window,rgb,pos)

    t=(time.time()-start)
    if t > 15:
        start = time.time()
    b= 80-int(t*10)
    pos = [160,110,70+(b),20]
    rgb = (0x00,0xff,0xff,0)
    pygame.draw.rect(window,rgb,pos)
    rgb = (0x00,0x00,0x00,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    window.blit(fr,pos[:2])


    pos = [160,90,70+80,20]
    pygame.draw.rect(window,rgb,pos)
    b= int(t*10)
    pos = [160,90,0+(b),20]
    rgb = (0x00,0xff,0xff,0)
    pygame.draw.rect(window,rgb,pos)
    rgb = (0x00,0x00,0x00,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    window.blit(fr,pos[:2])


    rgb = (0xaa,0xaa,0xaa,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    window.blit(fr,(500,500))

    for t in table:
        t.draw()


    resize_changed = 0
    for event in pygame.event.get(): 
        print("event",event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.VIDEORESIZE:
            scrsize = event.size
            width   = event.w
            hight   = event.h
            resize_changed = True

        for t in table:
            t.event(event)

    if resize_changed:# = True
        screen = pygame.display.set_mode(scrsize,pg.RESIZABLE)
