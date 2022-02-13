import os, sys
import random
import time

path = "/tmp/pipe"
# pipe as socket replacement

try:
    try:
        os.mkfifo(path)
        while 1:
            fifo = open(path, 'r')
            x=fifo.read()
            if x:
                print(x)
            time.sleep(0.3)
    except OSError as e:
        print( "EXC FIFO create", e)
        i = 0
        while 1:
            x=random.randint(1000,9999)
            print(i)
            fifo = open(path, 'w')
            fifo.write("{} {}\n".format(x,i))
            fifo.flush()
            fifo.close()
            i+=1
            time.sleep(1)

except:
    os.unlink(path)

