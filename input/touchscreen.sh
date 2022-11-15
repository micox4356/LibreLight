#!/usr/bin/bash
# xte is in part of xautomation
# apt install xautomation

#set -a
SESSION="touch.py"
CMD="/usr/bin/python3 /opt/LibreLight/Xdesk/input/touchscreen.py"
#echo "cmd: $CMD"
#echo "ses: $SESSION"
#echo
screen -X -S "$SESSION" quit
screen -d -m -S "$SESSION" sh -c "$CMD"
#sleep 1
#screen -ls
