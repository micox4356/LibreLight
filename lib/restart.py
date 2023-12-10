#!/usr/bin/python3

import os
import sys

BASE_PATH = "/opt/LibreLight/Xdesk/"

def easy(*args):
    print("easy",args)
    cmd="_LibreLightDesk.py"
    arg= "--easy"
    print("fork",[BASE_PATH,cmd,arg])
    os.execl("/usr/bin/python3", BASE_PATH, cmd,arg)
    time.sleep(3)
    sys.exit()

def pro(*args):
    print("pro",args)
    #cmd =  "Start.py"
    #arg=""
    cmd="_LibreLightDesk.py"
    arg= "--pro"
    print("fork",[BASE_PATH,cmd,arg])
    print("fork",[BASE_PATH,cmd,arg])
    os.execl("/usr/bin/python3", BASE_PATH, cmd,arg)
    time.sleep(3)
    sys.exit()
