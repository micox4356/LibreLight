#!/usr/bin/bash
set -e

path="/opt/LibreLight"
SES="EDITOR.py"
CMD="python3 $path/Xdesk/LibreLightDesk.py "

echo "- STARTING $SES"

cd "$path"
screen -XS "$SES" quit | echo ""
CMD="screen -d -m -S $SES $CMD"
#echo "$CMD"
$CMD
#sleep 1
#screen -ls