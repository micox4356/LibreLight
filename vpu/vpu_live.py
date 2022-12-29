
import math
import random
import time
import os


from optparse import OptionParser
...
parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode",
                  help="pixel mode") #, metavar="FILE")

parser.add_option("-X", "--XX", dest="XX", #default=1,
                  help="x-split") #, metavar="FILE")

parser.add_option("-x", "--xx", dest="xsplit", #default=1,
                  help="x-split") #, metavar="FILE")
parser.add_option("-y", "--yy", dest="ysplit",#default=1,
                  help="y-split") #, metavar="FILE")

#parser.add_option("-f", "--file", dest="filename",
#                  help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

START = time.time()


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

FUNC = 0



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
        #time.sleep(0.1)
        r = [0] *512
        for i in range(12*8+1):
            dmx = i*4
            #print(dmx)
            r[dmx:dmx+4] = [255,10,10,40] 
    return r



# ===== ARTNET DMX =========



p = 16
block = [p,p]
_x = 8
_y = 8


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

HD_x = 2
HD_y = 2

print( [options.xsplit])
print( [options.ysplit])

try:
    if options.xsplit:
        HD_x = int(options.xsplit)
    if options.ysplit:
        HD_y = int(options.ysplit)
except Exception as e:
    print( "Exc",options.mode,e)

print("HD",HD_x,HD_y)
print("xy",_x,_y)
print("++++++++++++++++++", p,_x,_y)

_x2 = _x

try:
    if options.XX:
        _x2 = int(options.XX)
except Exception as e:
    print( "Exc",options.mode,e)
print("_x2 , -X",_x2)
# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,164)
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
    def __init__(self,_id,pos,block=[16,16],univ=0,dmx=0,ch=4):
        #print("Fix",_id)
        self._id = _id
        self.dmx = (_id-1) * ch +1 #dmx
        self.univ = univ
        self.ch  = ch
        self.pos = pos
        self.rgb = [0,0,0]
        self.block = block #[10,10]
        self.x = pos[0]
        self.y = pos[1]
        self.strobo = time.time()
        self.bmp = 250
        self.sub_fix = []
        
        sub_block =[block[0]/HD_x,block[1]/HD_y] 
        if _id <= 0: #exit 
            return

        spalte = (_id-1)%_y +1
        zeile = int((_id-1)/_x2) #+1
        #zeile = zeile*_x*HD_x*HD_y

        add_row = _x*HD_x*HD_y

        #zeile 1
        sid = (_id-1)*2  + zeile*HD_x*_x2
        #for i in range(1,HD_x):
        sid = sid+1
        #sid = zeile
        sub_pos= [pos[0]*block[0],pos[1]*block[1]]
        sub_fix = SubFix(sid,sub_pos,sub_block,univ,dmx,ch)
        self.sub_fix.append(sub_fix)

        sid = sid+1
        #sid = zeile
        sub_pos= [pos[0]*block[0]+block[0]/2,pos[1]*block[1]]
        sub_fix = SubFix(sid,sub_pos,sub_block,univ,dmx,ch)
        self.sub_fix.append(sub_fix)

        #zeile 2
        sid = (_id-1)*2+1 + _x2*HD_x  + zeile*HD_x*_x2 # int(add_row)
        #sid = sid+1
        #sid = HD_x
        sub_pos= [pos[0]*block[0],pos[1]*block[1]+block[1]/2]
        sub_fix = SubFix(sid,sub_pos,sub_block,univ,dmx,ch)
        self.sub_fix.append(sub_fix)

        #sid = sid+1
        sid = sid+1   
        sub_pos= [pos[0]*block[0]+block[0]/2,pos[1]*block[1]+block[1]/2]
        sub_fix = SubFix(sid,sub_pos,sub_block,univ,dmx,ch)
        self.sub_fix.append(sub_fix)


    def calc(self,data):
        _rgb = [0,255,0]
        return _rgb

    def sub_calc(self,data):
        _rgb = [0,255,0]
        for sub_fix in self.sub_fix:
            sub_fix.block = self.block[:]
            _rgb = sub_fix.calc(data)
        return _rgb
        
     
    def POS(self,x=0,y=0,a=0,b=0):
        A = (self.pos[0])*self.block[0]
        B = (self.pos[1])*self.block[1]
        C = self.block[0]-a
        D = self.block[1]-b
        return [x+A,y+B,C,D]

    def subPOS(self,x=0,y=0,a=0,b=0):
        __out = []
        for sub_fix in self.sub_fix:
            __out.append( sub_fix.POS(x,y,a,b) )
        return __out 


class SubFix():
    def __init__(self,_id,pos,block=[16,16],univ=0,dmx=0,ch=4):
        #print("Fix",_id)
        self._id = _id
        self.dmx = (_id-1) * ch +1 #dmx
        self.univ = univ
        self.ch  = ch
        self.pos = pos
        self.rgb = [0,0,40]
        self.block = block #[10,10]
        self.x = pos[0]
        self.y = pos[1]
        self.strobo = time.time()
        self.bmp = 250

    def calc(self,data):
        #return [130,30,20]
        dmx_sub = [30]*10
        #print(dmx_sub)
        dmx = self.dmx -1
        _dmx_sub = []
        if self.dmx >= 0:
            dmx = rDMX(self.univ,self.dmx)-1
            if dmx+self.ch < len(data):
                _dmx_sub = data[dmx:dmx+self.ch]
        if _dmx_sub:
            dmx_sub = _dmx_sub
        #print(dmx_sub)
        dim = dmx_sub[0]/255

        #print("dmx",dmx,dmx_sub)
        r = dmx_sub[1]*dim
        g = dmx_sub[2]*dim
        b = dmx_sub[3]*dim

        r = int(r)
        g = int(g)
        b = int(b)
        self.rgb = [r,g,b]
        return self.rgb
     
    def POS(self,x=0,y=0,a=0,b=0):
        A = (self.pos[0]) #+self.block[0]
        B = (self.pos[1]) #+self.block[1]
        C = self.block[0]-a
        D = self.block[1]-b
        if NR:
            C-=1
            D-=1
        return [x+A,y+B,C,D]

class POINTER():
    def __init__(self):
        self.pos = [0,0,0,0]
        self.on = 0
        self.rgb = [0,100,10]
        self._x = 0
        self._y = 0
        self.x = 0
        self.y = 0
        self.fix = Fix(0 ,[999,999],[16,16],0,0,0)

    def row_move(self,x,y):
        self._x = x
        self._y = y
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

        
            # mouse grid posision
            fr = font15.render("{}/{}".format(self.fix.x+1,self.fix.y) ,1, (200,200,200))
            
            _nr = self.fix.y * _x + self.fix.x +1
            #fr = font15.render("{:02} {}/{}".format(_nr, self.fix.x+1,self.fix.y+1 ) ,1, (200,200,200))
            fr = font15.render("{:02}".format(_nr ) ,1, (200,200,200))

            window.blit(fr,(self.pos[0]+2,self.pos[1]+2 ))
            window.blit(fr,(200,25))

        # fix pos
        txt=str(self.pos)
        fr = font15.render(txt ,1, (200,200,200))
        #window.blit(fr,(self.pos[0]+2,self.pos[1]+2 ))
        window.blit(fr,(200,10))

        # univers
        #fr = font15.render("{:02}:{:03}".format(self.fix.univ,self.fix.dmx) ,1, (200,200,200))
        #window.blit(fr,(300,10))
        
        # pointer
        fr = font15.render("X:{:03}".format(self._x) ,1, (200,200,200))
        window.blit(fr,(10,30))
        fr = font15.render("Y:{:03}".format(self._y) ,1, (200,200,200))
        window.blit(fr,(10,40))

        # crosshair
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
        #print(event.dict)

        _button = None
        if "button" in event.dict:
             _button =  event.dict["button"]

        _state = None
        if "state" in event.dict:
            _state  = event.state 

        _key = None
        if "key" in event.dict:
            _key  = event.key 

        _pos = None
        if "pos" in event.dict:
            _pos  = event.pos 

        _type = None
        if "type" in event.dict:
            _type  = event.type 
        _type  = event.type 

        _mod = None
        if "mod" in event.dict:
            _mod  = event.mod 
        print( " ")
        print( "{:.02f}".format( time.time() - START ))
        print("button -",_button,end="\t| ")
        #print("state  -",_state)
        print("pos    -",_pos)
        print("type   -",_type, end="\t| ")
        print("key    -",_key)
        print("mod    -",_mod)

        try:
            if _type == 5:
                if _button == 1:
                    NR += 1
                    if NR > 1:
                        NR = 0
                if _button == 3:
                    NR -= 1
                    if NR < 0:
                        NR = 1

            if _pos:
                posA = _pos 
                fix = find_pix(_pos[0]-40,_pos[1]-60)
                if fix:
                    pos = fix.POS(40,60) 
                    rgb = [0,0,0] 
                    pointer.move(pos) 
                    pointer.fix  = fix
                else:
                    pointer.on = 0
                pointer.row_move(_pos[0],_pos[1]) 
                pointer.cross(_pos[0],_pos[1])


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
    fr = font.render("FPS:{}".format(fps) ,1, (200,0,255))
    window.blit(fr,(10,10))

    fr = font.render("ip:{}".format(IP) ,1, (200,0,255))
    window.blit(fr,(80,10))

def calc_fps():
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
    pygame.gfxdraw.aacircle(surface, int(x), int(y), radius-1, color)
    pygame.gfxdraw.filled_circle(surface, int(x), int(y), radius-1, color)

def rDMX(univ,dmx):
    return univ*512+dmx

grid_file = "/tmp/vpu_grid.csv"
grid_file = "/home/user/LibreLight/vpu_grid_hd.csv"

def generate_grid():
    log = open(grid_file,"w")
    head = "i,univ,dmx,x,y,ch\n"
    head = "i,univ,dmx,ch\n"
    head = "univ,dmx,x,y,ch\n"
    head = "nr,id,info\n"
    print("csv:",head)
    log.write(head)
    dmx = 1-1
    ch = 4

    y=0
    x=0
    for i in range((_y)*(_x)):
        if x > _x and i%_x == 0:
            print("--> -->")
            x=0
            y+=1
        
        _univ = int(dmx/512)
        _dmx = dmx - (_univ)*512 

        pos=[x,y]
        line="{},{},{},{},{},{}\n".format(i+1,_univ,_dmx+1,pos[0],pos[1],ch)
        line="{},{},{},{},{}\n".format(_univ,_dmx+1,x,y,ch)
        line="{},{},x\n".format(i+1,i+1)
        print("wcsv:",[line])
        log.write(line)
        dmx += ch
        x+=1
    log.close()
    return GRID

def init_grid():

    try:
        log = open(grid_file,"r")
    except:
        generate_grid()
        log = open(grid_file,"r")
    
    lines = log.readlines()

    GRID = []
    
    y=0
    x=0
    print("CSV header",[lines[0]])

    for i,line in enumerate(lines[1:]): #exclude first line
        #print("rcsv",[line])
        line = line.strip()
        line = line.split(",") # csv

        if i >= _x and i%_x == 0:
            x=0
            y+=1
        if y > _y:
            break


        #i    = int(line[0])
        _id    = int(line[1])
        #univ = int(line[0])
        #dmx  = int(line[1])
        #x    = int(line[3])
        #y    = int(line[4])
        #ch   = int(line[4])

        pos = [x,y] 
        f   = Fix(_id,pos,block) #pos,univ,dmx,ch)
        #f.x = x
        #f.y = y 
        #f.block = block
        GRID.append(f)
        x+=1
        #print("y, _y",y,_y)
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
    global IP,GRID,FUNC

    counter = time.time()
    GRID =  init_grid() #init_gird()
    print("GRID LEN:",len(GRID))


    s=time.time()
    print("run")
    r = ""
    IP = "xx"
    while running:
        event()
        pygame.display.flip()

        window.fill((0,0,0))
        calc_fps()
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
        try:
            ddd = 1023 #univ 3 512
            FUNC = data[ddd]
            #print("FUNC", FUNC )#:ddd+512])
            #FUNC = 15
        except Exception as e:
            print("EXC FUNC",e)
        i = 0
        dmx = 1
        h = 1
        v = 1
        for fix in GRID:
            pos = fix.POS(40,60)
            rgb = fix.rgb


            if 1:
                # draw row/col grid number
                if fix.pos[0] == 0:
                    fr = font12.render("{}".format(fix.pos[1]+1) ,1, (200,200,200))
                    window.blit(fr,(10,pos[1]+3 ))
                if fix.pos[1] == 0:
                    fr = font12.render("{}".format(fix.pos[0]+1) ,1, (200,200,200))
                    window.blit(fr,(pos[0]+2,35 ))

            pygame.draw.rect(window,rgb,pos)


            # DRAW SUB-FIXTURE
            j = 0
            for subfix in fix.sub_fix:#calc(data):
                subfix.calc(data)
                #fix = subfix
                spos = subfix.POS(40,60)
                srgb = subfix.rgb

                #print(fix.dmx,rgb,pos)
                #pygame.draw.circle(window,rgb,(pos[0]+int(pos[2]/2),pos[1]+int(pos[3]/2)),int(pos[3]/2))
                if FUNC > 10 and FUNC <= 20:
                    draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/2))
                elif FUNC > 20 and FUNC <= 30:
                    draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
                else:
                    pygame.draw.rect(window,srgb,spos)




                # draw row/col grid number
                if subfix.pos[0] == 0:
                    fr = font12.render("{}".format(v ) ,1, (200,200,200))
                    window.blit(fr,(25,spos[1] ))
                    v += 1
                if subfix.pos[1] == 0:
                    fr = font12.render("{}".format(1) ,1, (200,200,200))
                    fr = font12.render("{}".format(h ) ,1, (200,200,200))
                    h+=1
                    window.blit(fr,(spos[0],50 ))


                if NR:
                    #fr = font15.render("{:02}".format(j+1) ,1, (0,200,255))
                    fr = font15.render("{:02}".format(subfix._id) ,1, (250,200,5))
                    window.blit(fr,(spos[0]+2,spos[1]+10))
                j += 1
            i += 1


        # DRAW FIX NUMBER on TOP
        i=0
        for fix in GRID:
            pos = fix.POS(40,60)
            rgb = fix.rgb
            if NR:
                pygame.draw.rect(window,[0,0,0],[pos[0]+2,pos[1]+2,12,9])

            #if NR == 1:
            #    fr = font15.render("{:02}".format(i+1) ,1, (200,0,255))
            #    window.blit(fr,(pos[0]+2,pos[1]+2))
            #elif NR == 2:
            if NR:# == 2:
                if counter +5 < time.time():
                    counter = time.time()
                    try:
                        GRID =  init_grid() #init_gird()
                    except Exception as e:
                        print("Except: grid re init",e)
                if fix._id != i+1:
                    fr = font15.render("{:02}".format(fix._id) ,1, (255,255,0))
                else:
                    fr = font15.render("{:02}".format(fix._id) ,1, (100,100,255))
                window.blit(fr,(pos[0]+2,pos[1]+2))
            i += 1
            
        pointer.draw()
        pygame.display.flip()
        pg.time.wait(10)



if __name__ == "__main__":
    main()
