import json

f = open("show/Dimmer/patch.sav")
lines = f.readlines()
for i in range(512):
     line = lines[0]
     line=line.strip()
     x=line.split("\t")
     
     #print(x)
     j = x[-1]
     #print()
     #print(j)
     j = json.loads(j)
     j["DMX"] = i+1
     j["NAME"] = "D"+str(i+1)
     print("{}\t{}\t{}".format(i+1,i+1,json.dumps(j)))

