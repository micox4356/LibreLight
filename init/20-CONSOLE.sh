#!/usr/bin/bash
set -e

path="/opt/LibreLight"
SES="CONSOLE.py"
CMD="-- bash -c 'python3 $path/Xdesk/console.py'"

echo "- STARTING $SES"

cd "$path/Xdesk/"
#echo $(pwd)
screen -XS "$SES" quit | echo ""
CMD2="screen -d -m -S $SES $CMD"
#screen -d -m -S "$SES" -- bash -c 'python3 $path/Xdesk/console.py'
#screen -S "$SES" -- '/usr/sbin/python3 /opt/LibreLight/Xdesk/console.py'
screen -d -m -S "$SES" --  python3 /opt/LibreLight/Xdesk/console.py
#'/usr/sbin/python3 /opt/LibreLight/Xdesk/console.py'

#echo "$CMD2"
$CMD2
#sleep 2
#screen -ls
