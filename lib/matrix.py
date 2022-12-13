

def mprint(data,w=4,h=4):
    for i,v in enumerate(data):
        if i % w ==0:
            print()
        print(v,end=",")
    print()
    print("----")

sleep = 0
if __name__ == "__main__":
    sleep = 0.01321

print("y--")
class DIR():
    def __init__(self,w=4,h=4,w_min=0,h_min=0):
        self.d = 0
        self.w= w
        self.h= h

        self.x_max= w
        self.y_max= h

        self.x_min= w_min
        self.y_min= h_min
        self.x = 0 #//2
        self.y = 0 #//2
        self.i = 0
        self.i_max = self.x_max*self.y_max

    def get(self):
        if self.i >= self.i_max:
            return None # end
        out = self.x,self.y*self.w
        self.i += 1
        return out

    def right_reset(self):
        self.x = self.x_min
    def left_reset(self):
        self.x = self.x_max -1
    def down_reset(self):
        self.y = self.y_min
    def up_reset(self):
        self.y = self.y_max -1
    def right(self):
        if self.x < self.x_max-1:
            self.x+=1
            return 1
    def down(self):
        if self.y < self.y_max-1:
            self.y+=1
            return 1
    def up(self):
        if self.y > self.y_min:
            self.y-=1
            return 1
    def left(self):
        if self.x > self.x_min:
            self.x-=1
            return 1

    def x(self):
        return self.out
 
data = [ "1A","1B" ,"1C","1D","2A","2B","2C","2D","3A","3B","3B","3D"]



def right(w,h):
    out = ["----"] *(w*h) #*w*h
    d = DIR(w=w,h=h)
    r = d.get()
    i = 0
    import time
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        #out[x+y] = i 
        out[x+y] = "{:-4}".format(i) 
        if sleep:
            mprint(out,w,h)
        r=d.right()
        #print(r)
        if not r:
            d.right_reset()
            d.down()

        r = d.get()
        i += 1
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 40
    h = 30
    #out = right(w,h)
    #mprint(out,w,h)

def left(w,h):
    #mprint(data,w,h)


    out = ["----"] *(w*h) #a+2
    d = DIR(w=w,h=h)
    #d.up_reset()
    d.left_reset()
    r = d.get()
    i = 0
    import time
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        #out[x+y] = i 
        out[x+y] = "{:-4}".format(i) 
        #mprint(out,w,h)
        if sleep:
            mprint(out,w,h)
        r=d.left()
        #print(r)
        if not r:
            d.left_reset()
            #d.up()
            d.down()

        r = d.get()
        i += 1
        #time.sleep(.0151)
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 40
    h = 30
    #out = left(w,h)
    #mprint(out,w,h)


def up(w,h):
    #mprint(data,w,h)


    out = ["----"] *(w*h) #a+2
    d = DIR(w=w,h=h)
    #d.up_reset()
    d.up_reset()
    r = d.get()
    i = 0
    import time
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        #out[x+y] = i 
        out[x+y] = "{:-4}".format(i) 
        #mprint(out,w,h
        if sleep:
            mprint(out,w,h)
        r=d.up()
        #print(r)
        if not r:
            d.up_reset()
            #d.up()
            d.right()

        r = d.get()
        i += 1
        #time.sleep(.0151)
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 40
    h = 30
    #out = up(w,h)
    #mprint(out,w,h)




def down(w,h):
    #mprint(data,w,h)


    out = ["----"] *(w*h) #a+2
    d = DIR(w=w,h=h)
    #d.up_reset()
    d.down_reset()
    r = d.get()
    i = 0
    import time
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        #out[x+y] = i 
        out[x+y] = "{:-4}".format(i) 
        #mprint(out,w,h)
        if sleep:
            mprint(out,w,h)

        r=d.down()
        #print(r)
        if not r:
            d.down_reset()
            #d.up()
            d.right() #left()

        r = d.get()
        i += 1
        #time.sleep(.0151)
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 40
    h = 30
    #out = down(w,h)
    #mprint(out,w,h)





def spiral(w=10,h=4):
    mprint(data,w,h)


    out = ["----"] *(w*h) #*30 #*w*h+2
    d = DIR(w=w,h=h)
    d.up_reset()
    d.left_reset()
    r = d.get()
    i = 0
    import time
    q = 0
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        out[x+y] = "{:-4}".format(i) 
        #mprint(out,w,h)

        if sleep:
            mprint(out,w,h)
        if q == 0:
            m=d.left()
            #print(m)
            if not m:
                q+=1
                d.x_min += 1
        if q == 1:
            m=d.up()
            if not m:
                q+=1
                d.y_min += 1
        if q == 2:
            m=d.right()
            if not m:
                q+=1
                d.y_max -= 1
        if q == 3:
            m=d.down()
            if not m:
                d.left()
                q=0
                d.x_max -= 1
            

        r = d.get()
        i += 1
        #time.sleep(.01)
    return out

if __name__ == "__main__":
    w = 10
    h = 40
    #out = spiral(w,h)
    #mprint(out,w,h)






def left_right(w=10,h=4):
    mprint(data,w,h)


    out = ["----"] *(w*h) #*30 #*w*h+2
    d = DIR(w=w,h=h)
    d.down_reset()
    d.left_reset()
    r = d.get()
    i = 0
    import time
    q = 0
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        out[x+y] = "{:-4}".format(i) 

        if sleep:
            mprint(out,w,h)

        if q == 0:
            m=d.left()
            #print(m)
            if not m:
                q+=1
                d.down()
        elif q == 1:
            m=d.right()
            if not m:
                q=0
                d.down()
            

        r = d.get()
        i += 1
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 10
    h = 40
    out = left_right(w,h)
    mprint(out,w,h)

    #def dubble_spiral():
    #    pass
    #dubble_spiral()


def up_down(w=10,h=4):
    mprint(data,w,h)


    out = ["----"] *(w*h) #*30 #*w*h+2
    d = DIR(w=w,h=h)
    d.up_reset()
    d.left_reset()
    r = d.get()
    i = 0
    import time
    q = 0
    while type(r) is not type(None):
        x,y = r
        #print("r",r,x,y, d.i)
        out[x+y] = "{:-4}".format(i) 

        if sleep:
            mprint(out,w,h)

        if q == 0:
            m=d.up()
            #print(m)
            if not m:
                q+=1
                d.left()
        elif q == 1:
            m=d.down()
            if not m:
                q=0
                d.left()
            

        r = d.get()
        i += 1
        time.sleep(sleep)
    return out

if __name__ == "__main__":
    w = 40
    h = 20
    out = up_down(w,h)
    mprint(out,w,h)

