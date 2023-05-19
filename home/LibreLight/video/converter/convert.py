#!/usr/bin/python3
import os
import time

print("go")
for i in os.listdir("big/"):
    i2 = i.split(".",-1)[0] + ".mp4"
    #if not i.endswith("mov"):
    #    continue
    if os.path.isfile("big/"+i):
        print(i)
         	  
        cmd="ffmpeg -n -i 'big/"+i+"' -s 640x480 -c:a copy 'small/"+i2+"'"
        print(cmd)
        os.system(cmd)
        print(" ")
        print(" ")

print("")
input("ende")
time.sleep( 10)
