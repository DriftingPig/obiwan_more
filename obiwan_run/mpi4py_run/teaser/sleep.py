import multiprocessing
import subprocess

def sleep_slave(time):
    time = int(time)
    print('slave sleep %d s start working' %(time))
    subprocess.call(["./sleep.sh",str(time)])
    print('slave sleep %d s finishes working' %(time))
    return 0

def sleep_master():
    p = multiprocessing.Pool(10)
    p.map(sleep_slave,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

if __name__ == "__main__":
   sleep_master()
    
