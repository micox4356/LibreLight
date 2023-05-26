#!/usr/bin/python3
import os

print("go")
for i in os.listdir("groß/"):
    i2 = i.split(".",-1)[0]
    #if not i.endswith("mov"):
    #    continue
    if os.path.isfile("groß/"+i):
        print(i)
         	  
        cmd="ffmpeg -n -i 'groß/"+i+"' -s 640x480 -c:a copy 'klein/"+i2+".mp4'"
        print(cmd)
        os.system(cmd)
        print(" ")
        print(" ")

print("")
input("ende")
time.sleep( 10)
