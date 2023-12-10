#/usr/bin/python3
import os

def get_date():
    CAPTION =""
    try:
        _gcmd=r'git log -1 --format=%ci'
        r = os.popen(_gcmd)
        txt=r.read()
        print(txt)
        CAPTION += " " + txt.strip().split()[0]
    except Exception as e:
        print(e)
        CAPTION += " no-date" 
    return CAPTION

def get_commit_id():
    CAPTION = ""
    try:
        _gcmd='git rev-parse --short HEAD'
        r=os.popen(_gcmd)
        txt=r.read()
        CAPTION += " v:"+txt.strip()
    except Exception as e:
        print(e)
        CAPTION += " no git" 
    return CAPTION


def get_all():
    out = ""
    out += get_commit_id()
    out += get_date()
    return out
