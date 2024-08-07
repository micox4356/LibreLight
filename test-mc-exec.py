

import json
try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None

import time

start = time.time()
if mc:
    while 1:
        #index=[]
        #for i,v in enumerate(l):
        #    key=l[v].replace(" ","_")
        #    key=str("EXEC-"+str(i))
        #    print("EXEC-MC",[key,len(json.dumps(d[v]))])
        #    mc.set(key,json.dumps(d[v]))
        #    index.append(key)
        #mc.set("EXEC-INDEX",json.dumps(index))

        x = mc.get("EXEC-INDEX") #,json.dumps(index))
        for i in json.loads(x):
            y = mc.get(i) #,json.dumps(index))
            print(i,len(y))
        break

print(start- time.time())
import sys
nr=0
if len(sys.argv) >= 2:
    try:
        nr=int(sys.argv[1])
    except:pass
y = mc.get("EXEC-"+str(nr)) #,json.dumps(index))

if y:
    print(len(y))
    print(json.loads(y))

