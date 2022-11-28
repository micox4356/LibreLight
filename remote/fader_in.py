import sys
import os

sys.path.append(os.getcwd() + '/..')
import lib.zchat as chat


#sys.path.append(os.getcwd() + '/..')
import time
data = "hi"
data = data.encode("utf-8")
#c = chat.Client(port=30002)
c = chat.Client()
client = c
time.sleep(0.05)
client.send(data)
import time
#while 1:
#    try:
#        data = input("<")
#        data = bytes(data,"utf-8")
#        client.send(data)
#    except Exception as e:
#        print("Exc",e)
#    time.sleep(0.1)




import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

mc.set("some_key", "Some value")
value = mc.get("some_key")

mc.set("another_key", 3)
mc.delete("another_key")

import time
import json
data = {}
start = time.time()
delta = start

while 1:
    send = 0
    try:
        x=mc.get("dmx-0")
    except Exception as e:
        print("exc", e)
        time.sleep(1)
    #print(dir(mc))

    #if type(x) is None:
    #    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    #    time.sleep(1)
    #    print("recon memcache")
    #    continue


    if type(x) is list and len(x) == 512: 
        ch = 140
        #print(ch,x[ch])
        #data = input("<")

        v = x[ch]
        delta = time.time()-start
        cmd={"iDMX":ch,"iVAL":v,"iT":round(delta,2)} #".format(ch,v)
        cmd = json.dumps([cmd])
        if ch in data:
            if data[ch] != v:
                data[ch] = v
                send = 1
        else:
            data[ch] = cmd
            send = 1

        if send:
            print("+",cmd)
            _data = bytes(cmd,"utf-8")
            client.send(_data)
        else:
            pass
            #print("-",cmd)

    time.sleep(0.01)



