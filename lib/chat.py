#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is part of librelight.

librelight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

librelight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with librelight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha@librelight.de
"""

import socket
import sys 
import time


class tcp_sender(object):
    def __init__(self,port=50000):
        self.port = port
        self.connect()
        
    def connect(self,client_name="unkown"):
        self.xip = "127.0.0.1" #raw_input("IP-Adresse: ")
        self.xs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("port:",self.port)
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
            #self.xs.send(bytes(nachricht+";","utf-8") )
            self.xs.send(nachricht.encode("utf-8")+b";" )
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
            print("bind port:",port)
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
                        except BlockingIOError as e:
                            pass#print( "exception",e)

                        if not msg:
                            continue

                            
                        nachricht = msg
                        #print(msg)
                        #nachricht = str(nachricht,"utf-8")
                        nachricht = nachricht.replace(b";",b"")
                        nachrichten = nachricht.strip().replace(b"EOB",b"")
                        if b"client_name:" in nachrichten:
                            if sock in clients:
                                client_nr = clients.index(sock)
                                clients2[client_nr] = nachrichten
                        if sock in clients:
                            client_nr = clients.index(sock)
                            #print(clients2[client_nr])
                        ip = sock.getpeername()[0]
                        #print(">>>", ip, nachrichten.split(";"))
                        if nachrichten:
                            tstamp = time.strftime("%H:%M:%S")

                            #print("from:",client_nr,">>>", tstamp , ip, nachrichten.split(";"))
                            for xx,nachricht in enumerate(nachrichten.split(b";")):
                                cmd = nachricht #.split(" ")
                                #print(xx,cmd)
                                cb({"c":client_nr,"cmd":cmd})


                        else:
                            time.sleep(0.0001)
                        #else: #workaround json sock pkg-drops
                        #    print("+++ Verbindung zu %s beendet" % ip)
                        #    sock.close()
                        #    if sock in clients:
                        #        client_nr = clients.index(sock)
                        #        clients2[client_nr] = ""
                        #    clients.remove(sock)
        except KeyboardInterrupt:
            print(" strg+c")
        finally:
            for c in clients:
                print(c,"close")
                c.close()
            server.close()
            print("server close")


if __name__ == "__main__":
    print( sys.argv ) 
    if sys.argv[1] == "server":
        cmd()
    elif sys.argv[1] == "client":
        c = tcp_sender()
        while 1:
            x = input(":: ")
            c.send(x)


