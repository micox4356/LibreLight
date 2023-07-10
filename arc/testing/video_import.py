import time
import os
import _thread as thread
import cv2
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("", "--videoplayer", dest="videoplayer",#default=1,
              help="enable videoplayer") #, metavar="FILE")
(options, args) = parser.parse_args()

PLAYLIST = []
play_list = "/home/user/LibreLight/video/" #.format(path)

def open_playlist():
    print()
    print("======== OPEN PLAYLIST DIR !!",play_list)

    if not os.path.isdir(play_list):
        os.system("mkdir -p {}".format(play_list))

    _lines = os.listdir(play_list)
    _lines.sort()

    lines = ['']*25 # first is empty
    i=0
    for l in _lines:
        #print(">> ",l.strip(),len(lines))
        l = l.strip()
        if "_" in l:
            ll = l.split("_",1)
            print(">> ",ll)
            #ll = int(ll)
            try:
                lll = int(ll[0])
                #lines.append(l.strip())
                lines[lll] = l
            except:pass

    if len(lines) <= 10:
        for i in range(10-len(lines)):
            lines.append("")#"LINE ERROR")
    return lines

PLAYLIST_TIME = time.time()
PLAYLIST = open_playlist()

def rescale_frame2(frame, width):
    height = int(frame.shape[0]/frame.shape[1] * width )
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def rescale_frame(frame, percent=75):
    width  = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

class Vopen2():
    def __init__(self,dmx=None,_id=None):
            self.buffer = []
            self._run = 0
            self.fps = 1
            self.scale = 1
            self.fpath = "/home/user/LibreLight/video/"
            self.fname = "xx.mp4"
            self.cv2 = cv2
            self.dim = 0
            self.dmx = 0
            self.Rsuccess = 1
            self.Rcap = None
            self._video_nr=-1
            self._init()
    def next(self):
        pass
    def buf_size(self):
        sizeof = 0
        for i in self.buffer:
            sizeof += sys.getsizeof(i)

        #sizeof = sys.getsizeof(self.buffer)
        sizeof = sizeof/8/1024
        sizeof = sizeof/100 # gets real mb
        sizeof = int(sizeof)
        return sizeof

    def __repr__(self):
        sizeof = self.buf_size()

        return "< id:{}.. buf:{} run:{} fps:{} scale:{} name:{} sof:{}>".format(
                int(id(self)/10000000),len(self.buffer),self._run,self.fps,self.scale
                ,self.fname,sizeof
                )

    def select_video(self,dmx_value):
        print()
        print(self,"select_video()",dmx_value)
        try:
            dmx_value = int(dmx_value/10)

            if self._video_nr != dmx_value:
                self._video_nr = dmx_value

                if self._video_nr < len(PLAYLIST):
                    self.fname = str(PLAYLIST[self._video_nr])
                    print("- fname:",self.fname)
                    self._init()

        except Exception as e:
            print("Vopen.select_video()",dmx_value,e)

    def _init(self):
        print(self)
        print("videoplayer.init()",self.fpath,self.fname)

        if not os.path.isfile(self.fpath+self.fname):
            print("-- video file does not exits !! >",self.fpath,self.fname)
            print()
    
        self.Rsuccess = 0
        if self.cv2:
            self.Rcap = self.cv2.VideoCapture(self.fpath+self.fname, cv2.CAP_FFMPEG) 
            self.Rcap.read()
            self.Rsuccess = 1
            self._read()


    def _read(self):
        success = self.Rsuccess
        ok = 0
        if success and self.fname:
            cap = self.Rcap
            _break = 0

            try:
                success, img = cap.read()
                if not success:
                    self.Rcap.release()
                    self.Rcap.retrieve()
                    self.end = 1
                    return

                if self.fps == 0:
                    self.fps = cap.get(cv2.CAP_PROP_FPS)
                
                img = self.cv2.cvtColor(img, self.cv2.COLOR_BGR2RGB)
                img = rescale_frame2(img, 200)  # 1MB -> 45MB, saves MEMORY / RAM
                #img = rescale_frame2(img, 400) # 1MB -> 215MB
                
                # store frame into buffer list
                self.buffer.append(img)
                ok = 1
                if len(self.buffer) % 100 == 0:
                    _id = str(self.__repr__)[-5:-1]
                    print(_id,"video read",self.dmx,len(self.buffer),self.fname,"fps",self.fps,self.dim)

            except Exception as e:
                print("Excetpion","_init",self,e,end="")
        self.success = 1
        return ok



import sys
sys.path.insert(0,"../lib/")

        
if len(sys.argv) > 1 and sys.argv[1] == "client":
    pass
else:
    sstart = time.time()
    #v=Vopen() 
    v=Vopen2() 

    #input("start ?")
    v.select_video(20)
    #v.select_video(30)
    b1 = -1
    b2 = 0
    #for i in range(100):
    i=0
    print()
    while 1:
        v._read()
        #print(i,v)
        if b1 == len(v.buffer):
            break
        else:
            b1 = len(v.buffer)
        i+=1


    print(i,v)
    v.next()

    stime = time.time() - sstart
    l = len(v.buffer)
    print("frames",l,"fps:",int(l/stime))

    print(len(v.buffer),v)
    #input("end")


# ----------------------

import socket
import sys
import time


class tcp_sender(object):
    def __init__(self,port=50000):
        self.port = port
        self.buffer = []
        self.connect()
        self.loop()

    def connect(self,client_name="unkown"):
        self.xip = "127.0.0.1" #raw_input("IP-Adresse: ")
        self.xs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.xs.connect((self.xip, self.port)) #50000))
        except ConnectionRefusedError as e:
            print("ConnectionRefusedError: ", "ERR: {0} ".format(e.args) ,end="")
            print("Server nicht ereichbar/unterbrochen")
            time.sleep(1)
            self.connect()
        print("connected !")

    def read(self):
        #client.setblocking(0)
        x=[]
        out = 0
        while 1:
            _x = self.xs.recv(1)
            if b'\x0c' == _x:
                break
            if not _x:
                break
            x.append(_x)


        if x:
            x=b"".join(x) 
            if len(x) < 20:
                print("read::",x)
            else:
                print("read::",len(x))
            self.buffer.append(x)
            self.read()
            out = 1

        return out

    def poll(self):
        while 1:
            self.read()

    def loop(self):
        thread.start_new_thread(self.poll,())


    def send(self,nachricht):
        try:
            #self.xs.send(bytes(nachricht+";","utf-8") )
            msg = nachricht
            msg = bytes(msg,encoding="ascii",errors="ignore") #+b";"
            self.xs.send(msg+b";" )
        except socket.error as e:
            self.connect()
    def close(self):
        self.xs.close()



def dummyCB(msg):
    print("dummy_CB",msg)


def cmd(cb=dummyCB,port=50000):
    x=CMD(cb=cb,port=port)
    while 1:
        x.poll()

import socket
import select
class CMD():
    def __init__(self,cb=dummyCB,port=50000):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.xs.getsockopt(socket.AF_INET, socket.SO_REUSEADDR )

        while 1:
            try:
                server.bind(("", port))
                break
            except Exception as e:
                print("except",e)
                print( "bind error")
                time.sleep(1)



        server.listen(1)

        clients = []
        clients2 = [""]*300
        self.server = server
        self.clients = clients
        self.clients2 = clients2
        self.cb=cb
        self.select=select
        self.msg=b''
    def poll(self):
        server  = self.server
        clients = self.clients
        clients2 = self.clients2
        cb=self.cb
        select=self.select
        try:
            #if 1: #
            while True:
                try:
                    lesen, schreiben, oob = select.select([server] + clients,
                                                      [], [])
                except:
                    return 0
                for sock in lesen:
                    if sock is server:
                        client, addr = server.accept()
                        client.setblocking(0)
                        clients.append(client)
                        print("+++ Client %s verbunden" % addr[0])
                        #sock.send("hi du")
                    else:
                        msg=b''
                        try:
                            if self.msg:
                                xmsg = self.msg
                            else:
                                xmsg = sock.recv(1)#1024)#5120)
                            while xmsg:# != b"\x00":
                                if b'\x00' in xmsg:
                                    s = xmsg.split(b"\x00",1)
                                    msg += s[0]
                                    self.msg = s[1]
                                    break
                                msg += xmsg
                                xmsg = sock.recv(1)#5120)
                                #xmsg = xmsg.replace(b";",b"")
                            #print(msg)
                        except ConnectionResetError as e:
                            print( "exception",e)
                            pass 
                        except BlockingIOError as e:
                            print( "exception",e)
                            pass 

                        if not msg:
                            continue


                        print(msg,type(msg))
                        if type(msg) is not bytes:
                            msg = bytes(msg,encoding="ascii",errors="ignore") 

                        msg = msg.strip()
                        msg = msg.replace(b"EOB",b"")

                        if sock in clients:
                            client_nr = clients.index(sock)
                        ip = sock.getpeername()[0]

                        if msg:
                            tstamp = time.strftime("%H:%M:%S")

                            for xx,msg in enumerate(msg.split(b";")):
                                cmd = msg
                                if cmd:
                                    cmd += b'\x0c' #b"\ff"
                                    cb({"cmd":cmd},args={"client":client,"addr":addr})
                        else:
                            time.sleep(0.0001)
        except KeyboardInterrupt:
            print(" strg+c")
        finally:
            for c in clients:
                print(c,"close")
                c.close()
            server.close()
            print("server close")


PORT = 54001


def CB(msg,args={}):
    print()
    print("CB",msg)
    #print("CB",msg)
    #print(dir(msg["client"]))
    if "client" in args:
        print("-",args)
        r = msg["cmd"][:-1]
        lb = len(v.buffer) 
        if 1:
            try:
                a=0
                b=0
                if b"-" in r:
                    a,b = r.split(b"-") 
                a = int(a)
                b = int(b)
                _ok = 0
                if lb > a and lb > b:
                    frame = v.buffer[a:b]
                    for f in frame:
                        print("a",len(f))
                        args["client"].send(f)
                        args["client"].send(b"\x0c")
                        time.sleep(0.001)
                        _ok += 1
                    if _ok:
                        print("#",_ok)
                        return
            except Exception as e:
                print("3-.",e)
            try:
                p = int(r)
                if lb > p:
                    rr = v.buffer[p]
                    args["client"].send(rr)
                    args["client"].send(b"\x0c")
                    time.sleep(0.001)
                    return 
            except Exception as e:
                print("4-.",e)

        if len(r) < 20:
            print("5:- ok",type(r),len(r),r)
        else:
            print("6:- ok",type(r),len(r))
        args["client"].send(r)
        args["client"].send(b"\x0c")

    print("-")


if __name__ == "__main__":
    print( sys.argv )
    if len(sys.argv) >= 2:
        if sys.argv[1] == "server":
            cmd(port=PORT,cb=CB)
        elif sys.argv[1] == "client":
            c = tcp_sender(port=PORT)
            while 1:
                x = input(":: ")
                c.send(x)
                time.sleep(0.2)



exit()






