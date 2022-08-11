
import socket
import sys 
import time

import select

import zlib
import base64
import json 

import _thread

def dummyCB(msg):
    print("dummy_CB",msg)



class Server():
    def __init__(self,cb=dummyCB,port=51000):
        print("**** SERVER *****")
        self._t = time.time()
        self._last_check = time.time()
        self.port=port
        self.cb = cb
        self.clients = [] 
        self.msg=b''
        self.select = select.select

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
                print( "bind error")
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
                print("+++ Client %s open" % addr[0])
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
        xmsg=b""
        msg =b""

        try:
            xmsg = sock.recv(1)#1024)#5120)
            while xmsg:
                if xmsg == b"\x00":
                    break
                msg += xmsg
                xmsg = sock.recv(1)

            idle = 0
        except ConnectionResetError as e:
            pass
        except BlockingIOError as e:
            pass
        
        if msg:
            #print("msg**",msg)
            print("B64",sys.getsizeof(msg),len(msg))
            msg = base64.b64decode(msg)
            ##print("msg**",msg)
            ##msg = msg.decode("utf8")
            print("str",sys.getsizeof(msg),len(msg))

            try:
                msg=zlib.decompress(msg)
                print("uzip",sys.getsizeof(msg),len(msg))
                print("msg",msg)
            except Exception as e:
                print("SERVER decompress err",e)
                #msg = b"decompression error"

        
        return msg
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

    def poll(self):
        run = 1
        #try:
        if 1: #while run:
            self.check_client()
            idle = 1
            for sock in self.get_clients():
                #print(dir(sock))
                msg = self._recv(sock)

                if not msg:
                    continue

                idle = 0

                msg = msg.replace(b"\x00 ",b"")
                msg = {"cmd":msg}
                self.cb(msg)

        if idle:
            time.sleep(0.02)
        
        #finally:pass
        #except KeyboardInterrupt:
        #    print(" strg+c")
        #finally:
        #    for c in clients:
        #        print(c,"close")
        #        c.close()
        #    server.close()
        #    print("server close")
CMD = Server

def cmd(cb=dummyCB,port=51000):
    print("----cmd")
    x=CMD(cb=cb,port=port)
    while 1:
        x.poll()


class Client():
    def __init__(self,port=51000):
        print("-----CLIENT-----")
        self.port = port
        self.connect()
        
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

    def send(self,nachricht):
        try:
            #print(sys.getsizeof(msg),len(msg))

            if sys.getsizeof(nachricht):
                nachricht=zlib.compress(nachricht)
            #nachricht = bytes(nachricht,"utf-8")
            nachricht = base64.b64encode(nachricht)
            self.xs.send(nachricht + b"\00")
        except socket.error as e:
            self.connect()
        time.sleep(0.0001)
    def close(self):
        self.xs.close()
    def __del__(self):
        self.close()

tcp_sender = Client


if __name__ == "__main__":
    if "client" in sys.argv:
        c = Client()
        if "test" in sys.argv: # test server/client
            import random 
            import string
            client = c

            try:
                for i in range(100):
                    x=random.choice(string.printable)
                    msg=bytes("hi"+str(x*random.randint(10,9999)),"utf-8")
                    print(x,sys.getsizeof(msg),len(msg))
                    client.send(msg)
                    time.sleep(0.01)
            except Exception as e:
                print("e",e)
            finally:
                client.close()

            try:
                client = Client()
                for i in range(100):
                    x=random.choice(string.printable)
                    msg=bytes(x,"ho "+str(x*random.randint(10,9999)),"utf-8")
                    print(sys.getsizeof(msg),len(msg))
                    msg=zlib.compress(msg)
                    print(sys.getsizeof(msg),len(msg))
                    client.send(msg)
                    time.sleep(0.01)
            except Exception as e:
                print("e",e)
            finally:
                client.close()
        time.sleep(1)
        while 1:
            try:
                i=""
                i = input("cmd:")
                c.send(bytes(i,"utf8"))
            except Exception as e:
                print("e",e)
    else: 
        server = Server()
        
        while 1:
            server.poll()
            time.sleep(0.00001)



