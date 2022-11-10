#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of librelight.

librelight is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

librelight is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with librelight.  If not, see <http://www.gnu.org/licenses/>.

(c) 2012 micha.rathfelder@gmail.com
"""

import time
import struct
import sys
import tkinter as Tkinter
import _thread as thread

import nodescan_v6_2 as nodscaner 

title = "TK-ArtNet-Nodscaner"
sys.stdout.write("\x1b]2;"+title+"\x07")

node_list = []
def load(event):
    sel = int( li_nodes.curselection()[0] )
    print("li_nodes.get")
    try:
        sel = int(li_nodes.get(sel).split()[0])
        print(sel)
    except:
        return 0
    sel -= 1
    node_list[sel]
    clear_entry_ip()
    
    e_ip.configure(state='normal')
    e_ip.insert("end",node_list[sel]["IP"].replace("[","").replace("]",""))
    #e_ip.configure(state='readonly')
    
    e_ip_new.insert("end",node_list[sel]["IP"].replace("[","").replace("]",""))
    e_mac.delete("0","end")
    e_mac.insert("end",node_list[sel]["MAC"].replace("[","").replace("]",""))
    e_mac2.delete("0","end")
    e_mac2.insert("end",node_list[sel]["MAC"].split(":")[-1])
    
    
    #print(dir(event))
    #print(node_list)
    #for i in node_list:
    #    print(i)
    
def clear_entry_ip():
    e_ip.configure(state='normal')
    e_ip.delete("0","end")
    e_ip.configure(state='readonly')
    e_ip_new.delete("0","end")

    
def clear_node():
    global node_list
    li_nodes.delete("0","end")
    node_list = []
    li_nodes.delete("0","end")

    
def poll(delay=1):
    global old_tick
    
    #clear_entry_ip()
    clear_node()
    time.sleep(delay)
    nodscaner.poll()
    time.sleep(0.5)
    old_tick = 0
    
def clear(event= None):
    global rx
    rx.clear()
    poll()
    
def poll_loop(sleep):
    if sleep < 1:
        sleep = 1
    time.sleep(sleep)
    while 1:
        poll()
        time.sleep(sleep)

old_tick = 0
rx = nodscaner.ArtNetNodes()
        
def _scan():
    global rx,node_list,old_tick,Scrollbar
    
    rx.loop()
    print("get node from cache "    )
    li_nodes.insert("end",str("----"))
    while 1:
        nodes = rx.get()
        new_tick = rx.tick()
        #print("tick",new_tick)
        if new_tick == old_tick:
            pass
            continue
        old_tick = new_tick
        print("node",nodes)
        if nodes:
            li_node_scroll = li_nodes.yview()
            
            clear_node()

            #li_nodes.delete(0,"end")
            print("yea",len(nodes))
            node_nr = 1
            for node in nodes:
                #print(node)
                #try:
                li_nodes.insert("end",str(node_nr).rjust(3," ") +" "+ node["lname"])
                ip = str(node_nr).rjust(3," ") +" "+ node["IP"]
                bg = ""
                if node["PortTypes"][0] == "@":
                    ip += "  DMX-in"
                    bg ="yellow"
                else:
                    ip += "  DMX-out"
                    bg ="lightgreen" 
                if bg:
                    color = li_nodes.itemconfig("end", bg=bg)
                
                li_nodes.insert("end",str(node_nr).rjust(3," ") +" short Name:"+ node["sname"])
                li_nodes.insert("end",ip)
                if bg:
                    color = li_nodes.itemconfig("end", bg=bg)
                
                inout = " UNIVERS OUT="+ str(ord(node["SwOut"][0])+1)+" IN="+ str(ord(node["SwIn"][0])+1)
                li_nodes.insert("end",str(node_nr).rjust(3," ") + inout)
                
                li_nodes.insert("end",str(node_nr).rjust(3," ") +" "+ node["MAC"])
                
                timeline = ""
                timeline += " LASTCHANGE:%0.1f"% (time.time()-float(node["UPDATESTAMP"]) )
                REFRESHSTAMP = time.time()-float(node["REFRESHSTAMP"])
                timeline +="  LASTPING:%0.1f"% REFRESHSTAMP 
                li_nodes.insert("end",str(node_nr).rjust(3," ") +timeline )
                
                if node["BOOT"]:
                    BOOT = time.time()-float(node["BOOT"])
                else:
                    BOOT = 0
                timeline ="  BOOT:%0.1f"% BOOT
                li_nodes.insert("end",str(node_nr).rjust(3," ") +timeline +" sec" )
                bg = ""
                if REFRESHSTAMP > 5 :
                    bg="red"
                else:
                    bg="lightgreen"
                if bg:
                    li_nodes.itemconfig("end", bg=bg)
                #li_nodes.insert("end",str(node_nr).rjust(3," ") 
                #li_nodes.insert("end","")
                li_nodes.insert("end","*"*60)
                #li_nodes.itemconfig("end", bg="brown")
                node_nr += 1
                node_list += [node]
            
            #Scrollbar.set('0', '0.1')
            print(li_node_scroll)
            #print(dir(li_nodes))
            #li_node_scroll = int(li_node_scroll[0])
            #li_nodes.yview_moveto(li_node_scroll)
            
        time.sleep(0.2)
    

def get_new_ip(event=None):
    b = e_ip_new.get().replace("[","").replace("]","")
    return b

def get_new_ip_str(event=None):
    x = get_new_ip()
    #x = x[1:-1]
    x = x.strip()
    #x = x.replace(",",".")
    x = x.replace(" ","")
    x = x.split(",")
    print( "get_new_ip_str",x)
    return x
    
def send_none(event=None):
    pass
    
def send_mac(event=None):
    new_mac = "CMD MAC6 " + struct.pack("<B",(int(e_mac2.get(),16)))
    
    a = e_ip.get().replace("[","").replace("]","")
    cur_ip = []    
    for i in a.split(","):
        cur_ip +=[int(i)]
    print("SEND MAC:",cur_ip,new_mac)
    nodscaner.send_node_cmd(cur_ip,new_mac)
    poll(1.5)

def send_dmx_store(event=None):
    cmd = "CMD DMX STORE "
    
    a = e_ip.get().replace("[","").replace("]","")
    cur_ip = []    
    for i in a.split(","):
        cur_ip +=[int(i)]
    print("SEND:",cur_ip,cmd)
    nodscaner.send_node_cmd(cur_ip,cmd)
    poll(1.5)

def send_cmd(event=None):
    cmd = e_cmd.get() #"CMD DMX STORE "
    _send_cmd(cmd=cmd)
def send_cmd2(event=None):
    cmd = e_cmd2.get() #"CMD DMX STORE "
    _send_cmd(cmd=cmd)
def send_cmd3(event=None):
    cmd = e_cmd3.get() #"CMD DMX STORE "
    _send_cmd(cmd=cmd)
def send_cmd4(event=None):
    cmd = e_cmd4.get() #"CMD DMX STORE "
    _send_cmd(cmd=cmd)
def send_cmd5(event=None):
    cmd = e_cmd5.get() #"CMD DMX STORE "
    _send_cmd(cmd=cmd)

    
def _send_cmd(event=None,cmd=""):
    #cmd = e_cmd.get() #"CMD DMX STORE "
    cmd = cmd.split(" ")
    value = cmd[-1]
    try:
        value = struct.pack("<B",int(value))
    except:pass
    cmd = cmd[:-1] #.append(value)
    cmd.append(value)
    print("ERRRRR",cmd)
    cmd=" ".join(cmd )
    a = e_ip.get().replace("[","").replace("]","")
    cur_ip = []
    sep = "xx"
    if "," in a:
        sep = ","
    if "." in a:
        sep = "."
    for i in a.split(sep):
        cur_ip +=[int(i)]
    print("SEND:",cur_ip,cmd)
    nodscaner.send_node_cmd(cur_ip,cmd)
    poll(1.5)

    
def set_ip(event=None):
    print("SET NEW IP")

    cur_ip=(2,0,0,94)
    new_ip=(2,0,0,201)
    new_netmask=(255,0,0,0)
    
    a = e_ip.get().replace("[","").replace("]","")
    b = e_ip_new.get().replace("[","").replace("]","")
    c = variable.get() #e_mask_new.get()
    new_netmask = [] #c.split(".") #list(c)
    for i in c.split("."):
        new_netmask +=[int(i)]
    cur_ip = []    
    for i in a.split(","):
        cur_ip +=[int(i)]
    new_ip = []
    for i in b.split(","):
        new_ip +=[int(i)]
        
    if new_ip == cur_ip:
        print("neu und als IP sind gleich"  )
        return 0
    #cur_ip=(2,0,0,94)
    #new_ip=(2,0,0,201)
    
    print("new",[cur_ip, new_ip, new_netmask])
    print()
    nodscaner.set_ip4(cur_ip,new_ip, new_netmask)
    poll(1.5)
    
def set_node_pin(evnet=None):
    cmd = "CMD DMX=PIN"
    ip = get_new_ip_str()
    print("ip",[ip])
    nodscaner.send_node_cmd(ip,cmd=cmd)
    poll(1.5)
    
def set_node_in(evnet=None):
    cmd="CMD DMX=IN"
    ip = get_new_ip_str()
    nodscaner.send_node_cmd(ip,cmd=cmd)
    poll(1.5)
    
def set_node_out(evnet=None):
    cmd="CMD DMX=OUT"
    ip = get_new_ip_str()
    nodscaner.send_node_cmd(ip,cmd=cmd)
    poll(1.5)


    
root = Tkinter.Tk()
#root.geometry("900x700+100+100")
root.geometry("900x400+100+100")
root.title( title)
fframe = Tkinter.Frame(root)
fframe.pack(side="top",expand=0,fill="x")
cframe = Tkinter.Frame(root)
cframe.pack(side="top",expand=1,fill="both")

font1 = ("Helvetica", 8)
font2 = ("Helvetica", 10)
font3 = ("Helvetica", 16)
font20 = font=("Helvetica", 20)

b_scan = Tkinter.Button(fframe,text="ArtNetPoll",width=10,command=poll,font=font2)
b_scan.pack(side="left",expand=0,fill="y")
b_scan = Tkinter.Button(fframe,text="clear",width=10,command=clear,font=font2)
b_scan.pack(side="left",expand=0,fill="y")

scrollbar = Tkinter.Scrollbar(cframe)
scrollbar.pack(side=Tkinter.RIGHT, fill="y")

#pool = Tkinter.Listbox(root,selectmode="extended",exportselection=0)
li_nodes = Tkinter.Listbox(cframe,exportselection=0,width=35,font=font1)
li_nodes.pack(side="left",expand=0,fill="y")
li_nodes.bind("<ButtonRelease-1>",load )

li_nodes.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=li_nodes.yview)

eframe = Tkinter.Frame(cframe)
eframe.pack(side="left",expand=0,fill="y")
eframe1 = Tkinter.Frame(cframe)
eframe1.pack(side="left",expand=0,fill="y")



# ----------------------------------------------
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="OLD IP:",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_ip = Tkinter.Entry(line_frame,font=font20)
e_ip.pack(side="left")
#b_scan = Tkinter.Button(line_frame,width=14,font=font3)
#b_scan.pack(side="left",expand=1)

# ----------------------------------------------
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
e_ip_label = Tkinter.Label(line_frame,text=" IP:",font=font3,width=6)
e_ip_label.pack(side="left",expand=0,fill="y")
e_ip_new = Tkinter.Entry(line_frame,font=font20)
e_ip_new.bind("<Return>", set_ip )
e_ip_new.bind("<KP_Enter>", set_ip)
#e_ip_new.bind("<Tab>", update_name)
e_ip_new.bind("<ISO_Left_Tab>", set_ip)
e_ip_new.pack(side="left")

#-------------------------------------------- line


line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
variable = Tkinter.StringVar(root)
variable.set("255.0.0.0") # default value
Tkinter.Label(line_frame,text="IPMASK",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_mask_new = Tkinter.OptionMenu(line_frame, variable,"255.255.255.0","255.0.0.0")
e_mask_new.configure(font=("Helvetica", 20))
e_mask_new.configure(width=17)
#heigh=1,font=("Helvetica", 20)
e_mask_new.pack(side="left")
#e_mask_new.insert("end","255.0.0.0")
#e_mask_new.insert("end","255.255.255.0")

b_scan = Tkinter.Button(line_frame,text="SEND TO NODE",command=set_ip,width=14,font=font1)
b_scan.pack(side="left",expand=0)

#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="MAC:",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_mac = Tkinter.Entry(line_frame,width=16,font=font20)
e_mac.pack(side="left")
e_mac2 = Tkinter.Entry(line_frame,width=3,font=font20)
e_mac2.pack(side="left")
e_mac2.bind("<Return>", send_mac )
e_mac2.bind("<KP_Enter>", send_mac)
Tkinter.Button(line_frame,text="SEND TO NODE",command=send_mac,width=14,font=font1).pack(side="left",expand=0)
#-------------------------------------------- line


#b_scan = Tkinter.Button(eframe1,width=14,font=font3)
#b_scan.pack(side="top",expand=0)

line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="DMX:",font=font3,width=6).pack(side="left",expand=0,fill="y")
b_set_node_pin = Tkinter.Button(line_frame,text="HW-PIN",command=set_node_pin,width=6,font=font3)
b_set_node_pin.pack(side="left",expand=0)
b_set_node_in = Tkinter.Button(line_frame,text="IN",command=set_node_in,width=6,font=font3)
b_set_node_in.pack(side="left",expand=0)

b_set_node_out = Tkinter.Button(line_frame,text="OUT",command=set_node_out,width=6,font=font3)
b_set_node_out.pack(side="left",expand=0)



#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="CMD",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_cmd = Tkinter.Entry(line_frame,font=font3,width=16)
e_cmd.bind("<Return>", send_cmd )
e_cmd.pack(side="left")

#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="L-Name",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_lname = Tkinter.Entry(line_frame,font=font3,width=10)
e_lname.pack(side="left")

#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="S-Name",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_sname = Tkinter.Entry(line_frame,font=font3,width=10)
e_sname.pack(side="left")
#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="ArtNet",font=font3,width=6).pack(side="left",expand=0,fill="y")
Tkinter.Label(line_frame,text="SUB:",font=font3,width=4).pack(side="left",expand=0,fill="y")
e_artnet_uni1 = Tkinter.Entry(line_frame,font=font3,width=4)
e_artnet_uni1.pack(side="left")
Tkinter.Label(line_frame,text="NET:",font=font3,width=4).pack(side="left",expand=0,fill="y")
e_artnet_uni1 = Tkinter.Entry(line_frame,font=font3,width=4)
e_artnet_uni1.pack(side="left")
Tkinter.Label(line_frame,text="UNI:",font=font3,width=4).pack(side="left",expand=0,fill="y")
e_artnet_uni1 = Tkinter.Entry(line_frame,font=font3,width=4)
e_artnet_uni1.pack(side="left")
Tkinter.Button(line_frame,text="SEND TO NODE",command=send_none,width=14,font=font1).pack(side="left",expand=0)
#-------------------------------------------- line

b_scan = Tkinter.Text(eframe,width=20,font=font2)
b_scan.pack(side="top",expand=1,fill="x")



#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe1)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="CMD",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_cmd2 = Tkinter.Entry(line_frame,font=font3,width=16)
e_cmd2.insert("end","DMX ERASE ")
e_cmd2.bind("<Return>", send_cmd2 )
e_cmd2.pack(side="left")
#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe1)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="CMD",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_cmd3 = Tkinter.Entry(line_frame,font=font3,width=16)
e_cmd3.insert("end","DMX OUT STORE ")
e_cmd3.bind("<Return>", send_cmd3 )
e_cmd3.pack(side="left")
#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe1)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="CMD",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_cmd4 = Tkinter.Entry(line_frame,font=font3,width=16)
e_cmd4.insert("end","DMX OUT SET 2")
e_cmd4.bind("<Return>", send_cmd4 )
e_cmd4.pack(side="left")
#-------------------------------------------- line
line_frame = Tkinter.Frame(eframe1)
line_frame.pack(side="top",expand=0,fill="x")
Tkinter.Label(line_frame,text="CMD",font=font3,width=6).pack(side="left",expand=0,fill="y")
e_cmd5 = Tkinter.Entry(line_frame,font=font3,width=16)
e_cmd5.insert("end","REBOOT ")
e_cmd5.bind("<Return>", send_cmd5 )
e_cmd5.pack(side="left")


thread.start_new_thread(_scan, () )
nodscaner.bind_cmd_node()

def read_cmd_buf():
    b_scan.insert("end", "buf read\n" )
    while 1:
        if nodscaner.node_cmd_buf_list:
            msg = str(nodscaner.node_cmd_buf_list)
            print("read_cmd_buf msg",msg)
            nodscaner.node_cmd_buf_list = []
            b_scan.insert("end",str(time.time())+"\n")
            b_scan.insert("end", msg +"\n")
            
            b_scan.see("end")
        time.sleep(0.1)

#thread.start_new_thread(nodscaner.node_cmd_recive, () )
#thread.start_new_thread(read_cmd_buf, () )

def X():
    thread.start_new_thread(nodscaner.node_cmd_recive, () )
    thread.start_new_thread(read_cmd_buf, () )
    #thread.start_new_thread(node_cmd_recive, () )
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
            
        
            print("node count",len(nodes))
            #for i in nodes:
            #print(i)
        z += 1
        time.sleep(0.2)
        
    print()
    print("time out")
    raw_input("ENDE")

thread.start_new_thread(X,()) #node_cmd_recive, () )
root.mainloop()



