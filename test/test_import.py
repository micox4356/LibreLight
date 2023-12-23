#!/use/bin/python3

import os
import importlib

# check all sourcefiles
# if python module is indtalled 

cmd='grep -r -I "import " . | cut -d ":" -f 2-99 | sort | uniq ' #| sort -h | grep -v "from \|lib\|tkgui\|tksdl"'
r=os.popen(cmd)
data = {}
for line in r.readlines():
    line = line.strip()
    if line.startswith("#"):
        continue

    #print(line)
    line = line.split()
    module = line[1]
    module = module.split(",")[0] #.replace(",","")
    module = module.replace(";","")

    if module.startswith("-"):
        continue
    if module.startswith("_"):
        continue
    if "." in module:
        continue
    if module.startswith("lib"):
        continue
    if "nodesca" in module:
        continue

    if module not in data:
        data[module] = []
    data[module].append(line)

err = []
ok = []
for module in data:
    if importlib.util.find_spec(module):
        ok.append(module)
    else:
        err.append(module)

print()
ok.sort()
err.sort()

for i in ok:
    print((i +" OK").rjust(20," "))
print()
for i in err:
    #print(i,"ERR")
    print((i +" ERR").rjust(20," "))
print("OK",len(ok),"ERR",len(err))
print()
#print(dir())
