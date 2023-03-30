#!/usr/bin/env python3
import cv2
import pygame
import time
import os

class Vopen():
    def __init__(self):
        self.fname = '/home/user/Downloads/video.mp4'
        self.fname = '/home/user/Downloads/video.ogv'
        self.fname = '/home/user/Downloads/bbb_sunflower_480x320.mp4'
        self.x = 0
        self.y = 0
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
        cap = cv2.VideoCapture(self.fname)

        self.cap = cap
        self.success, self.img = self.cap.read()
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            #self.buffer.append(self.img)
            self.pos = 0
        except:pass
        self.shape = self.img.shape[1::-1]

    def read(self):
        #print(self,"read()")
        self.success, self.img = self.cap.read()
        #print(self.success)
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("exception 432",e)
    def prev(self):
        self.pos -= 1
        if self.pos < 0:
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
        if self.success and wn: # is not None:
            wn.blit(self.im, (self.x, self.y))

v = Vopen()

shape = [300,300]
if v.shape:
    shape  = v.shape

wn = pygame.display.set_mode(v.shape,pygame.RESIZABLE)
window = wn
clock = pygame.time.Clock()
pygame.display.set_caption('LibreLight VIDEO PLAYER (BOUNCE-LOOP)')

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

max_frame=0
success=1

loop = 1
run = 1
while v.success and success:
    
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

    
    if run:
        if loop:
            if max_frame < 100:
                v.next()
                max_frame+=1
            else:
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

        sub = grab()
        wn.blit(sub, (500,10))
        pygame.display.update()
    clock.tick(420)
    #clock.tick(60)

 
pygame.quit()
