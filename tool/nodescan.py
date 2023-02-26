#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Valid-License-Identifier: GPL-2.0-only
SPDX-URL: https://spdx.org/licenses/GPL-1.0.html

(c) 2012 micha@librelight.de
"""
print("suche ArtNet Nodes ")
import time
import socket, struct
import sys
import _thread as thread
import copy
import random
import traceback

sys.stdout.write("\x1b]2;Nodescan\x07")

print(socket.AF_INET)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6454))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error as e:
    print("Socket 6454 ", "ERR: {0} ".format(e.args))
    #sys.exit()
    
    
    
try:
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.bind(('', 6455))
    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error as e:
    print("Socket2 6455 ", "ERR: {0} ".format(e.args))
    #sys.exit()


print(socket.AF_INET)
sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
def bind_cmd_node():
    global sock_cmd
    try:
        sock_cmd.bind(('', 7601)) #7601
        #sock_cmd.bind(('', 49737))
        sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    except socket_cmd.error as e:
        print("Socket 6454 ", "ERR: {0} ".format(e.args))
        sys.exit()

if __name__ == "__main__":
    bind_cmd_node()  

def ArtNet_poll(ip,port=6454):
    print("POLL",[ip,port],end="")
    #traceback.print_exception()
    #try:
    if 1:
        sock.sendto(b'Art-Net\x00\x00 \x00\x0e\x06\x00',(ip,port)) # ArtPol / ping
        print(" OK ;",end="")
        #send_node_cmd(ip=(2,255,255,255),cmd="CMD GT ")
    #except Exception as e:
    #    print("Exception ArtNet-POLL",e,)

    print()

    
    
def ArtPollReplyDelay():
    time.sleep(1)
    ArtPollReply()
    
def ArtPollReply():
    print("ArtPollReply()")
    
    port = 6454
    content = []
    header = []

    # Name, 7byte + 0x00
    content.append("Art-Net\x00")
    # OpCode ArtPollReply -> 0x2100, Low Byte first
    content.append(struct.pack('<H', 0x2100))
    # Protocol Version 14, High Byte first
    content.append(struct.pack('>H', 14))
    # IP
    #ip = [int(i) for i in self.own_ip.split('.')]
    ip = [2, 0, 0, 10]
    content += [chr(i) for i in ip]
    # Port
    content.append(struct.pack('<H', 0x1936))
    # Firmware Version
    content.append(struct.pack('>H', 200))
    # Net and subnet of this node
    net = 0
    subnet = 0
    content.append(chr(net))
    content.append(chr(subnet))
    # OEM Code (E:Cue 1x DMX Out)
    content.append(struct.pack('>H', 0x0360))
    # UBEA Version -> Nope -> 0
    content.append(chr(0))
    # Status1
    content.append(struct.pack('>H', 0b11010000))
    # Manufacture ESTA Code
    content.append('LL')
    # Short Name
    content.append('LOOP-OpPollReplay\x00')
    # Long Name
    content.append('LOOP-OpPollReplay_ArtNet_Node' + '_' * 34 + '\x00')

    content.append('\x00'*100)
    # stitch together
    content = ''.join(content)
    #print(self.lang['send_ArtPollReply'])
    #self.s.sendto(content, ("<broadcast>", self.__port))
    
    print("send" ,[content])
    sock.sendto(content, ("<broadcast>", port))
    sock.sendto(content, ("2.0.0.255", port))
    sock.sendto(content, ("10.10.10.255", port))
    sock.sendto(content, ("192.168.2.255", port))
    #sock.sendto(content, ("2.0.0.255", port))
    #sock.sendto

def testBounce(ip,port):
    
    print(("TESTBOUNCE", (ip, port)))
    try:
        sock.sendto("TESTBOUNCE " +ip, (ip, port))
    except socket.error as e:
        print("Socket", "ERR: {0} ".format(e.args))
        print(("TESTBOUNCE", (ip, port)))
        
    
    
def reciveBounce(timeout=10):
    start = time.time()
    while 1:
        data = sock.recv(500)
        print("bounce",data)
        #data, addr = sock.recvfrom(500)
        if data:
            #print(addr)
            
            print("rBounte:",data)
            print()
        if time.time() > start+timeout:
            print("timeout stopping reciveBounce ")
            break 
        
def poll():
    port = 6454
    
    #ip   = "255.255.255.255"
    #ArtNet_poll(ip)
    #ip   = "<broadcast>"
    #ArtNet_poll(ip)
    ip   = "192.168.0.255"
    ArtNet_poll(ip)    
    ip   = "192.168.0.99"
    ArtNet_poll(ip)    
    ip   = "2.255.255.255"
    ArtNet_poll(ip)    
    ip   = "2.0.0.255"
    ArtNet_poll(ip)    

    ip   = "2.255.255.255"
    ArtNet_poll(ip)    
    #ip   = "2.0.0.255"
    #ArtNet_poll(ip)
    #ip   = "2.255.255.255"
    #ArtNet_poll(ip)
    print("")
    
class ArtNetNodes():
    def __init__(self):
        print("CONSTRUCKT:",self)
        self.__nodes = []
        self.__nodes_mac = []
        self.__lock = thread.allocate_lock()
        self.__tick = 0
        #self.__lock.acquire()
        #self.__lock.release()
    def clear(self):    
        self.__lock.acquire()
        self.__nodes = []
        self.__lock.release()    
    def add(self,add_node):        
        #print("ArtNetNodes.add()",add_node)
        #for i in add_node:
        #    print(i,[add_node[i]])
        #print()
        #print("add",add_node)
        try:
            self.__lock.acquire()
            update_node = 0
            if "MSG" in add_node and "BOOT" in add_node["MSG"].upper():
                BOOT = time.time()
                print("   BOOOOOOOOT")
            else:
                BOOT = 0            
        
            #self.__nodes_mac = []
            for node in self.__nodes:
                info = node["MAC"],node["IP"].ljust(16," "),[node["SwIn"],node["SwOut"],node["PortTypes"]]
                
            
                
                node_match = 1 
                keys = ["MAC","SwOut","SwIn","PortTypes"]
                for i in keys:
                   if node[i] != add_node[i]:
                       node_match = 0
                       break
                
                if node_match: # NODE MAC                
                    update_node = 0
                    for i in add_node:
                        UPDATECOUNTER = node["UPDATECOUNTER"]                    
                        #print("update i:",i,add_node[i])
                        if i not in node:    
                            node[i] = ""
                        if node[i] != add_node[i]:
                            node_match = 0
                            update_node += 1
                            node[i] = add_node[i]
                            UPDATECOUNTER +=1
                            self.__tick += 1
                            #break
                            
                    if update_node:
                        node["UPDATECOUNTER"] = UPDATECOUNTER
                        node["UPDATESTAMP"] = time.time()
                        node["REFRESHSTAMP"] = time.time()
                        if BOOT:
                            node["BOOT"] = BOOT
                            
                        print("UPDATE NODE".ljust(16," "),info)
                        
                    else:
                        #print("NODE NOT CHANGE".ljust(16," "),info)
                        node["REFRESHSTAMP"] = time.time()
                        update_node = 1
                update_node = 0
            print("x-node:",update_node,add_node)                
            if not update_node: # ADD NEW NODE
                node = add_node
                if node:
                    print("add_node",node)
                    node["BOOT"] = BOOT
                    info = node["MAC"],node["IP"].ljust(16," "),[node["SwIn"],node["SwOut"],node["PortTypes"]]
                    
                    node["UPDATECOUNTER"] = 1
                    node["REFRESHSTAMP"] = time.time()
                    node["UPDATESTAMP"] = time.time()
                    print("ADD NEW NODE".ljust(16," "),node["UPDATECOUNTER"],info)
                    self.__tick += 1
                    self.__nodes += [node]
                  
            
        finally:
            #print("release lock")
            self.__lock.release()
    def tick(self):
        self.__lock.acquire()
        x = self.__tick
        self.__lock.release()
        return x
        return random.randint(0,1000)
        
    def get(self):
        self.__lock.acquire()
        out = []
        #out = {}
        if self.__nodes:
            out = copy.deepcopy(self.__nodes)                
            #for node in self.__nodes:
            #    out[node["MAC"]] = node
        self.__lock.release()
        return out

    def recive(self):
        print("-- NODE READ LOOP START ---")
        print()
        while 1:
            data, addr = sock.recvfrom(300)
            new_node = ArtNet_decode_pollreplay( data )            
            #print("rvc loop",addr)
            if new_node:
                #print("rcv 333",new_node)
                self.add(new_node)
            time.sleep(0.001)
        print("-- NODE READ LOOP END ---")
        print()
        
    def loop(self):
        thread.start_new_thread(self.recive, () )
        time.sleep(5)
        #poll()
        
Reciver = ArtNetNodes



def ArtNet_decode_pollreplay(data):

    debug = 0
    node = {}
    if len(data) >= 10: #min opcode
    
        opcode = data[8:9+1]
        #print([opcode])
        #if opcode != struct.pack("<H",0x5000): #OpPollReplay
        if opcode == struct.pack("<H",0x2100): #OpPollReplay
            if len(data) >= 207: #Mal
                #if debug:print("-----------------------------------------")
                print("===================================================================-")
                print("decode",data[:13])           
                if debug:print([opcode] ,"OpPollReplay")
                _ip = []
                #print("data[10]",data[10])
                _ip.append( data[10] )
                _ip.append( data[11] )
                _ip.append( data[12] )
                _ip.append( data[13] )
                node["IP"] = str(_ip)
                
                if debug:print([_ip])
                _port = struct.unpack("<H",data[14:15+1] )
                #Versinfo = struct.unpack("<H",data[16:17+1] )
                Versinfo = data[16:17+1] 
                node["port"] = _port
                if debug:print("_port :", [_port ])
                
                node["version"] = Versinfo
                if debug:print("Version:",[Versinfo])
                
                NetSwitch = data[18] 
                node["NetSwitch"] = NetSwitch
                if debug:print("NetSwitch:",[NetSwitch])
                SubSwitch = data[19] 
                node["SubSwitch"] = SubSwitch
                if debug:print("SubSwitch:",[SubSwitch])
                
                #oem = struct.unpack("<H",data[19:20+1] )
                oem = data[20:21+1]
                node["oem"] = oem
                if debug:print("oem",[oem])
                
                ubea = data[22]
                node["ubea"] = ubea
                if debug:print("ubea ver.",[ubea])
                stat = data[23]
                node["status"] = stat
                if debug:print("Status1 ",[stat])
                esta = data[24:25+1]
                node["esta"] = esta
                if debug:print("esta Manuf",[esta])
                
                
                sname = data[26:26+17]
                #if debug:print(len(sname) #17+1)
                sname = sname.strip(b"\x00")
                node["sname"] = sname
                
                lname = data[44:44+43]
                #if debug:print(len(lname) #43+1)
                lname = lname.strip(b"\x00")
                node["lname"] = lname
                
                NodeReport = data[108:108+20]
                NodeReport = NodeReport.strip(b"\x00")
                #if debug:print("Node",node_nr,addr)
                if debug:print("43r:",[sname,lname,NodeReport])
                
                NumPort =  data[173] 
                node["NumPort"] = NumPort
                if debug:print("NumPort",[NumPort])
                
                PortTypes = data[174:174+4]
                node["PortTypes"] = PortTypes
                if debug:print("PortTypes",[PortTypes])
                
                GoodInput = data[178:178+4]
                node["GoodInput"] = GoodInput
                if debug:print("GoodInput",[GoodInput])
                GoodOutput = data[182:182+4]
                node["GoodOutput"] = GoodOutput
                if debug:print("GoodOutput",[GoodOutput])
                
                SwIn = data[186:186+4]
                node["SwIn"] = SwIn
                if debug:print("SwIn",[SwIn])
                
                SwOut = data[190:190+4]
                node["SwOut"] = SwOut
                if debug:print("SwOut",[SwOut])
                
                msg = data[108:108+40]
                node["MSG"] = msg.replace(b"\x00",b"")#.decode(errors="ignore")
                if debug:print("MSG",[msg])
                
                
                MAC = data[201:201+6]
                _MAC = []
                for x in MAC:
                    #x = hex(ord(x))[2:]
                    x = hex(x)[2:]
                    x = x.rjust(2,"0")
                    _MAC.append(x)
                #hex(ord("\xf9"))[2:]
                if debug:print("MAC",[":".join(_MAC)])
                node["MAC"] = ":".join(_MAC)
                
                #node_nr += 1
                #if debug:print([addr,data])
                #print()

                for k,v in node.items():
                    if type(node[k]) is bytes:
                        node[k] = v.decode(errors="ignore")
            else:
                print(opcode, len(data))
    return node


def ArtAddress(ip="192.168.0.99" ,ShortName="ShortName", LongName="LongName",Port="",Universes=0,raw=0):
    node_nr = 1

    #send port
    port = 7600
    port = 6454

    print( ip)
    data = [] # [struct.pack('<B', 0)]*150
    header = []
    # Name, 7byte + 0x00
    header.append(b"Art-Net\x00")
    # OpCode ArtDMX -> 0x6000, Low Byte first
    header.append(struct.pack('<H', 0x6000))
    # Protocol Version 14, High Byte first
    header.append(struct.pack('>H', 14))

    data = header[:]
    # NetSwitch
    data.append(struct.pack('<B',128)) # no change 0x7f
    data.append(struct.pack('<B', 0))     # filler

    #Short Name
    sname = ShortName[:17] 
    sname = sname.ljust(18,"\x00")
    data.append( sname )

    lname = LongName[:63] 
    lname = lname.ljust(64,"\x00") 
    #lname = lname[:-2]+"X\x00"
    data.append( lname )

    print( "len sname:lname",len(sname),len(lname))

    #SwIn 4; Port-Adress
    # univers 0-f == \x80 - \x8f
    i = 4
    i=int(Universes)+1 #random.randint(0,99)
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))


    #SwOut 4; Port-Adress
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))
    data.append(struct.pack('<B', 127+i))

    #SubSwitch comination with Swin[] SwOut[]
    data.append(struct.pack('<B', 0)) # SubSwitch Write 128
    data.append(struct.pack('<B', 255))
    data.append(struct.pack('<B', 0))
    data.append(struct.pack('<B', 0))

    #data.append("\xf4")

    #print( ["ArtAdress SEND:",data,(ip,port)] )
    data2 = b""
    for d in data:
        #print(d,type(d))
        if type(d) is str:
            data2+=bytes(d,"utf-8")
        elif type(d) is bytes:
            data2+=d
        else:
            data2+=bytes(str(d),"ascii")
    print(data2)
    if raw:
        return data2,(ip,port)
    sock.sendto(data2 ,(ip,port))


def set_ip4(cur_ip=(2,0,0,91),new_ip=(2,0,0,201),new_netmask=(255,0,0,0)):
    
    #send ip
    port = 7600
    
    #print(ip)
    data = []
    #New ip
    #_ip = [192, 168,   2,  91]
    _ip = [  2,   0,  0, 181] # CLASS C NET
    _ip = [  2,   0,  0, 101] # CLASS C NET
    #_ip = [192, 168,  0,  91]
    _ip = new_ip
    
    print("NEW NODE _ip:", _ip)
    data.append(struct.pack('<B', _ip[0]))
    data.append(struct.pack('<B', _ip[1]))
    data.append(struct.pack('<B', _ip[2]))
    data.append(struct.pack('<B', _ip[3]))

    #_ip = [255, 255, 255, 255] # cange all nodes in Network to the same _ip ! DANGER !
    #_ip = [002, 000, 000, 255] # cange all nodes in subnet to the same _ip ! DANGER !
    _ip = [  2,   0,   0, 199]  # CLASS A NET
    _ip = [192, 168,   0,  91]
    #_ip = [  2,   0,  0, 191] # CLASS C NET
    _ip = cur_ip
    
    print("OLD NODE _ip:", _ip)
    #OLD _ip , Target Node to change
    data.append(struct.pack('<B', _ip[0]))
    data.append(struct.pack('<B', _ip[1]))
    data.append(struct.pack('<B', _ip[2]))
    data.append(struct.pack('<B', _ip[3]))
    
    ip = ".".join(str(x) for x in _ip)
    #print("send to ip:", ip)
    
        
    # NETMASK
    MASK = []
    netmask = [255, 255, 255 ,  0] #fast CLASS C funktioniert
    #netmask = [255, 0, 0 ,  0]  #CLASS C funkioniert nicht
    netmask = new_netmask
    print("NEW NODE net:",netmask)
    MASK.append(struct.pack('<B', netmask[0]))
    MASK.append(struct.pack('<B', netmask[1]))
    MASK.append(struct.pack('<B', netmask[2]))
    MASK.append(struct.pack('<B', netmask[3]))
    
    data += MASK
    data += [struct.pack('<B', 255)]*11 
    
    
    print("------------------------------")
    data = b'CMD IP '+ b"".join(data)
    
    print("SENDING TO ",(ip,port))
    print([data]) #,    cur_ip=(2,0,0,91))
        
    #sock.sendto(data ,(ip,port))
    sock.sendto(data ,(ip,port))


def send_cmd(ip=(2,0,0,91),cmd=""):
    node_nr = 1
    port = 7600
    
    print(ip)
    data = []
    
    _ip = [  2,   0,  0, 91] # CLASS C NET
    
    
    print("NEW NODE _ip:", _ip)
    data.append(struct.pack('<B', _ip[0]))
    data.append(struct.pack('<B', _ip[1]))
    data.append(struct.pack('<B', _ip[2]))
    data.append(struct.pack('<B', _ip[3]))

    #_ip = [255, 255, 255, 255] # cange all nodes in Network to the same _ip ! DANGER !
    #_ip = [002, 000, 000, 255] # cange all nodes in subnet to the same _ip ! DANGER !
    _ip = [  2,   0,   0, 199]  # CLASS A NET
    _ip = [  2,   0,   0, 91]  # CLASS A NET
    #_ip = [192, 168,   0,  91]
    _ip = [  2,   0,  0, 255] # CLASS C NET
    #_ip = [  2,   255,  255, 255] # CLASS C NET
    
    print("OLD NODE _ip:", _ip)
    #OLD _ip , Target Node to change
    data.append(struct.pack('<B', _ip[0]))
    data.append(struct.pack('<B', _ip[1]))
    data.append(struct.pack('<B', _ip[2]))
    data.append(struct.pack('<B', _ip[3]))
    
    ip = ".".join(str(x) for x in ip)
    print("send to ip:", ip)
    
        
    # NETMASK
    MASK = []
    netmask = [255, 255, 255 ,  0] #fast CLASS C funktioniert
    netmask = [255, 0, 0 ,  0]  #CLASS C funkioniert nicht
    print("NEW NODE net:",netmask)
    MASK.append(struct.pack('<B', netmask[0]))
    MASK.append(struct.pack('<B', netmask[1]))
    MASK.append(struct.pack('<B', netmask[2]))
    MASK.append(struct.pack('<B', netmask[3]))
    
    data += MASK
    data += [struct.pack('<B', 255)]*11 
    print("------------------------------")
    data = 'CMD '+cmd+' '+ "".join(data)
    
    print("SENDING TO ",(ip,port))
    print([data]    )
        
    #sock.sendto(data ,(ip,port))
    sock.sendto(data ,(ip,port))


def pack_ip(_ip):
    data = [b"\x00",b"\x00", b"\x00", b"\x00"]
    if _ip:
        data[0] = struct.pack('<B', int(_ip[0]))
        data[1] = struct.pack('<B', int(_ip[1]))
        data[2] = struct.pack('<B', int(_ip[2]))
        data[3] = struct.pack('<B', int(_ip[3]))
    return data

def send_node_cmd(ip="",ip2="",cmd=""):
    print()
    port = 7600
    data = []
    print("send_node_cmd",ip,ip2,cmd,port)
    
    data = pack_ip(ip[:])
    
    print("ip",ip,ip2)
    if len(ip2) == 4:
        ip = ip2
    if len(ip) == 4:
       ip = ".".join(map(str,ip))

    print("send to ip:", ip)
    data2=""
    if not cmd:
        data2 = 'CMD GT'
        data2 = 'CMD ST'
        data2 = 'DMX OUT STORE'
        data2 = 'CMD DMX=IN '
        data2 = 'CMD DMX=OUT '
        data2 = 'CMD DMX=PIN '

    if type(cmd) == bytes:
        data2 = cmd
    else:
        data2 = bytes(str(cmd),"ascii",errors="ignore")

    print([data2],type(data2)    )
    data2 = data2.ljust(20,b" ") + b"".join(data)

    print("SENDING COMMAND TO ",[data2],(ip,port))
    sock.sendto(data2 ,(ip,port))
    

node_cmd_buf_list = []
    
def node_cmd_recive():
    global node_cmd_buf_list
    #sock.sendto('\x00\x00\x00\x00\x00',(ip,port)) # ArtPol / ping
    while 1:
        data, addr = sock_cmd.recvfrom(5000)
        #print(len(data))
        #print([addr,data])
        if len(data) == 207:
            print()
        else:
            print("NODE CMD RESPONSE:", [addr,data])
            node_cmd_buf_list = [addr,data]
        
            #print([data])
            pass
        time.sleep(0.05)





#send_node_cmd(ip="",cmd="CMD DMX=IN")
#send_node_cmd(ip="",cmd="CMD DMX=OUT")
#send_node_cmd(ip=(2,0,0,91),cmd="CMD DMX=PIN")
#send_node_cmd(ip=(2,0,0,91),cmd="DMX OUT STORE")

#send_node_cmd(ip=(2,0,0,255),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,201),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,255),ip2=(2,255,255,255),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,201),ip2=(2,255,255,255),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,255),ip2=(2,0,0,201),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,201),ip2=(2,0,0,201),cmd="DMX OUT STORE")
#send_node_cmd(ip=(2,0,0,201),ip2=(255,255,255,255),cmd="DMX OUT STORE")
#send_node_cmd(ip=(255,255,255,255),ip2=(255,255,255,255),cmd="DMX OUT STORE")
#exit()
#   
if __name__ == "__main__":        

    thread.start_new_thread(node_cmd_recive, () )
    #send_node_cmd(ip=(2,0,0,91),cmd="DMX OUT STORE")
    send_node_cmd(ip=(2,255,255,255),cmd="CMD GT ")
   

    rx = ArtNetNodes()
    rx.loop()
    z = 0
    while 1:
        
        nodes = rx.get()
        #print(len(nodes))
        
        if z % 10 == 0:
            print()
            pass
            
        
            print("node count",len(nodes),rx.tick(),2 )
            #for i in nodes:
            #print(i)
        z += 1
        time.sleep(0.2)
        
    print()
    print("time out")
    raw_input("ENDE")

