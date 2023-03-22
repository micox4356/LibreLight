#!/usr/bin/bash

#insert in xfce4-session on login event 
set -x
#firefox-esr -P

#screen -XS "vnc" quit
screen -XS "ASP" quit
screen -XS "shader" quit
screen -XS "vpu1_out" quit
screen -XS "vpu2_out" quit

screen -m -d -S vnc -- x11vnc -forever

#x=$(screen -ls | grep ASP | wc -c)
#echo "$x"

screen -m -d -S ASP -- python3 /opt/LibreLight/ASP/ArtNetProcessor.py

#screen -m -d -S shader -- python3 /opt/LibreLight/Xdesk/3d/demo_shader_live.py
#screen -m -d -S shader -- python3 /opt/LibreLight/Xdesk/vpu/shader_live.py
#screen -m -d -S shader -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,12,5
# Ayrton VPU Offset Y ___ Y ___ (Ghost 255)
#screen -m -d -S vpu1_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,8,8 -X 12 --pixel-map=_1 --gobo-ch=11
screen -m -d -S vpu1_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,12,5 -X 12 --pixel-map=_1 --gobo-ch=11 --countdown=31,51
# Ayrton VPU Offset X 235 Y 253 (Pannel 255)  7,5m-4m ... 9,5m-4m
#screen -m -d -S vpu2_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,8,8 -X 4  --pixel-map=_2 --gobo-ch=21 --win-pos 430,164 --start-univ=4 
screen -m -d -S vpu2_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,4,6 -X 4  --pixel-map=_2 --gobo-ch=21 --win-pos 430,164 --start-univ=4 --countdown=71,91

sleep 3
screen -ls
