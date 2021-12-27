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

(c) micha.rathfelder@gmail.com
"""


#import init
#init.init()
import socket,time

import sys
sys.stdout.write("\x1b]2;APCmini\x07")


import sys
import os

import lib.chat as chat

import random


if 0:#0: # if pygame midi ?
    # Midi modul von Python game zur Platformunabhängigkeit
    # z.b. Windows

    # 10 MB RAM
    from interfaces.midi.lib.pygamemidi_wraper import pygamemidi
    midi = pygamemidi(out=2,inp=3)
else: # if linux
    #  4 MB RAM
    #from simplemidi_wraper import simplemidi
    from lib.simplemidi_wraper import simplemidi
    midi = simplemidi("/dev/snd/midiC1D0") #,inp="/dev/midi1")


nr = 0
while 1:
    device = midi.get_device_info(nr)
    if device == None:
        break
    else:
        print(nr , device)
    nr += 1



cli = None

import socket, struct


c = chat.tcp_sender()
def send(msg):
    c.send(msg)



def main():
    global send
    global node
    global toggel,toggel1,toggel2,toggel3
    fader = 40
    values = []
    fader_value= [0]*9
    firstfader = 48
    fader_move_delay = 0
    tog = 0
    tog0 = 1
    tog1 = 1
    cmd = ""
    release = 1

    while True:
        if release:
            release = 0
            for i in range(4):
                midi.write([144,60+i,5])
                midi.write([144,52+i,5])
                midi.write([144,44+i,5])
                midi.write([144,36+i,5])

                midi.write([144,24+i,3])
                midi.write([144,24+i+4,3])


                midi.write([144,56+i,1])

                midi.write([144,8+i,1])
                midi.write([144,12+i,1])


        if midi.poll():
            midi_date = midi.read(1)

            print("in:",midi_date)
            if midi_date[0] == 176:
                if midi_date[1] == 55:
                    fader = midi_date[2]/127.*8

                    print("LED:",[144,7,fader])
                    midi.write([144,7,fader])


                    print("setfadert to", fader)
                if midi_date[1] >= firstfader and midi_date[1] <= firstfader+8:
                    value = int(midi_date[2]*2.008)
                    fader_id = midi_date[1] - firstfader
                    fader_value[fader_id] = value
                    print("FADER:",fader_id+1,value)
                    if fader_id == 0:
                        msg = "group 33 level "+str(int(value))
                        send(msg)
                    elif fader_id == 1:
                        msg = "group 34 level "+str(int(value))
                        send(msg)
                    elif fader_id == 2:
                        msg = "group 35 level "+str(int(value))
                        send(msg)
                    elif fader_id == 3:
                        msg = "group 36 level "+str(int(value))
                        send(msg)
                    elif fader_id == 4:
                        msg = "group 37 level "+str(int(value))
                        send(msg)
                    elif fader_id == 5:
                        msg = "group 38 level "+str(int(value))
                        send(msg)

                    elif fader_id == 6:
                        #value = value*-1+255 #invert
                        value2 = int(value/255.*100)*2
                        #msg = "stack 2 indelay="+str(value2)+" ;EOB"
                        msg = "effect 1 SIZE "+str(value2)+" ;EOB"
                        send(msg)
                    elif fader_id == 7:
                        #value = value*-1+255 #invert
                        value2 = int(value/255.*100)*2
                        #msg = "stack 2 indelay="+str(value2)+" ;EOB"
                        msg = "effect 7 SIZE "+str(value2)+" ;EOB"
                        send(msg)
                    elif fader_id == 8:
                        if value <= 127:
                            value2 = value  / 127.
                        else:
                            value2 = (value - 127) / 20.   +1.
                        #value2 = value / 30.5
                        msg = "preset time "+str(value2)+" ;EOB"
                        send(msg)

                        #value2 = value / 25.5
                        #msg = "preset time_pt "+str(value2)+" ;EOB"
                        #send(msg)

            elif midi_date[0] == 144:

                if midi_date[1] == 56:
                    send("clear")
                elif midi_date[1] == 57:
                    send("store")
                elif midi_date[1] == 58:
                    send("edit")
                elif midi_date[1] == 33:
                    send("preview")
                elif midi_date[1] == 34:
                    send("set")
                elif midi_date[1] == 35:
                    send("next")
                elif midi_date[1] >= 8 and midi_date[1] <= 15 :
                    nr = midi_date[1]-8+25
                    send("xpreset "+str(int( nr )) )
                elif midi_date[1] >= 24 and midi_date[1] <= 31 :
                    nr = midi_date[1]-24+33
                    send("xpreset "+str(int( nr )) )

                elif midi_date[1] == 20:
                    pass#send("stack 1 on")
                elif midi_date[1] == 12:
                    pass#send("stack 1 go")
                elif midi_date[1] == 4:
                    pass#send("stack 1 run")
                elif midi_date[1] == 68:
                    pass#send("stack 1 stop")
                elif midi_date[1] == 0:
                    pass#msg = "sel 1"
                    pass#send(msg)
                elif midi_date[1] == 1:
                    pass#msg = "sel 2"
                    pass#send(msg)
                elif midi_date[1] == 2:
                    pass#msg = "sel 3"
                    pass#send(msg)
                elif midi_date[1] == 64:
                    pass#msg = "group 1 sel 1 "
                    pass#send(msg)
                elif midi_date[1] == 65:
                    pass#msg = "group 25 sel 1 "
                    pass#send(msg)
                elif midi_date[1] == 66:
                    pass#msg = "group 17 sel 1 "
                    pass#send(msg)
                elif midi_date[1] == 86:
                    #msg = "group 25 sel 1 "
                    #send(msg)
                    #ipc = cli.ipc_write({"SDL-GUI":"VIEW:programmer"})
                    pass

                elif midi_date[1] == 85:
                    pass
                    #msg = "group 25 sel 1 "
                    #send(msg)
                    #ipc = cli.ipc_write({"SDL-GUI":"VIEW:groups"})
                elif midi_date[1] == 21:
                    pass
                    #send("stack 2 on")
                elif midi_date[1] == 13:
                    pass
                    #send("stack 2 go")
                elif midi_date[1] == 5:
                    pass
                    #send("stack 2 run")
                elif midi_date[1] == 69:
                    pass
                    #send("stack 2 stop")

                elif midi_date[1] == 22:
                    pass
                    #send("stack 2 mode ;")
                elif midi_date[1] == 14:
                    pass
                    #send("stack 2 dir ;")
                elif midi_date[1] == 6:
                    #send("stack 2 dyn=rider,,1 ;")
                    send("effect 1 DIR 0")
                elif midi_date[1] == 7:
                    pass
                    send("effect 7 DIR 0")
                    #send("stack 2 dyn=rnd,,1 ;")

            if midi_date[0] == 128:
                midi_date[2] = 0
                midi_date[0] = 144
                print("release")
                release = 1



            else:
                midi_date[2]  = int(fader)
            #if midi_date[1] <= 71:
            #    midi_date[1]  = midi_date[1]+8



            if midi_date[0] != 176:
                print("write",midi_date)
                midi.write(midi_date)


            if midi_date[0] == 128:
                for i in range(4):
                    midi.write([144,60+i,5])
                    midi.write([144,52+i,5])
                    midi.write([144,44+i,5])
                    midi.write([144,36+i,5])
        time.sleep(0.0002)

        if (int(time.time())) % 2 == 0:
            if tog0:
                tog0 = 0
                tog1 = 1
                midi.write([144,82,0])
                #print("o")
        else:
            if tog1:
                tog0 = 1
                tog1 = 0
                midi.write([144,82,3])
                #print("oo")

import _thread as thread
main()

node = 244

node2 = 0
while 1:
    inp = raw_input("end")
    try:
        inp = inp.split(" ")
        midi.write(inp)
        midi.write(inp)
    
    except:pass
