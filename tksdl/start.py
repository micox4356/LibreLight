#!/usr/bin/python3

import time
boot = time.time()

import random
import os
import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")

import pathlib

_file_path=pathlib.Path(__file__)
print("__file__ =",_file_path)


import lib.restart as restart
import lib.libconfig as libconfig

r = libconfig.check_pro_easy()
if r == "PRO":
    restart.pro()
if r == "EASY":
    restart.easy()



import tool.movewin as movewin

CAPTION = 'LibreLight Start XX'
movewin.check_is_started(CAPTION,_file_path)

from lib.xcolor import *


# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
pg = pygame
main_size=(550,400)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)

pg = pygame
pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()
icon = pygame.image.load('icon/scribble.png')
pygame.display.set_icon(icon)

import tool.movewin as movewin
import tool.sdl_elm as sdl_elm
import lib.showlib as showlib


CAPTION = 'LibreLight Start '
CAPTION += ':{}'.format(random.randint(100,999))

import tool.git as git
CAPTION += git.get_all()

if 0:
    _id = movewin.winfo(CAPTION)
    c1 = movewin.movewin(_id,200,50)
    os.system(c1)
    c1 = movewin.activate(_id)
    os.system(c1)

pg.display.set_caption(CAPTION)

font0  = pygame.font.SysFont("freesans",10)
font0b = pygame.font.SysFont("freesansbold",10)
font   = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
font22 = pygame.font.SysFont("FreeSans-bold",42)
#font  = pygame.font.SysFont(None,30)

fr = font.render("hallo" ,1, (200,0,255))

start = time.time()
table = []

x = 80
y = 120
import os
import lib.fork as fork

import lib.showlib as showlib
SHOW_NAME = showlib.current_show_name()
print([SHOW_NAME])
                
def exit(args=None):
    pygame.quit()
    sys.exit()





bx = sdl_elm.Button(window,pos=[x,y,400,60])
bx.text = "       EASY" 
bx.font0 = pygame.font.SysFont("freesans-bold",85)
bx.btn1.color = GREEN
bx.btn1.cb_on.set(restart.easy)
table.append(bx)
y+=bx.get_rect()[3]+20

bx = sdl_elm.Button(window,pos=[x,y,400,60])
bx.text = "        PRO" 
bx.btn1.color = GOLD
bx.btn1.cb_on.set(restart.pro)
bx.font0 = pygame.font.SysFont("freesans-bold",85)
table.append(bx)
y+=bx.get_rect()[3]+30

bx = sdl_elm.Button(window,pos=[x,y,400,60])
bx.text = "         Exit"
bx.btn1.cb_on.set(exit)
bx.font0 = pygame.font.SysFont("freesans-bold",80)
table.append(bx)

#-----------------------------------------------------------------
#b = tk.Button(frame,bg="darkgrey", text="HELP",command=libtk.online_help("librelight:20-exec")) #"0&do=index"))
x=450
y=10
bx = sdl_elm.Button(window,pos=[x,y,50,20])
bx.text = " HELP "
import lib.libtk as libtk
def xhelp(event=None):
    libtk.online_help("librelight:10-pro-easy-mode")()
bx.btn1.cb_on.set(xhelp)

bx.font0 = pygame.font.SysFont("freesans-bold",20)
table.append(bx)


mouse_down = 0
mouse_pos1 = [0,0]
mouse_pos2 = [0,0]
mouse_grab = []
print(int((time.time()-boot)*10),"loop...")
fps_t = time.time()
fps = 0
fps_old = 0


run = 1
while run:
    fps +=1
    t = time.time()
    if t-fps_t >= 1:
        #print("FPS:",fps)
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
    #window.blit(fr,(10,10 ))
    fr = font22.render("           Lichtsteuerung"  ,1, (255,255,0))
    window.blit(fr,(80,20 ))


    fr = font22.render("           Modus wählen ! "  ,1, (255,255,0))
    window.blit(fr,(80,60 ))

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
                    btn.btn2.val.set(1)
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

