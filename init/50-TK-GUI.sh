#!/usr/bin/bash
set -e

path="/opt/LibreLight"
SES="EDITOR.py"
CMD="python3 $path/Xdesk/LibreLightDesk.py "

echo "- STARTING $SES"

cd "$path/Xdesk/"
screen -XS "$SES" quit | echo ""
sleep 1
CMD="screen -d -m -S $SES $CMD"
#echo "$CMD"
$CMD
#sleep 1
#screen -ls
