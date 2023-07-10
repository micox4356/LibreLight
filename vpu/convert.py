#!/usr/bin/python3
import os

print("... checking home dir")
HOME = os.getenv('HOME')
try:
    os.chdir(HOME+"/LibreLight/video/converter")
except FileNotFoundError:  
    cmd =  "mkdir -p {}/LibreLight/video/converter".format(HOME)
    os.system(cmd)
    os.chdir(HOME+"/LibreLight/video/converter")

print("ok")

cmd =  "mkdir -p {}/LibreLight/video/converter/klein".format(HOME)
os.system(cmd)
cmd =  "mkdir -p {}/LibreLight/video/converter/groß".format(HOME)
os.system(cmd)

cmd =  "mkdir -p groß/"
os.system(cmd)


def convert_img(s,t):# to 1 sec video
    cmd="ffmpeg -y -framerate 1 -i 'groß/{}' -r 1000 'groß/{}.mp4'".format(s,t)
    cmd="ffmpeg -y -framerate 1 -i 'groß/{}' -s 640x480 -c:a copy -r 1000 'klein/{}.mp4'".format(s,t)
    print(cmd)
    os.system(cmd)
    print("*"*40)
    print("*"*40)
    print()

def convert_video(s,t):
    cmd="ffmpeg  -y -i 'groß/{}' -s 640x480 -c:a copy 'klein/{}.mp4'".format(s,t)
    print(cmd)
    os.system(cmd)
    print("*"*40)
    print("*"*40)
    print()

files = os.listdir("groß/")
if not files:
    print("- no files in groß")

for s in files:
    if "." not in s:
        continue

    t = s.rsplit(".",1)[0] # cut ending .mp4

    if os.path.isfile("groß/"+s):
        print(s)
        ending = s.lower().split(".")[-1] 
        if ending in  ["png","jpg","jpeg","bmp","gif"] :
            convert_img(s,t)
            #s = t+".mp4"
        else:
            convert_video(s,t)
        print(" ")
        print(" ")

print("")
input("ende")
