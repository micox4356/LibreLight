#!/usr/bin/bash

#insert in xfce4-session on login event 
set -x
#firefox-esr -P

#screen -XS "vnc" quit
screen -XS "ASP" quit
screen -XS "shader" quit

screen -m -d -S vnc -- x11vnc -forever

screen -m -d -S ASP -- python3 /opt/LibreLight/ASP/ArtNetProcessor.py

#screen -m -d -S shader -- python3 /opt/LibreLight/Xdesk/3d/demo_shader_live.py
screen -m -d -S shader -- python3 /opt/LibreLight/Xdesk/vpu/shader_live.py

sleep 3
screen -ls