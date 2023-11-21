#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
SPDX-License-Identifier: GPL-2.0-only
(c) micha@librelight.de
"""

import sys
sys.stdout.write("\x1b]2;APCmini\x07")

import os
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

            print(row,"in:",FN,"ch",ch,"raw",midi_date,_bin,int(_bin,2),_bin2)

            continue
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
                        #msg = "group 33 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
                        send(msg)
                    elif fader_id == 1:
                        msg = "group 34 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
                        send(msg)
                    elif fader_id == 2:
                        msg = "group 35 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
                        send(msg)
                    elif fader_id == 3:
                        msg = "group 36 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
                        send(msg)
                    elif fader_id == 4:
                        msg = "group 37 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
                        send(msg)
                    elif fader_id == 5:
                        msg = "group 38 level "+str(int(value))
                        msg = "d{}:{}:0".format(fader_id+1,value)
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
                    msg = "df{}:255:0".format(midi_date[1]-64+1)
                    send(msg)
                elif midi_date[1] == 65:
                    msg = "df{}:255:0".format(midi_date[1]-64+1)
                    send(msg)
                    pass#msg = "group 25 sel 1 "
                    pass#send(msg)
                elif midi_date[1] == 66:
                    msg = "df{}:255:0".format(midi_date[1]-64+1)
                    send(msg)
                    pass#msg = "group 17 sel 1 "
                    pass#send(msg)
                elif midi_date[1] == 86:
                    msg = "df{}:255:0".format(midi_date[1]-64+1)
                    send(msg)
                    #msg = "group 25 sel 1 "
                    #send(msg)
                    #ipc = cli.ipc_write({"SDL-GUI":"VIEW:programmer"})
                    pass

                elif midi_date[1] == 85:
                    msg = "df{}:255:0".format(midi_date[1]-64)
                    send(msg)
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
                #print("release")
                release = 1

                if midi_date[1] == 64:
                    msg = "df{}:off:0".format(midi_date[1]-64+1)
                    send(msg)
                if midi_date[1] == 65:
                    msg = "df{}:off:0".format(midi_date[1]-64+1)
                    send(msg)
                if midi_date[1] == 66:
                    msg = "df{}:off:0".format(midi_date[1]-64+1)
                    send(msg)
                if midi_date[1] == 67:
                    msg = "df{}:off:0".format(midi_date[1]-64+1)
                    send(msg)
                if midi_date[1] == 68:
                    msg = "df{}:off:0".format(midi_date[1]-64+1)
                    send(msg)


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
