#!/usr/bin/python3

import time
boot = time.time()

import random
import os
import sys
import json

sys.path.insert(0,"/opt/LibreLight/Xdesk/")
#print(sys.path)
#print()

import pathlib

_file_path=pathlib.Path(__file__)
print("file:",_file_path)

import tool.movewin as movewin

CAPTION = 'LibreLight SDL-MIDI '
movewin.check_is_started(CAPTION,_file_path,sleep=0)


# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font

pg = pygame
main_size=(500,100)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)

pg = pygame
pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()
icon = pygame.image.load('icon/scribble.png')
pygame.display.set_icon(icon)

import tool.movewin as movewin
import tool.sdl_elm as sdl_elm

CAPTION += ':{}'.format(random.randint(100,999))

import tool.git as git
CAPTION += git.get_all()

_id = movewin.winfo(CAPTION)
c1 = movewin.movewin(_id,200,50)
os.system(c1)
c1 = movewin.activate(_id)
os.system(c1)

pg.display.set_caption(CAPTION)

import lib.zchat as chat
cmd_client = chat.Client(port=30003)


font0  = pygame.font.SysFont("freesans",10)
font0b = pygame.font.SysFont("freesansbold",10)
font   = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
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
#bx.font0 = pygame.font.SysFont("freesans",20)
bx.btn4.val.set( 100)
bx.fader = 0
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[20,r,80,60])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.font0 = pygame.font.SysFont("freesans-bold",20)
bx.btn1.type = "flash"
table.append(bx)
r+=bx.get_rect()[3]

i += 1
bx = sdl_elm.Button(window,pos=[20,r,80,20])
bx.text = "FIX:{}\n<val>\nx".format(i+1)
#bx.font0 = pygame.font.SysFont("freesans",12)
table.append(bx)
table = []
mouse_down = 0
mouse_pos1 = [0,0]
mouse_pos2 = [0,0]
mouse_grab = []
print(int((time.time()-boot)*10),"loop...")
fps_t = time.time()
fps = 0
fps_old = 0




import _thread as thread
try:
    import remote.apcmini as apcmini
    apc_main = apcmini.MAIN()
    thread.start_new_thread(apc_main.loop,())
    time.sleep(1)
except Exception as e:
    print("MIDI INI",e)


#while 1:
#    if apc_main.buf:
#        buf = apc_main.buf[:]
#        apc_main.buf = []
#        for m in buf:
#            print("-> midi:",m)

def remap_midi_row(m,row_len=8):
    btn,val=m
    row_def = []
    row_def.append([56,63])
    row_def.append([48,55])
    row_def.append([40,47])
    row_def.append([32,39])
    row_def.append([24,31])
    row_def.append([16,23])
    row_def.append([8,15])
    row_def.append([0,7])
    row_def.append([64,71])

    b2=-1
    v2=0

    for i,b in enumerate(row_def):
        #print(i,btn,b,val)
        if btn >= b[0] and btn <= b[1]:
            b2 = btn-b[0]
            btn2 = (i)*row_len + b2+1
            #print("btn2",btn2,val)
            return [btn2,val]
            break
buf = []
buf2 = []
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

    fr = font15.render("FPS:"+str(fps_old)  ,1, (200,200,200))
    window.blit(fr,(10,2 ))

    fr = font15.render("SDL-MIDI "  ,1, (200,200,200))
    window.blit(fr,(100,2 ))



    try:
        if apc_main.buf:
            s = time.time()
            buf = apc_main.buf[:]
            apc_main.buf = []
            buf2=[]
            msgs = []
            for m in buf:
                if m[0] > 1000:
                    continue
                btn,val = remap_midi_row(m,row_len=10)
                btn+=400
                msg={"event":"EXEC","EXEC":str(btn),"VAL":str(val)}
                msgs.append(msg)
                #print("msg: ",msg)
                buf2.append(["EXEC",str(btn),val])

            if msgs:
                msgs = json.dumps(msgs).encode("utf-8")
                cmd_client.send(msgs)
                e = time.time()
                print("TIME:",int((e-s)*10000),int(e*100)/100)
                    
    except Exception as e:
        print("midi",e)

    r = 10
    fr = font15.render("MIDI: APCMINI"  ,1, (200,100,200))
    window.blit(fr,(330,10+r ))
    r+=10
    for m in buf:
        #print("-> midi:",m)
        fr = font15.render("MIDI:"+str(m)  ,1, (200,200,0))
        window.blit(fr,(330,10+r ))
        r+=10

    r = 10
    fr = font15.render("EXEC:"  ,1, (200,100,200))
    window.blit(fr,(10,10+r ))
    r+=10
    for m in buf2:
        #print("-> midi:",m)
        fr = font15.render("SEND:"+str(m)  ,1, (200,200,0))
        window.blit(fr,(10,10+r ))
        r+=10

    if 0: #timer balken
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

    clock.tick(10)
