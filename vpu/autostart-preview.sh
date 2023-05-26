#!/usr/bin/bash

#insert in xfce4-session on login event 
set -x
#firefox-esr -P

screen -XS "vpu1_pre" quit
screen -XS "vpu2_pre" quit

# Ayrton VPU Offset Y ___ Y ___ (Ghost 255)
screen -m -d -S vpu1_pre -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 40,12,5 -X 12 --gobo-ch=11 --countdown=31,51,151,171 --videoplayer=181,201
sleep 1

# Ayrton VPU Offset X 235 Y 253 (Pannel 255)  7,5m-4m ... 9,5m-4m
screen -m -d -S vpu2_pre -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 40,4,6 -X 4  --gobo-ch=21  --start-univ=4 --countdown=71,91,111,131 --videoplayer=221,241

sleep 3

screen -ls
