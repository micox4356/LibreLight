#!/usr/bin/bash

echo "\e[42mBOOTING LIBRELIGHT CONSOLE\e[0m"

killall ibus-daemon # ibus slowsdown tkinter/Editor

screen -ls
echo ""

/opt/LibreLight/Xdesk/input/touchscreen.sh

find /opt/LibreLight/Xdesk/init/ -name "*.sh" -exec {} \;
echo ""
sleep 3;
screen -ls

echo "BOOT END"
sleep 3;
