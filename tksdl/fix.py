#!/usr/bin/python3

import time
        
import traceback
boot = time.time()
from collections import OrderedDict
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
while 1:
    try:
        pids = movewin.search_process(_file_path)
        break
    except Exception as e:
        print("exception 34",e)
        time.sleep(1)

CAPTION = 'LibreLight FIXTURE-LIST '

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
font18 = pygame.font.SysFont("freemonobold",18)
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
    if y:
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
                k2_ATTR["VALUE2"] = -2

                if is_hidden_attr(k2):
                    #if k2.startswith("_"):
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


def reorder_table_by_pos(table_grid):

    if type(table_grid) in (dict,OrderedDict):
        # order table of type dict by pos [x,y]
        table_grid5 = {}
        for t5 in table_grid:
            t5_row = table_grid[t5]
            #print(t5,t5_row.pos)
            k5 = "{:010}-{:010}".format(t5_row.pos[0],t5_row.pos[1])
            table_grid5[k5] = [t5,t5_row]

        ordered = list(table_grid5.keys())
        ordered.sort()

        table_grid2 = OrderedDict()
        for k5 in ordered: #table_grid5:
            k5_row = table_grid5[k5]
            table_grid2[k5_row[0]] = k5_row[1]

        return table_grid2
    

    if type(table_grid) is list:
        # order table of type list by pos [x,y]
        table_grid5 = {}
        for t5 in table_grid:
            t5_row = t5 #table_grid[t5]
            #print(t5)#,t5_row.pos)
            k5 = "{:010}-{:010}".format(t5_row.pos[1],t5_row.pos[0])
            table_grid5[k5] = [t5,t5_row]

        ordered = list(table_grid5.keys())
        ordered.sort()
        table_grid2 = [] #OrderedDict()
        for k5 in ordered: #table_grid5:
            k5_row = table_grid5[k5]
            table_grid2.append( k5_row[1] )

        return table_grid2

    return table_grid

def is_active_fix(v):
    if "ATTRIBUT" in v:
        if "_ACTIVE" in v["ATTRIBUT"]:
            if "ACTIVE" in  v["ATTRIBUT"]["_ACTIVE"]:
                if v["ATTRIBUT"]["_ACTIVE"]["ACTIVE"] >=1:
                    return 1
    return 0

def is_hidden_attr(attr_name):
    if attr_name.endswith("-FINE"):
        return 1
    if attr_name.startswith("_"):
        return 1
    return 0

def count_active_attr(fix_row):
    return len(get_active_attr(fix_row))

def get_active_attr(fix_row):
    # fix_row = {ID:"12"NAME:"xyz",ATTRIBUTE:{"RED":{"VALUE":0}}}
    active_attr = []
    if "ATTRIBUT" in fix_row: 
        attr_row = fix_row["ATTRIBUT"]

        for attr_name in attr_row:
            if is_hidden_attr(attr_name):
                continue

            attr_data = attr_row[attr_name]
            if "ACTIVE" in attr_data:
                if attr_data["ACTIVE"] >=1:
                    active_attr.append(attr_name)

    return active_attr

def get_attr_count(attr_row):
    acount = 0
    for attr in attr_row:
        if is_hidden_attr(attr):
            continue
        acount+=1
    return acount

def get_fix_type(fix_row):
    attr2 = []
    if "ATTRIBUT" in fix_row:
        attr_row = fix_row["ATTRIBUT"]
        for attr in attr_row:
            if is_hidden_attr(attr):
                continue
            attr2.append(attr)

    if "PAN" in attr2 and "TILT" in attr2:
        return "MOVER"
    if "RED" in attr2 and "GREEN" in attr2 and "BLUE" in attr2:
        return "RGB"
    if len(attr2) == 1 and "DIM" in attr2:
        return "DIM"

    return "UNKNOWN"

table={}
table_grid={}
btn1_press = [] #["10.10.10.13:0"]
y=[]

                        
bx_font0 = pygame.font.SysFont("freesans-bold",20)

import lib.zchat as chat
cmd_client = chat.Client(port=30003)
err = []
#err.append([time.time(),"init"])

scroll_bar = sdl_elm.Button(window,pos=[640,40,40,400])
scroll_bar.btn1.color_on = [255,255,0]
scroll_bar.dbg = 0
scroll_bar.btn4.color_on=[0,0,0]
scroll_bar.btn4.color_off=[0,0,0]
scroll_bar.fader = "v" 
scroll_bar.text="\n"*10+"<ival%>%"
scroll_bar.text=" "

scroll_bar.btn4.nr_on  = [5]
scroll_bar.btn4.nr_off = [4]
scroll_bar.draw()

width,hight   = main_size #[1]
scroll_max = 100

def draw_frame(window):
    fr = font22.render("FIXTURE LIST " ,1, (200,200,200))
    window.blit(fr,(20,5 ))

    fr = font22.render("DEMO / TEST - MODE ! "  ,1, (200,200,200))
    #window.blit(fr,(10,30 ))

while 1:

    try:
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
        
        #window.fill((2,2,2))
        window.fill((0,0,0))
        pygame.draw.rect(window,(0,0,0),[0,0,main_size[0],main_size[1]])


        draw_frame(window)

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


        #scroll_bar.btn4.val._max = len(data)-8  #draw()
        scroll_max = len(data)-8
        scroll_max = len(data.keys())-8
        scroll_max = 1 
        block_wrap = int((width -200 ) /120)
        if block_wrap <= 0:
            block_wrap = 1


        for k in data.keys():
            fix_type = get_fix_type(data[k])
            if "ATTRIBUT" in data[k]:
                row = data[k]["ATTRIBUT"]
                acount = get_attr_count(row)
                if fix_type == "DIM":
                    continue

                scroll_max += 1
    
                if acount:
                    scroll_max += int(acount/block_wrap)


        #print()
        scroll_bar.btn4.val._max = scroll_max
        scroll_bar.increment = (len(data))/100*10  #draw()
        #data = add_dmx(data,dmx)
        scroll_pos = scroll_bar.btn4.val.get()
        scroll_bar.pos[0] = width-scroll_bar.pos[2]-5
        scroll_bar.pos[3] = hight-80

        #print(scroll_pos)
        table_grid_draw=[] #{}
        table_draw = []

        active_fix = 0
        active_attr = 0

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
                    #print(k)
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
                #fr = font22.render("SRC:"+str(k2) ,1, rgb) #(200,200,200))

                fr = font15.render("FPS:"+str(fps_old) ,1, rgb) #(200,200,200))
                window.blit(fr,(600,5))

                err_r = 0
                if err:
                    for e in err:
                        rgb = (255,0,0)
                        fr = font15.render("err:"+str(e) ,1, rgb) #(200,200,200))
                        window.blit(fr,(700,5+err_r))
                        err_r += 20

                i4 = 0
                for k in key:
                    k = str(k)
                    fix_row = y[k]

                    fix_type = get_fix_type(fix_row)
                    if fix_type == "DIM":
                        continue

                    active_fix  += is_active_fix(fix_row)
                    active_attr += count_active_attr(fix_row)


                for k in key:#y.items():

                    k = str(k)
                    v = y[k]
                    fix_row = v

                    fix_type = get_fix_type(fix_row)
                    if fix_type == "DIM":
                        continue


                    #scroll_max+=1
                    i4 += 1
                    if i4 < scroll_pos:
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
                        bx.ID = -1
                        if "ID" in v:
                            bx.ID = v["ID"]
                        if bx.ID == 0:
                            bx.ID = -2
                        bx.ATTR = "_ACTIVE"
                        table[k] = bx
                        
                        # color box
                        bxc = sdl_elm.Button(window,pos=[-11,r,5,20])
                        bxc.btn1.color_on = [255,255,0]
                        table[k+"_color"] = bxc



                    bx = table[k]
                    bx.data = v
                    bxc.data = {}

                    active = is_active_fix(v)
                    bx.btn1.val.set(active)

                    bx.text = "ID:"+ k 
                    bx.text += " "+v["NAME"]
                    bx.font0 = bx_font0
                    bx.btn1.bg_on = [0,255,255]
                    bx.btn1.type = "toggle"
                    bx.pos  = [10,r,120,20]

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

                    bxc.pos  = [140,r,20,20]
                    bxc.text = ""

                    bx.draw()
                    bxc.draw()
                    
                    r_buf=bx.get_rect()[3]+2

                    iii += 35
                    
                    rr = 0
                    acount = 0
                    if "ATTRIBUT" in v: # and 10: 
                        ATTR = v["ATTRIBUT"]
                        for k2 in ATTR:
                            k2_ATTR = ATTR[k2]

                            if is_hidden_attr(k2):
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
                                bx = sdl_elm.Button(window,pos=[600,rr,60,20])
                                bx.btn1.color_on = [255,255,0]
                                bx.ID = 0
                                if "ID" in v:
                                    bx.ID = v["ID"]
                                bx.ATTR = k2
                                table_grid[k3] = bx


                            if "ACTIVE" in k2_ATTR:
                                if k2_ATTR["ACTIVE"] >=1:
                                    table_grid[k3].btn1.val.set(1)
                                    #active_attr += 1
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
                            bx.pos  = [170+rr,r,120,20]
                            bx.draw()
                            rr+=bx.get_rect()[2]+2
                            

                            table_grid_draw.append(k3) #table_grid[k3]
                            if rr > 1000:
                                break
                            acount +=1
                            if acount %block_wrap==0:
                                r += r_buf
                                rr = 0

                    table_draw.append(k)

                    r += r_buf
                    if r > hight-30:#/20:
                        break



                active_ratio = 0
                if active_fix:
                    active_ratio = (active_attr/active_fix)
                fr = font18.render("ACTIVE:{}:{} ({:0.01f})".format(active_fix,active_attr,active_ratio) ,1, [255,255,0]) #(200,200,200))
                window.blit(fr,(300,5))



        resize_changed = 0
        for event in pygame.event.get(): 
            if "scancode" in event.dict:
                if event.scancode == 9:
                    for k in table_draw:
                        t = table[k]
                        #t.btn2.clean()
                        t.btn1.clean()
                    for k in table_grid_draw:
                        t = table_grid[k]
                        #t.btn2.clean()
                        t.btn1.clean()

                    msg=json.dumps([{"event":"CLEAR"}]).encode("utf-8")
                    print("ESC",msg)
                    cmd_client.send(msg)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.VIDEORESIZE:
                scrsize = event.size
                width   = event.w
                hight   = event.h
                resize_changed = True

            scroll_bar.event(event) #daraw()
            scroll_change = 0
            if scroll_bar.btn3.val.get(): #scroll_bar focus
                spos = scroll_bar.rel_pos[1]
                #print("------------------",spos)
                if "button" in event.dict:
                    if event.dict["button"] == 1:
                        scroll_bar.btn4.val.set(scroll_bar.btn4.val._max*spos)

                if "buttons" in event.dict:
                    if event.dict["buttons"][0]:
                        scroll_bar.btn4.val.set(scroll_bar.btn4.val._max*spos)

            event_lock = scroll_bar.btn3.val.get() #focus on

            if not event_lock:
                for t in table_draw:
                    table[t].event(event)
                    if table[t].btn3.get():
                        data = table[t].data
            


            if not event_lock:
                for k3 in table_draw:
                    #print(t)
                    row = table[k3]
                    change = table[k3].event(event)
                    if row.btn3.get():
                        # FIXTURE SELECTOR
                        data = row.data
                        FIX  = row.ID
                        ATTR = row.ATTR

                        key = "BUTTON"
                        if key in change:
                            if "press" in change[key]:
                                msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                print("   ",msg)
                                cmd_client.send(msg)
                            if "release" in change[key]:
                                pass
            if not event_lock:
                for k3 in table_grid_draw:
                    row = table_grid[k3]
                    change = table_grid[k3].event(event)
                    if row.btn3.get():
                        data = row.data
                        FIX  = row.ID
                        ATTR = row.ATTR

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
                            if "release" in change[key]:
                                pass


            if "pos" in event.dict:
                if "button" in event.dict:
                    if event.type == 5:#press
                        mouse_down = 1
                        mouse_pos1 = [event.pos[0],event.pos[1]]
                    if event.type == 6:#release
                        mouse_down = 0

                mouse_pos2 = [event.pos[0],event.pos[1]]



            if event_lock:
                pass

            elif "button" in event.dict:
                if event.type == 6:
                    #print("grab DOOOO",event)
                    #print("grab2", event.dict["button"],len(mouse_grab) )
                    if event.dict["button"] == 1:
                        mouse_grab_active = 0
                        for mg in mouse_grab:
                            if mg.btn1.val.get():
                                mouse_grab_active += 1
                        
                        for mg in mouse_grab:
                            FIX = str(mg.ID)
                            ATTR = str(mg.ATTR)

                            if mouse_grab_active:
                                if not mg.btn1.val.get():
                                    msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                    cmd_client.send(msg)
                            else: #no btn is on
                                msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                cmd_client.send(msg)

                        mouse_grab = []
                    if event.dict["button"] == 3:
                        mouse_grab_active = 0
                        for mg in mouse_grab:
                            if mg.btn1.val.get():
                                mouse_grab_active += 1
                        
                        for mg in mouse_grab:
                            FIX = str(mg.ID)
                            ATTR = str(mg.ATTR)

                            if mouse_grab_active:
                                if mg.btn1.val.get():
                                    msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                    #print("  mouse_grab ",msg,mg.btn1.val.get())
                                    cmd_client.send(msg)

                        mouse_grab = []



        
        if mouse_down:
            d1 = mouse_pos1[0]-mouse_pos2[0]
            d2 = mouse_pos1[1]-mouse_pos2[1] 
            pix = 10
            if ( d1 > pix or d1 < -pix)  or  ( d2 >pix or d2 < -pix):

                sdl_elm.draw_mouse_box(window,mouse_pos1,mouse_pos2)
                for k in table_draw: # FIX-ID
                    t = table[k]
                    pos = t.get_rect()

                    mpos = [mouse_pos1[0],mouse_pos1[1],mouse_pos2[0],mouse_pos2[1]]

                    if sdl_elm.check_area2(pos,mpos):
                        if t not in mouse_grab:
                            mouse_grab.append(t)
                    else:
                        if t in mouse_grab:
                            mouse_grab.remove(t)


                for k3 in table_grid_draw: # FIX-ATTR
                    t = table_grid[k3]
                    pos = t.get_rect()

                    mpos = [mouse_pos1[0],mouse_pos1[1],mouse_pos2[0],mouse_pos2[1]]

                    if sdl_elm.check_area2(pos,mpos):
                        if t not in mouse_grab:
                            mouse_grab.append(t)
                    else:
                        if t in mouse_grab:
                            mouse_grab.remove(t)


            for k3 in table_grid:
                t = table_grid[k3]
                t._set_mouse_focus(0)

            i = 1
            if mouse_grab:
                mouse_grab = reorder_table_by_pos(mouse_grab)
                for t in mouse_grab:
                    t._set_mouse_focus(1)
                    pos = t.pos[:2]
                    pos[0] += 100
                    pos[1] += 8
                    rgb = (0,255,255)
                    fr = font15.render(""+str(i) ,1, rgb) #(200,200,200))
                    #print(pos)
                    pygame.draw.rect(window,(0,0,0),[pos[0]-2,pos[1]-2,15,13])
                    window.blit(fr,pos)
                    i+=1

                



        if resize_changed:# = True
            screen = pygame.display.set_mode(scrsize,pg.RESIZABLE)







        scroll_bar.draw()

        clock.tick(6)

    except Exception as e:
        err.append([int((time.time()-boot)*100),e])
        traceback.print_exc()
        print("Exc",e)

