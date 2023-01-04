
Stage Lighting Control Software, Movingheads, Movinglights, Dimmer, LED, Spotlight, Washlight 

![LibreLightScreen](https://user-images.githubusercontent.com/98694752/152388271-54c6e915-0357-47d5-9d1c-f0c71ea8fa12.png)


HomePage
- http://librelight.de

Youtube Tutorial
- https://youtu.be/sIp39YimyVw

---

## Quick Setup / Install

Prerequisites
- Operating System: Debian 11
- set two static ip address 10.10.10.x/24 and 2.0.0.x/8 on a LAN-Interface

```
adduser user
mkdir /opt/LibreLight
mkdir /opt/LibreLight/git/
chown -R user:user /opt/LibreLight

mkdir /opt/netns

# clone all repos
wget https://raw.githubusercontent.com/micox4356/LibreLight/master/upgrade.sh 

sh upgrade.sh

# install all deb packages
sudo bash /opt/LibreLight/Xdesk/install.sh


```



