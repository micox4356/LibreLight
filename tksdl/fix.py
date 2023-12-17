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

CAPTION = 'LibreLight SDL-FIXTURE '

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

def read_dmx():
    dmx = {} #univ
    iii = 0
    y=mc.get("index")
    key=y.keys()
    key = list(key)
    key.sort()

    for k in key:
        if k.startswith("ltp-out"):
            #v = y[k]
            u = k.split(":")[-1]
            x=mc.get(k)
            dmx[u] = x
    return dmx
            
def read_fix(dmx):
    y=mc.get("fix")#cmd)
    key=y.keys()
    key = list(key)
    key.sort()
    for k in key:#y.items():
        v = y[k]
        #print(k,v)
        x=mc.get(k)
        dmx_start = 0
        if "DMX" in v:
            dmx_start = v["DMX"]

        univ_start = 0
        if "UNIVERS" in v:
            univ_start = v["UNIVERS"]

        if "ATTRIBUT" in v: # and 10: 
            ATTR = v["ATTRIBUT"]
            for k2 in ATTR:
                k2_ATTR = ATTR[k2]

                #print(ATTR) #[k2_ATTR]) #["VALUE2"] = -2
                k2_ATTR["VALUE2"] = -2

                #if k2.endswith("-FINE"):
                #    continue
                if k2.startswith("_"):
                    continue
                k3 = k+"-"+k2
                
                dmx_nr = 0
                if "NR" in k2_ATTR:
                    if k2_ATTR["NR"] >= 1:
                        dmx_nr = k2_ATTR["NR"]+1
                
                val2 = ""
                if "VALUE" in k2_ATTR:
                    val2 = k2_ATTR["VALUE"]

                dmx_val=-1
                dmx_x=-1
                if dmx_nr > 0 and dmx_start > 0:
                    try:
                        dmx_x = dmx_start-1+dmx_nr-1
                        dmx_val = dmx[str(univ_start)][dmx_x-1]
                    except:pass
                if type(dmx_val) in [int,float]:
                    k2_ATTR["VALUE2"] = dmx_val
                else:
                    k2_ATTR["VALUE2"] = 0
    return y

def add_dmx(data,dmx):
    pass

table={}
table_grid={}
btn1_press = [] #["10.10.10.13:0"]
y=[]

                        
bx_font0 = pygame.font.SysFont("freesans-bold",20)

import lib.zchat as chat
cmd_client = chat.Client(port=30003)


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

    fr = font22.render("FIXTURE DATA (READONLY!)" ,1, (200,200,200))
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

    dmx = read_dmx()

    rgb = (0xff,0,0xaa,0)

    data = read_fix(dmx)
    #data = add_dmx(data,dmx)


    i = 0
    r=40
    if 1:
        ch = 141
        send = 0
        #cmd="stats items" 
        #if not y:
        y=data #mc.get("fix")#cmd)
        if y:
            iii = 0
            key=y.keys()
            key = list(key)
            key2 = []
            for k in key:
                try:
                    key2.append(int(k))
                except:
                    pass
            key2.sort()
            key = key2 #.sort()
            if len(btn1_press) == 0:
                btn1_press = [key[0]]
            rgb = (0x00,0,0xff,0)
            k2 = btn1_press[-1]
            fr = font22.render("SRC:"+str(k2) ,1, rgb) #(200,200,200))
            window.blit(fr,(400,1))

            fr = font22.render("FPS:"+str(fps_old) ,1, rgb) #(200,200,200))
            window.blit(fr,(600,1))


            for k in key:#y.items():
                k = str(k)
                v = y[k]
                attr_count = 0
                if "ATTRIBUT" in v:
                    for ATTR in v["ATTRIBUT"]:
                        if ATTR.startswith("_"):
                            continue
                        if ATTR.endswith("-FINE"):
                            continue
                        if ATTR == "DIM":
                            continue
                        attr_count += 1
                if attr_count <= 0:
                    continue

                #print(k,v)
                x=mc.get(k)
                cccount = 0
                txt = str([k,v,ch,"=",cccount]) #x[ch-1]])

                rgb = (0xaa,0xaa,0xaa,0)
                
                i += 1
                if k not in table:
                    bx = sdl_elm.Button(window,pos=[20,r,50,20])
                    bx.btn1.color_on = [255,255,0]
                    table[k] = bx

                    bxc = sdl_elm.Button(window,pos=[-11,r,5,20])
                    bxc.btn1.color_on = [255,255,0]
                    table[k+"_color"] = bxc

                bx = table[k]
                bx.data = v
                bxc.data = {}

                active = 0
                if "ATTRIBUT" in v:
                    if "_ACTIVE" in v["ATTRIBUT"]:
                        if "ACTIVE" in  v["ATTRIBUT"]["_ACTIVE"]:
                            if v["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] >=1:
                                active = 1

                bx.btn1.val.set(active)
                bx.text = "ID:"+ k #str(txt) #+"\n<val>\n" #.format(i+1)
                bx.font0 = bx_font0 #pygame.font.SysFont("freesans-bold",20)
                bx.btn1.bg_on = [0,255,255]
                bx.btn1.type = "toggle"
                bx.pos  = [10,r,70,20]

                if "ATTRIBUT" in v:
                    bcv_r = 0
                    bcv_g = 0
                    bcv_b = 0
                    if "RED" in v["ATTRIBUT"]:
                        bcv_r = v["ATTRIBUT"]["RED"]["VALUE2"]
                    if "GREEN" in v["ATTRIBUT"]:
                        bcv_g = v["ATTRIBUT"]["GREEN"]["VALUE2"]
                    if "BLUE" in v["ATTRIBUT"]:
                        bcv_b = v["ATTRIBUT"]["BLUE"]["VALUE2"]


                    #print("bvc_rgb" [bcv_r,bcv_g,bcv_b])
                    if bcv_r > 255:
                        bcv_r=255
                    if bcv_g > 255:
                        bcv_g=255
                    if bcv_b > 255:
                        bcv_b=255

                    bxc.btn1.color  = [bcv_r,bcv_g,bcv_b]
                    bxc.btn1.color_on  = [bcv_r,bcv_g,bcv_b]

                bxc.pos  = [85,r,20,20]
                bxc.text = ""

                bx.draw()
                bxc.draw()
                
                r_buf=bx.get_rect()[3]+2

                iii += 35
                
                rr = 0
                if "ATTRIBUT" in v: # and 10: 
                    ATTR = v["ATTRIBUT"]
                    for k2 in ATTR:
                        k2_ATTR = ATTR[k2]
                        if k2.endswith("-FINE"):
                            continue
                        if k2.startswith("_"):
                            continue
                        k3 = k+"-"+k2
                        

                        val2 = ""
                        if "VALUE" in k2_ATTR:
                            val2 = k2_ATTR["VALUE"]

                        virt = 1
                        if "NR" in k2_ATTR:
                            if k2_ATTR["NR"] > 0:
                                virt = 0

                        dmx_val = -3
                        if "VALUE2"in k2_ATTR:
                            dmx_val = k2_ATTR["VALUE2"]

                        if k3 not in table_grid:
                            bx = sdl_elm.Button(window,pos=[300,rr,60,20])
                            bx.btn1.color_on = [255,255,0]
                            bx.ID = 0
                            if "ID" in v:
                                bx.ID = v["ID"]
                            bx.ATTR = k2
                            table_grid[k3] = bx

                        if "ACTIVE" in k2_ATTR:
                            if k2_ATTR["ACTIVE"] >=1:
                                table_grid[k3].btn1.val.set(1)
                            else:
                                table_grid[k3].btn1.val.set(0)

                        bx = table_grid[k3]
                        bx.data = k2_ATTR

                        try:val = v
                        except:pass

                        bx.text = k2 +" "+str(val2)+" "+str(dmx_val) 
                        bx.font0 = bx_font0 
                        if k2 == "RED":
                            bx.btn4.color_on = [255,0,0]
                        elif k2 == "GREEN":
                            bx.btn4.color_on = [0,255,0]
                        elif k2 == "BLUE":
                            bx.btn4.color_on = [0,0,255]


                        if virt == 1:
                            bx.btn3.color= [0,0,0]

                        bx.btn1.type = "toggle"
                        if type(dmx_val) == int:
                            bx.btn4.val.set(dmx_val) # "toggle"
                        bx.pos  = [100+rr,r,120,20]
                        bx.draw()
                        rr+=bx.get_rect()[2]+2
                        if rr > 1000:
                            break

                r += r_buf
                if r > 800:
                    break



    if 0:#kill:
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
                    #t.btn2.clean()
                    t.btn1.clean()
                for k in table_grid:
                    t = table_grid[k]
                    #t.btn2.clean()
                    t.btn1.clean()

        #print("event",event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.VIDEORESIZE:
            scrsize = event.size
            width   = event.w
            hight   = event.h
            resize_changed = True

        for t in table:
            #print(t)
            table[t].event(event)
            if table[t].btn3.get():
                data = table[t].data
                print("FIX:",data)

        for t in table_grid:
            #print(t)
            change = table_grid[t].event(event)
            if table_grid[t].btn3.get():
                data = table_grid[t].data
                FIX = table_grid[t].ID
                ATTR = table_grid[t].ATTR
                print("change",change)

                key = "MOUSE ENCODER"
                if key in change:
                    if "press" in change[key]:
                        msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"++","ATTR":ATTR}]).encode("utf-8")
                    if "release" in change[key]:
                        msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"--","ATTR":ATTR}]).encode("utf-8")
                    print("   ",msg)
                    cmd_client.send(msg)

                key = "BUTTON"
                if key in change:
                    if "press" in change[key]:
                        #print(" ATTR:",FIX,ATTR,data)
                        #print("  CHANGE",change)
                        msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                        print("   ",msg)
                        cmd_client.send(msg)
                
            


        if "pos" in event.dict:
            if "button" in event.dict:
                if event.type == 5:#press
                    mouse_down = 1
                    mouse_pos1 = [event.pos[0],event.pos[1]]
                if event.type == 6:#release
                    mouse_down = 0

                for btn in mouse_grab:
                    #btn.btn2.val.set(1)
                    btn.btn1.val.set(1)
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

            for k3 in table_grid:
                t = table_grid[k3]
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



