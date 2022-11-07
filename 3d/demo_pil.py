import PIL
import PIL.Image
import PIL.ImageFilter

import os
import time


import pygame
pg = pygame

pygame.init()

w = 1600 
w = 600 
h = int(600/16*9) # 16:9
main_size=(w,h)
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight PIL')
#pg.transform.smoothscale(window,(100,100))


class IMG():
    def __init__(self,w=300,h=200,color=[255,0,0]):
        self.w = w
        self.h = h
        self.color = color
        self.img = PIL.Image.new("RGBA", (w, h))
        self.pixels = [(color[0],color[1],color[2],100)]*(w*h)
        self.img.putdata(self.pixels)
        self._blur_dir = 1
        self._blur = 5
    def reset(self):
        self.pixels = [(self.color[0],self.color[1],self.color[2],100)]*(self.w*self.h)
    def draw(self,x=10,y=10,b=10,h=10,color=(255,255,255,255)):
            
        _len = len(self.pixels)

        for i in range(b):
            _x = (i+x)* (self.w )
            if _x < _len:
                pass#print(self.pixels[_x])
            for j in range(h):
                _y = j +y
                idx = _x+_y
                if idx < _len:
                    self.pixels[idx] = color #(255,255,255)

    
    def get(self):
        self.img.putdata(self.pixels)
        #self.img = self.img.resize((300, 200), PIL.Image.ANTIALIAS)
        #self.img = self.img.filter(PIL.ImageFilter.BLUR)
        if self._blur_dir:
            self._blur += .1
        else:
            self._blur -= .1
        if self._blur > 6:
            self._blur_dir = 0
        elif self._blur < 0:
            self._blur_dir = 1

        #self.img = self.img.filter(PIL.ImageFilter.GaussianBlur(self._blur))
        self.img = self.img.filter(PIL.ImageFilter.GaussianBlur(4))
        #print( dir(self.img)) #.getpixel((1,1)) )
        t = self.img.tobytes() 
        #print( t[:20] ) 
        tt = bytearray(t)
        for i in range(100):
             tt[i+600] = 255 #).to_bytes(1,byteorder='big')
        t = bytes(tt)
        s = self.img.size
        m = self.img.mode

        img = PIL.Image.frombytes(m ,s ,t) #t,s,m) #s,tb) 
        #img = PIL.Image.frombytes(m ,s ,t) #t,s,m) #s,tb) 
        #img = img.resize((main_size[0], main_size[1]))

        #print( self.img.getpixel((1,1)) )
        t = img.tobytes()
        s = img.size
        m = img.mode

        out = pygame.image.fromstring( t,s,m).convert()
        return out



run = True
x = 10
x_dir = 1

#img = IMG(w=300,h=168)
img = IMG(w=600,h=337)
#img = IMG(w=500,h=281)
#img = IMG(w=1900,h=800)

start_fps = time.time()
fps_c = 0
fps = 0
while run:
    #pg.clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pg.transform.smoothscale(window,(600,600))
    window.fill(0)

    
    #img = IMG(w=400,h=300)
    #img = IMG(w=1900,h=800)
    img.reset()
    img.draw()
    img.draw(x=30,y=30, color=(0,0,0))
    img.draw(x=x,y=x)#50)
    pygameSurface = img.get()
    pygameSurface = pygame.transform.scale(pygameSurface,[main_size[0]-10,main_size[1]-10])

    #player_rect = img.get_rect(center=(200, 200))
    #window.blit(pygameSurface, pygameSurface.get_rect(center = (150, 150)))
    window.blit(pygameSurface, pygameSurface.get_rect(topleft= (5, 5)))
    pygame.display.flip()
    #pg.transform.smoothscale(window,(100,200))
    pg.time.wait(10)
    

    print(fps,x_dir,x)
    if x_dir:
        x+=1
        if x > 200:
            x_dir = 0
    else:
        x-=1
        if x <= 0:
            x_dir = 1

    if start_fps+1 < time.time():
        start_fps = time.time()
        fps = fps_c
        fps_c = 0
    fps_c += 1





exit()

