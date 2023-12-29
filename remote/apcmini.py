#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
SPDX-License-Identifier: GPL-2.0-only
(c) micha@librelight.de
"""

import sys
sys.stdout.write("\x1b]2;APCmini\x07")

import os
#sys.path.append(os.getcwd() + '/..')
sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import time
import socket, struct
import random

import lib.chat as chat

if 0:
    # z.b. Windows
    # 10 MB RAM
    from interfaces.midi.lib.pygamemidi_wraper import pygamemidi
    midi = pygamemidi(out=2,inp=3)
else: 
    # 4 MB RAM , only tested on linux
    import lib.simplemidi_wraper as smidi
    device = smidi.list_device(filter="APC_MINI")
    _id = device[-1][-1]
    midi = smidi.simplemidi("/dev/snd/midiC{}D0".format(_id) ) #,inp="/dev/midi1")



cli = None


class dummyChat():
    def __init__(self):
        pass
    def send(self,*arg,**args):
        print("dummyChat",self,arg,args)

#c = chat.tcp_sender()
c = dummyChat() 
def send(msg):
    print("send",msg)
    c.send(msg)

BLACK = 0
YELLOW = 5
YELLOW_BLINK = 6
GREEN = 1
GREEN_BLINK = 2
RED = 3
RED_BLINK = 4


class MAIN():
    def __init__(self):
        self.buf = []
        self.dbg = 0
    def loop(self):
        release = 0
        if 0:
            r = 225
            for i in range(4):
                for i in range(r):
                    if self.dbg:print(i)
                    midi.write([144,40+i,GREEN])
                time.sleep(0.2)
                for i in range(r):
                    print(i)
                    midi.write([144,40+i,BLACK])
                time.sleep(0.2)
                for i in range(r):
                    print(i)
                    midi.write([144,40+i,RED])
                time.sleep(1.52)
            for i in range(r):
                print(i)
                midi.write([144,60+i,BLACK])
        
            time.sleep(0.5)


        while True:
            if release:
                release = 0
                for i in range(4):
                    midi.write([144,60+i,YELLOW])
                    midi.write([144,52+i,YELLOW])
                    midi.write([144,44+i,YELLOW])
                    midi.write([144,36+i,YELLOW])

                    midi.write([144,24+i,RED])
                    midi.write([144,24+i+4,RED])


                    midi.write([144,56+i,GREEN])

                    midi.write([144,8+i,GREEN])
                    midi.write([144,12+i,GREEN])

            #midi.write([144,82,YELLOW])
            #time.sleep(.5)
            #midi.write([144,82,BLACK])

            rows = [56,48,40,32,24,16,8,0,64,48]
            midi_function = {
                    "Off": (128,144),
                    "On ":(144,160),
                    "PLY":(160,176),
                    "CC ":(176,192),
                    "PC ":(192,208),
                    "CA ":(208,223),
                    "QtrFrame":(241,242),
                    "tclock":(248,249),
            }
            # cut byte
            # x=174;((x)^(x>>4<<4))
            # int(bin(151)[-4:],2)+1
            #nibl =  x=174;((x)^(x>>4<<4))
            #nibl = int(bin(151)[-4:],2)+1
            ch = -123
            if midi.poll():
                midi_date = midi.read(1)
                #print("MIDI",midi_date)
                if 1:# midi_date[0] >= 128 midi_date[0] <= 143:
                    ch = int(bin(midi_date[0])[-4:],2)+1

                for fn,v in midi_function.items():
                    if midi_date[0] >= v[0] and midi_date[0] < v[1]:
                        FN = fn
                        break

                r_old = 0
                row = 0
                for r in rows: 
                    #print(r_old,r)
                    if r_old and midi_date[1] >= r_old and midi_date[1] < r:
                        row = midi_data[1] - r+1
                        print("jo")
                    r_old=r   

                nibl = int(bin(midi_date[1])[2:][-4:],2)+1
                _bin2 = bin(midi_date[1])
                _bin2 = _bin2[2:]
                _bin2 = _bin2.rjust(8,"0")
                _bin2 = int(_bin2[1:5],2)

                _bin = bin(midi_date[1])
                _bin = _bin[2:]
                _bin = _bin.rjust(8,"0")
                _bin = _bin[-3:] # 3 bit

                value = ""
                btn = int(midi_date[1]) #btn_row*btn_col
                if FN == "CC ":
                    _bin2 =str(int(_bin2)+1000)
                    value = midi_date[-1]
                    btn += 1000
                if FN == "On ":
                    value = 1
                    midi.write([144,midi_date[1],YELLOW])
                if FN == "Off":
                    value = 0
                    release = 1
                    midi.write([144,midi_date[1],BLACK])

                btn_row = int(_bin2)+1 
                btn_col =int(_bin,2)+1

                #print(row,"in:",FN,"ch",ch,"raw",midi_date,_bin,btn_row,btn_col,[value])
                #print([btn_row,btn_col,btn,value])
                if self.dbg:print([btn,value])

                self.buf.append([btn,value])


if __name__ == "__main__":
    import _thread as thread

    main = MAIN()
    thread.start_new_thread(main.loop,())
    time.sleep(1)


    while 1:
        if main.buf:
            buf = main.buf[:]
            main.buf = []
            for m in buf:
                print("-> midi:",m)

        time.sleep(0.1)
