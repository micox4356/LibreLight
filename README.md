
Stage Lighting Control Software, Movingheads, Movinglights, Dimmer, LED, Spotlight, Washlight 


![LibreLight20230802](https://librelight.de/downloads/screenshot/screenshot_23.08.png)

HomePage
- http://librelight.de

Youtube Tutorial
- https://youtu.be/sIp39YimyVw

---

## Quick Setup / Install

Prerequisites
- Operating System: Debian 11, Proxmox 7.3
- xfce4-desktop
- min 1GB of free Memory
- min 2x CPU cores i5 2Ghz
- external Mouse with Mouse-Wheel
- set two static ip address 10.10.10.x/24 and 2.0.0.x/8 on a vmbr0 or on br0 LAN-Bridge-Interface

execute as root
```
adduser user 

mkdir -p /opt/LibreLight/git/
mkdir -p /opt/LibreLight/Xdesk/
mkdir -p /opt/LibreLight/ASP/

# network namespace" 
mkdir -p /opt/netns

# add to /etc/sudoers 
# user      ALL=(ALL) NOPASSWD:/opt/netns/_exec, /opt/netns/create

# install git
apt install git

# clone all repos
cd /tmp/
wget https://gogs.librelight.de/librelight/Xdesk/raw/master/upgrade.sh
sh upgrade.sh

chown -R user:user /opt/LibreLight

# install all deb packages
bash /opt/LibreLight/Xdesk/install.sh

```

execute as user

```

# copy starter to Desktop
cp /opt/LibreLight/Xdesk/desktop/* /home/user/Desktop

# copy show files to Home
mkdir -p /home/user/LibreLight
cp -rv /opt/LibreLight/Xdesk/home/LibreLight/ /home/user/LibreLight/
echo "Dimmer" > /home/user/LibreLight/init.txt

# start LibreLight with
bash /opt/LibreLight/Xdesk/start.sh


```



