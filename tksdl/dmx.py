#!/usr/bin/python3

import time
boot = time.time()

import random
import os
import sys
#sys.path.insert(0,os.path.realpath(os.getcwd() + '/..'))
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
print(sys.path)
print()


import pathlib

_file_path=pathlib.Path(__file__)
print("file:",_file_path)

import tool.movewin as movewin
pids = movewin.search_process(_file_path)

CAPTION = 'LibreLight SDL-DMX '

if len(pids) >= 2:
    search = CAPTION[:]
    _ids = movewin.winfo(search)
    for _id in _ids:
        c3  = movewin.activate(_id)
        os.system(c3)
    sys.exit()



# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
pg = pygame
main_size=(850,460)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)

pg = pygame
pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()
icon = pygame.image.load('icon/scribble.png')
pygame.display.set_icon(icon)

import tool.movewin as movewin
import tool.sdl_elm as sdl_elm


#CAPTION = 'LibreLight DMX '
CAPTION += ':{}'.format(random.randint(100,999))

import tool.git as git
CAPTION += git.get_all()


_id = movewin.winfo(CAPTION)
c1 = movewin.movewin(_id,main_size[0],main_size[1]) #800,500)
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
font16 = pygame.font.SysFont("freemonobold",16)
font22 = pygame.font.SysFont("FreeSans",22)
#font  = pygame.font.SysFont(None,30)

fr = font.render("hallo" ,1, (200,0,255))

start = time.time()
table = []

r = 80
i = 1

bx = sdl_elm.Button(window,pos=[20,r,80,40])
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
bx.btn4.val.set( 100)
bx.fader = 0
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[30,r,190,60])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
bx.font0 = pygame.font.SysFont("freesans-bold",20)
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




import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

mc.set("some_key", "Some value")
value = mc.get("some_key")

mc.set("another_key", 3)
mc.delete("another_key")

import time
import json
data = {}
start = time.time()
delta = start
#for i in dir(mc):
#    print(i)#,[i.__doc__])
#    print()

#for i in mc.get_stats():
#    print("keys",i)


#fps_btn = []
#fps_btn_press = [] 

#i += 1
#bx = sdl_elm.Button(window,pos=[30,r,190,60])
#bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.font0 = pygame.font.SysFont("freesans-bold",20)
#bx.btn1.type = "flash"
#fps_btn.append(bx)
#r+=bx.get_rect()[3]



table={}
btn1_press = [] #["10.10.10.13:0"]

font0 = pygame.font.SysFont("freesans-bold",15)

while 1:
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

    fr = font22.render("RAW DMX DATA" ,1, (200,200,200))
    window.blit(fr,(20,10 ))

    fr = font22.render("DEMO / TEST - MODE ! "  ,1, (200,200,200))
    #window.blit(fr,(10,30 ))

    pos = [160,110,70+80,20]
    #pygame.draw.rect(window,rgb,pos)

    t=(time.time()-start)
    if t > 15:
        start = time.time()
    b= 80-int(t*10)
    pos = [160,110,70+(b),20]
    rgb = (0x00,0xff,0xff,0)
    #pygame.draw.rect(window,rgb,pos)
    rgb = (0x00,0x00,0x00,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    #window.blit(fr,pos[:2])
    
    pos = [160,200,80,20]
    #fd = sdl_elm.Fader(window,pos)
    #fd.draw()
    
    pos = [160,90,70+80,20]
    #pygame.draw.rect(window,rgb,pos)
    b= int(t*10)
    pos = [160,90,0+(b),20]
    rgb = (0x00,0xff,0xff,0)
    #pygame.draw.rect(window,rgb,pos)
    rgb = (0x00,0x00,0x00,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    # window.blit(fr,pos[:2])


    rgb = (0xaa,0xaa,0xaa,0)
    fr = font22.render(str(round(t,1)) ,1, rgb) #(200,200,200))
    #window.blit(fr,(500,500))

    rgb = (0xff,0,0xaa,0)
    #for t in table:
    #    t.draw()
    jjjj=330
    iiii=25
    for i in range(20):
        fr = font15.render(str(i+1) ,1, rgb) #(200,200,200))
        window.blit(fr,(jjjj,10+iiii))
        jjjj+=25

    jjjj=300
    iiii=40
    for i in range(26):
        fr = font15.render(str(i*20+1) ,1, rgb) #(200,200,200))
        window.blit(fr,(jjjj,10+iiii))
        iiii+=15

    r=40
    if 1:
        ch = 141
        send = 0
        #cmd="stats items" 
        y=mc.get("index")#cmd)
        if y:
            #print(x)
            #print()
            iii = 0
            key=y.keys()
            key = list(key)
            key.sort()
            if len(btn1_press) == 0:
                btn1_press = [key[0]]
            rgb = (0x00,0,0xff,0)
            k2 = btn1_press[-1]
            fr = font22.render("SRC:"+str(k2) ,1, rgb) #(200,200,200))
            window.blit(fr,(300,1))

            fr = font22.render("FPS:"+str(fps_old) ,1, rgb) #(200,200,200))
            window.blit(fr,(600,1))

            for k in key:#y.items():
                v = y[k]
                #print(k,v)
                x=mc.get(k)
                cccount = 0
                for ch in x:
                    try:
                        if ch > 0:
                            cccount +=1
                    except:pass
                txt = str([k,v,ch,"=",cccount]) #x[ch-1]])
                #print(txt )#k,v,ch,"=",x[ch-1])

                rgb = (0xaa,0xaa,0xaa,0)
                fr = font22.render(str(txt) ,1, rgb) #(200,200,200))
                #window.blit(fr,(30,40+iii))
                
                i += 1
                if k not in table:
                    bx = sdl_elm.Button(window,pos=[20,r,230,20])
                    bx.btn1.color_on = [255,255,0]
                    table[k] = bx

                bx = table[k]
                bx.text = str(txt) #+"\n<val>\n" #.format(i+1)
                bx.font0 = font0 #pygame.font.SysFont("freesans-bold",15)
                bx.btn1.bg_on = [0,255,255]
                #bx.dbg = 1
                #bx.btn4.val.set( 100)
                bx.btn1.type = "toggle"
                #bx.fader = 0
                #table.append(bx)
                bx.pos  = [20,r,230,20]
                bx.draw()
                r+=bx.get_rect()[3]+2


                iii += 35



                iiii=40
                jjjj=330
                k2 = ""
                try:
                    k2 = btn1_press[-1]
                except:pass
                if k2 == k:
                    for l,m in enumerate(x):
                        #fr = font15.render(str([l,m]) ,1, rgb) #(200,200,200))
                        fr = font16.render(str(m) ,1, rgb) #(200,200,200))
                        window.blit(fr,(jjjj,10+iiii))
                        jjjj+=25
                        if (l+1) % 20 == 0:
                            iiii+=15
                            jjjj=330
        #time.sleep(.13)
    last_k = ""
    for k in table:
        t = table[k]
        if t.btn1.val.get():
            if k not in btn1_press:
                btn1_press.append(k)

    #print(btn1_press)
    if len(btn1_press) > 1:
        for k in table:
            table[k].btn1.val.set(0)
        
        k = btn1_press[-1]
        if k in table:
            btn1_press = [k]

    try:
        k = btn1_press[-1]
        table[k].btn1.val.set(1)
    except:pass

    resize_changed = 0
    for event in pygame.event.get(): 
         
        if "scancode" in event.dict:
            if event.scancode == 9:
                for k in table:
                    t = table[k]
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
            print(t)
            table[t].event(event)

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
            for k in table:
                t = table[k]
                pos = t.get_rect()

                mpos = [mouse_pos1[0],mouse_pos1[1],mouse_pos2[0],mouse_pos2[1]]

                if sdl_elm.check_area2(pos,mpos):
                    t._set_mouse_focus(1)
                    mouse_grab.append(t)
                else:
                    t._set_mouse_focus(0)

    if resize_changed:# = True
        screen = pygame.display.set_mode(scrsize,pg.RESIZABLE)








    clock.tick(10)



