import cv2
import pygame
import time

class Vopen():
    def __init__(self):
        cap = cv2.VideoCapture('/home/user/Downloads/video.mp4')
        #cap = cv2.VideoCapture('/home/user/Downloads/video.ogv')
        cap = cv2.VideoCapture('/home/user/Downloads/bbb_sunflower_480x320.mp4')
        self.cap = cap
    def init(self):
        success, img = self.cap.read()
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:pass
        self.shape = img.shape[1::-1]
        #print( img.shape[0:10] )
        return success,self.shape
    def read(self):
        success, img = self.cap.read()
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            pass
        #cv2.CvtColor(img, im, cv.CV_BGR2RGB)
        #print( img.shape[0:10] )
        #print( self.shape )
        return success,img

v = Vopen()
success,shape = v.init()

wn = pygame.display.set_mode(shape,pygame.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
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

while success:
    clock.tick(60)
    success, img = v.read()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
    try:
        im = pygame.image.frombuffer(img.tobytes(), shape, "RGB")
        #im = pygame.image.frombuffer(img.tobytes(), shape, "BGR")
        wn.blit(im, (0, 0))
    except AttributeError as e:
        print("except",e)
        time.sleep(1)
        v = Vopen()
        success,shape = v.init()

    sub = grab()
    window.blit(sub, (500,10))
    pygame.display.update()

 
pygame.quit()
