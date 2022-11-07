import PIL
import PIL.Image

import os
import time


#def SCREEN():
img = PIL.Image.new("RGB", (200, 200))
img.show() # see a black image
pixels = [(255,0,0)]*(200*200)

for i in range(10):
    x = (i+20)* (200 )
    print(pixels[x])
    for j in range(10):
        y = j +10
        pixels[x+y] = (255,255,255)

img.putdata(pixels)

#print( img)
#image = img

#mode = image.mode
#size = image.size
#data = image.tostring()

#img.show() # see a red image
#input()


import pygame

pg = pygame
pygame.init()

main_size=(600,300)
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight PIL')


this_image = img #pygame.image.fromstring(data, size, mode)


img2 = pygame.image.load(os.path.join( 'brush.png'))
img2 = pygame.transform.scale(img2, (25, 25))
img2.set_colorkey([0,0,0] ) #pygame.image.BLACK)
player_rect2 = img2.get_rect(center=(20, 20))
#window.blit(img2, player_rect2)

#window.blit(img, player_rect2)

    #window.blit(img2, player_rect2)

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

pygameSurface = pilImageToSurface(img)

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


run = 1
while run:
    #event_read()
    window.fill(0) #[255,0,0])



    pygame.display.flip()
    pg.time.wait(10)

pygame.quit()
exit()
