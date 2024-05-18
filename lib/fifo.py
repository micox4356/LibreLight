
cmd="mkfifo backpipe"
fname = "/home/user/backpipe" # fifo named pipe
import json
import sys
import time
import _thread as thread

def write(data):
    txt =json.dumps(data)
    f = open(fname,"w")
    f.write(txt)
    f.close()


def read():
    f = open(fname,"w")
    txt = f.read()
    f.close()
    txt =json.loads(txt)
    return txt

class read_loop():
    def __init__(self):
        self.fname = fname
        #self.f = open(self.fname,"r")
        self.s = time.time()
        self.buf = []
        self.lock = thread.allocate_lock()
    def loop(self):
        thread.start_new_thread(self._loop,())
    def read(self):
        #print("read",self)
        out = []
        self.lock.acquire()
        try:
            if self.buf:
                out = self.buf[:]
                self.buf = []
        finally:
            self.lock.release()
        return out

    def _loop(self):

        print("start._loop",self)
        while 1:
            #print(2)
            self.lock.acquire()
            self.f = open(self.fname,"r")
            #print(1)
            txt="null"
            try:
                txt = self.f.read()
                txt=txt.strip()
                txt=json.loads(txt)
                #print("read",txt)
                self.buf.append(txt)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("TXT",[txt])
                print("ERR",e)
            finally:
                self.lock.release()
            time.sleep(0.01)

if __name__ == "__main__":
    if "server" in sys.argv:
        server = read_loop()
        server.loop()
        while 1:
            try:
                data = server.read()
                if data:
                    for i in data:
                        print(":",i)
                else:
                    time.sleep(0.01)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                print("ERR1",e)


    elif "client" in sys.argv:
        i=0
        while 1:
            #msg=json.dumps({"event":"EXEC","EXEC":btn_nr,"VAL":v,"F-KEY":btn_nr_raw})#.encode("utf-8")
            #cmd =  "echo '{}' > ~/backpipe ".format(msg)
            data = ["data {}".format(i)]*100
            data = {"hi":i}
            print(data)
            txt = write(data)
            time.sleep(.1)
            i+=1
