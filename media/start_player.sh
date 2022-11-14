#!/usr/bin/bash 
#sleep 3;

exit # no sound !!  if in netns

sudo /opt/netns/create 19
CMD="ip a"  
/opt/netns/exec --id=19 --cmd="$CMD" 
CMD="python3 /opt/LibreLight/Xdesk/media/player.py"  
/opt/netns/exec --id=19 --cmd="xterm -e screen $CMD" &



