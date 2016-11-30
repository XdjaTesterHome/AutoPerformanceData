import os
import multiprocessing
import time

def pabing():
    for i in range(20):
        print 'xxxx'
        i +=1
        time.sleep(1)
    # os.system("python /Users/SvenWeng/Develop/H5/pachong/pabing/run.py")

def mongod():
    for i in range(20):
        print 'yyyy'
        i +=1
        time.sleep(1)
    # os.system("mongod")

if __name__ == '__main__':
    func_list = [pabing, mongod]
    pool = multiprocessing.Pool()
    for x in func_list:
        pool.apply_async(x)
        print type(x)
    pool.close()
    pool.join()