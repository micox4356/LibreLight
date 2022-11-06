

import pygame
import pygame.gfxdraw
import math
import random

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
        #pixel_array = pygame.PixelArray(window)
        pixel_array = {} # pygame.PixelArray(window)
        #pixel_array.open()

        a_x_max = 600 #pixel_array[0])
        a_y_max = 300 #pixel_array)
        
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
                #pixel_array[x:x+b_w-1,y:y+b_h-1] = color 
                k = "{}:{},{}:{} {}".format(x,x+b_w-1,y,y+b_h-1,color) #x,x+10,y,y+10)
                pixel_array[k] = (x,x+b_w-1,y,y+b_h-1,color)




        #pixel_array.close()
        #one = 0
        
        if self.blue_dir:
            self.blue += 10
        else:
            self.blue -= 10
        return pixel_array

class Planet():
    def __init__(self,x,y,ang=0):
        self._pos_center = (x,y)
        self._quadrant = 0
        if ang > 90:
            self._quadrant = ang//90
            ang -= self._quadrant * 90
            
        self._ang = ang 
        self._ang_dir = 1 
        self._r  = 10 # 
        self._orbit = 30 # orbit,umlaufbahn 
        self._color = [255,255,0]
        self._x=0
        self._y=0
        self._ix = 0
        self._iy = 0 

    def rotate(self):
        q = 0
        if self._ang_dir: 
            self._ang += 5 # degree
            if self._ang > 90:
                self._ang = 0
                self._quadrant += 1
            #    q = 1
            #if self._ang < 0:
            #    self._ang = 0
            #    q = 1
        else:
            self._ang -= 1 # degree

        if q:
            r1 = random.randint(0,255)
            r2 = random.randint(0,255)
            self._color = [255,r1,r2]
        
        self._ix = math.sin(math.radians(self._ang))*self._orbit
        #self._ix = math.sin(self._ang)*self._orbit
        #self._ix = math.sin(math.degrees(self._ang))*self._orbit
        self._iy = math.sqrt(self._orbit**2 - self._ix**2) 
    
        y = self._iy 
        x = self._ix 
        if self._quadrant == 1:
            self._iy = -x
            self._ix = y
        elif self._quadrant == 2:
            self._iy = -y
            self._ix = -x
        elif self._quadrant == 3:
            self._iy = x
            self._ix = -y
        else: 
            self._quadrant = 0


    def draw(self,x,y):
        self._pos_center = (x,y)
        self.rotate()
        self._x = int(self._pos_center[0] + self._ix)
        self._y = int(self._pos_center[1] + self._iy)
        print("ang {} {} {:3} {:3} {}".format( self._ang,self._quadrant,self._x,self._y,self._color))
        return (self._x,self._y,self._color)


class Gobo1():
    def __init__(self,x=20,y=20,speed=1):
        self.pos_x=x
        self.pos_x_dir = 1 
        self.pos_y=y
        self.pos_y_dir = 1 
        self.r = 7
        self.r_dir = 1
        self.speed = speed
        self.ang = 0
        self.ix=0
        self.iy=0
        self.planetes = []
        p = Planet(self.pos_x,self.pos_y,ang=10) 
        self.planetes.append(p)
        p = Planet(self.pos_x,self.pos_y,ang=240) 
        self.planetes.append(p)
        p = Planet(self.pos_x,self.pos_y,ang=120) 
        self.planetes.append(p)
    def rotate(self):
        self.ix = math.sin(math.radians(0))*self.r
        self.iy = math.sqrt(self.r**2 - self.ix**2) 
        self.ang+=1
        if self.ang >= 360:
            self.ang = 0
        
    def draw(self,color=[255,255,255]):
        self.rotate()
        #pixel_array = pygame.PixelArray(window)
        pixel_array = {}
        self.color = pygame.Color(color[0],color[1],color[2])
        
        x=self.pos_x
        y=self.pos_y
        for i,planet in enumerate(self.planetes):
            px,py,pcolor = planet.draw(x,y)
            k = "{}.{}:{},{}:{}".format(i,px,px+10,py,py+10)
            pixel_array[k] = (px,px,py,py , pcolor )


        if self.pos_x > 300:
            self.pos_x_dir = 0
        if self.pos_x <= self.speed:
            self.pos_x_dir = 1

        if self.pos_x_dir:
            self.pos_x += self.speed
        else:
            self.pos_x -= self.speed

        if self.r > 20:
            self.r_dir = 0
        if self.r <=7:
            self.r_dir = 1

        if self.r_dir:
            self.r+=1
        else:
            self.r-=1
        return pixel_array

run = True
one = 1
blue = 0
blue_dir = 1
pos_x_dir = 1
#pixel_array = pygame.PixelArray(window)
import time
#time.sleep(1)
grid = Grid()
gobo1 = Gobo1(speed=5)
gobo2 = Gobo1(200,150,speed=2)

while run:
    event_read()
    if one:
        window.fill(0)
        d=grid.draw()
        d1=gobo1.draw()#20,10)
        d2=gobo2.draw()#20,10)
        pixel_array = pygame.PixelArray(window)

        for k in d:
            i = d[k]
            #rect = pygame.draw.circle(window,i[4] , (i[0]+10,i[2]) ,10) 
            #rect = pygame.gfxdraw.aacircle(window, i[0]+10,i[2] ,10,i[4])

        #rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
        #pygame.display.flip()

        for k in d1:
            i = d1[k]
            #print( k,"i",i)
            #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
            rect = pygame.draw.circle(window,i[4] , (i[0]+10,i[2]) ,10) 
            rect = pygame.gfxdraw.aacircle(window, i[0]+10,i[2] ,10,i[4])

        for k in d2:
            i = d2[k]
            #print( k,"i",i)
            #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
            rect = pygame.draw.circle(window,i[4] , (i[0]+10,i[2]) ,10) 
            rect = pygame.gfxdraw.aacircle(window, i[0]+10,i[2] ,10,i[4])

        pixel_array.close()
        #pygame.display.flip()
        #gobo2.draw(color=[255,0,0])
        #pygame.display.flip()
        
    pg.time.wait(10)
    pygame.display.flip()
    pg.time.wait(10)

pygame.quit()
exit()
