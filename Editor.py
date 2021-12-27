#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of librelight.

librelight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

librelight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with librelight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""

import time
import tkinter 
import sys
import _thread as thread
import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.pack(fill=tk.X, side=tk.TOP)
data = []
i=0
for r in range(3):
    frame.columnconfigure(r, weight=1)
    cd = []
    for c in range(8):
        i+=1
        frame.columnconfigure(c, weight=1)
        b = tk.Button(frame,bg="red", text='MH'+str(i)+' r:'+str(r+1)+' c:'+str(c+1))
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        cd.append(b)

frame = tk.Frame(root)
frame.pack(fill=tk.X, side=tk.TOP)
data = []
i=0
for c in range(8):
    frame.columnconfigure(c, weight=1)
    cd = []
    for r in range(3):
        i+=1
        frame.columnconfigure(r, weight=1)
        b = tk.Button(frame,bg="green", text='PAN'+str(i)+' r:'+str(r+1)+' c:'+str(c+1))
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        cd.append(b)


frame = tk.Frame(root)
frame.pack(fill=tk.X, side=tk.TOP)
data = []
for c in range(10):
    frame.columnconfigure(c, weight=1)
    cd = []
    for r in range(10):
        frame.columnconfigure(r, weight=1)
        b = tk.Button(frame, text='r:'+str(r+1)+' c:'+str(c+1))
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        cd.append(b)


frame = tk.Frame(root)
frame.pack(fill=tk.X, side=tk.TOP)
data = []
for c in range(3):
    frame.columnconfigure(c, weight=1)
    cd = []
    for r in range(3):
        frame.columnconfigure(r, weight=1)
        b = tk.Button(frame,bg="grey", text='r:'+str(r+1)+' c:'+str(c+1))
        b.grid(row=r, column=c, sticky=tk.W+tk.E)
        cd.append(b)        

root.mainloop()
