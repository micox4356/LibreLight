#!/usr/bin/bash
set -e

path="/opt/LibreLight"
SES="TKSDL.py"
CMD="python3 $path/Xdesk/tksdl/fix.py "

echo "- STARTING $SES"

cd "$path/Xdesk/"
screen -XS "$SES" quit | echo ""
CMD="screen -d -m -S $SES $CMD"
#echo "$CMD"
$CMD
#sleep 1
#screen -ls
