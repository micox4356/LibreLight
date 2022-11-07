#! /usr/bin/python3
# -*- coding: utf-8 -*-
import time
"""
This file is part of LibreLight.

LibreLight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

LibreLight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LibreLight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha@uxsrv.de
"""

import sys
import pygame as pg
#from pygame.locals import *
import OpenGL.GL  as gl
import OpenGL.GLU as glu

def wall(v=(0,0,0),size=(10,10),rgb=(0.2,0.2,0.2)):
    s=size

    edges = ( #kanten
            ( s[0]+v[0],  s[1]+v[1],0+v[2]),
            ( s[0]+v[0], -s[1]+v[1],0+v[2]),
            (-s[0]+v[0], -s[1]+v[1],0+v[2]),
            (-s[0]+v[0],  s[1]+v[1],0+v[2]),
        )
    gl.glBegin(gl.GL_QUADS)
    for e in edges:
        gl.glColor4f(rgb[0], rgb[1], rgb[2], 0)
        gl.glVertex3fv(e)
        
    gl.glVertex3fv(edges[0])
    gl.glEnd()

def floor(v=(0,0,0),size=(10,8),rgb=(0.2,0.2,0.2)):
    s=size

    edges = ( #kanten
            ( s[0]+v[0],-0.2+v[1],  s[1]+v[2]),
            ( s[0]+v[0],-0.2+v[1], -s[1]+v[2]),
            (-s[0]+v[0],-0.2+v[1], -s[1]+v[2]),
            (-s[0]+v[0],-0.2+v[1],  s[1]+v[2]),
        )
    gl.glBegin(gl.GL_QUADS)
    for e in edges:
        gl.glColor4f(rgb[0], rgb[1], rgb[2], 0)
        gl.glVertex3fv(e)
        
    gl.glVertex3fv(edges[0])
    gl.glEnd()
   

_z_init = 1
def zerror():
    global _z_init
    edges = ( #kanten
            ((1,0,0),(0,0,0)),
            ((0,1,0),(0,0,0)),
            ((0,0,1),(0,0,0)),
        )
    i=0
    for e in edges:
        rgb=[0,0,0]
        rgb[i]=1
        if _z_init:
            print(rgb)
        gl.glColor4f(rgb[0], rgb[1], rgb[2], 0)
        gl.glBegin(gl.GL_LINES)
        for x in e:
            gl.glVertex3fv(x)
        gl.glEnd()
        i+=1
    _z_init = 0

import random
class Spot():
    def __init__(self,v=(0,0,0)):
        self.v = v
        self.l = 3
        self.v2 = [v[0],v[1]+5,v[2]+3]
        self.dir = random.randint(0,1)
        self.delta = 0
        self.delta2 = random.random()/100
    def draw(self):
        if self.dir:
            self.delta += (0.01 +self.delta2)
        else:
            self.delta -= (0.01 +self.delta2)

        if self.delta < -0.5:
            self.dir = 1
        if self.delta > 0.5:
            self.dir = 0
            
        self.v2[2] += self.delta
        edges = ( #kanten
                self.v,
                self.v2,
            )
        i=0
        gl.glBegin(gl.GL_LINES)
        #print("-----")
        for e in edges:
            #print("spot",e)
            rgb=[1,1,1]
            #rgb[i]=0.2
            gl.glColor4f(rgb[0], rgb[1], rgb[2], 0)
            #print(e)
            gl.glVertex3fv(e)
            
            i+=1
            if i >= len(edges):
                i = 0
        gl.glEnd()

def test():
    gl.glBegin(gl.GL_LINES)
    #  gl.glBegin(gl.GL_QUADS)
    x=(0,0,0)
    gl.glVertex3fv(x)
    x=(1,0,0)
    gl.glVertex3fv(x)
    
    x=(0,0,1)
    gl.glVertex3fv(x)
    x=(0,1,1)
    gl.glVertex3fv(x)
    gl.glEnd()

def event_read():

    inc = 1

    for event in pg.event.get():
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
        if event.type == pg.KEYDOWN:
            print(event.key,event)
            print(event.mod)
            if event.key == pg.K_LEFT:
                if event.mod == 1:
                    move_x = inc
                else:
                    rot_z = 1
            if event.key == pg.K_RIGHT:
                if event.mod == 1:
                    move_x = -inc
                else:
                    rot_z = -1
            if event.key == pg.K_UP:
                if event.mod == 1:
                    move_z = inc
                else:
                    rot_x = 1
            if event.key == pg.K_DOWN:
                if event.mod == 1:
                    move_z = -inc
                else:
                    rot_x = -1
        
        gl.glTranslatef(move_x,move_z,move_y)
        a = 0
        for r in [rot_z,rot_x,rot_y]:
            if r == 0:
                a += 1
                continue

            deg = 10
            if r > 0:
                d = deg
            if r < 0:
                d = -deg


            gl.glRotatef(d,a,1,0)
            a += 1
    
#pg.init()   #pulseaudio assert error after some time
#pg.font.init()
#pg.mixer.init() #pulsaudio assert error after some time
pg.display.init()
pg.key.set_repeat(1,100)
pg.display.set_caption('LibreLight 3D Stage (Demo!)')
display= (400,400)
display= (800,600)
pg.display.set_mode(display,pg.DOUBLEBUF|pg.OPENGL)
glu.gluPerspective( 45, (display[0]/display[1]), 0.1, 80.0)
gl.glTranslatef(0.0,0.0,-50)
gl.glRotatef(25,2,1,0)
gl.glRotatef(25,0,1,0)
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glDepthFunc(gl.GL_LEQUAL)

spots = []
for z in [1,3,5]:
    s = Spot(v=(-4,z,0))
    spots.append(s)
    s = Spot(v=(-2,z,0))
    spots.append(s)
    s = Spot(v=(2,z,0))
    spots.append(s)
    s = Spot(v=(4,z,0))
    spots.append(s)
frame = 0
frame_time = time.time()
fps = 0
while True:
    try:
        pg.display.set_caption('LibreLight 3D Stage {: 10} frame (DEMO!)'.format(fps))
        if frame_time+1 < time.time():
            frame_time = time.time()
            fps = frame
            frame = 0
        
        event_read()
        
        #gl.glRotatef(1,1,1,1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        floor(v=(0,-2.2,20),size=(30,30),rgb=(.1,.1,.1)) # hall
        wall(v=(0,5,-8),size=(20,8),rgb=(.2,.2,.3))   # backdrop
        wall(v=(0,-1.2,8),size=(10,1),rgb=(.3,.2,.2))   # stage-border
        #floor(v=(0,-2.2,20),size=(10,10),rgb=(.3,.2,.2))
        floor() # stage-plain
        zerror() # zerror-cross

        for s in spots:
            s.draw()
        pg.display.flip()
        pg.time.wait(10)
        pg.time.wait(10)

        frame += 1
    except Exception as e:
        print("Exception ",e)
        time.sleep(1)
#finally:
#    print("end -- frame:",frame)
