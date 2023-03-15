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
screen -m -d -S vpu1_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,8,8 -X 12 --pixel-map=_1
screen -m -d -S vpu2_out -- python3 /opt/LibreLight/Xdesk/vpu/vpu_live.py -m 16,8,8 -X 4 --win-pos 450,164 --start-univ=4 --gobo-ch=2 --pixel-map=_2

sleep 3
screen -ls
