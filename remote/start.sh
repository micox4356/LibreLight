#!/usr/bin/bash 
#sleep 3;

sudo /opt/netns/create 19
CMD="ip a"  
/opt/netns/exec --id=19 --cmd="$CMD" 
CMD="python3 /opt/LibreLight/Xdesk/remote/s.py"  
/opt/netns/exec --id=19 --cmd="xterm -e screen $CMD" &



