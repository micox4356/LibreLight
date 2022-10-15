
import time

print("====== IMPORT ======")
import unittest
import _console as console

#print(dir())
print()
print("====== TEST START ======")
master_fx = console.MASTER_FX()

clock = 0
start = time.time()
fx = []

i=20
f= console.FX(master=master_fx,offset=i) 
print(f)
print()
tick = 1
n=f.next(clock=tick)
print(f)
if int(n*1000) == 3715:
    print("TEST: fx.next",tick,n, "\tOK")
else:
    print("TEST: fx.next",tick,n, "\tfail")
print()
#print("next",n,time.time()-start)
tick=33
n=f.next(clock=tick)
print(f)
if int(n*1000) == -4755:
    print("TEST: fx.next",i*tick,n, "\tOK")
else:
    print("TEST: fx.next",i*tick,n, "\tfail")



if 0: #simulation
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
            #print("next {:0.04} {:0.04} ".format(n,time.time()-start))
        time.sleep(tick)
    print()





if 1: #test
    time.sleep(0.1)
    print()
    print()
    htp_master = console.HTP_MASTER()
    htp_master.data[1] = {"DMX":[22,23,24],"VALUE":80}
    htp_master.data[2] = {"DMX":[42,43,44],"VALUE":70}
    htp_master.data[3] = {"DMX":[22,23,24],"VALUE":99}


    for i in htp_master.data:
         print("data",i,htp_master.data[i])
    print()
    m = 3
    r = htp_master.dmx_by_id(3)
    print("TEST: htp_master.dmx_by_id Master:",m,"is:",r,end="\t")
    c = ('DMX', [22, 23, 24])
    if r == c:
        print("\tOK")
    else:
        print("(",r,"!=",c,")\tfail")

    #print("htp_master r=",r)
    #print()

    m=22
    r = htp_master.master_by_dmx(m)
    print("TEST: the highes master-value of dmx:",m, "is:",r ,end="\t")
    c=99
    if r == c:# ('DMX', [22, 23, 24]):
        #print("\\e[42m") #Red Text\e[0m")
        print("\tOK")
    else:
        print("(",r,"!=",c,")\t\tfail")
    print()
    #print("the highes master-value of dmx",m, "is:",r)
    #input("end")
    #print()
    #print()
    #print()
    #exit()
