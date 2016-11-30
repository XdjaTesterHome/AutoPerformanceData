# -*- coding: utf-8 -*-
__author__ = 'lzz'
import threading
import time
class CpuGet(threading.Thread):
    _start0 = 0
    test=[1,2,3]
    def __init__(self,num=20,sleepTime=1):
        threading.Thread.__init__(self)
        self.num = num
        self.sleepTime = sleepTime
    def run(self):
        print self._start0,self.test
        time.sleep(5)
        print "这是一个多线程函数"
        p=5
        return p
ti =CpuGet()
if __name__ == '__main__':
    p = ti.run()
    # time.sleep(5)
    print p
    print "这是主线程"
pass
