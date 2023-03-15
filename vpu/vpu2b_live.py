
# ===== GUI =========
import pygame
import pygame.gfxdraw
import pygame.font
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,164)
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
#font = pygame.font.SysFont(None,30)

fr = font.render("hallo" ,1, (200,0,255))


main_size= [400,400]
window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
pg.display.set_caption('LibreLight LED-SCREEN')



mouse = {"pos":(0,0)}
def pointer():#xxxevent=None):
    global mouse
    event = mouse # = None
    if not event:
        return
    if "pos" in event:#:.dict:
        print("pointer",event)

        rgb = [0,0,200,200]
        x = event["pos"][0]
        y = event["pos"][1]
        p = 100
        
        print(window,rgb,event["pos"])
        pygame.draw.rect(window,rgb,(x-5,y-5,10,10))
        #pygame.draw.line(window,self.rgb, (self.pos[0],self.pos[1]) , (self.pos[0]+100,self.pos[1]) ) 

        # mouse grid posision
        fr = font15.render("{}/{}".format(x,y) ,1, (200,200,200))
        window.blit(fr,(200,25))

        # crosshair
        pygame.draw.line(window,rgb, (x-p,y) , (x-2,y) ) 
        pygame.draw.line(window,rgb, (x,y-p) , (x,y-2) ) 

        rgb = [0,200,0]
        pygame.draw.line(window,rgb, (x+2,y) , (x+p,y) ) 
        pygame.draw.line(window,rgb, (x,y+2) , (x,y+p) ) 



def draw_circle(surface,color, pos, radius):
    x,y=pos
    pygame.gfxdraw.aacircle(surface, int(x), int(y), radius-1, color)
    pygame.gfxdraw.filled_circle(surface, int(x), int(y), radius-1, color)


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

def event():
    #global NR,running
    global mouse
    for event in pygame.event.get(): 
        print(event.dict)
        if "pos" in event.dict:
            mouse = event.dict
i = 0
while 1:
    event()
    window.fill((20,20,20))

    pygame.draw.rect(window,[100,0,0,127],[10,10,10,10])

    fr = font15.render("{:02}".format(i) ,1, (100,100,255,255))
    window.blit(fr,(40,30))

    
    rgb = [255,255,255]

    pygame.draw.line(window,rgb, (0,255) , (400,255) ) 
    pointer() #event)

    sub = grab(x=0,y=0)
    window.blit(sub, (200,10))



    pygame.display.flip()
    pg.time.wait(30)

    pygame.display.flip()


    i += 1
