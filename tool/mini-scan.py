
import socket
import sys
import struct
import time

sys.stdout.write("\x1b]2;Nodescan\x07")

print(socket.AF_INET)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6454))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
except socket.error as e:
    print("Socket 6454 ", "ERR: {0} ".format(e.args))
    sys.exit()
    

def ArtNet_poll(ip,port=6454):
    print("POLL",[ip,port],end="")
    sock.sendto(b'Art-Net\x00\x00 \x00\x0e\x06\x00',(ip,port)) # ArtPol / ping
    print(" OK ;",end="")
    print()


def ArtNet_decode_pollreplay(data):

    debug = 1
    node = {}
    if len(data) >= 10: #min opcode
    
        opcode = data[8:9+1]
        #print([opcode])
        #if opcode != struct.pack("<H",0x5000): #OpPollReplay
        if opcode == struct.pack("<H",0x2100): #OpPollReplay
            if len(data) >= 207: #Mal
                print("decode",data[:13])           
                if debug:print("-----------------------------------------")
                print("===================================================================-")
                if debug:print([opcode] ,"OpPollReplay")
                _ip = []
                print(data[10])
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
                if debug:print([sname,lname,NodeReport])
                
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
                node["MSG"] = msg.replace(b"\x00",b"")
                if debug:print("MSG",[msg])
                
                
                MAC = data[201:201+6]
                _MAC = []
                for x in MAC:
                    #x = hex(ord(x))[2:]
                    x = hex(x)#[2:]
                    x = x.rjust(2,"0")
                    _MAC.append(x)
                #hex(ord("\xf9"))[2:]
                if debug:print("MAC",[":".join(_MAC)])
                node["MAC"] = ":".join(_MAC)
                
                #node_nr += 1
                #if debug:print([addr,data])
                #print()
            else:
                print(opcode, len(data))
    return node


def loop():
    print("-- NODE SCAN START ---")
    print()
    while 1:
        data, addr = sock.recvfrom(500)
        new_node = ArtNet_decode_pollreplay( data )            
        print("rvc loop",addr)
        if new_node:
            print("rcv",new_node)
            #self.add(new_node)
        time.sleep(0.001)
    print("-- NODE SCAN STOP ---")
    print()


#loop()
import _thread as thread
thread.start_new_thread(loop, () )

time.sleep(2)
if __name__ == "__main__":
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    print()
    print()
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)
    print()
    print()


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
    ArtNet_poll("10.0.0.255")
    time.sleep(0.5)
    ArtNet_poll("2.255.255.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.2.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.1.255")
    time.sleep(0.5)
    ArtNet_poll("192.168.0.255")
    time.sleep(0.5)


    while 1:
        time.sleep(1)
