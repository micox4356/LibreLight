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

CAPTION = 'LibreLight SDL-FIX-LIST '
SHIFT_FINE = 0

sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import tool.movewin as movewin
import tool.git as git
#CAPTION += git.get_all()


win_title =CAPTION.strip().split()[-1]
store = movewin.load_all_sdl(win_title)
print(store)
W=850
H=460
POS=[20,20]
if store:
    W = store[-4]
    H = store[-3]
    POS=[store[-2],store[-1]]
#exit()

#CAPTION += ':{}'.format(random.randint(100,999))
CAPTION += git.get_all()

import pathlib
_file_path=pathlib.Path(__file__)
print("file:",_file_path)

#_id = movewin.winfo(CAPTION)
#c1 = movewin.movewin(_id,200,50)
#os.system(c1)
#c1 = movewin.activate(_id)
#os.system(c1)

movewin.check_is_started(CAPTION,_file_path)



# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
pg = pygame
main_size=(W,H)#850,460)
window = pygame.display.set_mode(main_size,pg.RESIZABLE,32)

pg = pygame
pygame.init()
pygame.mixer.quit()
clock = pygame.time.Clock()
try:
    icon = pygame.image.load('icon/scribble.png')
    pygame.display.set_icon(icon)
except Exception as e:
    print("      ERROR:",os.getcwd())
    print("      ERROR:set_icon ",e) #,color="red")

import tool.movewin as movewin
import tool.sdl_elm as sdl_elm

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
#bx.btn1['type'] = "flash"
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
    global mc
    y=mc.get("fix")#cmd)
    if y is None:
        print("==== "*10)
        print("error -- read_fix(dmx) mc.get('fix') return",y)
        print()
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        return {}
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


win_con = movewin.Control()
win_con.title = win_title
win_con.winfo()
if POS:
    win_con.move(POS[0],POS[1])
print(POS,win_con.title)


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


# -------------------
x=200
y=5
bx = sdl_elm.Button(window,pos=[x,y,50,20])
bx.text = " HELP "
import lib.libtk as libtk
def xhelp(event=None):
    #print(event)
    libtk.online_help("librelight:20-exec")()
bx.btn1.cb_on.set(xhelp)
#bx.draw()
btn_help=bx
# -------------------

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

        fr = font15.render("FPS:"+str(fps_old) ,1, rgb) #(200,200,200))
        window.blit(fr,(600,5))

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



        BTN_WIDTH = 120
        #scroll_bar.btn4.val._max = len(data)-8  #draw()
        scroll_max = len(data)-8
        scroll_max = len(data.keys())-8
        scroll_max = 1 
        block_wrap = int( (width-200) / BTN_WIDTH)
        if block_wrap <= 0:
            block_wrap = 1


        for k in data.keys():
            fix_type = get_fix_type(data[k])
            if "ATTRIBUT" in data[k]:
                row = data[k]["ATTRIBUT"]
                acount = get_attr_count(row)
                if fix_type == "DIM":
                    continue

    
                if acount > block_wrap:
                    scroll_max += int(acount/block_wrap)
                else:
                    scroll_max += 1


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
                        bx = sdl_elm.Button(window,pos=[20+20,r,50,20])
                        bx.btn1.color_on = [255,255,0]
                        bx.ID = -1
                        if "ID" in v:
                            bx.ID = v["ID"]
                        if bx.ID == 0:
                            bx.ID = -2
                        bx.ATTR = "_ACTIVE"
                        table[k] = bx
                        
                        # color box
                        bxc = sdl_elm.Button(window,pos=[-11+20,r,5,20])
                        bxc.btn1.color_on = [255,255,0]
                        table[k+"_color"] = bxc



                    bx = table[k]
                    bx.data = v
                    bxc.data = {}

                    active = is_active_fix(v)
                    bx.btn1.val.set(active)
                    try:
                        if int(k) % 10 == 0:
                            #pygame.draw.aaline(window,[255,0,0],[2,r],[800,r],1)
                            pygame.draw.rect(window,[58,58,58],[2,r,2000,25])
                    except:pass
                    bx.text = "ID:"+ k 

                    bx.text += " "+v["NAME"]
                    bx.font0 = bx_font0
                    bx.btn1.bg_on = [0,255,255]
                    bx.btn1.type = "toggle"
                    bx.pos  = [10+10,r,BTN_WIDTH,20]

                    if "ATTRIBUT" in v:
                        try: # info
                            if int(k) == 12001:
                                #print("   ",k,k2,k2_ATTR)
                                print("-",v["ATTRIBUT"].keys())
                        except: pass
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

                    bxc.pos  = [140+5,r,20,20]
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
                            bx.pos  = [170+rr,r,BTN_WIDTH,20]
                            bx.draw()
                            rr+=bx.get_rect()[2]+2
                            

                            table_grid_draw.append(k3) #table_grid[k3]

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

                if SHIFT_FINE:
                    fr = font18.render("ENCODER:±0.25" ,1, [255,255,0])
                else:
                    fr = font18.render("ENCODER:±5.00" ,1, [255,255,0])
                window.blit(fr,(420,5))


        if 0: #show line number +scroll_pos
            bxc = sdl_elm.Button(window,pos=[-11+10,(0*23),50,10])
            bxc.text = "{:0.02f} {}".format(scroll_pos,scroll_max)
            ii = int(scroll_pos) #int(scroll_pos/23*29)
            bxc.font0 = bx_font0
            bxc.draw()

            for i in range(40+1):
                bxc = sdl_elm.Button(window,pos=[0,40+(i*23),30,10])
                bxc.text = "{}".format(1+i+ii)
                bxc.btn1.color = [255,200,200]
                bxc.btn2.color = [255,200,200]
                bxc.btn3.color = [255,200,200]
                bxc.font0 = bx_font0
                bxc.draw()

        btn_help.draw()
        resize_changed = 0
        for raw_event in pygame.event.get(): 
            x_change=btn_help.event(raw_event)
            event = {'unicode': '', 'key': 0, 'mod': 0, 'scancode': 0, 'window': None,'type':'','button':''}
            event['type'] = raw_event.type
            event.update( raw_event.dict)
            if event['button'] and event["type"] in [pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP]:
                event["type"] -= 1020

            if event["button"] or event['scancode']:
                print(" event:",event)


            if "scancode" in event:
                #print(" ",event)
                if event['scancode'] in [50,225]: # shift old/new
                    if event['type'] in [2,768]: # press
                        #pg.display.set_caption(CAPTION+ " SHIFT/FINE")
                        SHIFT_FINE = 1
                    if event['type'] in [3,769]: # release
                        #pg.display.set_caption(CAPTION)
                        SHIFT_FINE = 0

                if event['scancode'] in [9,41]:
                    for k in table_draw:
                        t = table[k]
                        t.btn1.clean()
                    for k in table_grid_draw:
                        t = table_grid[k]
                        t.btn1.clean()

                    msg=json.dumps([{"event":"ESC"}]).encode("utf-8")
                    print("ESC",msg)
                    cmd_client.send(msg)

                if event['mod'] == 0:
                    keycode = {27:"REC",39:"SELECT",46:"LABEL",54:"CFG-BTN",56:"BLIND",41:"FLASH",26:"EDIT"}
                    #print(" 45:", event['scancode'] in keycode,event['scancode'])
                    if event['scancode'] in keycode: # r
                        if event['type'] == 2: # press
                                
                            msg=json.dumps([{"event":keycode[event['scancode']]}]).encode("utf-8")
                            print("SPCIAL-KEY",msg)
                            cmd_client.send(msg)
                if event['mod'] == 64:
                    keycode = {39:"SAVE\nSHOW",54:"RESTART"}
                    print( " 56:",event['scancode'] in keycode,event['scancode'])
                    if event['scancode'] in keycode: # r
                        if event['type'] == 2: # press
                                
                            msg=json.dumps([{"event":keycode[event['scancode']]}]).encode("utf-8")
                            print("SPCIAL-KEY",msg)
                            cmd_client.send(msg)

                if event['scancode'] in range(10,20+1) or event['scancode'] in range(30,39+1):
                    if event['type'] in [2,3,768,769]: # press
                        if event['type'] in [2,769]:
                            v=0
                        if event['type'] in [3,768]:
                            v=255
                        btn_nr=-3000

                        if event['scancode'] in range(10,20+1):
                            btn_nr = event['scancode']-10+1
                        if event['scancode'] in range(30,39+1):
                            btn_nr = event['scancode']-30+1
                        btn_nr_raw = btn_nr
                        btn_nr += 161-1
                        msg=json.dumps([{"event":"EXEC","EXEC":btn_nr,"VAL":v,"NR-KEY":btn_nr_raw}]).encode("utf-8")

                        print("SPCIAL-KEY",msg)
                        cmd_client.send(msg)

                def f1_bis_f12_alt(scancode,_type):
                    if scancode in range(67,76+1) and _type in [2,3]:   # F1-F12 OLD
                        return 1

                def f1_bis_f12_neu(scancode,_type):
                    if scancode in range(58,92+1) and _type in [768,769]:  # F1-F12 NEW
                        return 1


                if f1_bis_f12_alt(event['scancode'], event['type']) or f1_bis_f12_neu(event['scancode'], event['type']) or  event['scancode'] in [95,96]:
                    if event['type'] in [2,3,768,769]: # press
                        if event['type'] in [2,769]:
                            v=0
                        if event['type'] in [3,768]:
                            v=255

                        btn_nr = event['scancode']
                        if btn_nr == 95:
                            btn_nr = 11
                        elif btn_nr == 96:
                            btn_nr = 12
                        else:
                            if event['type'] in [768,769]:
                                btn_nr = event['scancode']-57
                            else:
                                btn_nr = event['scancode']-66
                        btn_nr_raw = btn_nr
                        if f1_bis_f12_alt(event['scancode'], event['type']):
                            btn_nr_raw = str(btn_nr) +"-ALT"
                        if f1_bis_f12_neu(event['scancode'], event['type']):
                            btn_nr_raw = str(btn_nr) +"-NEU"

                        btn_nr += 81-1
                        msg=json.dumps([{"event":"EXEC","EXEC":btn_nr,"VAL":v,"F-KEY":btn_nr_raw}]).encode("utf-8")
                        print("SPCIAL-KEY",msg)
                        cmd_client.send(msg)

            if event['type'] == pygame.QUIT:
                print()
                print("quit",event)
                pygame.quit()
                sys.exit(0)
            elif event['type'] == pygame.VIDEORESIZE:
                print()
                print("resize",event)
                scrsize = event['size']
                width   = event['w']
                hight   = event['h']
                resize_changed = True

            scroll_bar.event(raw_event) #daraw()
            scroll_change = 0
            if scroll_bar.btn3.val.get(): #scroll_bar focus
                spos = scroll_bar.rel_pos[1]
                #print("------------------",spos)
                if "button" in event:
                    if event["button"] == 1:
                        scroll_bar.btn4.val.set(scroll_bar.btn4.val._max*spos)

                if "buttons" in event:
                    if event["buttons"][0]:
                        scroll_bar.btn4.val.set(scroll_bar.btn4.val._max*spos)

            event_lock = scroll_bar.btn3.val.get() #focus on

            if not event_lock:
                for t in table_draw:
                    table[t].event(raw_event)
                    if table[t].btn3.get():
                        data = table[t].data
            


            if not event_lock:
                for k3 in table_draw:
                    #print(t)
                    row = table[k3]
                    change = table[k3].event(raw_event)
                    if row.btn3.get():
                        # FIXTURE SELECTOR
                        data = row.data
                        FIX  = row.ID
                        ATTR = row.ATTR

                        key = "BUTTON"
                        if key in change:
                            if "press" in change[key]:
                                msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                print("  msg:",msg)
                                cmd_client.send(msg)
                            if "release" in change[key]:
                                pass


            if not event_lock:
                for k3 in table_grid_draw:
                    row = table_grid[k3]
                    change = table_grid[k3].event(raw_event)
                    if row.btn3.get():
                        data = row.data
                        FIX  = row.ID
                        ATTR = row.ATTR

                        key = "MOUSE ENCODER"
                        if key in change:
                            ACC = 2
                            if SHIFT_FINE:
                                ACC = 1

                            VAL = ""
                            if "press" in change[key]:
                                VAL = "+"*ACC
                            if "release" in change[key]:
                                VAL = "-"*ACC

                            msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":VAL,"ATTR":ATTR}]).encode("utf-8")
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


            if "pos" in event:
                if "button" in event:
                    if event['type'] in [5,pygame.MOUSEBUTTONDOWN]:#press
                        mouse_down = 1
                        mouse_pos1 = [event['pos'][0],event['pos'][1]]
                    if event['type'] in [6,pygame.MOUSEBUTTONUP]:#release
                        mouse_down = 0

                mouse_pos2 = [event['pos'][0],event['pos'][1]]



            if event_lock:
                pass

            elif "button" in event:
                if event['type'] in [6,pygame.MOUSEBUTTONUP]:
                    if event["button"] == 1:
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
                                    print("    send:",msg)
                                    cmd_client.send(msg)
                            else: #no btn is on
                                msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS","FIX":str(FIX),"VAL":"click","ATTR":ATTR}]).encode("utf-8")
                                print("    send:",msg)
                                cmd_client.send(msg)

                        mouse_grab = []
                    if event["button"] == 3:
                        mouse_grab_active = 0
                        for mg in mouse_grab:
                            if mg.btn1.val.get():
                                mouse_grab_active += 1
                        
                        for mg in mouse_grab:
                            FIX = str(mg.ID)
                            ATTR = str(mg.ATTR)

                            if mouse_grab_active:
                                if mg.btn1.val.get():
                                    msg = json.dumps([{"event":"FIXTURES","TYPE":"ENCODERS"
                                                        ,"FIX":str(FIX),"VAL":"click"
                                                        ,"ATTR":ATTR}]).encode("utf-8")
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

