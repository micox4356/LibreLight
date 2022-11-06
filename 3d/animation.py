import pygame
pg = pygame
pygame.init()
#window = pygame.display.set_mode((600, 300))#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
window = pygame.display.set_mode((600, 300),pg.RESIZABLE,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode((600, 300),pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode((1600, 900),pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode((600, 300),pygame.FULLSCREEN) #x left->right ,y top-> bottom
# pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))) ,pygame.FULLSCREEN)
pg.display.set_caption('LibreLight Animation')

def event_read():

    inc = 1

    for event in pg.event.get():
        print("event",event)
        move_x = 0
        move_y = 0
        move_z = 0

        rot_x = 0
        rot_y = 0
        rot_z = 0
        if event.type== pg.QUIT:
            print("quit")
            pg.quit()
            quit()
            sys.exit()
        if "key" in dir(event):
            if event.key == 27: #ESC pg.KEYDOWN:
                print("quit")
                pg.quit()
                quit()
                sys.exit()


class Grid():
    def __init__(self):

        pixA = []

        for c in range(10):
            row = []
            for r in range(10):
                color = [r,r,r]
                row.append(color)
            pixA.append(row)
        self.pixA = pixA

        self.red = 0
        self.green = 0
        self.blue = 0
        self.blue_dir = 1
    def draw(self):
        pixA = self.pixA
        pixel_array = pygame.PixelArray(window)
        #pixel_array.open()

        a_x_max = len(pixel_array[0])
        a_y_max = len(pixel_array)
        
        b_x_max = len(pixA[0])
        b_y_max = len(pixA)
    
        b_h =  int(a_x_max / b_x_max)
        b_w =  int(a_y_max / b_y_max)
        self.red = 0
        self.green = 0
        #blue = 255
        for r,row in enumerate(pixA):
            self.red += 30
            if self.red > 255:
                self.red = 255
            self.green = 0

            if self.blue > 255:
                self.blue = 255
                self.blue_dir = 0
            if self.blue <= 0:
                self.blue = 0
                self.blue_dir = 1
            for c,col in enumerate(row):
                self.green += 30
                if self.green > 255:
                    self.green = 255
                color = pygame.Color(self.red,self.green,self.blue)
                #print("x:{:3} y:{:3} {:3} {:3} c:{}".format(x,y,x+bc,y+br,color))
                x = r*b_w
                y = c*b_h
                #pixel_array[r*b_w][c*b_h] = color 
                pixel_array[x:x+b_w-1,y:y+b_h-1] = color 




        pixel_array.close()
        #one = 0
        
        if self.blue_dir:
            self.blue += 2
        else:
            self.blue -= 2

class Gobo1():
    def __init__(self,x=20,y=20):
        self.pos_x = 10 
        self.pos_x_dir = 1 
        self.pos_y = 30
        self.pos_y_dir = 1 
        self.r = 7
        self.r_dir = 1
        self.pos_x=x
        self.pos_y=y
    def draw(self,color=[255,255,255]):

        #pixel_array = pygame.PixelArray(window)
        pixel_array = {}
        self.color = pygame.Color(color[0],color[1],color[2])
        
        x=self.pos_x
        y=self.pos_y

        x-=self.r
        y-=self.r
        pixel_array[x:x+10,y:y+10] = self.color 
        x+=self.r*2
        pixel_array[x:x+10,y:y+10] = self.color 
        y+=self.r*2
        x-=self.r
        pixel_array[x:x+10,y:y+10] = self.color 
        pixel_array.close()

        if self.pos_x > 300:
            self.pos_x_dir = 0
        if self.pos_x <= 10:
            self.pos_x_dir = 1

        if self.pos_x_dir:
            self.pos_x += 1
        else:
            self.pos_x -= 1

        if self.r > 20:
            self.r_dir = 0
        if self.r <=7:
            self.r_dir = 1

        if self.r_dir:
            self.r+=1
        else:
            self.r-=1

run = True
one = 1
blue = 0
blue_dir = 1
pos_x_dir = 1
#pixel_array = pygame.PixelArray(window)
import time
time.sleep(1)
grid = Grid()
gobo1 = Gobo1()
gobo2 = Gobo1(20,150)

while run:
    event_read()
    if one:
        window.fill(0)
        grid.draw()
        rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
        pygame.display.flip()

        #gobo1.draw()#20,10)
        #pygame.display.flip()
        #gobo2.draw(color=[255,0,0])
        #pygame.display.flip()
        
    pygame.display.flip()
    pg.time.wait(10)

pygame.quit()
exit()
