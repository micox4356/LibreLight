#!/usr/bin/python3

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print( "Content-type: text/html")
print()

print( """
<html>

<head><title>Licht WEB</title></head>

<body>

  <h3> Sample CGI Script </h3>
""")


form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

print("<br>")

import os

ENV = os.environ

for env in ENV:
    val=ENV[env]
    #print(env)
    #print(" = ")
    #print(val)
    #print("<br>")

ARGS = {}
if "QUERY_STRING" in ENV:
    _args = ENV["QUERY_STRING"]
    if "&" in _args:
        args = _args.split("&")
    else:
        args = _args
    
    for arg in args:
        import urllib.parse
        if "=" in arg:
            k,v = arg.split("=",1)
            v = urllib.parse.unquote(v)
            ARGS[k]=v
            print("{} = {} <br>".format(k,v))

print("""
<script>

function xGET(){
    dmx = document.getElementById("DMX").value;
    val = document.getElementById("VALUE").value;
    fade = document.getElementById("FADE").value;
    xget(dmx,val,fade)
}

function xget(dmx=1,val=100,fade=1){
    const http = new XMLHttpRequest();

    url = './licht.cgi?&CMD=[{"VALUE": '+val+', "args": [], "FADE": '+fade+', "DMX": "'+dmx+'"}]'
    http.open("GET", url);
    http.send();

    http.onreadystatechange = (e) => {
      console.log('done',e)
    }
}

function hN(){ // NEXT
    dmx = document.getElementById("highlight").value;
    dmx = parseInt(dmx) +1
    document.getElementById("highlight").value = dmx;
    if( dmx != 63 && dmx != 66){
        xget(dmx,255,0)
    }
    dmx -= 1
    if( dmx != 63 && dmx != 66){
        xget(dmx,0,0)
    }
    

}

function hP(){ // PREVIEW
    dmx = document.getElementById("highlight").value;
    dmx = parseInt(dmx)-1
    document.getElementById("highlight").value = dmx;
    
    if( dmx != 63 && dmx != 66){
        xget(dmx,255,0)
    }
    dmx += 1
    if( dmx != 63 && dmx != 66){
        xget(dmx,0,0)
    }

}

</script>

DMX<input type=number id=DMX value=10>
<br>
VALUE<input type=number id=VALUE value=255>
<br>
FADE<input type=number id=FADE value=1>
<br>
<input type=button value=GO onclick=xGET()>






<br>
<br>
<br>
Highlight
<input type=button value="-" onclick=hP() size=10>
<input type=number id=highlight value=10 size=5>
<input type=button value="+" onclick=hN() size=10>
<br>
<br>
<br>
""")

print("<br>")
print("beispiel <br>")
print('&CMD=[{"VALUE": 55, "args": [], "FADE": 3, "DMX": "1"}]')
print("<br>")

if "CMD" in ARGS:
    CMD = ARGS["CMD"]
    CMD = CMD.replace("'","")
    CMD = CMD.replace("<","")
    CMD = CMD.replace(">","")
    CMD = CMD.replace(";","")
    CMD = CMD.replace("|","")

    #python3 /opt/LibreLight/Xdesk/lib/zchat.py data '[{"VALUE": 255, "args": [], "FADE": 0, "DMX": "1"}]
    cmd = 'python3 /opt/LibreLight/Xdesk/lib/zchat.py data \'{}\''.format(CMD)
    print("$ ",cmd, "<br>")
    print("<br>")
    r=os.popen(cmd)
    for l in r:
        l=l.replace("<","&lt;")
        l=l.replace(">","&gt;")
        print(">",l,"<br>")




print( """
</html>
""")
