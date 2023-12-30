#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
SPDX-License-Identifier: GPL-2.0-only
(c) 2012 micha@librelight.de
"""

# file descriptor on linux /dev/midi1
import sys
import os
#import fcntl
import _thread as thread
import time
import copy



def list_device(filter="APC_MINI"):
    dpath = "/dev/snd/"
    filter = "APC_MINI"
    out = []
    for i in os.listdir(dpath):
        if i.startswith("controlC"):
            #print(i)
            cmd = "udevadm info {}/{}".format(dpath,i)
            #print("midi device_info",cmd)
            r=os.popen(cmd)
            lines = r.readlines()
            ok = 0
            for j in lines:
                if filter in j:
                    ok = 1

            if ok:
                out.append(i)
                for j in lines:
                    j=j.strip()
                    print("-",j)
    return out

class simplemidi(object):
    def __init__(self,device="/dev/midi1"):
        self.__lock = thread.allocate_lock()
        self.__mode = ""
        #self.__lock.acquire() 
        #self.__lock.release()
        self.__data = ""
        self.__name = device
        self.__open()
    def __close(self):    
        os.close( self.__midi )
    def __open(self):
        try:
            option = os.O_RDWR | os.O_NONBLOCK # os.O_RDONLY | os.O_NONBLOCK
            self.__midi = os.open( self.__name, option)
                
            self.__mode = "a"
            self.is_open = 1
        except OSError as e:
            print("__open File", self.__name, "ERR: {0} ".format(e.args) )
            print(" sleep 1sec...")
            time.sleep(1)
            self.is_open = 0
                
        print("DEVICE MODE:",self.__mode)

    def init(self):
        #placeholder pygame
        pass

    def get_device_info(self,nr):
        if nr == 1:
            return "simplemidi", self.__device
        return None

    def write_delayed(self,data):
        #import thread        
        thread.start_new_thread(self._write_delayed,([data,0.01],)) #midi writeloop
        thread.start_new_thread(self._write_delayed,([data,0.1],)) #midi writeloop
        thread.start_new_thread(self._write_delayed,([data,1],)) #midi writeloop

    def _write_delayed(self,data):
        time.sleep(data[1])
        self.write(data[0])
                    
    def write(self,data):
        try:
            self.__lock.acquire() 
            # change midi file to write mode
            if self.__mode == "rw":
                os.close(self.__midi)
                option = os.O_WRONLY | os.O_NONBLOCK
                self.__midi = os.open( self.__name, option)

            if len(data) == 3:
                msg = ""
                
                try:
                    msg = chr(int(data[0])) + chr(int(data[1])) + chr(int(data[2]) ) 
                    os.write(self.__midi, bytes(msg,"utf-8")  )
                except Exception as e:# SyntaxError:print("midi err",[msg,data ])
                    print("midi-single-write:", e, data)
                    time.sleep(1)
                    self.__open()

            elif len(data) > 3:
                #print("multi sending---------------------------")
                for i in data:
                    if len(i) == 3:
                        msg = ""
                        
                        try:
                            msg = chr(int(i[0])) + chr(int(i[1])) + chr(int(i[2])) 
                            print([msg])
                            os.write(self.__midi, msg  )
                        except Exception as e:
                            pass
                            print("midi-multi-write:", e, data)
                    
            
            # change midi file to read mode
            if self.__mode == "rw":
                os.close(self.__midi)
                option = os.O_RDONLY | os.O_NONBLOCK
                self.__midi = os.open( self.__name, option)
        finally:
            self.__lock.release()
        
    def read(self,count=3):
        self.__lock.acquire()
        data = copy.deepcopy(self.__data)
         
        self.__lock.release()
        return data
        
    def poll(self,sysex=0):
        self.__lock.acquire() 
        ok = 0
        try: 
            if sysex:
                self.__data = os.read(self.__midi, 1) #read abort if no data to read
            else:
                inp = os.read(self.__midi, 3) #read abort if no data to read
                try:
                    #self.__data =  [ ord( inp[0] ) ,ord( inp[1] ), ord( inp[2] ) ]
                    self.__data =  [ inp[0]  , inp[1] ,  inp[2] ]
                except KeyError as e:
                    print("File", self.__name, "ERR: {0} ".format(e.args) ,[inp])
                except IndexError as e:
                    print("File", self.__name, "ERR: {0} ".format(e.args) ,[inp])
                        
            ok = 1
        except KeyboardInterrupt as e:
            raise e
        except: # OSError: 
            time.sleep(0.01) # CPU STRESSLESS
        finally:
            self.__lock.release()

        return ok




