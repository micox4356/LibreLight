#!/usr/bin/env python3
import cv2
import pygame
import time

class Vopen():
    def __init__(self):
        self.fname = '/home/user/Downloads/video.mp4'
        self.fname = '/home/user/Downloads/video.ogv'
        self.fname = '/home/user/Downloads/bbb_sunflower_480x320.mp4'
        self.x = 0
        self.y = 0
        self.im = None
        self.init()

    def init(self):
        print(self,"init()")
        cap = cv2.VideoCapture(self.fname)
        self.cap = cap
        self.success, self.img = self.cap.read()
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        except:pass
        self.shape = self.img.shape[1::-1]

    def read(self):
        print(self,"read()")
        self.success, self.img = self.cap.read()
        print(self.success)
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("exception 432",e)

    def next(self):
        print(self,"play",time.time())
        self.read()
        try:
            self.im = pygame.image.frombuffer(self.img.tobytes(), self.shape, "RGB")
            # wn.blit(im, (self.x, self.y))
        except AttributeError as e:
            print("except",e)
            time.sleep(1)
            self.init()
            self.success,self.shape = v.init()

    def draw(self,wn):
        if self.success:
            wn.blit(self.im, (self.x, self.y))

v = Vopen()
#success,shape = v.init()
shape = [300,300]
if v.shape:
    shape  = v.shape

wn = pygame.display.set_mode(v.shape,pygame.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#wn = pygame.display.set_mode(shape)
window = wn
clock = pygame.time.Clock()

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

while v.success and success:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
    
    if max_frame < 300:
        v.next()
        max_frame+=1
    #print(i)
    v.draw(wn) #,x=0,y=0)

    sub = grab()
    window.blit(sub, (500,10))
    pygame.display.update()
    clock.tick(60)

 
pygame.quit()
