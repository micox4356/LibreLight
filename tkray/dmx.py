from pyray import *
init_window(800, 450, "RAY-DMX")

import time

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)


#x=mc.get(k)

old_x = -10
old_y = -10

while not window_should_close():
    try:
        y=mc.get("index")#cmd)
        begin_drawing()
        clear_background(BLACK)
        GREY = [122,122,122,255]
        p=0
        keys = []
        for k in y:
            keys.append(k)
        keys.sort()

        k=keys[2]
        xi=0
        yi=0
        for i,v in enumerate(range(20+1)):
            txt=str(i+1)
            draw_text(txt, 180+xi*30, 5+yi*13, 11, YELLOW)# VIOLET)
            xi+=1
            if xi % 20 == 0:
                break
        xi=0
        yi=0

        #draw_text(str(1), 170+xi*30, 5+yi*13, 11, YELLOW)# VIOLET)
        for i,v in enumerate(mc.get(k)):
            #print(i,v)
            txt = str(i)+":"+str(v)
            txt = str(v)
            x2 = 180+xi*30
            y2 =  25+yi*13

            try:
                draw_rectangle(x2-2, y2-2,24,13,[255,255,255,int(v)])
            except:
                draw_rectangle(x2-2, y2-2,24,13,[255,2,2,255])
            try:
                int(v)
            except:
                v=0
            if int(v) > 100:
                draw_text(txt, x2, y2, 11, BLACK)# VIOLET)
            else:
                draw_text(txt, x2, y2, 11, GREY)# VIOLET)
            xi+=1

            if xi % 20 == 0:
                #for o in FontType:
                #    print(o)
                ##exit()
                #draw_texture_pro(FontType.FONT_DEFAULT,"hi",[10,10],[0,0],0,10)
                #draw_text_pro(font: Font, text: str, position: Vector2, origin: Vector2, rotation: float, fontSize: float, spacing: float, tint: Color)
                draw_text(str(int(yi*20)+1), 170-30, y2, 11, YELLOW)# VIOLET)
                xi = 0
                yi += 1



        draw_text(str(int(yi*20)+1), 170-30, y2, 11, YELLOW)# VIOLET)
        p=0
        for k in keys:
            #print(k)
            txt =":"+str(k) 
            draw_text(txt, 10, 20+p, 20, GREY)# VIOLET)
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
        #draw_text("Hello world", 190, 200, 20, VIOLET)
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
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:# KeyInterupt
        print("err",e)
        time.sleep(1)
        #raise e
close_window()

