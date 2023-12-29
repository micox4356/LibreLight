#!/usr/bin/python3

import os

def scan_capture(name="MiraBox",serial=""):
    ls = os.listdir("/dev/")
    name = name.upper()
    serial = serial.upper()
    out = []
    for l in ls:
        if l.startswith("video"):
            #print(l)
            cmd="udevadm info --query=all /dev/{}".format(l)
            print("# cmd:",cmd)
            r = os.popen(cmd)
            ok_name = 0
            ok_capture = 0
            ok_serial = 0

            for line in r.readlines():
                line = line.strip()
                line = line.upper()

                #print(l,line)
                #ID_V4L_CAPABILITIES=:capture:
                if "ID_V4L_CAPABILITIES=:capture:".upper() in line:
                    ok_capture = 1
                if name != "" and "_MODEL" in line and name in line:
                    ok_name = 1
                if serial != "" and "ID_SERIAL_SHORT" in line and serial in line:
                    ok_serial = 1

            if (name == "" or ok_name) and (serial == "" or ok_serial) and ok_capture:
                print(l,"# name:",ok_name,"capture:",ok_capture,"serial:",ok_serial,"# OK !",[name,serial])
                out.append([l,name,serial])
            else:
                print("#",l,"# name:",ok_name,"capture:",ok_capture,"serial:",ok_serial,"# FAIL !",[name,serial])
            print()
    return out

