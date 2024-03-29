

import pygame
import pygame.gfxdraw
import math
import random

import os 

pg = pygame
pygame.init()

main_size=(600,300)
#main_size=(1600,900)
#, pygame.DOUBLEBUF, 32)
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.RESIZABLE|pygame.DOUBLEBUF,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
##window = pygame.display.set_mode(main_size,pg.RESIZABLE)#,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.RESIZABLE, pygame.SRCALPHA)# 32)
window = pygame.display.set_mode(main_size,pg.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE, 32)

#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pg.NOFRAME,32)#,pygame.FULLSCREEN) #x left->right ,y top-> bottom
#window = pygame.display.set_mode(main_size,pygame.FULLSCREEN) #x left->right ,y top-> bottom
# pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))) ,pygame.FULLSCREEN)
#pg.display.set_mode(window,pg.DOUBLEBUF) #|pg.OPENGL)
pg.display.set_caption('LibreLight Animation')


def colorize(image, newColor):
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(newColor[0:4] , None, pygame.BLEND_RGBA_ADD)
    return image

img2 = pygame.image.load(os.path.join( 'brush.png'))
img2 = pygame.transform.scale(img2, (25, 25))
img2.set_colorkey([0,0,0] ) #pygame.image.BLACK)
#player_rect2 = img2.get_rect(center=(200, 200))
#window.blit(img2, player_rect2)

def draw_alpha():
    surface1 = pygame.Surface((100,100))
    surface1.set_colorkey((0,0,0))
    surface1.set_alpha(128)
    pygame.draw.circle(surface1, (0,255,0), (50,50), 50)


class _Particale():
    def __init__(self,x,y,xvel,yvel,radius,color):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.radius = radius
        self.color = color
        self.time = time.time()
        self.start = time.time()
        self.start2 = random.randint(1,20)/10.
        if self.start2 > 1.8:
            self.start2 += random.randint(1,20)/10.
        self.colors = [(255,255,0),(255,210,0),(255,90,0)]
        self.color = random.choice(self.colors)
    def draw(self,win):
        if time.time() > self.time+0.05:
            self.x += self.xvel
            self.y += self.yvel
            self.time = time.time()
        if self.start+self.start2 < time.time():
            self.radius -= 0.1
        #if time.time() > self.time+0.2:
        #pygame.draw.circle(win, color, (int(self.x),int(self.y)),self.radius)
        color = self.color
        x= round(self.x)
        y= round(self.y)
        r = round(self.radius)
        if len(color) == 3:
            color = list(color)
            color.append(0)
        #pygame.gfxdraw.filled_circle(win, x,y ,r,color )#[0,0,255])
        #pygame.gfxdraw.aacircle(win, x,y ,r,color )#[0,0,255])
        r = round(r*5)

        #img3 = img2.copy()
        #img3 = colorize(img2, color ) #(0, 0, 255,15) )
        #img3 = colorize(img2,(255, 120, 255,15) )
        img3 = colorize(img2,color )
        img3 = pygame.transform.scale(img3, (r, r))
        player_rect3 = img3.get_rect(center=(x,y))
        window.blit(img3, player_rect3)

class Particales():
    def __init__(self):
        self.data = []
    def add(self,x,y):
        for z in range(random.randint(1,3)):
            s = 10
            xvel = random.randint(0,s) -(s/2)
            yvel = random.randint(0,s) -(s/2) 
            r = random.randint(1,2)
            p = _Particale(x ,y ,xvel ,yvel,r,(255,255,255))
            self.data.append(p)

    def draw(self,win):
        rem = []
        for p in self.data:
            p.draw(win)
            if p.radius <= 0:
                rem.append(p)

        for p in rem:
            self.data.remove(p)

particales = Particales()

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
        if "pos" in event.dict:
            _pos  = event.pos 
            pointer.move(x=_pos[0],y=_pos[1])
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

        a_x_max = main_size[1] #n600 #pixel_array[0])
        a_y_max = main_size[0] #300 #pixel_array)
        
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

class Flow():
    def __init__(self,x,y,ang=0):
        self._pos_center = (x,y)
        self._quadrant = 0
            
        self._ang = ang 
        self._ang_dir = 1 
        self._r  = 2 # 
        self._orbit = 100 # orbit,umlaufbahn 
        self._color_org = [255,255,0]
        self._color = [0,0,255,255]
        self._x=0
        self._y=0
        self._ix = 0
        self._iy = 0 

    def rotate(self):
        q = 0

        if self._ang_dir: 
            self._ang += 0.5 # degree
        else:
            self._ang -= 1 # degree

        if self._ang >= 360:
            self._ang = 0 #self._ang -360
        elif self._ang < 0:
            self._ang = 360

        
        self._ix = 0 # math.sin(math.radians(ang))*self._orbit
        self._iy = int(self._orbit *2 * (self._ang /360)) # math.sqrt(self._orbit**2 - self._ix**2) 
    


    def draw(self,x,y):
        self._pos_center = (x,y)
        self.rotate()
        self._x = int(self._pos_center[0] + self._ix)
        self._y = int(self._pos_center[1] + self._iy)
        f=1
        if self._ang > 300:
             f = (self._ang -300) / 60
             f = 1-f
             rgb = self._color_org # = [255,255,0]
             #self._color = [ int(rgb[0]*f) , int(rgb[1]*f) ,int(rgb[2]*f) ,0]
        elif self._ang < 60:
             f = self._ang / 60
             rgb = self._color_org # = [255,255,0]
             #self._color = [ int(rgb[0]*f) , int(rgb[1]*f) ,int(rgb[2]*f) ,0 ]
        self._color[3] =  int(f*255)
        #print(self._color)
        #print("ang {} {} {:3} {:3} {}".format( self._ang,self._quadrant,self._x,self._y,self._color))
        #print(self._ang,f)
        #print(self,"Q:",int(self._quadrant),self._ang)
        return (self._x,self._y,self._color)


class Planet():
    def __init__(self,x,y,ang=0):
        self._pos_center = (x,y)
        self._quadrant = 0
            
        self._ang = ang 
        self._ang_dir = 1 
        self._r  = 2 # 
        self._orbit = 60 # orbit,umlaufbahn 
        self._color_org = [255,255,0]
        self._color = [0,255,0]
        self._x=0
        self._y=0
        self._ix = 0
        self._iy = 0 

    def rotate(self):
        q = 0

        if self._ang_dir: 
            self._ang += 2 # degree
        else:
            self._ang -= 1 # degree

        if self._ang >= 360:
            self._ang = 0 #self._ang -360
        elif self._ang < 0:
            self._ang = 360

        ang = self._ang
        self._quadrant = ang//90
        ang -= self._quadrant * 90
        
        
        self._ix = math.sin(math.radians(ang))*self._orbit
        self._iy = math.sqrt(self._orbit**2 - self._ix**2) 
    
        y = self._iy 
        x = self._ix 
        if   self._quadrant == 1:
            self._iy = -x
            self._ix = y
        elif self._quadrant == 2:
            self._iy = -y
            self._ix = -x
        elif self._quadrant == 3:
            self._iy = x
            self._ix = -y


    def draw(self,x,y):
        self._pos_center = (x,y)
        self.rotate()
        self._x = int(self._pos_center[0] + self._ix)
        self._y = int(self._pos_center[1] + self._iy)
        if self._ang > 300:
             f = (self._ang -300) / 60
             f = 1-f
             rgb = self._color_org # = [255,255,0]
             self._color = [ int(rgb[0]*f) , int(rgb[1]*f) ,int(rgb[2]*f) ]
        elif self._ang < 60:
             f = self._ang / 60
             rgb = self._color_org # = [255,255,0]
             self._color = [ int(rgb[0]*f) , int(rgb[1]*f) ,int(rgb[2]*f) ]
        #print("ang {} {} {:3} {:3} {}".format( self._ang,self._quadrant,self._x,self._y,self._color))
        #print(self,"Q:",int(self._quadrant),self._ang)
        return (self._x,self._y,self._color)


class Animation():
    def __init__(self,x=20,y=20,speed=1,_dir=1):
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
        a = 360
        d = 3
        for i in range(d+1):
            i=i+1
            p = Flow(self.pos_x,self.pos_y,ang=a/d*i) 
            p._ang_dir = _dir 
            self.planetes.append(p)

    def rotate(self):
        self.ix = math.sin(math.radians(0))*self.r
        self.iy = math.sqrt(self.r**2 - self.ix**2) 
        self.ang+=1
        if self.ang >= 360:
            self.ang = 0
        
    def draw(self,color=[255,255,255,255]):
        self.rotate()
        #pixel_array = pygame.PixelArray(window)
        pixel_array = {}
        self.color = pygame.Color(color[0],color[1],color[2],color[3])
        
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

class Gobo1():
    def __init__(self,x=20,y=20,speed=1,_dir=1,r=17):
        self.pos_x=x
        self.pos_x_dir = 1 
        self.pos_y=y
        self.pos_y_dir = 1 
        self.r = r
        self.r_dir = 1
        self.speed = speed
        self.ang = 0
        self.ix=0
        self.iy=0
        self.planetes = []
        a = 360
        d = 3
        for i in range(d+1):
            i=i+1
            p = Planet(self.pos_x,self.pos_y,ang=a/d*i) 
            p._ang_dir = _dir 
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


        if self.pos_x > 1600:
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


font15 = pygame.font.SysFont("freemonobold",15)
class POINTER():
    def __init__(self):
        self.pos = [0,0,0,0]
        self.on = 1
        self.rgb = [0,100,10,255]
        self._x = 0
        self._y = 0
        self.x = 0
        self.y = 0

    def move(self,x,y):
        self._x = x
        self._y = y
    def cross(self,x,y):
        self.x = x
        self.y = y

    def draw(self,window,x=0,y=0,alpha=255):
        if self.on:
            self.rgb[-1] = alpha
            #print(self.rgb)
            pos = (self._x-5-10,self._y-5-10,10,10)
            pos = (self._x-5-10+x,self._y-5-10+y,10,10)
            #pygame.gfxdraw.rectangle(window,self.rgb[:3],pos)
            #pygame.gfxdraw.rectangle(window,self.rgb[:3],pos)
            thickLine = pygame.gfxdraw.rectangle(window,pos , self.rgb)
            thickLine = pygame.gfxdraw.rectangle(window,pos , self.rgb)
            #thickLine.fill()
            # mouse grid posision
            fr = font15.render("{}/{}".format(self._x,self._y) ,1, (200,200,200))
            window.blit(fr,(200,25))
            

pointer = POINTER()


def vdim(color,dim):
    color[0] =  int(color[0]/255*dim) 
    color[1] =  int(color[1]/255*dim) 
    color[2] =  int(color[2]/255*dim) 
    return color

run = True
one = 1
blue = 0
blue_dir = 1
pos_x_dir = 1
#pixel_array = pygame.PixelArray(window)
import time
#time.sleep(1)
grid = Grid()
gobo1 = Gobo1(main_size[0],main_size[1]/3,speed=3)
gobo2 = Gobo1(200,150,speed=0,_dir=0,r=5)
gobo3 = Gobo1(main_size[0]/2,main_size[1]/2,speed=0,r=30)
anim1 = Animation(main_size[0]/2,main_size[1]/2,speed=1)

#eg. 
img = pygame.image.load(os.path.join( 'brush.png'))
img = pygame.transform.scale(img, (25, 25))
img.set_colorkey([0,0,0] ) #pygame.image.BLACK)
player_rect = img.get_rect(center=(200, 200))
#window.blit(img, player_rect)

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

_start = time.time()
xbg = [0,0,0]
xbg_dir = 1
def main():
    global _start
    global xbg,xbg_dir
    event_read()
    if one:
        #print(_start+0.1<time.time()) #,end="")
        if 0:#_start+0.1 > time.time():
            #time.sleep(0.01)
            #continue
            return
        #print(_start-time.time(),end="")
        _start = time.time()
        #print(".",end="")
        if xbg_dir > 0 and xbg[0] >= 255:
                xbg_dir = -1
        if xbg_dir < 0 and xbg[0] <= 0:
                xbg_dir = 1

        xbg[0] += xbg_dir

        if 0:
            d=grid.draw()
            d1=gobo1.draw()#20,10)
            d2=gobo2.draw()#20,10)
            d3=gobo3.draw()#20,10)
            a1=anim1.draw()#20,10)
            window.fill(0) #[255,0,0])
            pg.time.wait(10)
            pg.time.wait(10)
            pg.time.wait(10)
            pixel_array = pygame.PixelArray(window)
            vd = 255#80 
            for k in d:
                i = d[k]
                #rect = pygame.draw.circle(window,i[4] , (i[0]+12,i[2]+12) ,10) 
                #rect = pygame.gfxdraw.aacircle(window, i[0]+12,i[2]+12 ,10,i[4])
                #print(i)
                i = list(i)
                i[4] = vdim(i[4],vd)
                rect = pygame.gfxdraw.box(window, (i[0],i[2] ,i[1]-5,i[3]-5) ,i[4])

            #rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
            #pygame.display.flip()

            for k in d1:
                i = d1[k]
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                i = list(i)
                i[4] = vdim(i[4],vd)
                #arect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4])
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,20,i[4] )#[0,0,255])

            for k in d2:
                i = d2[k]
                i = list(i)
                i[4] = vdim(i[4],vd)
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                #rect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,[0,0,255])
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
            for k in d3:
                i = d2[k]
                i = list(i)
                i[4] = vdim(i[4],vd)
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                #rect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,[0,0,255])
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,10,i[4] )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4] )#[0,0,255])

            for k in a1:
                i = a1[k]
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                #print("anim",i)
                i = list(i)
                _v = i[4]
                vd = 200
                #_v = vdim(i[4],vd)
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,10,_v )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4] )#[0,0,255])

                vd = 255
                #_v = vdim(i[4],vd)
                #rect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,20,_v )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,20,i[4] )#[0,0,255])

            #pixel_array.close()
            #pygames.fill([255,0,0,127],(10,10))

        if 1:
            #window.fill(10)
            vd =255
            d1=gobo1.draw()#20,10)
            d2=gobo2.draw()#20,10)
            d3=gobo3.draw()#20,10)
            a1=anim1.draw()#20,10)
            #window.fill(0) #[255,0,0])
            window.fill(xbg)
            pointer.draw(window)
            z = 0
            for k in d1:
                i = d1[k]
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                i = list(i)
                i[4] = vdim(i[4],vd)
                #arect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                ##rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4])
                #rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
                if 0:#z % 33 == 0:
                    particales.add(i[0],i[2])
                    particales.draw(window)
                z+=1
                #pygame.gfxdraw.pixel(window,i[0],i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]+1,i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]+1,i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0],i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2]-1,i[4])
            for k in d2:
                i = d2[k]
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                i = list(i)
                i[4] = vdim(i[4],vd)
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4] )#[0,0,255])
                pygame.gfxdraw.line(window,i[0],i[2]-10,i[0],i[2]+10,(255,0,255))
            for k in d3:
                i = d3[k]
                i = list(i)
                i[4] = vdim(i[4],vd)
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,30,i[4] )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,30,i[4] )#[0,0,255])
                pygame.gfxdraw.box(window,(i[0]-20,i[2]-5,40,10),(255,255,0))
            for k in a1:
                i = a1[k]
                #print( k,"i",i)
                #pixel_array[i[0]:i[1],i[2]:i[3]] = i[4] #(x,x+10,y,y+10 , self.color )
                #print("anim",i)
                i = list(i)
                _v = i[4]
                vd = 200
                #_v = vdim(i[4],vd)
                #rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,10,_v )#[0,0,255])
                #rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,10,i[4] )#[0,0,255])

                vd = 255
                #_v = vdim(i[4],vd)
                #rect = pygame.draw.circle(window,i[4] , (i[0],i[2]) ,10) 
                rect = pygame.gfxdraw.filled_circle(window, i[0],i[2] ,20,_v )#[0,0,255])
                rect = pygame.gfxdraw.aacircle(window, i[0],i[2] ,20,i[4] )#[0,0,255])
                #print(i)
                #particales.add(i[0],i[2])
                #particales.draw(window)


                #pygame.gfxdraw.pixel(window,i[0],i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]+1,i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]+1,i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0],i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2]+1,i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2],i[4])
                #pygame.gfxdraw.pixel(window,i[0]-1,i[2]-1,i[4])
                
                window.blit(img, player_rect)

        #pygame.display.flip()
        #gobo2.draw(color=[255,0,0])
        #pygame.display.flip()
    sub = grab(190,0)
    pygame.gfxdraw.box(window,(430-2,10-2,60+4,60+4),(255,255,200))
    window.blit(sub, (430,10))
        
    sub = grab(190,190)
    pygame.gfxdraw.box(window,(500-2,10-2,60+4,60+4),(255,255,200))
    window.blit(sub, (500,10))

    pointer.draw(window,x=-10,y=-10,alpha=120)
    pg.time.wait(10)
    #pg.time.wait(10)
    pygame.display.update()
    #pygame.display.flip()

try:
    while run:
        main()
except Exception as e:
    print("e",e)
pygame.quit()
exit()
