#!/usr/bin/python3
import os
import time

# Ayrton VPU Offset X 235 Y 253 (Pannel 255)  7,5m-4m ... 9,5m-4m

#os.chdir(""")
print(os.getcwd())

print("-- init --")
#cmd = 'screen -XS "watchdog_vpu" quit'
#print("CMD:",cmd)
#os.system(cmd)
cmd = 'screen -XS "vpu01_out" quit'
print("CMD:",cmd)
os.system(cmd)
cmd = 'screen -XS "vpu02_out" quit'
print("CMD:",cmd)
os.system(cmd)

print("-- loop --")

def vpu01():
    # Ayrton VPU Offset Y ___ Y ___ (Ghost 255)

    cmd = 'screen -ls | grep "\.vpu01_out"'
    print("CMD:",cmd)
    r = os.popen(cmd)
    lines = r.readlines()

    if lines:
        print(" ok")
        return 0

    cmd = 'screen -XS "vpu01_out" quit'
    print("CMD:",cmd)
    os.system(cmd)

    cmd = "screen -m -d -S vpu01_out --"
    cmd = "screen -m -d -S vpu01_out --"
    cmd+= " python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py"
    cmd+= " -m 16,12,5"
    cmd+= " -X 12 "
    cmd+= " --pixel-map=_1 "
    cmd+= " --gobo-ch=11"
    cmd+= " --countdown=31,51,151,171 --videoplayer=181,201 --title=LIVE"

    print("CMD:",cmd)
    os.system(cmd)
    #time.sleep(1)
    return 1


def vpu02():
    # Ayrton VPU Offset X 235 Y 253 (Pannel 255)  7,5m-4m ... 9,5m-4m

    cmd = 'screen -ls | grep "\.vpu02_out"'
    print("CMD:",cmd)
    r = os.popen(cmd)
    lines = r.readlines()

    if lines:
        print(" ok")
        return 0

    cmd = 'screen -XS "vpu02_out" quit'
    print("CMD:",cmd)
    os.system(cmd)

    cmd ="screen -m -d -S vpu02_out --"
    cmd += " python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py"
    cmd += " -m 16,4,6"
    cmd += " -X 4"
    cmd += " --pixel-map=_2"
    cmd += " --gobo-ch=21"
    cmd += " --win-pos 430,164"
    cmd += " --start-univ=4"
    cmd += " --countdown=71,91,111,131"
    cmd += " --videoplayer=221,241"
    cmd += " --title=LIVE"
    print("CMD:",cmd)
    os.system(cmd)
    #time.sleep(1)

    return 1



while 1:
    r1=vpu01()
    r2=vpu02()

    time.sleep(3)



