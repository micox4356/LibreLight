import cv2
import pygame
import time

class Vopen():
    def __init__(self):
        cap = cv2.VideoCapture('/home/user/Downloads/video.mp4')
        #cap = cv2.VideoCapture('/home/user/Downloads/video.ogv')
        self.cap = cap
    def init(self):
        success, img = self.cap.read()
        self.shape = img.shape[1::-1]
        return success,self.shape
    def read(self):
        success, img = self.cap.read()
        return success,img

v = Vopen()
success,shape = v.init()

wn = pygame.display.set_mode(shape)
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

while success:
    clock.tick(60)
    success, img = v.read()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
    try:
        wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "RGB"), (0, 0))
        #wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
    except AttributeError as e:
        print("except",e)
        time.sleep(1)
        v = Vopen()
        success,shape = v.init()

    sub = grab()
    window.blit(sub, (500,10))
    pygame.display.update()

 
pygame.quit()
