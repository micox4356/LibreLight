
import math
import random
import time
import os
import sys
import gc

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


import numpy


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
    r = ""
    if ip:
        #t = int(math.sin(time.time() - s)*10)
        r = mc.get(ip) #"2.0.0.13:2")
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

PLAYLIST = []
try:
    PLAYLIST = open_playlist()
except:pass

#import json
#import pickle


class Vopen():

    def __init__(self,dmx=None,_id=None):
        global PLAYLIST

        self._id = _id
        self.fpath = '/home/user/Downloads/'
        self.fpath = '/home/user/LibreLight/video/'
        self.fname = '' #'bbb_sunflower_480x320.mp4'
        #self.fname = 'no-video.mp4'
        try:
            self.fname = PLAYLIST[0]
        except Exception as e:
            print("Exception set video from PLAYLIST 5543:",e)

        self.restart_t = time.time()
        self.fps = 0
        self.scale = 50 #%
        self.dmx=dmx
        self.dim = 0
        self.x = 0
        self.y = 0
        self.init_count = 0
        self.cap = None
        self.shape = [200,200]  
        self.img = None
        self.success = 1
        self.cv2 = None
        self._run = 0
        self.end = 0
        self._video_nr = 0


        self.shape_x = 370
        self.shape_y = 235
        try:
            global cv2
            self.cv2 = cv2
        except:
            pass

        self.init()

    def restart(self):
        print(self,"reset()")
        self.pos = 0 
        self.restart_t = time.time()

    def init(self):
        print("---- ---- Vopen.init()",[self.fname,self._video_nr])
        print(PLAYLIST)
        self.time = 0
        self.t_delta = 0 
        self.t_last  = time.time()
        self.im = None
        self.pos = 0
        self.buffer = []
        self._init()
        self.init_count = 1

    def select_video(self,dmx_value):
        try:
            dmx_value = int(dmx_value/10)

            if self._video_nr != dmx_value:
                self._video_nr = dmx_value

                if self._video_nr < len(PLAYLIST):
                    self.fname = str(PLAYLIST[self._video_nr])
                    self.init()

        except Exception as e:
            print("Vopen.select_video()",dmx_value,e)

    def close_cap():
        print(dir(self.Rcap)) # = self.cv2.VideoCapture(self.fpath+self.fname)

    def _init(self):
        print(self)
        print("videoplayer.init()",self.fpath,self.fname)

        if not os.path.isfile(self.fpath+self.fname):
            print()
            print("video file does not exits !! >",self.fpath,self.fname)
            print()
            #exit()
    
        self.Rsuccess = 0
        if self.cv2:
            #self.Rcap = self.cv2.VideoCapture(self.fpath+self.fname)

            #self.Rcap = self.cv2.VideoCapture(self.fpath+self.fname, cv2.CAP_GSTREAMER) 
            #GSTREAMER Assertion fctx->async_lock failed at libavcodec/pthread_frame.c:175
            
            self.Rcap = self.cv2.VideoCapture(self.fpath+self.fname, cv2.CAP_FFMPEG) 
            #FFMPEG malloc(): unsorted double linked list corrupted ... Abgebrochen

            self.Rcap.read()

            #self.Rfvs = FileVideoStream(self.fpath+self.fname).start()
            self.Rsuccess = 1
            self._read()
    def _del(self):
        #self.Rcap = self.cv2.VideoCapture(self.fpath+self.fname)
        #for i in dir(self.Rcap):
        #    print(i)

        #print()
        #for i in dir(self.cv2):
        #    print(i)
        #time.sleep(0.01)

        self.buffer = [] #.append(self.img)
        self.Rcap.release()
        self.Rcap.retrieve()

        self.Rcap = None
        self.cap = None
        del self.Rcap #.release()
        #time.sleep(4)
        #sys.exit()
        #gc.collect()
        #import gc
        gc.collect()


    def _read(self):
        success = self.Rsuccess
        ok = 0
        if success and self.fname:
            cap = self.Rcap
            #fvs = self.Rfvs
            _break = 0

            try:
                success, img = cap.read()
                #self.img = fvs.read()
                if not success:
                    self.Rcap.release()
                    self.Rcap.retrieve()
                    self.end = 1
                    #j = json.dumps(self.buffer) #.append(img)
                    #f = open("/tmp/buff")
                    #f.write(j)
                    #f.close()
                    return

                if self.fps == 0:
                    self.fps = cap.get(cv2.CAP_PROP_FPS)
                
                img = self.cv2.cvtColor(img, self.cv2.COLOR_BGR2RGB)
                img = self.rescale_frame2(img, 200)
                #ret, img = self.cv2.threshold(img, 100, 130, self.cv2.THRESH_BINARY) # treshold
                #self.img = self.cv2.Canny(self.img, 100, 200) # kanten
                
                #M = cv2.getPerspectiveTransform(Punkte_A, Punkte_B)
                #warped = cv2.warpPerspective(Bild, m, (420,594))
                
                #self.cv2.normalize(self.img, self.img, 0, self.dim, self.cv2.NORM_MINMAX) 
                
                # store frame into buffer list
                self.buffer.append(img)
                ok = 1
                if len(self.buffer) % 100 == 0:
                    _id = str(self.__repr__)[-5:-1]
                    print(_id,"video read",self.dmx,len(self.buffer),self.fname,"fps",self.fps,self.dim)

            except Exception as e:
                print("Excetpion","_init",self,e,end="")
        self.success = 1
        return ok

    def read(self):
        pass

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self.buffer)-1
        if self.pos >= len(self.buffer):
            self.pos = len(self.buffer)-1
        self.im = self.buffer[int(self.pos)]

    def rescale_frame2(self,frame, width):
        height = int(frame.shape[0]/frame.shape[1] * width )
        dim = (width, height)
        return self.cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def rescale_frame(self,frame, percent=75):
        width  = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return self.cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def pause(self):
        #print("pause",self.t_last)
        t = time.time()
        self.t_delta = 0 
        self.t_last = t

    def next_frame(self):
        #return 0
        
        if self._run and len(self.buffer) > 30:
            t = time.time()
            self.t_delta = t-self.t_last 
            self.pos += self.t_delta*self.fps
            self.t_last = t
        else:
            self.pause()

        if self.restart_t > time.time()-0.5:
            # prevent flickerung by reset
            #self.pause()
            self.pos = 5
            pass

        # restart at the end
        if self.pos >= len(self.buffer):
            self.pos = 0 
        
        self.img = None
        self._img = self.buffer[int(self.pos)]
        self.img = self._img

    def next(self):
         
        try:
            self.next_frame()

            #self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
            self.img = self.rescale_frame(self.img, percent=self.scale)

            self.shape = self.img.shape[1::-1]

            if len(self.buffer) % 100 == 0:
                _id = str(self.__repr__)[-5:-1]
                print("next",_id)

            # add DIMER to videplayer
            self.cv2.normalize(self.img, self.img, 0, self.dim, self.cv2.NORM_MINMAX) 
            
            img = self.img 
            if img is None:
                return 
            self.im = None
            self.im = pygame.image.frombuffer(img.tobytes(), self.shape, "RGB")

            #self.next_frame()

        except AttributeError as e:
            time.sleep(.05)
            #if self.init_count % 100 == 0:
            print("except 776",e)
            #self.init()
        except Exception as e:
            print("except 756",e)

    def draw(self,wn=None):
        
        if self.dim <= 1:
            return

        if self.scale < 255*.05:
            self.scale = 255*0.05

        # draw video background box
        __xw = int(self.shape_x*self.scale/255)
        __yw = int(self.shape_y*self.scale/255)
    
        #xx ,yy = (370,235)
        xx = self.shape_x #= xx
        yy = self.shape_y #= yy
        try:
            xx ,yy = self.im.get_size()[:2]
            self.shape_x = xx
            self.shape_y = yy
        except AttributeError as e:
            pass

        xx = int(xx*self.scale/255)
        yy = int(yy*self.scale/255)

        __xw = int(xx) #*self.scale/255)
        __yw = int(yy) #*self.scale/255)
        yellow = [105,50,0]
        yellow[0] = int(yellow[0]*self.dim/255)  
        yellow[1] = int(yellow[1]*self.dim/255)  
        yellow[2] = int(yellow[2]*self.dim/255)  
        #print(yellow)
        if 1: #corner left up
            p1 = [self.x+2,self.y+2]  
            p2 = [self.x+__xw-4,self.y+__yw-4]
            p3 = [self.x+__xw-4,self.y+2]
            p4 = [self.x+2,self.y+__yw-4]

            p1 = [self.x,self.y]  
            p2 = [self.x+__xw,self.y+__yw]
            p3 = [self.x+__xw,self.y]
            p4 = [self.x,self.y+__yw]
            
            hx=int(xx/2)
            hy=int(yy/2)
            #print(hx,hy,xx,yy) #,ratio)
            #print("-")
            #print(sys.getsizeof(self.buffer))
            #print(sys.getsizeof(self))
            #print(sys.getsizeof(self.Rcap))
            #print(dir(self.Rcap))
            p1 = [self.x-hx,self.y-hy]  
            p2 = [self.x+__xw-hx,self.y+__yw-hy]
            p3 = [self.x+__xw-hx,self.y-hy]
            p4 = [self.x-hx,self.y+__yw-hy]

            pygame.draw.rect(wn,yellow    ,[p1[0]  ,p1[1]  ,__xw  ,__yw])
            pygame.draw.rect(wn,[25,20,20],[p1[0]+1,p1[1]+1,__xw-2,__yw-2])
            pygame.draw.line(wn,yellow    ,p1      ,p2)
            pygame.draw.line(wn,yellow    ,p3      ,p4)
        if 0: #corner left up
            pygame.draw.rect(wn,yellow,[self.x,self.y,__xw,__yw])
            pygame.draw.rect(wn,[25,20,20],[self.x+1,self.y+1,__xw-2,__yw-2])
            pygame.draw.line(wn,yellow,[self.x+2,self.y+2],[self.x+__xw-4,self.y+__yw-4])
            pygame.draw.line(wn,yellow,[self.x+__xw-4,self.y+2],[self.x+2,self.y+__yw-4])
        if 0: #corner right down
            pygame.draw.rect(wn,yellow,[self.x-__xw,self.y-__yw,__xw,__yw])
            pygame.draw.rect(wn,[25,20,20],[self.x+1-__xw,self.y+1-__yw,__xw-2,__yw-2])
            pygame.draw.line(wn,yellow,[self.x+2-__xw,self.y+2-__yw],[self.x+__xw-4-__xw,self.y+__yw-4-__yw])
            pygame.draw.line(wn,yellow,[self.x+__xw-4-__xw,self.y+2-__yw],[self.x+2-__xw,self.y+__yw-4-__yw])

        #pygame.draw.line(wn,yellow,[self.x,self.y],[self.x,self.y+300])
        #pygame.draw.line(wn,yellow,[self.x,self.y],[self.x+300,self.y])
        pz = 0
        #txt = "FPS:{} F:{:05} von {:05} sec:{:0.02f} von {:0.02f}"
        #txt = txt.format(self.fps,int(self.pos),len(self.buffer),(-1),pz ) 
        #if self.end:
        #    fr = font15.render(txt,1, (0,255,0))
        #else:
        #    fr = font15.render(txt,1, (255,0,0))
        #wn.blit(fr,(10,MAIN_SIZE[1]-(self._id+1)*35))

        if self.success and wn and self.im: # is not None:
            #wn.blit(self.im, (int(self.x), int(self.y)))
            #wn.blit(self.im, (int(self.x-__xw), int(self.y-__yw)))
            #xx ,yy = self._img.shape[:2]
            xx ,yy = self.im.get_size()[:2]
            #print(xx,yy)
            #wn.blit(self.im, (int(self.x+xx/2), int(self.y+yy/2)))
            wn.blit(self.im, (int(self.x-xx/2), int(self.y-yy/2)))

    def overlay(self,wn=None,mode="x"):
        # overlay 

        pygame.draw.rect(wn,[255,200,0],[5,MAIN_SIZE[1]-(self._id+1)*35,300,28])
        font15 = pygame.font.SysFont("freemonobold",17)

        pz = 0

        if self.end:
            rgb = [ 100,255,100]
        else:
            rgb = [255,100,0]
        pygame.draw.rect(wn,rgb,[220,MAIN_SIZE[1]-(self._id+1)*35,80,13])

        _line = "error no _line"
        _line ="FPS:{} F:{:05} von {:05} sec:{:0.02f} von {:0.02f}"
        if self.fps == 0: # check if div zerro
            _line = _line.format(self.fps,int(self.pos),len(self.buffer),(-1),pz )
        else:
            pz = (len(self.buffer)/self.fps)
            _line = _line.format(self.fps,int(self.pos),len(self.buffer),(self.pos/self.fps),pz )  

        fr = font15.render(_line ,1, (0,0,0))
        wn.blit(fr,(10,MAIN_SIZE[1]-(self._id+1)*35))

        if self._run:
            mode = "run"
        else:
            mode = "pause"
        fr = font15.render(" {} {} >:{} ".format(self._id+1,self._video_nr,mode) ,1, (0,0,0))
        wn.blit(fr,(3,MAIN_SIZE[1]-(self._id+1)*35+15))

        fr = font15.render("{}".format(self.fname) ,1, (0,0,0))
        wn.blit(fr,(70,MAIN_SIZE[1]-(self._id+1)*35+15))

Vopen = Vopen

VIDEO = []
videoplayer=[]            
cv2 = None
FileVideoStream = None

_vid = 0
if type(options.videoplayer) is str:
    try:
        import cv2
    except Exception as e:
        print("Except Import:",e)
    try:
        # faster video reading ... ???
        from imutils.video import FileVideoStream
    except Exception as e:
        print("Except Import:",e)

    max_videoplayer = 4
    dmx_start =  options.videoplayer.split(",")
    for cdmx in dmx_start:
        if len(videoplayer) > max_videoplayer:
            print("-- videoplayer max count {} !! break".format(max_videoplayer))
            break
        print("-- videoplayer dmx:",cdmx)
        try:
            cdmx = int(cdmx)
            videoplayer.append( Vopen(cdmx,_id=_vid) )
            _vid += 1
            VIDEO.append({"DMX":cdmx,"DIM":0,"PAN":127,"TILT":127,"CONTROL":0,"SEC":10,"VIDEO":"3","RED":255,"GREEN":255,"BLUE":255,"_time":time.time(),"_RUN":0,"_SEC":">{}<".format(cdmx)})
        except Exception as e:
            print("EXCEPTION COUNTER INIT ",cdmx)

def loop_videoplayer():
    while 1:
        _videoplayer = videoplayer[:]
        #print(".")
        ok = 0
        for i in _videoplayer: #.append( Vopen(cdmx,_id=_vid) )
            try:
                r = i._read() # read next frame from file
                if r:
                    ok = 1
            except Exception as e:
                print("EXCEPTION loop_videoplayer ",e)
            #time.sleep(0.002)
        #time.sleep(1/120)
        if ok == 0:
            time.sleep(0.1)
        else:
            time.sleep(0.005)

thread.start_new_thread(loop_videoplayer,())
# ===== ======

#self.fname = PLAYLIST[0]
videoplayer2 = []
def loop2_videoplayer():
    while 1:
        print()
        print()
        print()
        for i,v in enumerate(PLAYLIST):
            try:
                video1 = videoplayer2[i] 
                video1.select_video(i)
            except:
                vi = Vopen(181,1) 
                videoplayer2.append( vi )


        _videoplayer = videoplayer2[:]
        #print(".")
        ok = 0
        j =0 
        for i in _videoplayer: #.append( Vopen(cdmx,_id=_vid) )
            try:
                r = i._read() # read next frame from file
                #print(j,len(videoplayer2),i,len(i.buffer))
                if r:
                    print(j,len(videoplayer2),i,len(i.buffer))
                    ok = 1
            except Exception as e:
                print("EXCEPTION loop2_videoplayer ",e)
            time.sleep(0.002)
            j += 1
        if ok == 0:
            pass#time.sleep(0.01)
        else:
            pass#time.sleep(0.005)

#thread.start_new_thread(loop2_videoplayer,())

# PARSE COMMANDLINE ARGUMENTS
CFG_IN    = {"name":"CFG_IN","x1":40,"y1":60,"x2":300,"y2":300 ,"w":300,"h":300}
CFG_OUT   = {"name":"CFG_OUT","x1":40,"y1":60,"x2":300,"y2":300 ,"w":300,"h":300,"on":0}
CFG_BLOCK = {"name":"CFG_BLOCK","size":16,"h-split":2,"v-split":2,"h-count":8,"v-count":8}


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

    

if _x < 1:
    _x = 1
if _y < 1:
    _y = 1

CFG_BLOCK["h-count"] = _x
CFG_BLOCK["v-count"] = _y # int(8*8/_x) #/_x+0.5) #_y
CFG_BLOCK["size"]    = p

print( [options.xsplit])
print( [options.ysplit])

try:
    if options.xsplit:
        CFG_BLOCK["h-split"] = int(options.xsplit)
    if options.ysplit:
        CFG_BLOCK["v-split"] = int(options.ysplit)
except Exception as e:
    print( "Exc",options.mode,e)


print("HD",CFG_BLOCK["h-split"],CFG_BLOCK["v-split"])
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
play_list = "/home/user/LibreLight/video/" #.format(path)
pm_wy = 0
if options.pixel_mapping:
    PIXEL_MAPPING = 1
    CFG_OUT["on"] = 1
    path = options.pixel_mapping
    path = path.replace("/","-")
    path = path.replace(".","-")
    path = path.replace("\"","-")
    path = path.replace("'","-")
    grid_file = "/home/user/LibreLight/vpu_grid_hd{}.csv".format(path)
    text_file = "/home/user/LibreLight/vpu_text_hd{}.csv".format(path)
    play_list = "/home/user/LibreLight/vpu_playlist_hd{}.csv".format(path)
    play_list = "/home/user/LibreLight/video/" #.format(path)
    #_x = 8
    #_y = 8

print("  ",[options.pixel_mapping],"grid_file",grid_file)
#grid_file = "/home/user/LibreLight/vpu_grid_hd.csv"


MAIN_SIZE=(600,500)
try:
    if _x < 8 and PIXEL_MAPPING >= 1:
        wx = 30+30+block[0] * 8
        CFG_IN["w"] = CFG_BLOCK["size"] * 8
    else:
        wx = 30+30+block[0] * _x 

    wy = 40+40+block[1] * _y 

    if type(options.videoplayer) is str:
        wy += 150 # video playlist

    MAIN_SIZE=(wx,wy)

    if PIXEL_MAPPING >= 1:
        pm_wy = 11*p #+ p*3
        CFG_IN["y1"] += 11*p
        MAIN_SIZE=(wx,wy+pm_wy)

except Exception as e:
    print("Exception:",e)

CFG_IN["w"] = CFG_BLOCK["size"] * CFG_BLOCK["h-count"] 
CFG_IN["h"] = CFG_BLOCK["size"] * CFG_BLOCK["v-count"] 

CFG_OUT["w"] = CFG_BLOCK["size"] * 8
CFG_OUT["h"] = CFG_BLOCK["size"] * 8



def CFG_CALC_P(CFG):
    CFG["x2"] = CFG["x1"]+CFG["w"]
    CFG["y2"] = CFG["y1"]+CFG["h"] 
    CFG["p1"] = [CFG["x1"] ,CFG["y1"]] 
    CFG["p2"] = [CFG["x2"] ,CFG["y2"]] 
    print("CFG",CFG)

# ?
#CFG_IN["w"] = int(CFG_BLOCK["v-count"]-2) * CFG_BLOCK["size"] 

CFG_CALC_P(CFG_IN)
CFG_CALC_P(CFG_OUT)

print("CFG_BLOCK",CFG_BLOCK)
print()
print()
print()
print()
print()

window = pygame.display.set_mode(MAIN_SIZE,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
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
        
        sub_block =[block[0]/CFG_BLOCK["h-split"],block[1]/CFG_BLOCK["v-split"]] 
        if _id <= 0: #exit 
            return

        spalte = (_id-1)%_y +1
        zeile = int((_id-1)/_x2) #+1
        #zeile = zeile*_x*CFG_BLOCK["h-split"]*CFG_BLOCK["v-split"]

        add_row = _x*CFG_BLOCK["h-split"]*CFG_BLOCK["v-split"]

        #zeile 1
        sid = (_id-1)*2  + zeile*CFG_BLOCK["h-split"]*_x2
        #for i in range(1,CFG_BLOCK["h-split"]):
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
        sid = (_id-1)*2+1 + _x2*CFG_BLOCK["h-split"]  + zeile*CFG_BLOCK["h-split"]*_x2 # int(add_row)
        #sid = sid+1
        #sid = CFG_BLOCK["h-split"]
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
fps2 = 0
frame = 0
frame2 = 0
frame_t = time.time()
frame2_t = time.time()
IP = "yyy"
def draw_overlay():
    global fps,fps2
    fr = font15.render("DMX-FPS:{}".format(fps) ,1, (200,0,255))
    window.blit(fr,(10,10))

    fr = font15.render("GUI-FPS  :{}".format(fps2) ,1, (200,0,255))
    window.blit(fr,(10,20))

    fr = font.render("ip:{}".format(IP) ,1, (200,0,255))
    window.blit(fr,(90,10))

def draw_frame(window,rgb,p1,p2,offset=0):
    o = offset 
    _p1 = [p1[0]-o,p1[1]-o]
    _p2 = [p1[0]-o,p2[1]+o]
    pygame.draw.line(window,rgb,_p1,_p2)  # left
    _p1 = [p2[0]+o,p2[1]+o]
    pygame.draw.line(window,rgb,_p1,_p2)  # bottom
    _p2 = [p2[0]+o,p1[1]-o]
    pygame.draw.line(window,rgb,_p1,_p2)  # right
    _p1 = [p1[0]-o,p1[1]-o]
    pygame.draw.line(window,rgb,_p1,_p2)  # top

def calc_fps():
    global fps,frame,frame_t
    t = time.time()
    if frame_t+1 < t:
        fps = frame #frame_t- t #frame
        frame = 1
        frame_t = time.time()

def calc_fps2():
    global fps2,frame2,frame2_t
    t = time.time()
    if frame2_t+0.1 < t:
        fps2 = frame2*10 #frame_t- t #frame
        frame2 = 1
        frame2_t = t #time.time()


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


def open_playlist():
    print("======== OPEN PLAYLIST DIR !!",play_list)

    if not os.path.isdir(play_list):
        os.system("mkdir -p {}".format(play_list))

    _lines = os.listdir(play_list)
    _lines.sort()

    lines = ['']*25 # first is empty
    i=0
    for l in _lines:
        #print(">> ",l.strip(),len(lines))
        l = l.strip()
        if "_" in l:
            ll = l.split("_",1)
            print(">> ",ll)
            #ll = int(ll)
            try:
                lll = int(ll[0])
                #lines.append(l.strip())
                lines[lll] = l
            except:pass

    if len(lines) <= 10:
        for i in range(10-len(lines)):
            lines.append("")#"LINE ERROR")
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
    """reshape LED-WALL Block/Pixel mapping"""
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

    # black background for -> output MAP
    pygame.draw.rect(window,[0,0,20],[0,60,600,pm_wy-1]) 
    pygame.draw.rect(window,[0,0,20],[wx,wy-80,400,pm_wy+10]) 
    
    tmp_font = pygame.font.SysFont("freemonobold",int(p*0.8))

    fr   = tmp_font.render("OUTPUT" ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),int(60+pm_wy-p*1.5)))
    window.blit(fr,fr_r)

    fr   = tmp_font.render("↑  ↑    MAP    ↑  ↑" ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),int(60+pm_wy-p)))
    window.blit(fr,fr_r)

    fr   = tmp_font.render("INPUT" ,1, (255,255,255))
    fr_r = fr.get_rect(center=(x+int(wx/2),int(60+pm_wy-p/2)))
    window.blit(fr,fr_r)


    j = 0
    for fix in _GRID:
        if j >= 8*8: # max output size
            break
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
            csize = int(count[k]) #/60*p)
        if csize < 5:
            csize = 5

        k = "PAN"
        if k in count:
            cpan = int(count[k])/255*(block[0] *(_x))
            #cpan = int(cpan * 1.2)
            cpan = int(cpan)
        k = "TILT"
        if k in count:
            ctilt = int(count[k])/255*(block[1] *(_y))
            #ctilt = int(cpan * 1.2)
            ctilt = int(ctilt)

        ddim = cdim/255
        if "DIM" in count and count["DIM"] > 0:
            tmp_font = pygame.font.SysFont("freemonobold",int(p/100*csize))
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

            fr_r = fr.get_rect(center=(40+cpan-(block[0]),60+ctilt+pm_wy))
            pygame.draw.rect(window,[0,0,0],fr_r)
            window.blit(fr,fr_r)

def draw_video(VIDEO):
    global videplayer
    i = 0

    # set DMX-VALUE to videoplayer Object
    for count in VIDEO:
        cpan = 0
        ctilt = 0
        cr=255
        cg=255
        cb=255
        csize=10
        cdim=0
        

        video1 = videoplayer[i]
        k = "VIDEO"
        if k in count:
            #video1.select_video(count[k])

            play_nr = int(count[k]/10)
            if play_nr != video1._video_nr:
                print( "+ + + +  + + + + + + +", play_nr , video1._video_nr ,str(video1))
                _vid  = video1._id
                _cdmx = video1.dmx
                del_video1 = video1

                video1 = Vopen(cdmx,_id=_vid) 
                video1.select_video(count[k])
                videoplayer[i] = video1

                del_video1._del()
                del del_video1

        k = "DIM"
        if k in count:
            cdim = int(count[k])
            video1.dim = cdim
        #if i == 0:
        #    print(i,cdim)

        k = "SIZE"
        if k in count:
            csize = int(count[k]/16*p)
        if csize < 5:
            csize = 5

        k = "PAN"
        cpan_max = block[0] *(_x) #+block[0]
        if k in count:
            cpan = int(count[k]) / 255*cpan_max
            cpan = int(cpan)
        k = "TILT"

        ctilt_max = block[1] *(_y) #+block[1]
        if k in count:
            ctilt = int(count[k]) / 255*ctilt_max
            ctilt = int(ctilt)

        


        k = "_reset"
        if k in count:
            if count[k]:
                count[k] = 0
                video1.restart()

        k = "_RUN"
        if k in count:
            video1._run = count[k]



        video1.pos 
        video1.x=40+0+cpan 
        video1.y=60+0+pm_wy+ctilt
        video1.scale = int((csize))

        if cdim:
            video1.next()
        i += 1

    # draw

    i=0
    for count in VIDEO:
        video1 = videoplayer[i]
        video1.draw(window) #,x=0,y=0)
        i+=1


    i=0
    for count in VIDEO:
        video1 = videoplayer[i]
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
                count["_reset"] = 1

            if count["CONTROL"] >= 20 and count["CONTROL"] < 30:
                if count["_RUN"] == 1:
                    print(  "_RUN:0",count["DMX"]-1)
                count["_RUN"] = 0 

            if count["CONTROL"] >= 30 and count["CONTROL"] < 40:
                if count["_RUN"] == 0:
                    print(  "_RUN:1",count["DMX"]-1)
                count["_RUN"] = 1

            count["SIZE"]  = dataA[cDMX+4]#*2
            count["SEC"]   = dataA[cDMX+5]

            count["VIDEO"] = dataA[cDMX+6]
            #count["RED"]   = dataA[cDMX+6]
            #count["GREEN"] = dataA[cDMX+7]
            #count["BLUE"]  = dataA[cDMX+8]
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

def frame_area():
    rgb = [255,255,0]
    CFG = CFG_IN
    
    
    p1 = CFG_IN["p1"]
    p2 = CFG_IN["p2"]
    draw_frame(window,rgb,p1,p2,offset=2)
    rgb = [255,0,0]
    #draw_frame(window,rgb,p1,p2,offset=4)


    if CFG_OUT["on"]:
        rgb = [255,0,0]
        p1 = CFG_OUT["p1"]
        p2 = CFG_OUT["p2"]
        #pygame.draw.line(window,rgb,p1,p2)
        draw_frame(window,rgb,p1,p2,offset=3)

ips=[]
dataA=[]
data=[]

def dmx_raw():
    global frame
    frame += 1

    global ips,dataA,data
    ips = read_index()
    
    # ----
    ip = select_ip(ips,univ=1) # univ 1 gobo
    dataA = read_dmx(ip)
    # ----

    data = read_dmx_data(ip,ips)


    if options.countdown:
        counter_dmx(COUNTER,dataA)
    
    if len(VIDEO) > 0:
        video_dmx(VIDEO,dataA)
    return ips,dataA,data


def dmx_loop():
    while 1:
        dmx_raw()
        time.sleep(1/40) # fast high cpu
        #time.sleep(1/25)

dmx_raw()

thread.start_new_thread(dmx_loop,())

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
    global dataA
    global frame2

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

        window.fill((10,0,30))
        calc_fps()
        calc_fps2()
        draw_overlay()





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

        if VIDEO:
            draw_video(VIDEO)

        if options.countdown:
            draw_counter(COUNTER)

        pointer.draw(0,pm_wy) #wy
        spos = [0,0,0,0]
        if PIXEL_MAPPING >= 1:
            reshape(0,0) #start pos
        else:
            reshape(spos[0]+spos[2]+20,10) #start pos
            #reshape(spos[0]+spos[2]+20,10) #start pos


        frame_area()


        pygame.display.flip()
        #pg.time.wait(55)
        #clock.tick(120) # fast hight cpu

        clock.tick(25)
        #time.sleep(1/120)

        if 'SDL_VIDEO_WINDOW_POS' in os.environ:
            del os.environ['SDL_VIDEO_WINDOW_POS'] #= '%i,%i' % (200,164)
        #if 'SDL_VIDEO_CENTERED' in os.environ['SDL_VIDEO_CENTERED']:
        #    del os.environ['SDL_VIDEO_CENTERED'] #= '0'
        frame2 += 1

if __name__ == "__main__":
    main()
