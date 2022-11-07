import PIL
import PIL.Image

import os
import time


import pygame
pg = pygame



class IMG():
    def __init__(self,w=300,h=200,color=[255,0,0]):
        self.w = w
        self.h = h
        img = PIL.Image.new("RGB", (w, h))
        pixels = (color[0],color[1],color[2])*(w*h)
        img.putdata(pixels)

    def draw(self,x=10,y=10,b=10,w=10):
        img = PIL.Image.new("RGB", (200, 200))
    
        #img.show() # see a black image
        pixels = [(255,0,0)]*(200*200)

        for i in range(10):
            x = (i+20)* (200 )
            print(pixels[x])
            for j in range(10):
                y = j +10
                pixels[x+y] = (255,255,255)

        img.putdata(pixels)
        self.img = img
    
    def get(self):
        t = self.img.tobytes()
        s = self.img.size
        m = self.img.mode
        out = pygame.image.fromstring( t,s,m).convert()
        return out


img = IMG()
pygame.init()

main_size=(600,300)
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight PIL')

img.draw()
pygameSurface = img.get()

run = True
while run:
    #pg.clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(0)
    window.blit(pygameSurface, pygameSurface.get_rect(center = (150, 150)))
    pygame.display.flip()

exit()

