import pyglet
import math
from pyglet import shapes
import random
import time






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
        r = round(r)

        #img3 = img2.copy()
        #img3 = colorize(img2, color ) #(0, 0, 255,15) )
        #img3 = colorize(img2,(255, 120, 255,15) )
        #img3 = colorize(img2,color )
        #img3 = pygame.transform.scale(img3, (r, r))
        #player_rect3 = img3.get_rect(center=(x,y))
        #window.blit(img3, player_rect3)
        if r > 0:
            batch1 = pyglet.graphics.Batch()
            circle = shapes.Circle(x,y, r+5, color=(50, 225, 30), batch=batch1)

            batch1.draw()
        #print("ok")    
        return [x,0,y,0,color]

class Particales():
    def __init__(self):
        self.data = []
    def add(self,x,y):
        for z in range(random.randint(1,1)):
            s = 10
            xvel = random.randint(0,s) -(s/2)
            yvel = random.randint(0,s) -(s/2) 
            r = random.randint(1,2)
            p = _Particale(x ,y ,xvel ,yvel,r,(255,255,255))
            self.data.append(p)

    def draw(self,win=None):
        rem = []
        for p in self.data:
            p.draw(win)
            if p.radius <= 0:
                rem.append(p)

        for p in rem:
            self.data.remove(p)

particales = Particales()

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
        self.color = [255,255,255,255] #pygame.Color(color[0],color[1],color[2],color[3])
        
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
    def __init__(self,x=20,y=20,speed=1,_dir=1):
        self.pos_x=x
        self.pos_x_dir = 1 
        self.pos_y=y
        self.pos_y_dir = 1 
        self.r = 17
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
        self.color = [255,255,255,255] #pygame.Color(color[0],color[1],color[2])
        
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





def display_get_width():
    display = pyglet.canvas.get_display()
    screen = display.get_default_screen()
    return screen.width

def display_get_height():
    display = pyglet.canvas.get_display()
    screen = display.get_default_screen()
    return screen.height



sw = display_get_width()
sh = display_get_height()
print(sw, sh)

window = pyglet.window.Window(sw//2,sh//2)
gobo1 = Gobo1()



def loop(event=None):
    #print(event)
    batch = pyglet.graphics.Batch()
    x = 100
    y = 100
    rectangle = shapes.BorderedRectangle(x, y, y+100, y+100, border=1, color=(255, 255, 255), border_color=(100, 100, 100), batch=batch)
    rectangle2 = shapes.BorderedRectangle(x, y , x+100,y+100, border=1, color=(255, 255, 255), border_color=(100, 100, 100), batch=batch)
    circle = shapes.Circle(x,y, 100, color=(50, 225, 30), batch=batch)


    window.clear()
    batch.draw()

    batch1 = pyglet.graphics.Batch()
    d1 = gobo1.draw()
    for k in d1:
        i = d1[k]
        #print("i",i)
        x=i[0] +200
        y=i[2] +200
        circle = shapes.Circle(x,y, 10, color=(50, 225, 30), batch=batch1)
           
        particales.add(x,y)
    batch1.draw()
    particales.draw()
    #print("ok")    


@window.event
def on_draw():
    loop()

pyglet.clock.schedule_interval(loop, 0.001)


pyglet.app.run()
