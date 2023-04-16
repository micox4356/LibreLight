
import math
import random
import time
import os

import _thread as thread


from optparse import OptionParser
...
parser = OptionParser()
parser.add_option("-m", "--mode", dest="mode",
                  help="pixel mode pix,x,y --mode 40,10,8") #, metavar="FILE")

parser.add_option("-X", "--XX", dest="XX", #default=1,
                  help="x-split") #, metavar="FILE")

parser.add_option("-x", "--xx", dest="xsplit", #default=1,
                  help="x-split") #, metavar="FILE")
parser.add_option("-y", "--yy", dest="ysplit",#default=1,
                  help="y-split") #, metavar="FILE")

parser.add_option("", "--start-univ", dest="start_univ",#default=1,
                  help="set start-univers default=2") #, metavar="FILE")

parser.add_option("", "--gobo-ch", dest="gobo_ch",#default=1,
                  help="gobo ch univ on 1") #, metavar="FILE")

#os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,164)
parser.add_option("", "--win-pos", dest="win_pos",default="200,164",
                  help="SDL_VIDEO_WINDOW_POS --win-pos=200,164") #, metavar="FILE")

parser.add_option("", "--pixel-mapping", dest="pixel_mapping",default=0,
                  help="pixel_mapping file/on --pixel-mapping=_x") #, metavar="FILE")

parser.add_option("", "--countdown", dest="countdown",#default=1,
                  help="enable countdown") #, metavar="FILE")

parser.add_option("", "--videoplayer", dest="videoplayer",#default=1,
                  help="enable videoplayer") #, metavar="FILE")

#parser.add_option("-f", "--file", dest="filename",
#                  help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

for o in dir(options):
    if "_" in o:
        continue
    print(o,options.__getattribute__(o))

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
COUNTER = []

if options.countdown:
    
    cdmx_start = options.countdown.split(",")
    for cdmx in cdmx_start:
        try:
            cdmx = int(cdmx)
            COUNTER.append({"DMX":cdmx,"DIM":0,"PAN":127,"TILT":127,"CONTROL":0,"SEC":10,"RED":255,"GREEN":255,"BLUE":255,"_time":time.time(),"_RUN":0,"_SEC":">{}<".format(cdmx)})
        except Exception as e:
            print("EXCEPTION COUNTER INIT ",cdmx)



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



class Vopen():

    def __init__(self,dmx=None):
        self.fname = '/home/user/Downloads/video.mp4'
        self.fname = '/home/user/Downloads/video.ogv'
        self.fname = '/home/user/Downloads/bbb_sunflower_480x320.mp4'
        self.scale = 50 #%
        self.dmx=dmx
        self.x = 0
        self.y = 0
        self.init_count = 0
        self.cap = None
        self.shape = [200,200]  
        self.img = None
        self.success = 1
        self.cv2 = None
        try:
            global cv2
            self.cv2 = cv2
        except:
            pass

        self.im = None
        self.pos = 0
        self.buffer = []
        self.init()

    def init(self):
        #self._init()
        thread.start_new_thread(self._init,())
        self.init_count = 1

    def _init(self):
        print(self)
        print("videoplayer.init()",self.fname)

        if not os.path.isfile(self.fname):
            print()
            print("video file does not exits !! >",self.fname)
            print()
            exit()

        if self.cv2:
            cap = self.cv2.VideoCapture(self.fname)
            self.cap = cap
            success = 1
            while success:
                success, self.img = self.cap.read()
                #self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
                self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
                self.img = self.rescale_frame2(self.img, 100)
                self.buffer.append(self.img)
                if len(self.buffer) % 100 == 0:
                    _id = str(self.__repr__)[-5:-1]
                    print(_id,"video read",self.dmx,len(self.buffer))
            self.pos = 0
            self.img = self.buffer[self.pos]
            self.success = 1

    def read(self):
        #print(self,"read()")
        try:
            self.img = self.buffer[self.pos]
            #self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
            self.img = self.rescale_frame(self.img, percent=self.scale)
            self.pos += 1
            #print("video.read",self.pos)
            self.shape = self.img.shape[1::-1]
        except Exception as e:
            print("exception 432",e)
            #self.init()

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self.buffer)-1
        if self.pos >= len(self.buffer):
            self.pos = len(self.buffer)-1
        self.im = self.buffer[self.pos]

    def rescale_frame2(self,frame, width):
        height = int(frame.shape[0]/frame.shape[1] * width )
        dim = (width, height)
        #print("rescale_frame2",dim)
        #sys.exit()
        return self.cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def rescale_frame(self,frame, percent=75):
        width  = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return self.cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def next(self):
        #print(self,"next",time.time())
        #self.success = 0
         
        self.read()
        try:
            if len(self.buffer) % 100 == 0:
                #print("video pos",self.pos)
                _id = str(self.__repr__)[-5:-1]
                print(_id,"video pos",self.dmx,self.pos,len(self.buffer))
            img = self.img #self.rescale_frame(self.img, percent=30)
            if img is None:
                return 
            self.im = pygame.image.frombuffer(img.tobytes(), self.shape, "RGB")
            #print(type(self.im))
            #self.buffer.append(self.im)
            self.pos += 1
            if self.pos > len(self.buffer):
                self.pos = 0
            # wn.blit(im, (self.x, self.y))
            #self.success = 1
        except AttributeError as e:
            time.sleep(.05)
            #if self.init_count % 100 == 0:
            print("except 776",e)
            #self.init()
        except Exception as e:
            print("except 756",e)

    def draw(self,wn=None):
        if self.success and wn and self.im: # is not None:
            wn.blit(self.im, (self.x, self.y))

    def overlay(self,wn=None,mode="x"):
        # overlay 
        img_shape = [100,100]
        if type(self.img) is list:
            img_shape = self.img.shape

        pygame.draw.rect(wn,[255,200,0],[5+self.x-3,4+self.y-1+img_shape[0],140,20])
        font15 = pygame.font.SysFont("freemonobold",17)
        fr = font15.render(">:{}".format(mode) ,1, (0,0,0))
        wn.blit(fr,(3+self.x,4+self.y+img_shape[0]))

        fr = font15.render("FRAME:{}".format(self.pos) ,1, (0,0,0))
        wn.blit(fr,(45+self.x,4+self.y+img_shape[0]))


VIDEO = []
videoplayer=[]            
cv2 = None

if type(options.videoplayer) is str:
    try:
        import cv2
    except:pass
    max_videoplayer = 2
    dmx_start =  options.videoplayer.split(",")
    for cdmx in dmx_start:
        if len(videoplayer) > max_videoplayer:
            print("-- videoplayer max count {} !! break".format(max_videoplayer))
            break
        print("-- videoplayer dmx:",cdmx)
        try:
            cdmx = int(cdmx)
            videoplayer.append( Vopen(cdmx) )
            VIDEO.append({"DMX":cdmx,"DIM":0,"PAN":127,"TILT":127,"CONTROL":0,"SEC":10,"RED":255,"GREEN":255,"BLUE":255,"_time":time.time(),"_RUN":0,"_SEC":">{}<".format(cdmx)})
        except Exception as e:
            print("EXCEPTION COUNTER INIT ",cdmx)

# ===== ======


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
        pass#_x2 = int(options.XX)
except Exception as e:
    print( "Exc",options.mode,e)
print("_x2 , -X",_x2)
# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,164)
if options.win_pos:
    if "," in options.win_pos:
        win_pos = options.win_pos.split(",")
        try:
            WIN_POS = '%i,%i' % (int(win_pos[0]),int(win_pos[1]) )
            os.environ['SDL_VIDEO_WINDOW_POS'] = WIN_POS
        except Excetpion as e:
            print("win_pos",win_pos,e)


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
font40 = pygame.font.SysFont("freemonobold",40)
font80 = pygame.font.SysFont("freemonobold",70)
#font = pygame.font.SysFont(None,30)

fr = font.render("hallo" ,1, (200,0,255))



PIXEL_MAPPING = 0
grid_file = "/tmp/vpu_grid_hd.csv"
text_file = "/home/user/LibreLight/vpu_text_hd.csv"
play_list = "/tmp/vpu_playlist_hd.csv"
pm_wy = 0
if options.pixel_mapping:
    PIXEL_MAPPING = 1
    path = options.pixel_mapping
    path = path.replace("/","-")
    path = path.replace(".","-")
    path = path.replace("\"","-")
    path = path.replace("'","-")
    grid_file = "/home/user/LibreLight/vpu_grid_hd{}.csv".format(path)
    text_file = "/home/user/LibreLight/vpu_text_hd{}.csv".format(path)
    play_list = "/home/user/LibreLight/vpu_playlist_hd{}.csv".format(path)
    #_x = 8
    #_y = 8

print("  ",[options.pixel_mapping],"grid_file",grid_file)
#grid_file = "/home/user/LibreLight/vpu_grid_hd.csv"


main_size=(600,500)
try:
    if _x < 8 and PIXEL_MAPPING >= 1:
        wx = 60+block[0] * 8
    else:
        wx = 60+block[0] * _x 
    wy = 80+block[1] * _y 
    main_size=(wx,wy)
    if PIXEL_MAPPING >= 1:
        pm_wy = 120+block[0] * 8 
        main_size=(wx,wy+pm_wy)

except Exception as e:
    print("Exception:",e)
#main_size=(280,200)

main_size = (main_size[0],main_size[1])
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight VPU-SCREEN')


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
        return [int(x+A),int(y+B),int(C),int(D)]

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

    def draw(self,x,y):
        pos = self.pos[:]
        #print("draw",x,y,pos)
        pos[0] += x
        pos[1] += y
        fix_x= self.fix.x
        fix_y= self.fix.y +y
        #print("draw",x,y,pos)

        if self.on:
            pygame.draw.rect(window,self.rgb,pos)
            #pygame.draw.line(window,self.rgb, (pos[0],pos[1]) , (pos[0]+100,pos[1]) ) 

        
            # mouse grid posision
            fr = font15.render("{}/{}".format(fix_x+1,fix_y) ,1, (200,200,200))
            
            _nr = fix_y * _x + fix_x +1
            #fr = font15.render("{:02} {}/{}".format(_nr, fix_x+1,fix_y+1 ) ,1, (200,200,200))
            fr = font15.render("{:02}".format(_nr ) ,1, (200,200,200))

            window.blit(fr,(pos[0]+2,pos[1]+2 ))
            window.blit(fr,(130,1))

        # fix pos
        txt=str(pos) #"[0, 0, 0, 0]"
        fr = font15.render(txt ,1, (200,200,200))
        #window.blit(fr,(pos[0]+2,pos[1]+2 ))
        window.blit(fr,(10,1))

        # univers
        #fr = font15.render("{:02}:{:03}".format(fix.univ,fix.dmx) ,1, (200,200,200))
        #window.blit(fr,(300,10))
        
        # pointer
        fr = font15.render("X:{:03}".format(self._x) ,1, (200,200,200))
        window.blit(fr,(10,30))
        fr = font15.render("Y:{:03}".format(self._y) ,1, (200,200,200))
        window.blit(fr,(10,40))

        # crosshair
        self.rgb = [0,0,200]
        pygame.draw.line(window,self.rgb, (self.x-p,self.y) , (self.x-2,self.y),4 ) 
        pygame.draw.line(window,self.rgb, (self.x,self.y-p) , (self.x,self.y-2),4 ) 

        self.rgb = [0,200,0]
        pygame.draw.line(window,self.rgb, (self.x+2,self.y) , (self.x+p,self.y),4 ) 
        pygame.draw.line(window,self.rgb, (self.x,self.y+2) , (self.x,self.y+p),4 ) 
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
        if 0:
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
                fix = find_pix(_pos[0]-40,_pos[1]-60+pm_wy)
                if fix:
                    pos = fix.POS(40,60+pm_wy) 
                    rgb = [0,0,0] 
                    pointer.move(pos) 
                    pointer.fix  = fix
                else:
                    pointer.on = 0
                pointer.row_move(_pos[0],_pos[1]) 
                pointer.cross(_pos[0],_pos[1])

            if event.type == pygame.VIDEORESIZE:
                 window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
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


TEXT_BLOCK = []

def _create_text_block():
    print("======== CREATE NEW TEXT FILE !!",text_file)
    f = open(text_file,"w")
    for i in range(10):
        f.write("TEXT {}\n".format(i+1))
    f.close()

def open_text_block():
    print("======== OPEN TEXT FILE !!",text_file)
    _lines = []
    try:
        f = open(text_file,"r")
        _lines = f.readlines()
        f.close()
    except FileNotFoundError as e:
        print("TEXT",e)
        _create_text_block()

    if len(_lines) <= 0:
        _create_text_block()
    lines = []
    for l in _lines:
        #print(">> ",l.strip())
        lines.append(l.strip())
    if len(lines) <= 10:
        for i in range(10-len(lines)):
            lines.append("LINE ERROR")
    return lines
TEXT_BLOCK = open_text_block()
TEXT_BLOCK_TIME = time.time()

# video playlist 

PLAYLIST = []

def _create_playlist():
    print("======== CREATE NEW PLAYLIST FILE !!",play_list)
    f = open(play_list,"w")
    for i in range(10):
        f.write("Video-file {}\n".format(i+1))
    f.close()

def open_playlist():
    print("======== OPEN PLAYLIST FILE !!",play_list)
    _lines = []
    try:
        f = open(play_list,"r")
        _lines = f.readlines()
        f.close()
    except FileNotFoundError as e:
        print("TEXT",e)
        _create_playlist()

    if len(_lines) <= 0:
        _create_playlist()

    lines = []
    for l in _lines:
        print(">> ",l.strip())
        lines.append(l.strip())

    if len(lines) <= 10:
        for i in range(10-len(lines)):
            lines.append("LINE ERROR")
    return lines

PLAYLIST_TIME = time.time()
PLAYLIST = open_playlist()
# ===== GUI =========


#def draw_circle(surface, x, y, radius, color):
def draw_circle(surface,color, pos, radius):
    x,y=pos
    pygame.gfxdraw.aacircle(surface, int(x), int(y), radius-1, color)
    pygame.gfxdraw.filled_circle(surface, int(x), int(y), radius-1, color)

def rDMX(univ,dmx):
    return univ*512+dmx


def generate_grid(mapping=0):
    _log = []
    #if PIXEL_MAPPING:
    #    log = open(grid_file,"w")
    head = "i,univ,dmx,x,y,ch\n"
    head = "i,univ,dmx,ch\n"
    head = "univ,dmx,x,y,ch\n"
    head = "nr,id,info\n"
    print("csv:",head)
    #if PIXEL_MAPPING:
    #    log.write(head)
    _log.append(head)
    dmx = 1-1
    ch = 4

    y=0
    x=0
    #for i in range((_y)*(_x)):
    for i in range((8)*(8)):
        #if x > _x and i%_x == 0:
        if x > 8 and i%8 == 0:
            #print("--> -->")
            x=0
            y+=1
        
        _univ = int(dmx/512)
        _dmx = dmx - (_univ)*512 

        pos=[x,y]
        line="{},{},{},{},{},{}\n".format(i+1,_univ,_dmx+1,pos[0],pos[1],ch)
        line="{},{},{},{},{}\n".format(_univ,_dmx+1,x,y,ch)
        line="{},{},x\n".format(i+1,i+1)
        #print("wcsv:",[line])
        #if PIXEL_MAPPING:
        #    log.write(line)
        _log.append(line)
        dmx += ch
        x+=1

    if mapping and PIXEL_MAPPING:
        print("CREATE NEW PIXELMAP FILE !!",grid_file)
        log = open(grid_file,"w")
        log.writelines(_log)
        log.close()

    return _log[:] #GRID

def init_grid(mapping=0,_x=4,_y=4):

    if mapping and PIXEL_MAPPING:
        try:
            log = open(grid_file,"r")
        except:
            generate_grid(mapping=mapping)
            log = open(grid_file,"r")
        lines = log.readlines()
    else:
        lines = generate_grid()
    

    GRID = []
    
    y=0
    x=0
    print("CSV header",[lines[0]],[PIXEL_MAPPING])

    for i,line in enumerate(lines[1:]): #exclude first line
        #print("rcsv",[line])
        line = line.strip()
        line = line.split(",") # csv

        if i >= _x and i%_x == 0:
            x=0
            y+=1
        if y >= _y:
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
        #pos = fix.POS()
        #pos = fix.POS(40,60-pm_wy)
        #pos = fix.POS(x,y+pm_wy)#40,60)
        if x > pos[0] and x < pos[0]+pos[2]:
            X = 1
        if y > pos[1] and y < pos[1]+pos[3]:
            Y = 1
        if X and Y:
            #print(pos,x,y)
            #print("find",X,Y)
            return fix
            
GRID = []
_GRID = []
_GRID =  init_grid(_x=8,_y=8,mapping=1) #init_gird()
NR = 0
START_UNIV=2
if options.start_univ:
    try:
        START_UNIV=int(options.start_univ)
    except Exception as e:
        print("Exception START UNIV",e) 

gobo_ch=1
if options.gobo_ch:
    try:
        gobo_ch=int(options.gobo_ch)
    except Exception as e:
        print("Exception gobo_ch",e) 

if gobo_ch <= 0:
    gobo_ch = 1


def draw_box(pos1,pos2,color=[128,128,128],text=1):

        color = [200,0,0,127]

        if text:
            fr = font15.render("A" ,1, (200,200,200))
            window.blit(fr,pos1)

            fr = font15.render("B" ,1, (200,200,200))
            window.blit(fr,[pos2[0]-10,pos2[1]-10])

        # h unten
        _pos1 = [pos1[0],pos2[1]]
        _pos2 = [pos2[0],pos2[1]]
        pygame.draw.aaline(window,color,_pos1,_pos2,1)

        color = [255,255,0,127]
        # h rechts
        _pos1 = [pos2[0],pos1[1]]
        _pos2 = [pos2[0],pos2[1]]
        pygame.draw.aaline(window,color,_pos1,_pos2,1)


        color = [0,200,0,127]
        # h links
        _pos1 = [pos1[0],pos1[1]]
        _pos2 = [pos1[0],pos2[1]]
        pygame.draw.aaline(window,color,_pos1,_pos2,1)


        color = [0,0,200,127]
        # h oben
        _pos1 = [pos1[0],pos1[1]]
        _pos2 = [pos2[0],pos1[1]]
        pygame.draw.aaline(window,color,_pos1,_pos2,1)

def grab(x=55,y=55,w=60,h=60):
    # usage
    # sub = grab()
    # window.blit(sub, (500,10))
    crop = None
    rect = pygame.Rect(x, y, w, h)
    try:
        sub = window.subsurface(rect)
        #pixArray = pygame.PixelArray(screen)
        crop = pygame.Surface((w,h))
        crop.blit(sub, (0,0))
    except ValueError as e:
        pass#print("exception",e,"line715")
    #except Exception as e:
    #    print("exception",e,"line715")
    #print(rect)
        
    return crop



def reshape(_x,_y):
    if PIXEL_MAPPING <= 0:
        return None

    global GRID
    global _GRID

    x = _x
    y = _y
    i = 0
    counter = 0
    z=0
    x_min = 99999
    x_max = 0
    y_min = 99999
    y_max = 0

    fr = font.render("OUTPUT MAP".format(t1.get()) ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),y+pm_wy-5))
    #window.blit(fr,(x+int(wx/2),y+pm_wy))
    window.blit(fr,fr_r)
    fr = font.render("↑    ↑    ↑".format(t1.get()) ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),y+pm_wy+15))
    #window.blit(fr,(x+int(wx/2),y+pm_wy))
    window.blit(fr,fr_r)
    fr = font.render("INPUT".format(t1.get()) ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),y+pm_wy+35))
    #window.blit(fr,(x+int(wx/2),y+pm_wy))
    window.blit(fr,fr_r)


    j = 0
    for fix in _GRID:
        if j >= 8*8: # max output size
            break
        #if j >= _x*_y: # max input size
        #    break
        j+=1
        ii = i
        #z= i # helping border offset 
        pos = fix.POS(40,60)
        rgb = fix.rgb

        # green
        pygame.draw.rect(window,[0,40,0],pos)

        xposs = [] #None #pos[:]
        for fix2 in GRID:
            if fix._id == fix2._id:
                xposs.append( fix2.POS(40,60) )

        for xpos in xposs:
            sub = grab(xpos[0],xpos[1]+pm_wy,xpos[2],xpos[3])
            if sub:
                if 1:#j <= _x*_y: # max input size
                    window.blit(sub, (x+pos[0]+z,y+pos[1]+z))
            else:
                # red
                pygame.draw.rect(window,[40,0,0],pos) #[x+pos[0]+2+z,y+pos[1]+2+z-pm_wy,12,9])


            if xpos[0] < x_min:
                x_min = xpos[0]
            if xpos[0] > x_max:
                x_max += xpos[2]

            if xpos[1] < y_min:
                y_min = xpos[1]
            if xpos[1] > x_max:
                y_max += xpos[3]
            # DRAW FIX NUMBER on TOP

        #apos = pos
        #argb = rgb
        apos = fix.POS(40,60+pm_wy)
        argb = fix.rgb

        # overwrite number overlay
        if  NR:
            #pygame.draw.rect(window,[30,40,0],apos)
            pygame.draw.rect(window,[20,40,0],[x+apos[0]+2+z,y+apos[1]+2+z-pm_wy,12,9])

        if NR:# == 2:
            if fix._id != i+1:
                fr = font15.render("{:02}".format(fix._id) ,1, (255,255,0))
                window.blit(fr,(x+apos[0]+2+z,y+apos[1]+2+z-pm_wy))
                #print(fix._id,xposs,pos)
            else:
                fr = font15.render("{:02}".format(fix._id) ,1, (100,100,255))
                window.blit(fr,(x+apos[0]+2+z,y+apos[1]+2+z-pm_wy))
        i += 1
        #print("--#")

    # frame box
    #pygame.draw.box(window,[100,0,0],[x+x_min,y+x_min,x_max+x_min,y_min+y_max])
    pos1= [x+x_min,y+x_min]
    pos2= [x_max+x_min,y_min+y_max]
    #draw_box(pos1,pos2,text=0)



class Timer():
    def __init__(self,start=120):
        self.start = start
        self.timer = self.start

        self.timer_t = time.time()

    def reset(self):
        self.timer = self.start

    def get(self):
        self.timer -= time.time()-self.timer_t
        self.timer_t = time.time()
        if self.timer <= 0:
            self.reset()
        return self.timer

def reload_grid():
    print("==== reload_grid")
    global GRID
    global _GRID
    try:
        GRID =  init_grid(_x=_x,_y=_y) #init_gird()
        _GRID =  init_grid(_x=8,_y=8,mapping=1) #init_gird()
    except Exception as e:
        print("Except: grid re init",e)

VPU_TEXT = []
def load_vpu_text(nr=0):
    txt = "NONE"
    if not VPU_TEXT:
        pass #create VPU_TEXT_FILE
    if len(VPU_TEXT) > nr:
        txt = VPU_TEXT[0]
    return txt



grid_counter = time.time()
def draw_fix_nr(GRID):
    global grid_counter
    i=0
    y=0

    for fix in GRID:
        pos = fix.POS(40,60+pm_wy)
        rgb = fix.rgb


        if NR:
            pygame.draw.rect(window,[0,0,0],[pos[0]+2,pos[1]+2,12,9])
            if fix._id%_x-1 == 0: # line break border
                pygame.draw.line(window,[255,255,0],(pos[0],pos[1]+4),(pos[0],pos[1]+pos[3]-4),1)
                pygame.draw.line(window,[255,255,0],(pos[0],pos[1]+int(pos[3]/2)),(pos[0]+int(pos[2]/2),int(pos[1]+pos[3]/2)),1)
            if fix._id%_x == 0: # line break border
                pygame.draw.line(window,[255,255,255],(pos[0]+pos[2]-1,pos[1]+4),(pos[0]+pos[2]-1,pos[1]+pos[3]-4),1)
                pygame.draw.line(window,[255,255,255],(pos[0]+pos[2]-1,int(pos[1]+pos[3]/2)),(pos[0]+int(pos[2]/2-1),int(pos[1]+pos[3]/2)),1)

            if grid_counter +5 < time.time():
                grid_counter = time.time()
                reload_grid()
            if fix._id != i+1:
                fr = font15.render("{:02}".format(fix._id) ,1, (255,255,0))
            else:
                fr = font15.render("{:02}".format(fix._id) ,1, (100,100,255))
            window.blit(fr,(pos[0]+2,pos[1]+2))
        i += 1
 

def draw_counter(COUNTER):
    for count in COUNTER:
        cpan = 0
        ctilt = 0
        cr=255
        cg=255
        cb=255
        csize=10
        cdim=0
        k = "DIM"
        if k in count:
            cdim = int(count[k])
        k = "RED"
        if k in count:
            cr = int(count[k])
        k = "GREEN"
        if k in count:
            cg = int(count[k])
        k = "BLUE"
        if k in count:
            cb = int(count[k])

        k = "SIZE"
        if k in count:
            csize = int(count[k])
        if csize < 5:
            csize = 5

        k = "PAN"
        if k in count:
            cpan = int(count[k])/255*(block[0] *(_x))
            cpan = int(cpan)
        k = "TILT"
        if k in count:
            ctilt = int(count[k])/255*(block[1] *(_y))
            ctilt = int(ctilt)

        ddim = cdim/255
        if "DIM" in count and count["DIM"] > 0:
            tmp_font = pygame.font.SysFont("freemonobold",int(block[0]/100*csize))
            rgb =(int(cr*ddim),int(cg*ddim),int(cb*ddim),cdim) 
            
            _sec = count["_SEC"]
            
            try:
                _sec = int(count["_SEC"])
            except:
                pass

            if type(_sec) is int:
                #print(_sec)
                if _sec <= 60:
                    fr = tmp_font.render("{:0}".format(_sec) ,1, rgb)
                else:
                    _xx = time.strftime("%M:%S",time.localtime(_sec))
                    #print("_xx",_xx)
                    fr = tmp_font.render("{}".format(_xx) ,1, rgb)
            else:
                fr = tmp_font.render("{}".format((count["_SEC"])) ,1, rgb)

            fr_r = fr.get_rect(center=(60+cpan-(block[0]),60+ctilt+pm_wy))
            pygame.draw.rect(window,[0,0,0],fr_r)
            window.blit(fr,fr_r)

def draw_video(VIDEO):
    global videplayer
    i = 0
    for count in VIDEO:
        cpan = 0
        ctilt = 0
        cr=255
        cg=255
        cb=255
        csize=10
        cdim=0
        k = "DIM"
        if k in count:
            cdim = int(count[k])

        k = "SIZE"
        if k in count:
            csize = int(count[k])
        if csize < 5:
            csize = 5

        k = "PAN"
        if k in count:
            cpan = int(count[k])/255*(block[0] *(_x))
            cpan = int(cpan)
        k = "TILT"
        if k in count:
            ctilt = int(count[k])/255*(block[1] *(_y))
            ctilt = int(ctilt)

        video1 = videoplayer[i]
        video1.pos 
        video1.x=40+cpan
        video1.y=60+pm_wy+ctilt
        video1.scale = int((csize))

        if cdim:
            video1.next()
            #video1.prev()

            video1.draw(window) #,x=0,y=0)

            # overlay 
            video1.overlay(window,"run")


        i += 1

def counter_dmx(COUNTER,dataA):
    for count in COUNTER:
        cDMX=count["DMX"]-1
        try:
            count["DIM"]   = dataA[cDMX]
            count["PAN"]   = dataA[cDMX+1]
            count["TILT"]  = dataA[cDMX+2]
            count["CONTROL"] = dataA[cDMX+3]

            if count["CONTROL"] >= 10 and count["CONTROL"] < 20:
                count["_time"] = int(time.time()*10)/10
                count["_SEC"] = int(count["SEC"] - (time.time() - count["_time"]))
            if count["CONTROL"] >= 20 and count["CONTROL"] < 30:
                count["_RUN"] = 0 
            if count["CONTROL"] >= 30 and count["CONTROL"] < 40:
                count["_RUN"] = 1



            count["SIZE"]  = dataA[cDMX+4]
            count["SEC"]   = dataA[cDMX+5]
            if count["_RUN"]:
                try:
                    count["_SEC"] = int(count["SEC"] - (time.time() - count["_time"]))
                except Exception as e:
                    pass
            if type(count["_SEC"]) is int:
                if count["_SEC"] < 0:
                    count["_SEC"] = 0
            for ti in range(10):
                #print(ti,(ti+6)*10)
                if count["CONTROL"] >= (ti+6)*10 and count["CONTROL"] < (ti+7)*10:
                    count["_SEC"] = "----" #text 1
                    try:
                        count["_SEC"] = TEXT_BLOCK[ti]
                    except Exception as e:
                        pass

            if count["CONTROL"] >= 250 and count["CONTROL"] < 256:
                count["_SEC"] = ">{}<".format(cDMX+1)

            count["RED"]   = dataA[cDMX+6]
            count["GREEN"] = dataA[cDMX+7]
            count["BLUE"]  = dataA[cDMX+8]
        except Exception as e:
            print("EXC FUNC",e,count)
        #print(count)


def video_dmx(VIDEO,dataA):
    for count in VIDEO:
        cDMX=count["DMX"]-1
        try:
            count["DIM"]   = dataA[cDMX]
            count["PAN"]   = dataA[cDMX+1]
            count["TILT"]  = dataA[cDMX+2]
            count["CONTROL"] = dataA[cDMX+3]

            if count["CONTROL"] >= 10 and count["CONTROL"] < 20:
                count["_time"] = int(time.time()*10)/10
                count["_SEC"] = int(count["SEC"] - (time.time() - count["_time"]))
            if count["CONTROL"] >= 20 and count["CONTROL"] < 30:
                count["_RUN"] = 0 
            if count["CONTROL"] >= 30 and count["CONTROL"] < 40:
                count["_RUN"] = 1



            count["SIZE"]  = dataA[cDMX+4]
            count["SEC"]   = dataA[cDMX+5]
            if count["_RUN"]:
                try:
                    count["_SEC"] = int(count["SEC"] - (time.time() - count["_time"]))
                except Exception as e:
                    pass
            if type(count["_SEC"]) is int:
                if count["_SEC"] < 0:
                    count["_SEC"] = 0
            for ti in range(10):
                #print(ti,(ti+6)*10)
                if count["CONTROL"] >= (ti+6)*10 and count["CONTROL"] < (ti+7)*10:
                    count["_SEC"] = "----" #text 1
                    try:
                        count["_SEC"] = TEXT_BLOCK[ti]
                    except Exception as e:
                        pass

            if count["CONTROL"] >= 250 and count["CONTROL"] < 256:
                count["_SEC"] = ">{}<".format(cDMX+1)

            count["RED"]   = dataA[cDMX+6]
            count["GREEN"] = dataA[cDMX+7]
            count["BLUE"]  = dataA[cDMX+8]
        except Exception as e:
            print("VIDEOPLAYER EXCEPT FUNC",e,count)
        #print(count)

def read_dmx_data(ip,ips):
    ip = select_ip(ips,univ=START_UNIV)
    IP = ip
    data = read_dmx(ip)


    ip = select_ip(ips,univ=START_UNIV+1)
    data3 = read_dmx(ip)
    data.extend(data3)

    ip = select_ip(ips,univ=START_UNIV+2)
    data3 = read_dmx(ip)
    data.extend(data3)

    ip = select_ip(ips,univ=START_UNIV+4)
    data3 = read_dmx(ip)
    data.extend(data3)

    #ip = select_ip(ips,univ=START_UNIV+5)
    #data3 = read_dmx(ip)
    #data.extend(data3)
    
    return data

def draw_gobo(GRID,data):

    i = 0
    dmx = 1
    h = 1
    v = 1
    for fix in GRID:
        pos = fix.POS(40,60+pm_wy)
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
            spos = subfix.POS(40,60+pm_wy)
            srgb = subfix.rgb

            #print(fix.dmx,rgb,pos)
            #pygame.draw.circle(window,rgb,(pos[0]+int(pos[2]/2),pos[1]+int(pos[3]/2)),int(pos[3]/2))
            #FUNC = 0
            if FUNC > 10 and FUNC <= 20: # big dot
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/2))
            elif FUNC > 20 and FUNC <= 30:#small dot
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
            elif FUNC > 30 and FUNC <= 40:#donut
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/2))
                draw_circle(window,[0,0,0],(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
            elif FUNC > 40 and FUNC <= 50: # rec with hole
                pygame.draw.rect(window,srgb,spos)
                draw_circle(window,[0,0,0],(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
            elif FUNC > 50 and FUNC <= 60: # rec with big hole
                pygame.draw.rect(window,srgb,spos)
                draw_circle(window,[0,0,0],(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/2))
            elif FUNC > 60 and FUNC <= 70: # rec with donat
                pygame.draw.rect(window,srgb,spos)
                draw_circle(window,[0,0,0],(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/2))
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
            elif FUNC > 70 and FUNC <= 80: # rec boarder
                pygame.draw.rect(window,srgb,[spos[0]+1,spos[1]+1,spos[2]-2,spos[3]-2])
            elif FUNC > 80 and FUNC <= 90: # rec big boarder
                pygame.draw.rect(window,srgb,[spos[0]+2,spos[1]+2,spos[2]-4,spos[3]-4])
            elif FUNC > 90 and FUNC <= 100: # rec thin line
                pygame.draw.rect(window,srgb,spos)
                pygame.draw.rect(window,[0,0,0],[spos[0]+1,spos[1]+1,spos[2]-2,spos[3]-2])
            elif FUNC > 100 and FUNC <= 110: # rec big line
                pygame.draw.rect(window,srgb,spos)
                pygame.draw.rect(window,[0,0,0],[spos[0]+2,spos[1]+2,spos[2]-4,spos[3]-4])
            elif FUNC > 110 and FUNC <= 120: # rec with dot
                pygame.draw.rect(window,srgb,spos)
                pygame.draw.rect(window,[0,0,0],[spos[0]+1,spos[1]+1,spos[2]-2,spos[3]-2])
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
            elif FUNC > 120 and FUNC <= 130: # rec inline
                pygame.draw.rect(window,srgb,[spos[0]+2,spos[1]+2,spos[2]-4,spos[3]-4])
                pygame.draw.rect(window,[0,0,0],[spos[0]+3,spos[1]+3,spos[2]-6,spos[3]-6])
            elif FUNC > 130 and FUNC <= 140: # 3 dot (heart)
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2)+2,spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2)-2,spos[1]+int(spos[3]/2)),int(spos[3]/3.5))
                draw_circle(window,srgb,(spos[0]+int(spos[2]/2),spos[1]+int(spos[3]/2)+2),int(spos[3]/3.5))
            else:
                pygame.draw.rect(window,srgb,spos)


        for subfix in fix.sub_fix:#calc(data):
            subfix.calc(data)
            #fix = subfix
            spos = subfix.POS(40,60+pm_wy)
            srgb = subfix.rgb

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


            if p >= 40:
                if NR:
                    #fr = font15.render("{:02}".format(j+1) ,1, (0,200,255))
                    fr = font15.render("{:02}".format(subfix._id) ,1, (250,200,5))
                    window.blit(fr,(spos[0]+2,spos[1]+10))
            j += 1
        i += 1

t1 = Timer(143)
time.sleep(0.33)
t2 = Timer(11)

count_tilt = 0
def main():
    global IP
    global GRID
    global _GRID
    global FUNC
    global count_tilt
    global TEXT_BLOCK
    global TEXT_BLOCK_TIME
    global PLAYLIST
    global PLAYLIST_TIME

    GRID =  init_grid(_x=_x,_y=_y) #init_gird()
    #GRID =  init_grid(_x=8,_y=8) #init_gird()
    print("GRID LEN:",len(GRID))


    s=time.time()
    print("run")
    r = ""
    IP = "xx"
    while running:

        if  TEXT_BLOCK_TIME+5 < time.time():
            TEXT_BLOCK = open_text_block()
            TEXT_BLOCK_TIME = time.time()

        if  PLAYLIST_TIME+6 < time.time():
            PLAYLIST = open_playlist()
            PLAYLIST_TIME = time.time()


        pygame.display.flip()
        event()

        window.fill((10,0,20))
        calc_fps()
        draw_overlay()

        ips = read_index()
        
        # ----
        ip = select_ip(ips,univ=1) # univ 1 gobo
        dataA = read_dmx(ip)
        # ----

        data = read_dmx_data(ip,ips)


        if options.countdown:
            counter_dmx(COUNTER,dataA)
        
        if VIDEO:
            video_dmx(VIDEO,dataA)



        # GRID loop
        try:
            ddd = 1023 #univ 3 512
            #FUNC = data[ddd]
            FUNC2 = dataA[gobo_ch-1]
            FUNC = FUNC2
            #print("FUNC", FUNC )#:ddd+512])
            #FUNC = 15
        except Exception as e:
            print("EXC FUNC",e)


        draw_gobo(GRID,data) 

        # DRAW FIX NUMBER on TOP
        draw_fix_nr(GRID)
        

        #COUNTER.append({"DMX":31,"DIM":0,"PAN":127,"TILT":127,"CONTROL":0,"SEC":10,"RED":255,"GREEN":255,"BLUE":255,"_time":time.time(),"_RUN":0,"_SEC":0})
        if options.countdown:
            draw_counter(COUNTER)

        if VIDEO:
            draw_video(VIDEO)

        pointer.draw(0,pm_wy) #wy
        spos = [0,0,0,0]
        if PIXEL_MAPPING >= 1:
            reshape(0,0) #start pos
        else:
            reshape(spos[0]+spos[2]+20,10) #start pos
            #reshape(spos[0]+spos[2]+20,10) #start pos





        pygame.display.flip()
        #pg.time.wait(15)
        clock.tick(10)

        if 'SDL_VIDEO_WINDOW_POS' in os.environ:
            del os.environ['SDL_VIDEO_WINDOW_POS'] #= '%i,%i' % (200,164)
        #if 'SDL_VIDEO_CENTERED' in os.environ['SDL_VIDEO_CENTERED']:
        #    del os.environ['SDL_VIDEO_CENTERED'] #= '0'


if __name__ == "__main__":
    main()
