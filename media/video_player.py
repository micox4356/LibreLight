#!/usr/bin/env python3

#import cv2
import pygame
import pygame.font
import time
import os

pygame.init() 

class Vopen():
    def __init__(self):
        self.fname = '/home/user/Downloads/video.mp4'
        self.fname = '/home/user/Downloads/video.ogv'
        self.fname = '/home/user/Downloads/bbb_sunflower_480x320.mp4'
        self.x = 0
        self.y = 0
        self.cap = None
        self.shape = [200,200]  
        self.success = 1
        self.cv2 = None
        try:
            self.cv2 = cv2
        except:
            pass

        self.im = None
        self.pos = 0
        self.buffer = []
        self.init()

    def init(self):
        print(self,"init()",self.fname)
        if not os.path.isfile(self.fname):
            print()
            print("video file does not exits !! >",self.fname)
            print()
            exit()
        self.buffer = []

        if self.cv2:
            cap = self.cv2.VideoCapture(self.fname)

            self.cap = cap
            self.success, self.img = self.cap.read()
            try:
                self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
                #self.buffer.append(self.img)
                self.pos = 0
            except:pass
            self.shape = self.img.shape[1::-1]

    def read(self):
        #print(self,"read()")
        #print(self.success)
        try:
            self.success, self.img = self.cap.read()
            self.img = self.cv2.cvtColor(self.img, self.cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("exception 432",e)
    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self.buffer)-1
        if self.pos >= len(self.buffer):
            self.pos = len(self.buffer)-1
        self.im = self.buffer[self.pos]

    def next(self):
        #print(self,"play",time.time())
        #print(dir(self.cap))
        #print(self.cap.set.__doc__)
        #print(self.cap.grab.__doc__)
         
        self.read()
        try:
            self.im = pygame.image.frombuffer(self.img.tobytes(), self.shape, "RGB")
            self.buffer.append(self.im)
            self.pos += 1
            # wn.blit(im, (self.x, self.y))
        except AttributeError as e:
            print("except",e)
            time.sleep(1)
            self.init()

    def draw(self,wn=None):
        if self.success and wn and self.im: # is not None:
            wn.blit(self.im, (self.x, self.y))

    def overlay(self,wn=None,mode="x"):
        # overlay 
        font15 = pygame.font.SysFont("freemonobold",20)
        fr = font15.render(">:{}".format(mode) ,1, (0,0,0))
        wn.blit(fr,(10,10))

        font15 = pygame.font.SysFont("freemonobold",20)
        fr = font15.render("FRAME:{}".format(self.pos) ,1, (0,0,0))
        wn.blit(fr,(110,10))

v = Vopen()

shape = [300,300]
if v.shape:
    shape  = v.shape


wn = pygame.display.set_mode(v.shape,pygame.RESIZABLE)
window = wn
clock = pygame.time.Clock()
pygame.display.set_caption('LibreLight VIDEO PLAYER (BOUNCE-LOOP)')
window.fill((30,30,20))
pygame.display.update()

def grab(x=55,y=55,w=60,h=60):
    # usage
    # sub = grab()
    # window.blit(sub, (500,10))
    rect = pygame.Rect(x, y, w, h)
    sub = window.subsurface(rect)
    #pixArray = pygame.PixelArray(screen)
    crop = pygame.Surface((w,h))
    crop.blit(sub, (0,0))
    return crop


class VideoDemo():
    def __init__(self):
        pass

max_frame=0
success=1

loop = 1
run = 1
while v.success and success:
    
    window.fill((30,30,20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False

        _button = None
        if "button" in event.dict:
             _button =  event.dict["button"]

        if event.type:
            print(_button, event.type,run)

        if _button == 1:
           if event.type == 5:
               print("----")
               if run:
                   run = 0
               else:
                   run = 1

    # error message
    pygame.draw.rect(wn,[255,0,0],[18,48,100,20])
    font15 = pygame.font.SysFont("freemonobold",20)
    fr = font15.render("NO VIDEO" ,1, (0,0,0))
    wn.blit(fr,(20,50))



    d = "PAUSE"
    if run:
        if loop:
            d = "PLAY"
            if max_frame < 100:
                v.next()
                max_frame+=1
            else:
                d = "REVERSE"
                #max_frame = 0
                #v.init()
                v.prev()
                if v.pos <= 0:
                    max_frame = 0
                    v.pos = len(v.buffer)-1

        else:
            v.next()
    #print(i)
    if wn:
        v.draw(wn) #,x=0,y=0)

        # overlay 
        v.overlay(wn,d)

        sub = grab()
        wn.blit(sub, (500,10))
        pygame.display.update()
    clock.tick(420)
    #clock.tick(60)

 
pygame.quit()
