
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
#for i in dir(mc):
#    print(i)#,[i.__doc__])
#    print()

#for i in mc.get_stats():
#    print("keys",i)

#exit()

while 1:
    ch = 141
    send = 0
    #cmd="stats items" 
    x=mc.get("index")#cmd)
    if x:
        #print(x)
        print()
        for k,v in x.items():
            #print(k,v)
            x=mc.get(k)
            print(k,v,ch,"=",x[ch-1])
    time.sleep(.13)
