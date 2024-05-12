from pyray import *
import pyray 
ConfigFlags(FLAG_MSAA_4X_HINT) #|FLAG_WINDOW_RESIZABLE  )
#ConfigFlags(FLAG_WINDOW_RESIZABLE  )
ConfigFlags(FLAG_WINDOW_HIGHDPI )
init_window(800, 450, "RAY-DMX",10,10,10,10)
#pyray.TextureFilter(font1,1)

import sys
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import tool.tk_elm as tk_elm

img = "/opt/LibreLight/Xdesk/icon/scribble.png"
IMG = load_image(img)
print(set_window_icon(IMG)) 



#SetWindowIcon(Image image) 
#for d in dir():
#    if "image" in d.lower():
#        print(d)

import time

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)


#x=mc.get(k)

old_x = -10
old_y = -10
start = time.time()
frame_count = 0
fps_count = 0

#a = "resources/pixantiqua.ttf"
#a = "/lib/firefox-esr/fonts/TwemojiMozilla.ttf"
#a = "/lib/python3/dist-packages/pygame/freesansbold.ttf"
#a = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
#a = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
#a = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
a = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
#a = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"


k=200
i= 40 #60
#font1 = load_font_ex(a, i, pyray.ffi.new('int *', 6), 1024);
font1 = load_font_ex(a, i, None, 0);
#font1 = load_font(a ) #, i, pyray.ffi.new('int *', 2), k);

# `SetTextureFilter(font.texture, TEXTURE_FILTER_TRILINEAR)` did the trick. 
# `TEXTURE_FILTER_BILINEAR` also worked fine, but the trilinear option worked better. 

pyray.TextureFilter(3)

while not window_should_close():
    begin_drawing()
    for o in dir(font1):
        print(o)
    print()
    print(font1.texture) # (3)

    clear_background(BLACK)
    Color(255,0,0,0)
    rl_enable_smooth_lines()
    if 0: # font test
        draw_line(2, 2, 100, 2, (255,225,0,220))
        print(load_font_ex.__doc__) #("resources/pixantiqua.ttf", 32, 0, 250);

        i = 20
        
        draw_text_ex(font1,b"73qwertzuio", [30,12], 45, 0, YELLOW)# VIOLET)
        draw_text_ex(font1,"11a", [37,212], 45, 0, YELLOW)# VIOLET)
        draw_text_ex(font1,"a1131", [44,302], 45, 0, YELLOW)# VIOLET)

        draw_text(str("{} {}".format(i,k)), 50, 75, 34, YELLOW)# VIOLET)

    if 10:
        btn = tk_elm.Button(None,pos=[350,12])
        x=btn.btn1.name
        a = btn.pos
        draw_text(str(x), 5, a[0]   , a[1], YELLOW)# VIOLET)
        x=btn.btn2.name

        draw_text(str(x), 5, a[0]+15, a[1], YELLOW)# VIOLET)
        x=btn.btn3.name
        draw_text(str(x), 5, a[0]+30, a[1], YELLOW)# VIOLET)
        x=btn.btn4.name

    font_size = 14
    try:
        y=mc.get("index")#cmd)
        GREY = [122,122,122,255]
        p=0
        keys = []
        for k in y:
            keys.append(k)
        keys.sort()

        k=keys[2]
        for i,v in enumerate(range(20+1)):
            # COL NUMBER -> 1 2... 20
            x2 = 180+i*30
            y2 =   5 #+i*13
            txt=str(i+1)
            #draw_text(txt, x2, y2, 11, YELLOW)
            draw_text_ex(font1,txt, [x2,y2], font_size, 0, YELLOW)
            i+=1
            if i % 20 == 0:
                break
        xi=0
        yi=0

        for i,v in enumerate(mc.get(k)):
            #print(i,v)
            txt = str(i)+":"+str(v)
            txt = str(v)
            x2 = 180+xi*30
            y2 =  25+yi*16
            try:
                draw_rectangle(x2-2, y2-2,24,13,[255,255,255,int(v)])
            except:
                draw_rectangle(x2-2, y2-2,24,13,[255,2,2,255])
            try:
                int(v)
            except:
                v=0

            if int(v) > 100:
                draw_text_ex(font1,txt, [x2,y2], font_size, 0, BLACK)# VIOLET)
            else:
                draw_text_ex(font1,txt, [x2,y2], font_size, 0, GREY)# VIOLET)
            xi+=1

            if xi % 20 == 0:
                txt = str(int(yi*20)+1)
                draw_text_ex(font1,txt, [170-30,y2], font_size, 0, YELLOW)# VIOLET)
                xi = 0
                yi += 1



        txt = str(int(yi*20)+1)
        draw_text_ex(font1,txt, [170-30,y2], font_size, 0, YELLOW)# VIOLET)
        p=0
        for k in keys:
            # HOST LIST  
            x2 = 10
            y2 =  20+p
            txt =":"+str(k) 
            #draw_text(txt, x2, y2, 20, GREY)# VIOLET)
            draw_text_ex(font1,txt, [x2,y2], font_size, 0, YELLOW)# VIOLET)
            p+=20

        x=100
        y=100
        w=200
        h=50
        #draw_rectangle(x, y,w,h,[255,0,20,255])
        x=200
        y=200
        #draw_rectangle_lines(x,y,w,h,[255,200,20,255])
        #for i in  MouseButton:
        #    if is_key_down(i):
        #        print(i)
        #for i in  range(0,512):
        #    if is_key_down(i):
        #        print(i)
        draw_text("FPS:{}".format(fps_count), 3, 3, 3, VIOLET)
        #Color(255,0,0,0)
        m=get_mouse_position()
        if m.x != old_x or m.y != old_y:
            old_x = m.x
            old_y = m.y
            print(m.x,m.y)
        draw_rectangle(int(old_x-10),int(old_y-1),20,2,[255,0,255,255])
        draw_rectangle(int(old_x-1),int(old_y-10),2,20,[255,0,255,255])
        end_drawing()
        time.sleep(0.1)

        frame_count += 1
        if time.time()-start > 1:
            start = time.time()
            fps_count = frame_count
            frame_count = 0

    except KeyboardInterrupt as e:
        raise e
    except Exception as e:# KeyInterupt
        print("err",e)
        time.sleep(1)
        #raise e
close_window()

