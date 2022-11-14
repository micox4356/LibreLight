
import os
import fcntl
import time
import socket
import struct
import random



import copy
import _thread as thread

import sys

def unpack_art_dmx(data):
    dmx = ["x"]*512
    for i in range(len(data[18:]) ):
        x=data[18+i]
        #print("x",x)
        #print( "data",b'!B', data[18+i])
        #x=struct.unpack( b'!B',data[18+i])
        #print( "data",b'!B', data[18+i],x)
        #x=x[0]
        dmx[i] = x
    return dmx

        
class Socket():
    def __init__(self,bind='',port=6454,options_recive=""):
        self.__port =port
        self.__bind =bind
        self.options_recive=options_recive
        self.__poll = 0
        self.__data = []
        self.__addr = "NONE"
        #self.__hosts = {"host":{"9":[0]*512}}
        self.__hosts = {}
        self.hosts = self.__hosts
        self.open()
        self._poll_clean_time = time.time()
        self._poll_clean_count = 0
    def open(self):
        try:
            print("connecting to ArtNet bind:",self.__bind,"Port",self.__port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            self.sock.bind((self.__bind, self.__port))
            fcntl.fcntl(self.sock, fcntl.F_SETFL, os.O_NONBLOCK)
            #self.sock.setblocking(0)
            
        except socket.error as e:
            print("Socket ",self.__bind,self.__port, "ERR: {0} ".format(e.args))
            #raw_input()
            #sys.exit()
    def poll_clean(self):
        if self._poll_clean_time+(1/25.) <= time.time():
            self._poll_clean_time = time.time()
            self._poll_clean()
            x = self._poll_clean_count 
            self._poll_clean_count = 0
            return x
    def _poll_clean(self):
        while 1:
            try:
                self.__data, self.__addr = self.sock.recvfrom(self.__port)
                self._poll_clean_count += 1
                #return 1
            except socket.timeout as e:
                err = e.args[0]
                if err == 'timed out':
                    time.sleep(1)
                    print('recv timed out, retry later')
                else:
                    print(e)
                break
            except socket.error as e:
                break
    def poll(self ):
        if not self.__poll:
            try:
                self.__data, self.__addr = self.sock.recvfrom(self.__port)


                data, addr = (self.__data,self.__addr)
                self.host = addr[0]
                head    = data[:18]
                rawdmx  = data[18:]
                #print([head],addr)
                self.univ = -1
                try:
                    self.head = struct.unpack("!8sHBBBBHBB" , head )
                except Exception as e:
                    pass#print( "======E09823" , e)
                univ = self.head[6]/255 # /512  # * 512
                self.univ = int(univ)

                if self.host.startswith("127."): #allways recive localhost on port 
                    self.__poll = 1
                    return 1
                elif not self.options_recive:
                    self.__poll = 1
                    return 1
                elif self.host.startswith(self.options_recive): 
                    self.__poll = 1
                    return 1
                else:
                    self.__poll = 0
                
                addr = str(addr)
                univ = str(univ)
                if self.__poll:
                    if addr not in self.__hosts:
                        self.__hosts[addr] = {}
                    if univ not in self.__hosts[addr]:
                        self.__hosts[addr][univ] = {}
			
                    self.__hosts[addr][univ] = {"head":head,"addr":addr,"univ":univ,"dmx":rawdmx}
                    self.hosts = self.__hosts

            except socket.timeout as e:
                err = e.args[0]
                if err == 'timed out':
                    time.sleep(1)
                    print('recv timed out, retry later')
                else:
                    print(e)
            except socket.error as e:
                pass
    
    def recive(self):
        if self.__poll:
            self.__poll = 0

            data, addr = (self.__data,self.__addr)
            #print( self.univ,self.head)

            self.dmx  = unpack_art_dmx(data)

            return { "host":self.host,"dmx":self.dmx,"univ":self.univ,"head":self.head,"data":data,"addr":addr}
    

def get_value(sdata=[] ,univ=0,dmx=[1,121]):
    data=[]
    for k in sdata:
        xx = sdata[k]
        _univ = int(xx["head"][6] /256)
        if xx["host"].startswith('2.0.0.') and _univ == univ:
            for d in dmx:
                y = xx["dmx"][d-1]
                data.append(y)

    return data

class ArtNetRead():
    def __init__(self):
        self.sdata = {}
        self.xsocket = Socket()
        self.lock = thread.allocate_lock()
    def loop(self):
        sdata = {}
        print("loop")
        while 1:
            flag = 0
            while self.xsocket.poll():
                xx = self.xsocket.recive()
                k = xx["host"] +":"+ str(xx["head"][6])
                sdata[k] = xx
                flag = 1

            if flag:
                try:
                    self.lock.acquire()
                    self.sdata = copy.deepcopy(sdata)
                finally:
                    self.lock.release()
            time.sleep(0.001)
    def get(self):
        
        try:
            self.lock.acquire()
            x = self.sdata #= copy.deepcopy(asdata)
            self.sdata = {}
            return x
        finally:
            self.lock.release()



if __name__ == "__main__":
    e = ArtNetRead()
    thread.start_new_thread(e.loop,())
