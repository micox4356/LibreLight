
import time

import unittest
import console

print(dir())


master_fx = console.MASTER_FX()

clock = 0
start = time.time()
fx = []
for i in range(100):
    fx.append( console.FX(master=master_fx,offset=i) )
    n = 0# fx[-1].next()
    print("init",n,time.time()-start)
print()
for f in fx:
    n=f.next(clock=1)
    print("next",n,time.time()-start)

print()
print(time.time()-start)

print(dir(fx))

tick = 0.01
for i in range(100):

    #for f in fx:
    f = fx[-1]
    if 1:
        n=f.next(clock=i*tick)
        print("next {:0.04} {:0.04} ".format(n,time.time()-start))
    time.sleep(tick)
print()

