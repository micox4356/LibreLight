#!/usr/bin/bash

ID=$(id -u)
if [ "x$ID" != 'x0' ]; then
    echo "please start with sudo"
    exit 
fi
echo "-- apt update"
apt update
#apt upgrade -y

echo ""
echo "-- system tools"
pkg="vim lm-sensors htop nmap tcpdump rsync git psmisc screen git gitk memtest86" 
apt install -y $pkg 

echo ""
echo "-- touchscreen tools"
#xautomation -> xte mouse  #xrand -> x11-xserver-utils
pkg="xdotool x11-xserver-utils xinput xautomation" 
apt install -y $pkg 

echo ""
echo "-- media pkg's"
pkg="python3-opencv ffmpeg "
# v4l-utils"
# guvcview 
apt install -y $pkg 

echo ""
echo "-- python pkg's"
pkg="python3-tk python3-pygame memcached python3-memcache python3-pip python3-pyglet idle python3-psutil"
apt install -y $pkg 

echo ""
echo "-- python 3d pkg's"
pkg="python3-opengl python3-pyglet python3-pil "
apt install -y $pkg 
#exit


echo ""
echo "-- update pip"
su -- user <<EOF
id
pip install pip --upgrade --break-system-packages
EOF

echo ""
echo "-- python-pip pkg's"
su -- user <<EOF
pip install pyopengltk --break-system-packages
pip install moderngl --break-system-packages
pip install moderngl-window --break-system-packages
echo ""
pip install glfw --break-system-packages
pip install glwindow --break-system-packages
pip install glnext --break-system-packages
#pip install glnext_compiler --break-system-packages
pip install glcontext --break-system-packages
pip install pyopengltk --break-system-packages
pip install imutils --break-system-packages
pip install raylib --break-system-packages
EOF

echo ""
echo "-- sync netns"
rsync -apv /opt/LibreLight/ASP/netns/ /opt/netns/
chmod -R 755 /opt/netns/ 
chown -R root:root /opt/netns/

chown -R user:user /opt/LibreLight




