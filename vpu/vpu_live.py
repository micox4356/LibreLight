
import math
import random
import time
import os


from optparse import OptionParser
...
parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode",
                  help="pixel mode") #, metavar="FILE")
#parser.add_option("-f", "--file", dest="filename",
#                  help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()



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



p = 16
block = [p,p]
_x = 12
_y = 5

#HD = "0"
if options.mode:
    try:
        HD = options.mode
        p,_x,_y = HD.split(",")
        _x = int(_x)
        _y = int(_y)
        p = int(p)
        block = [p,p]
    except Exception as e:
        print( "Exc",options.mode,e)






# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,184)
os.environ['SDL_VIDEO_CENTERED'] = '0'

pg = pygame
pygame.init()
pygame.mixer.quit()


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
try:
    wx = 100+block[0] * _x
    wy = 100+block[1] * _y
    main_size=(wx,wy)

except Exception as e:
    print("Exception:",e)
#main_size=(280,200)

window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight LED-SCREEN')


class Fix():
    def __init__(self,pos,univ,dmx,ch):
        self.dmx = dmx
        self.univ = univ
        self.ch = ch
        self.pos = pos
        self.rgb = [0,0,40]
        self.block = [10,10]
        self.x = 0
        self.y = 0
        self.strobo = time.time()
        self.bmp = 250

    def calc(self,data):
        dmx_sub = [210]*10
        dmx = rDMX(self.univ,self.dmx)-1
        if dmx+self.ch < len(data):
            dmx_sub = data[dmx:dmx+self.ch]
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
        A = (self.pos[0])*self.block[0]
        B = (self.pos[1]-1)*self.block[1]
        C = self.block[0]-a
        D = self.block[1]-b
        return [x+A,y+B,C,D]

class POINTER():
    def __init__(self):
        self.pos = [0,0,0,0]
        self.on = 0
        self.rgb = [0,100,10]
        self.x = 0
        self.y = 0
        self.fix = Fix([999,999],0,0,0)

    def move(self,pos):
        self.pos = pos
        self.on = 1
    def cross(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        if self.on:
            pygame.draw.rect(window,self.rgb,self.pos)
            #pygame.draw.line(window,self.rgb, (self.pos[0],self.pos[1]) , (self.pos[0]+100,self.pos[1]) ) 

        #fr = font15.render(self.txt ,1, (200,200,200))
        fr = font15.render("{}/{}".format(self.fix.x,self.fix.y) ,1, (200,200,200))
        window.blit(fr,(self.pos[0]+2,self.pos[1]+2 ))
        window.blit(fr,(200,25))

        txt=str(self.pos)
        fr = font15.render(txt ,1, (200,200,200))
        #window.blit(fr,(self.pos[0]+2,self.pos[1]+2 ))
        window.blit(fr,(200,10))

        fr = font15.render("{:02}:{:03}".format(self.fix.univ,self.fix.dmx) ,1, (200,200,200))
        window.blit(fr,(300,10))
        
        self.rgb = [0,0,200]
        pygame.draw.line(window,self.rgb, (self.x-p,self.y) , (self.x-2,self.y) ) 
        pygame.draw.line(window,self.rgb, (self.x,self.y-p) , (self.x,self.y-2) ) 

        self.rgb = [0,200,0]
        pygame.draw.line(window,self.rgb, (self.x+2,self.y) , (self.x+p,self.y) ) 
        pygame.draw.line(window,self.rgb, (self.x,self.y+2) , (self.x,self.y+p) ) 
        self.rgb = [200,0,0]

pointer = POINTER()

NR = 0

running = True
def event():
    global NR,running
    for event in pygame.event.get(): 
        print("a",event)
        print("b",event.type)
        print("c",dir(event) ) #event.button)
        try:
            print("d",event.dict ) #event.button)
            if event.type == 5:
                if "button" in event.dict and event.dict["button"] == 1:  #event.button)
                    NR += 1
                    if NR > 2:
                        NR = 0
                if "button" in event.dict and event.dict["button"] == 3:  #event.button)
                    NR -= 1
                    if NR < 0:
                        NR = 2
            if "pos" in event.dict:
                posA = event.dict["pos"]
                fix = find_pix(posA[0]-40,posA[1]-60)
                if fix:
                    pos = fix.POS(40,60) #40,60)
                    rgb = [0,0,0] #fix.rgb
                    #print(fix)
                    #pygame.draw.rect(window,rgb,pos)
                    pointer.move(pos) #,posA[0],posA[1])
                    pointer.fix  = fix
                else:
                    pointer.on = 0
                pointer.cross(posA[0],posA[1])


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


#def draw_circle(surface, x, y, radius, color):
def draw_circle(surface,color, pos, radius):
    x,y=pos
    pygame.gfxdraw.aacircle(surface, x, y, radius-1, color)
    pygame.gfxdraw.filled_circle(surface, x, y, radius-1, color)

def rDMX(univ,dmx):
    return univ*512+dmx

grid_file = "/tmp/vpu_grid.csv"

def init_grid():
    log = open(grid_file,"w")
    head = "i,univ,dmx,x,y,ch\n"
    head = "i,univ,dmx,ch\n"
    head = "univ,dmx,x,y,ch\n"
    print("csv:",head)
    log.write(head)
    dmx = 1-1
    ch = 4

    y=0
    x=0
    for i in range((_y)*(_x)):
        if i%_x == 0:
            x=0
            y+=1
        
        _univ = int(dmx/512)
        _dmx = dmx - (_univ)*512 

        pos=[x,y]
        line="{},{},{},{},{},{}\n".format(i+1,_univ,_dmx+1,pos[0],pos[1],ch)
        line="{},{},{},{},{}\n".format(_univ,_dmx+1,x,y,ch)
        print("wcsv:",[line])
        log.write(line)
        dmx += ch
        x+=1
    log.close()
    return GRID

def open_grid():
    #global GRID

    #init_grid()
    try:
        log = open(grid_file,"r")
    except:
        init_grid()
        log = open(grid_file,"r")
    
    lines = log.readlines()

    # "i,dmx,x,y,ch  # csv
    GRID = []
    
    y=0
    x=0
    #for i in range((_y)*(_x)):
    for i,line in enumerate(lines[1:]):
        if i%_x == 0:
            x=0
            y+=1
        print("rcsv",[line])
        line = line.strip()
        line = line.split(",")

        #i    = int(line[0])
        univ = int(line[0])
        dmx  = int(line[1])
        #x    = int(line[3])
        #y    = int(line[4])
        ch   = int(line[4])

        pos = [x,y] 
        f   = Fix(pos,univ,dmx,ch)
        f.x = x
        f.y = y 
        f.block = block
        GRID.append(f)
        x+=1
    return GRID

def find_pix(x,y):
    global GRID
    for fix in GRID:
        X = 0
        Y = 0
        pos = fix.POS()
        if x > pos[0] and x < pos[0]+pos[2]:
            X = 1
        if y > pos[1] and y < pos[1]+pos[3]:
            Y = 1
        if X and Y:
            print(pos,x,y)
            print("find",X,Y)
            return fix
            
GRID = []
NR = 0
START_UNIV=2
def main():
    global IP,GRID
    GRID =  open_grid() #init_gird()
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

            pos = fix.POS(40,60)
            rgb = fix.rgb

            #print(fix.dmx,rgb,pos)
            pygame.draw.rect(window,rgb,pos)
            #pygame.draw.circle(window,rgb,(pos[0]+int(pos[2]/2),pos[1]+int(pos[3]/2)),int(pos[3]/2))
            #draw_circle(window,rgb,(pos[0]+int(pos[2]/2),pos[1]+int(pos[3]/2)),int(pos[3]/2))
            if NR == 1:
                fr = font15.render("{:2}".format(i+1) ,1, (200,0,255))
                window.blit(fr,(pos[0]+2,pos[1]+3))
            elif NR == 2:
                univ = int(dmx/512)
                _dmx = dmx
                if univ:
                    _dmx = dmx%512
                    #_dmx += 1

                #fr = font12.render("{:2} {}".format(univ+START_UNIV,_dmx) ,1, (200,0,255))
                fr = font12.render("{:2} {}".format(fix.univ,fix.dmx) ,1, (200,0,255))
                window.blit(fr,(pos[0],pos[1]+3))

            if 1:
                if fix.pos[0] == 0:
                    fr = font12.render("{}".format(fix.pos[1]) ,1, (200,200,200))
                    #fr = font12.render("{}:{}".format(fix.univ,fix.dmx) ,1, (200,200,200))
                    #fr = font12.render("-" ,1, (100,100,255))
                    window.blit(fr,(10,pos[1]+3 ))
                if fix.pos[1] == 1:
                    fr = font12.render("{}".format(fix.pos[0]+1) ,1, (200,200,200))
                    #fr = font12.render("-" ,1, (100,100,255))
                    window.blit(fr,(pos[0]+2,35 ))

            dmx += 4
            i += 1

        pointer.draw()
        pygame.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
