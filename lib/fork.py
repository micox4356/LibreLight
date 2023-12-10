#!/usr/bin/python3

import sys
import os 

def fork(cmd=" ",run="/usr/bin/python3"):
    print("FORK:",run,[cmd])
    os.execl(run,cmd)
    sys.exit()

if __name__ == "__main__":
    fork()
