#!/usr/bin/python3

import os
import json

h = os.environ["HOME"]

def cprint(txt,*args):
    print(txt)

def _load_remote_ip(cfg_file):
    f = open(cfg_file)
    lines = f.readlines()
    f.close()
    ip = ""
    for line in lines:
        # take the last IP in config file
        if "DMX-REMOTE-IP" in line:
            try:
                jd=json.loads(line)
                jip = jd["DMX-REMOTE-IP"]
                if ":" in jip and jip.count(".") :
                    ip = jip
            except:pass
    return ip

def _write_default_remote_ip(cfg_file):
    try:
        f = open(cfg_file ,"a")
        f.seek(99999999999)
        txt ='\n'
        txt+=json.dumps({"DMX-REMOTE-IP":"10.10.10.13:0"})
        f.write(txt)
        f.flush()
        f.close()
    except Exception as e:
        print("EXCEPT",e)

def _create_default_config():
    txt=''
    txt+='{"POS_TOP":10}'
    txt+="\n"
    txt+='{"POS_LEFT":10}'
    txt+="\n"

    for i in range(10):
        txt+='{"DMX-FADER-'+str(i+1)+'":500}'
        txt+="\n"

    txt+='{"START_MODE":"PROx"}'
    txt+="\n"
    txt+='{"START_MODE":"EASYx"}'
    txt+="\n"
    txt+=json.dumps({"DMX-REMOTE-IP":"10.10.10.13:0"})
    txt+="\n"

    f = open(h +"/LibreLight/config.json","w")
    f.write(txt)
    f.close()

def _load_config():
    _config = []

    lines = [{}]
    try:
        f = open(h +"/LibreLight/config.json")
        lines = f.readlines()
    except FileNotFoundError as e: #Exception as e:
        _create_default_config()
        cprint("Exception:",e)

    try:
        cprint("config read")
        for line in lines:
            line=line.strip()
            print("   config:",line)
            row = json.loads(line)
            _config.append(row)

    except Exception as e:
        cprint("Exception:",e)

    return _config



def load_remote_ip():
    cfg_file = "/home/user/LibreLight/config.json"
    
    ip = _load_remote_ip(cfg_file)
    if not ip:
        _write_default_remote_ip(cfg_file)
        ip = _load_remote_ip(cfg_file)

    if not ip:
        ip = "0.0.0.0:err"

    return ip



def check_pro_easy():
    try:
        f = open("/home/user/LibreLight/config.json")
        lines = f.readlines()
        f.close()
        for line in lines:
            if '{"START_MODE":"PRO"}' in line:
                print(" PRO")
                return "PRO"
            elif '{"START_MODE":"EASY"}' in line:
                print(" EASY")
                return "EASY"
            print(line)

    except Exception as e:
        print("Exception",e)

    return ""


