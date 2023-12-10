#!/usr/bin/python3

import time
boot = time.time()

import random
import os
import sys
import tool.movewin as movewin

# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
pg = pygame
main_size=(600,500)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)

pg = pygame
pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()

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
table = []

r = 80
i = 1

bx = sdl_elm.Button(window,pos=[20,r,60,20])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.bg_on = [255,0,255]
bx.btn1.color_on = [255,0,155]
bx.btn1.type = "flash"
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[20,r,80,40])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
table.append(bx)
r+=bx.get_rect()[3]

i += 1
r+=bx.get_rect()[3]
bx = sdl_elm.Button(window,pos=[20,r,80,40])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.font0 = pygame.font.SysFont("freesans",20)
bx.val.set( 100)
bx.fader = 0
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[30,r,190,60])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.font0 = pygame.font.SysFont("freesans",20)
bx.btn1.type = "flash"
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[20,r,60,20])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.font0 = pygame.font.SysFont("freesans",12)
table.append(bx)

mouse_down = 0
mouse_pos1 = [0,0]
mouse_pos2 = [0,0]
mouse_grab = []
print(int((time.time()-boot)*10),"loop...")
fps_t = time.time()
fps = 0
fps_old = 0
while 1:
    fps +=1
    t = time.time()
    if t-fps_t >= 1:
        print("FPS:",fps)
        fps_old = fps
        fps=0
        fps_t =t

    pygame.display.flip()
    pos = [160,10,70,60]
    rgb = (0xdd,0xdd,0xdd,0)
    rgb = (0xaa,0xaa,0xaa,0)
    
    window.fill((5,5,5))
    pygame.draw.rect(window,(0,0,0),[0,0,main_size[0],main_size[1]])

    fr = font22.render("FPS:"+str(fps_old)  ,1, (200,200,200))
    window.blit(fr,(10,10 ))

    fr = font22.render("DEMO / TEST - MODE ! "  ,1, (200,200,200))
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
    
    pos = [160,200,80,20]
    #fd = sdl_elm.Fader(window,pos)
    #fd.draw()
    
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
         
        if "scancode" in event.dict:
            if event.scancode == 9:
                for t in table:
                    t.btn2.clean()

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

        if "pos" in event.dict:
            if "button" in event.dict:
                if event.type == 5:#press
                    mouse_down = 1
                    mouse_pos1 = [event.pos[0],event.pos[1]]
                if event.type == 6:#release
                    mouse_down = 0

                for btn in mouse_grab:
                    btn.btn2.val = 1
                mouse_grab = []
            mouse_pos2 = [event.pos[0],event.pos[1]]

    
    if mouse_down:
        d1 = mouse_pos1[0]-mouse_pos2[0]
        d2 = mouse_pos1[1]-mouse_pos2[1] 
        pix = 23
        #print(d1,d2)
        if ( d1 > pix or d1 < -pix)  or  ( d2 >pix or d2 < -pix):

            sdl_elm.draw_mouse_box(window,mouse_pos1,mouse_pos2)
            for t in table:
                pos = t.get_rect()

                mpos = [mouse_pos1[0],mouse_pos1[1],mouse_pos2[0],mouse_pos2[1]]

                if sdl_elm.check_area2(pos,mpos):
                    t._set_mouse_focus(1)
                    mouse_grab.append(t)
                else:
                    t._set_mouse_focus(0)

    if resize_changed:# = True
        screen = pygame.display.set_mode(scrsize,pg.RESIZABLE)

    clock.tick(30)

