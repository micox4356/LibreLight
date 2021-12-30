
import time
import socket
import struct
import random

class ArtNetNode():
    """simple Object to generate ArtNet Network packages 
       works in Python2 and Python3  2021-12-05

    """
    def __init__(self, to="10.10.10.255",univ=7,port=6454):
        try: 
            univ = int(univ)
        except:
            print("errror univ",univ ,"is not int ... set to 7")
            univ = 7
        self.univ=univ
        self.sendto = to
        self.portto = port
        print(__name__,"bind",to,port,univ)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.stamp = time.time()
        self.test_stamp = time.time()
        self.dmx=[33]*512
        self.v=0
        self.d=1

    def head(self):
        self._header = []
        self._header.append(b"Art-Net\x00")            # Name, 7byte + 0x00
        self._header.append(struct.pack('<H', 0x5000)) # OpCode ArtDMX -> 0x5000, Low Byte first
        self._header.append(struct.pack('>H', 14))     # Protocol Version 14, High Byte first
        self._header.append(b"\x00")                   # Order -> nope -> 0x00
        self._header.append(struct.pack('B',1))        # Eternity Port

        # Address
        #if 0 <= universe <= 15 and 0 <= net <= 127 and 0 <= subnet <= 15
        net, subnet, universe = (0,0,self.univ) #address
        self._header.append(struct.pack('<H', net << 8 | subnet << 4 | universe))

        self._header = b"".join(self._header)

    def send(self,dmx=None,port=''):
        if dmx is None:
            dmx = self.dmx
        else:
            self.dmx = dmx
        self.head()
        c=[self._header]

        c.append( struct.pack('>H', len(dmx) ) )
        #print([c])

        dmx_count = 0
        for v in dmx:
            if not (type(v) is int or type(v) is float):
                v=0
                
            v = int(v)
            if v > 255: # max dmx value 255
                v = 255
            elif v < 0: # min dmx value 0
                v = 0
            dmx_count += 1
            c.append(struct.pack("B",v))
        c = b"".join(c)
        if port:
            self.s.sendto(c, (self.sendto, port)) # default 6454
        else:
            self.s.sendto(c, (self.sendto, self.portto)) # default 6454
        #print(self.v)
        time.sleep(0.0001)
        return c
    def _test_frame(self):
        if self.test_stamp+(.01) < time.time():
            self.test_stamp = time.time()
            #dmx = [0]*512
            self.dmx[201-1] = self.v
            #self.dmx = dmx
            if self.v >= 255:
                self.d=0
            elif self.v <=0:
                self.d=1

            if self.d:
                self.v+=1
            else:
                self.v-=1
            #print( self.v)
        #time.sleep(1/30.)
    def next(self):
        if self.stamp + (1/30.) < time.time():
            self.send()

def artnet_test():
    #artnet = ArtNetNode(to="127.0.0.1",port=6555,univ=12)
    #artnet = ArtNetNode(to="127.0.0.1",port=6555,univ=0)
    artnet = ArtNetNode(to="10.10.10.255",univ=0)
    #artnet = ArtNetNode(to="2.0.0.255",univ=0)
    #artnet = ArtNetNode(to="10.10.10.255",univ=1)
    while 1:
        artnet._test_frame()
        artnet.next()
        time.sleep(0.01)

if __name__ == "__main__":
    artnet_test()
