
import math
import random
import time
import os




# ===== ARTNET DMX =========

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def read_index():
    ips=mc.get("index")#cmd)
    if ips is None:
        ips = {}

    #for k,v in ips.items():
    #    print(k,v)
    return ips

def select_ip(ips, univ=2): # artnet univ
    _univ = ":{}".format(univ)
    for ip in ips: #high priority
        if "2.0.0" in ip and _univ in ip:
            return ip

    for ip in ips:
        if "ltp-out" in ip and _univ in ip:
            return ip





def read_dmx(ip):
    global frame
    r = ""
    if ip:
        #t = int(math.sin(time.time() - s)*10)
        r = mc.get(ip) #"2.0.0.13:2")
        frame += 1
        rr = [0]*512
        for i,v in enumerate(r):
            try: #cleanup ltp-out to int
                v = int(v)
                rr[i] = v
            except:pass
        r = rr


    if not r:
        c = 0
        time.sleep(0.1)
        r = [0] *512
        for i in range(12*8+1):
            dmx = i*4
            #print(dmx)
            r[dmx:dmx+4] = [255,10,10,40] 
    return r



# ===== ARTNET DMX =========









# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,184)
os.environ['SDL_VIDEO_CENTERED'] = '0'

pg = pygame
pygame.init()

f = pygame.font.get_fonts()
for i in f:
    if "mono" in i.lower():
        print(i)
    

font = pygame.font.SysFont("freemonobold",22)
font10 = pygame.font.SysFont("freemonobold",10)
font12 = pygame.font.SysFont("freemonobold",12)
font15 = pygame.font.SysFont("freemonobold",15)
#font = pygame.font.SysFont(None,30)
fr = font.render("hallo" ,1, (200,0,255))

main_size=(600,500)
#main_size=(280,200)

window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight LED-SCREEN')


NR = 0

running = True
def event():
    global NR,running
    for event in pygame.event.get(): 
        print(event)
        print(event.type)
        print(dir(event) ) #event.button)
        try:
            print(event.dict ) #event.button)
            if event.type == 5:
                if "button" in event.dict and event.dict["button"] == 1:  #event.button)
                    NR += 1
                    if NR > 2:
                        NR = 0
                if "button" in event.dict and event.dict["button"] == 3:  #event.button)
                    NR -= 1
                    if NR < 0:
                        NR = 2

        except Exception as e:
            print(e)
        if event.type==pygame.QUIT: 
            running=False


fps = 0
frame = 0
frame_t = time.time()
IP = "yyy"
def draw_overlay():
    global fps
    fr = font.render("fps:{}".format(fps) ,1, (200,0,255))
    window.blit(fr,(10,10))

    fr = font.render("ip:{}".format(IP) ,1, (200,0,255))
    window.blit(fr,(80,10))

def FPS():
    global fps,frame,frame_t
    t = time.time()
    if frame_t+1 < t:
        fps = frame #frame_t- t #frame
        frame = 1
        frame_t = time.time()

# ===== GUI =========






class Fix():
    def __init__(self,pos,dmx,ch):
        self.dmx = dmx
        self.ch = ch
        self.pos = pos
        self.rgb = [0,0,40]
        self.block = [10,10]

        self.strobo = time.time()
        self.bmp = 250

    def calc(self,data):
        dmx_sub = [210]*10
        if self.dmx+self.ch < len(data):
            dmx_sub = data[self.dmx:self.dmx+self.ch]
        dim = dmx_sub[0]/255

        r = dmx_sub[1]*dim
        g = dmx_sub[2]*dim
        b = dmx_sub[3]*dim

        r = int(r)
        g = int(g)
        b = int(b)
        self.rgb = [r,g,b]
        return self.rgb
     
    def POS(self,x=0,y=0,a=0,b=0):
        A = self.pos[0]*self.block[0]
        B = self.pos[1]*self.block[1]
        C = self.block[0]-a
        D = self.block[1]-b
        return [x+A,y+B,C,D]


def init_gird():
    GRID = []
    #init loop
    dmx = 1-1
    ch = 4

    block = [22,22]
    _x = 6
    _y = 3

    HD = 1
    if HD == 1:
        block = [8,8]
        _x = 24
        _y = 16
    elif HD == 2:
        block = [22,22]
        _x = 24
        _y = 16
    else:
        block = [16,16]
        _x = 12
        _y = 8

        _x = 24
        _y = 16


    y=0
    x=0
    for i in range((_y)*(_x)):
        if i%_x == 0:
            x=0
            y+=1
        
        pos=[x,y]
        f = Fix(pos,dmx,ch)
        f.block = block
        GRID.append(f)
        #print(f)
        dmx += ch
        x+=1
    return GRID



NR = 0
START_UNIV=2
def main():
    global IP,GRIP
    GRID =  init_gird()
    print("GRID LEN:",len(GRID))


    s=time.time()
    print("run")
    r = ""
    IP = "xx"
    while running:
        event()
        pygame.display.flip()

        window.fill((0,0,0))
        FPS()
        draw_overlay()

        ips = read_index()
        ip = select_ip(ips,univ=START_UNIV)
        IP = ip
        #print("IP",ip)

        data = read_dmx(ip)

        ip = select_ip(ips,univ=START_UNIV+1)
        data3 = read_dmx(ip)
        data.extend(data3)

        ip = select_ip(ips,univ=START_UNIV+2)
        data3 = read_dmx(ip)
        data.extend(data3)

        #ip = select_ip(ips,univ=START_UNIV+4)
        #data3 = read_dmx(ip)
        #data.extend(data3)
        # GRID loop

        i = 0
        dmx = 1
        for fix in GRID:
            fix.calc(data)

            pos = fix.POS(40,40,-2,-2)
            rgb = fix.rgb

            #print(fix.dmx,rgb,pos)
            pygame.draw.rect(window,rgb,pos)
            if NR == 1:
                fr = font15.render("{:2}".format(i+1) ,1, (200,0,255))
                window.blit(fr,(pos[0]+2,pos[1]+3))
            elif NR == 2:
                univ = int(dmx/512)
                _dmx = dmx
                if univ:
                    _dmx = dmx%512
                    #_dmx += 1

                fr = font12.render("{:2} {}".format(univ+START_UNIV,_dmx) ,1, (200,0,255))
                window.blit(fr,(pos[0],pos[1]+3))

            if 1:
                if fix.pos[0] == 0:
                    fr = font12.render("{}".format(fix.pos[1]) ,1, (200,200,200))
                    #fr = font12.render("-" ,1, (100,100,255))
                    window.blit(fr,(10,pos[1]+3 ))
                if fix.pos[1] == 1:
                    fr = font12.render("{}".format(fix.pos[0]+1) ,1, (200,200,200))
                    #fr = font12.render("-" ,1, (100,100,255))
                    window.blit(fr,(pos[0]+2,35 ))

            dmx += 4
            i += 1

        pygame.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
