import json
import sys
import os

sys.path.insert(0,"/opt/LibreLight/Xdesk/")
import lib.zchat as chat

cmd_client = chat.Client(port=30003)

#buf2.append(["EXEC",str(btn),val,m[0],m[1]])
#msgs = json.dumps(msgs).encode("utf-8")
msg={}
msgs=[]
print("ARGS:",sys.argv,len(sys.argv))

if len(sys.argv) >= 4:
    if sys.argv[1] == "exec":

        if sys.argv[3] == "on":
            msg={"event":"EXEC","EXEC":str(sys.argv[2]),"VAL":str(1)}
        if sys.argv[3] == "off":
            msg={"event":"EXEC","EXEC":str(sys.argv[2]),"VAL":str(0)}

        if msg:
            msgs.append(msg)
            msgs = json.dumps(msgs).encode("utf-8")
            print("send:",msgs)
            cmd_client.send(msgs)


