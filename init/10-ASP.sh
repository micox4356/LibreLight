#!/usr/bin/bash
set -e

path="/opt/LibreLight"
SES="ASP"
CMD="sh $path/ASP/start_ASP.sh "

echo "- STARTING $SES"

cd "$path"
screen -XS "$SES" quit | echo ""
CMD="screen -d -m -S $SES $CMD"
#echo "$CMD"
$CMD
#sleep 1
#screen -ls
