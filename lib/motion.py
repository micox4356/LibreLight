#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of librelight.

librelight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

librelight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with librelight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha@uxsrv.de
"""
import math, random
import time,json
class Sequence(object):
    def __init__(self):
        pass
    def go(self,ID,RANGE,ATTRIBUT):
        pass

class Stack(object):
    "List of Presets"
    def __init__(self):
        self.__stacks = show.load_stacks(self.__show["NAME"],self.__stacks)

    def save(self):
        show.save_stacks(self.__show["NAME"],self.__stacks)
    def __str__(self):
        pass 
    def go(self,ID):
        pass
    def pause(self,ID):
        pass
    def set(self,optinon,value):
        pass
    def next(self,FIX,ATTR):
        pass 

class Effect(object):
    """Effect sinus, cosinus, linear"""
    def __init__(self,TYPE="sinus",size=10,speed=100,offset=0,egroup=None,DIR=1):
            
        self.__type=TYPE
        self.__msize=255
        self.__mspeed=255
        self.__moffset=1
        self.__dir=DIR
        self.__mdir=1
        self.__size=size
        self.__speed=speed
        self.__base = None 
        self.__offset = offset
        self.__vmax = -1000000
        self.__vmaxt = 0
        self.__vmin = 1000000
        self.__vmint = 0
        if self.__offset:
            self.__step = float(self.__offset*self.__moffset)           
        else:
            self.__step = 0
        #self.__step = 0
        self.__old_step = 0#self.__step 
        self.__old_rand = 0 

        self.__egroup = egroup
        print(self)
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return '<%(klass)s type:%(TYPE)s size:%(size)s base:%(base)s speed:%(speed)s offset:%(offset)s egroup:%(egroup)s msize:%(msize)s mspeed:%(mspeed)s moffset:%(moffset)s mdir:%(mdir)s _dir:%(_dir)s>' % dict(
			klass  = self.__class__.__name__,
			TYPE   = self.__type,
			size   = self.__size,
            base   = self.__base,
			speed  = self.__speed,
            offset = self.__offset,
            egroup = self.__egroup,
            msize  = self.__msize,
            mspeed = self.__mspeed,
            moffset = self.__moffset,
            mdir = self.__mdir,
            _dir = self.__dir
		)
    def __sinus(self,current_value):
        
        out = current_value + math.sin(self.__step/1000.)*self.__size*self.__msize/255  #+ self.__offset*self.__moffset/10
        if self.__mdir:
            if self.__dir:
                DIR = 0
            else:
                DIR = 1
        else: 
            if self.__dir:
                DIR = 1
            else:
                DIR = 0
        #print(DIR)
        if DIR:
            self.__step += (self.__speed/100)*self.__mspeed/255 #+ self.__offset*self.__moffset/10
        else:
            #out = current_value + math.cos(self.__step/1000.)*self.__size*self.__msize/255  #+ self.__offset*self.__moffset/10
            self.__step -= (self.__speed/100)*self.__mspeed/255 #+ self.__offset*self.__moffset/10
    
        if int(out) > self.__vmax:
            self.__vmaxt = time.time()
            self.__vmax = int(out)
            #print("max schrittbreite ",self.__vmaxt - self.__vmint,"sec \t",self)
        if int(out) < self.__vmin:
            self.__vmint = time.time()
            self.__vmin = int(out)
            #print("min schrittbreite ",self.__vmaxt - self.__vmint,"sec \t",self)
        if out > 255:
            out = 255
        elif out < 0:
            out = 0
        #print(self)
        return out
    def __cosinus(self,current_value):
        
        out = current_value + math.cos(self.__step/1000.)*self.__size*self.__msize/255 #+ self.__offset*self.__moffset/10
        if self.__mdir:
            if self.__dir:
                DIR = 0
            else:
                DIR = 1
        else: 
            if self.__dir:
                DIR = 1
            else:
                DIR = 0

        #if self.__mdir + self.__dir == 1:
        if DIR:
            #out = current_value + math.cos(self.__step/1000.)*self.__size*self.__msize/255 #+ self.__offset*self.__moffset/10
            self.__step += (self.__speed/100)*self.__mspeed/255 #+ self.__offset*self.__moffset/10
        else:
            #out = current_value + math.sin(self.__step/1000.)*self.__size*self.__msize/255 #+ self.__offset*self.__moffset/10
            self.__step -= (self.__speed/100)*self.__mspeed/255 #+ self.__offset*self.__moffset/10
            
        if out > 255:
            out = 255
        elif out < 0:
            out = 0
        
        return out
    def __linear(self,current_value):
        pass
    def __rand(self,current_value):
        #self.__step += int(self.__speed/10000)
        #print(self.__old_step-int(self.__speed/1000.) , time.time())
        if self.__old_step < time.time():
            self.__old_rand =  random.randint(0,int(self.__size*self.__msize/255)  ) 
            self.__old_step = time.time() + ( 10-  (  ( self.__speed/100. ) *self.__mspeed/255 )  / 30000.  )       
            print("NEW SPEED :" ,self.__old_step, time.time() - self.__old_step)
            print("NEW RAND :" ,self.__old_rand)
        return self.__old_rand 
    def get_egroup(self):
        return self.__egroup        
    def set_mdir(self, mdir):
        if type(mdir) is int:
            if mdir != 0:
                mdir = 1
            self.__mdir=mdir
        else:
            print(self, "mdir not an int")
        #print(self.__mdir * self.__dir)
    def set_msize(self,msize):
        if type(msize) is int:
            self.__msize=msize
        else:
            print(self, "msize not an int")
    def set_mspeed(self,mspeed):
        if type(mspeed) is int:
            self.__mspeed=mspeed
        else:
            print(self, "mspeed not an int")

    def set_moffset(self,moffset):
        # set Master Offset
        if type(moffset) is int:
            if moffset != self.__moffset:
                val = self.__offset*self.__moffset
                self.__step -= float(val)            
                #print("old offset ",val)
                self.__moffset = moffset
                val = self.__offset*self.__moffset
                self.__step += float(val)            
                #print("new offset ",val)
                #self.__offset = float(val)    self.__moffset=moffset
                #print("set moffset",moffset, self.__offset*self.__moffset/10)
        else:
            print(self, "moffset not an int")

    def set_size(self,val):
        self.__size = val
    def set_speed(self,val):
        self.__speed = val
    def set_type(self,val):
        self.__type = val
    def set_offset(self,val):
        self.__step -= float(self.__offset)            
        self.__step += float(val)            
        self.__offset = float(val)           
    def next(self,current_value):
        self.__base = current_value

        if self.__type == "sinus":
            return self.__sinus(current_value)            
        elif self.__type == "cosinus":
            return self.__cosinus(current_value)
        elif self.__type == "linear":
            return 0
            pass
        elif self.__type == "rand":
            return self.__rand(current_value)
        else:
            print("effect type \""+str(self.__type) +"\" unknown")
            return 0

    
  



class FadeFast(object):
    """Fade 16bit mode as FLOAT 

    Berechnet Schritte in "on the fly"
    """    
    def __init__(self,start,target,fadetime=None,start_time=None):
        self.INIT = 0 
        if target > 255.999:
            target = 255.999
        elif target < 0:
            target = 0
        if start_time:
            self.__start_time = start_time
        else:
            self.__start_time = time.time()
        self.fakt = 1. #1000.
        #feine aufloesung
        start = int(start*self.fakt)
        target = int(target*self.fakt)
        if not fadetime:
            start = target
        self.__start = start
        self.value = start
        self.old_ret = start
        self.__current = start
        self.__target = target
        self.__fadetime = fadetime
        self.__dist = target - start
        self.fine = 0
        #print(self.__class__.__name__,"(", self.__start/self.fakt, self.__target/self.fakt, self.__dist/self.fakt, self.__fadetime , ") NEW FADE OBJ")
        if self.__dist != 0:
            self.__step_time = fadetime / (self.__dist * 1.0)
        else:
            self.__step_time = 0
            
        if self.__step_time < 0:
            self.__step_time = self.__step_time *-1

        #print(self.__step_time)
        #print(self)
    def __dict__(self):
        return None
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        #return {"non":None}
        return '<%(klass)s start:%(start)s target:%(target)s fadetime:%(fadetime)ssec start_time:%(start_time)ssec>' % dict(
			klass    = self.__class__.__name__,
			start   = self.__start/self.fakt,
			target = self.__target/self.fakt,
			fadetime = self.__fadetime,
            start_time = self.__start_time
		) 


    def next(self):
        
        jetzt = time.time()
        if self.fine:
            return 0
        
        if jetzt >= self.__fadetime + self.__start_time or not self.__step_time :
            if not self.INIT:
                #print(self.__fadetime,jetzt - self.__start_time)
                #print("end")
                self.INIT = 1
            self.value = self.__target/self.fakt
            self.fine = 1
            return 1

        elif jetzt < self.__start_time:
            self.value = self.__start
            return 0
            #return self.__start
        if self.__step_time :
            step = (jetzt - self.__start_time) / self.__step_time 
        else:
            step = 0
        #print(self.__class__.__name__,"fade",self.__fadetime,"jetzt",jetzt,"start_t", self.__start_time,"start",self.__start,"step", step,"step_t",self.__step_time)
        if self.__start < self.__target:
            ret = int(self.__start + step)/self.fakt
        else:
            ret = int(self.__start - step)/self.fakt

        self.value = ret
        if self.old_ret != ret:
            self.old_ret = ret
            return 1
        #return ret
        return 0


class Fade(object):
    """altes fade objekt

    Speicher fresser und initialisierung dauert
    alle einzelschritte werden bei der initialisierung erzeugt
    """

    def __init__(self,start,target,fadetime=None,start_time=None):
        self.INIT = 0 
        if target > 255:
            target = 255
        if start_time:
            self.__time = start_time
        else:
            self.__time = time.time()

        #feine aufloesung
        start = int(start*100.)
        target = int(target*100.)
        if not fadetime:
            start = target
        self.__start = start
        self.__current = start
        self.__target = target
        self.__fadetime = fadetime
        self.__dist = target - start
        print(self.__class__.__name__,"(", self.__start/100., self.__target/100., self.__dist/100, self.__fadetime , ") NEW FADE OBJ")
        if self.__dist != 0:
            self.__step_time = fadetime / (self.__dist * 1.0)
        else:
            self.__step_time = 0
            
        self.__steps = []
        
        if self.__dist < 0: 
            for i in range(self.__dist*-1):
                self.__steps.append([self.__start,0])
        elif self.__dist > 0:            
            for i in range(self.__dist):
                self.__steps.append([self.__start,0])            
        else:
            self.__steps.append([self.__target,time.time()])
            #print("DIST == 0")
        
        if self.__step_time < 0:
            self.__step_time = self.__step_time *-1

            
        i = 0 
        #print(self#.__dist, self.__start ,self.__step_time)
        #erstelle alle schritte mit absolutem zeitstempel
        while self.__dist != 0:
            if self.__dist > 0:
               self.__current += 1
               self.__dist -= 1
            else:
               self.__current -= 1
               self.__dist += 1
            self.__time += self.__step_time 
            self.__steps[i][0] =  self.__current
            self.__steps[i][1] =  self.__time
            
            i += 1
        #print(i,self.__steps, self.__dist, self.__start )

    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return '<%(klass)s start:%(start)s target:%(target)s fadetime:%(fadetime)s sec>' % dict(
			klass    = self.__class__.__name__,
			start   = self.__start/100.,
			target = self.__target/100.,
			fadetime = self.__fadetime,
		) 
    def next(self):
        out = self.__start
        jetzt = time.time()
        #print(self.__start,self.__steps[-1])
        if jetzt < self.__steps[-1][1]: 
            for i in self.__steps:
                if jetzt >= i[1]:
                     out = i[0]
                     #print(i, jetzt  ,jetzt >= i[1])
            return out /100.
        else:
            return self.__steps[-1][0]/100. 


