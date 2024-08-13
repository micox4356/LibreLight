

import json
try:
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
except:
    mc = None

import time

start = time.time()
if mc:
    #while 1:
    for i in range(512):
        #index=[]
        #for i,v in enumerate(l):
        #    key=l[v].replace(" ","_")
        #    key=str("EXEC-"+str(i))
        #    print("EXEC-MC",[key,len(json.dumps(d[v]))])
        #    mc.set(key,json.dumps(d[v]))
        #    index.append(key)
        #mc.set("EXEC-INDEX",json.dumps(index))

        #x = mc.get("EXEC-INDEX") #,json.dumps(index))
        x = mc.get("EXEC-META-"+str(i)) #,json.dumps(index))
        print( i, json.loads(x) )

        #for j in json.loads(x):
        #    y = mc.get(i) #,json.dumps(index))
        #   print(i,len(y))
        #break
print()
i=77-1
x = mc.get("EXEC-META-"+str(i)) #,json.dumps(index))
print( i, json.loads(x) )
i=80-1
x = mc.get("EXEC-META-"+str(i)) #,json.dumps(index))
print( i, json.loads(x) )
print()

print(start- time.time())
import sys
nr=0
if len(sys.argv) >= 2:
    try:
        nr=int(sys.argv[1])
    except:pass
#y = mc.get("EXEC-"+str(nr)) #,json.dumps(index))
y = mc.get("EXEC-"+str(nr)) #,json.dumps(index))
if y:
    print(len(y))
    try:
        print(json.loads(y))
    except Exception as e:
        print("ERR",e)

k = "EXEC-META-"+str(nr)
y = mc.get(k) #,json.dumps(index))
y = json.loads(y)
y["LABEL"]=str(int(y["LABEL"])+100)
print([k,y])
y = mc.set(k,json.dumps(y)) #,json.dumps(index))
#y = mc.set("EXEC-META-"+str(nr),y) #,json.dumps(index))
