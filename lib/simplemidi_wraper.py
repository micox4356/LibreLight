#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of LibreLight.

LibreLight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

LibreLight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LibreLight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""

# file descriptor on linux /dev/midi1
import sys
import os
#import fcntl
import _thread as thread
import time
import copy

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
            
        except OSError as e:
            print("File", self.__name, "ERR: {0} ".format(e.args) )

            try:
                self.__mode = "rw"
                option = os.O_RDONLY | os.O_NONBLOCK
                self.__midi = os.open( self.__name, option)
                print("DEVICE MODE:",self.__mode)
            except OSError as e:
                print("File", self.__name, "ERR: {0} ".format(e.args) )
                input()
                sys.exit()
                
        print("DEVICE MODE:",self.__mode)
    def init(self):
        #placeholder pygame
        pass
    def get_device_info(self,nr):
        if nr == 1:
            return "simplemidi", self.__device
        else:
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
                #if data[0] != 191:
                #    print(data#[msg])
                os.write(self.__midi, bytes(msg,"utf-8")  )
            except Exception as e:# SyntaxError:print("midi err",[msg,data ])
                print("midi-single-write:", e, data)
                #self.__close() #STOPPING MIDI ...
                #self.__open()
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
        self.__lock.release()
        
    def read(self,count=3):
        self.__lock.acquire()
        data = copy.deepcopy(self.__data)
         
        self.__lock.release()
        return data
        
    def poll(self,sysex=0):
        self.__lock.acquire() 
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
                        
            self.__lock.release()
            return 1
        except OSError: 
            time.sleep(0.01) # CPU STRESSLESS
            self.__lock.release()
            return 0

