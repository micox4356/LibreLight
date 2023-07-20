
import socket
import sys 
import time

import select

import zlib
import base64
import json 
import time

import traceback

import _thread
import _thread as thread


dbg=0

def dummyCB(msg):
    
    t = str(time.time())[7:]
    t = float(t)
    t1 = 0

    try:
        cmd = json.loads(msg["cmd"])
        t1 = cmd#[0]
        t1 = float(t1)
    except:pass
    print("d:",round(t1-t,3),"dummy_CB",msg)

def _compress(msg):
    _msg = msg[:]
    if sys.getsizeof(_msg):
        _msg=zlib.compress(_msg)
    _msg = base64.b64encode(_msg)
    return _msg + b"\00"

def _decompress(msg):
    _msg = b""
    if msg:
        #print("msg**",msg)
        _msg = msg[:]
        if _msg[-1] == b"\00":
            _msg = _msg[:-1]
        _msg = base64.b64decode(msg)

        try:
            _msg=zlib.decompress(_msg)
        except Exception as e:
            print("SERVER decompress err",e)
    
    return _msg

def _send(sock,msg):
    try:
        if dbg:print("_send",[msg])
        if dbg:print()
        _msg = _compress(msg)
        r=sock.send(_msg)
        return r
    except Exception as e:
        print("excep _send",e)


def _recv(sock):
    xmsg=b""
    msg =b""

    try:
        xmsg = sock.recv(1)#1024)#5120)
        if xmsg == b".":
            xmsg = b""
        #print(":",xmsg)
        while xmsg:
            #print(":::",xmsg)
            if xmsg == b"\x00":
                break
            msg += xmsg
            xmsg = sock.recv(1)
            if xmsg == b".":
                xmsg = b""
    except ConnectionResetError as e:
        pass
    except BlockingIOError as e:
        pass
    if msg:
        #if dbg:print("_recvA",[msg]) 
        msg = _decompress(msg)
        if dbg:print("_recvB",[msg]) 
    return msg




class Poll():
    def __init__(self,sock,cb=None,name="<name>"):
        print(name,"Poll.__init__()")
        self.cb = cb
        self.name = name
        self.data_in = []
        self.data_out = []
        self.sock = sock
        self.lock = _thread.allocate_lock()
        _thread.start_new_thread(self._rloop,())
        if cb:
            _thread.start_new_thread(self._wloop,())
    def _get_out(self):
        out = []
        try:
            self.lock.acquire()
            out = self.data_out[:]
            self.data_out = []
        finally:
            self.lock.release()
        return out
    def _wloop(self):
        while 1:
            out = self._get_out()
            #print(self,"_wloop",out)
            if out and self.cb:
                if dbg:print(self.name,"Poll._wloop",out)
                try:
                    self.cb(out,self.sock)
                except Exception as e:
                    print("Exception self.cb",e)
                    print(traceback.format_exc())
            else:
                time.sleep(0.02)

    def _rloop(self):
        msg = b""
        while 1:
            #print(self.name,_loop",self.sock)
            msg = _recv(self.sock)

            if msg:
                if dbg:print(self.name,"Poll._rloop",[msg])#self.sock)
                #print([msg])
                try:
                    self.lock.acquire()
                    self.data_out.append(msg)
                finally:
                    self.lock.release()
            else:
                time.sleep(0.1)

# CORE CLASSES ---

class Server():
    def __init__(self,cb=dummyCB,port=51000):
        print("**** SERVER ***** PORT:",port)
        self._t = time.time()
        self._last_check = time.time()
        self.port=port
        self.cb = cb
        self.clients = [] 
        self._client_nr = 0
        self.msg=b''
        self.select = select.select
        self._poll = []

        self._start()

    def _start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.xs.getsockopt(socket.AF_INET, socket.SO_REUSEADDR )

        while 1:
            try:
                self.server.bind(("", self.port))
                break
            except Exception as e:
                print("except",e)
                print( "SERVER - bind error PORT:",self.port)
                print()
                time.sleep(1)
        
        self.server.listen(1)
        self.client_loop()

    def time(self):
        return self._t - time.time()

    def client_loop(self):
        self.client_lock = _thread.allocate_lock()
        print(dir(self.client_lock),"-----2:") # = _thread.allocate_lock()
        _thread.start_new_thread(self._client_loop,())

    def _client_loop(self):
        print("---- start server loop ----")
        while 1:
            try:
                client, addr = self.server.accept()
                client.setblocking(0)
                self.client_lock.acquire()
                self.clients.append(client)
                self._client_nr += 1
                Poll(client,cb=self.cb,name="Server c:{}".format(self._client_nr))
                print("+++ Client %s open" % addr[0],client)
            finally:
                self.client_lock.release()
                time.sleep(0.2)

    def rem_client(self,client):
        self.client_lock.acquire()
        try:
            self.clients.remove(client)
            #print(dir(client))
            #print((client.family.name))
            print("+++ Client %s close" % client)
        finally:
            self.client_lock.release()

    def get_clients(self):
        self.client_lock.acquire()
        clients = self.clients[:]
        self.client_lock.release()
        return clients

    def _recv(self,sock):
        return _recv(sock)

    def check_client(self):
        if self._last_check+1 < time.time():
            self._last_check = time.time()
            for sock in self.get_clients():
                try:
                    sock.send(b".")
                except BrokenPipeError as e: 
                    self.rem_client(sock)
                except ConnectionResetError as e:
                    self.rem_client(sock)

    def poll(self,cb=None):
        self.check_client()
        idle = 1
        time.sleep(0.1)
        return

        for sock in self.get_clients():
            msg = self._recv(sock)

            if not msg:
                continue

            idle = 0

            msg = {"cmd":msg}
            if cb:
                cb(msg,sock)
            else:
                self.cb(msg)

        if idle:
            time.sleep(0.02)
        


class Client():
    def __init__(self,port=51000,cb=None):
        print("-----CLIENT----- PORT:",port)
        self.port = port
        self.cb = cb
        self._poll = None
        self.connect()
        
    def connect(self,client_name="unkown"):
        self.xip = "127.0.0.1" #raw_input("IP-Adresse: ")
        self.xs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.xs.connect((self.xip, self.port)) #50000))
            self._poll = Poll(self.xs,cb=self.cb,name="Client :x")
        except ConnectionRefusedError as e:
            print("exception 654 ConnectionRefusedError: ", "ERR: {0} ".format(e.args) ,end="")
            print("Server nicht ereichbar/unterbrochen")
            print(self.xip,self.port)
            print(self.xs)
            print("-------")
            time.sleep(1)
            self.connect()
        print("connected !")

    def _recv(self):
        sock = self.xs
        return _recv(sock)

    def read(self):
        return self._recv()

    def send(self,msg):
        r=_send(self.xs,msg)
        if not r:
            self.connect()

    def close(self):
        self.xs.close()

    def __del__(self):
        self.close()




# --- single app ---

PORT=51111
for a in sys.argv:
    if "port=" in a:
        PORT = a.split("=")[-1]
        PORT = int(PORT)

def bounce(data,B=None):
    print("XxX",data)#,B)a
    #data = data.decode()
    for line in data:
        line = json.loads(line)
        for i in line:
            print("line:",i)

def single_client():
    c = Client(port=PORT,cb=bounce)
    if "test" in sys.argv: # test server/client
        run_client_test(c)

    time.sleep(1)
    while 1:
        try:
            i=""
            print()
            i = input("cmd:: ")
            c.send(bytes(i,"utf8"))
            time.sleep(0.5)
            #x=c.read()
            #print(x)
        except Exception as e:
            print("e445",e)


# single server
def single_server():
    server = Server(port=PORT)
    
    while 1:
        server.poll()
        time.sleep(0.001)


# =======================
def main():
    if "client" in sys.argv:
        single_client()
    else: 
        single_server()


if __name__ == "__main__":
    main()



