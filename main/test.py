#/***************************************************************************
# *-
# * Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# *-
# **************************************************************************/
#-
#-
#-
#/**
# * @file c.py
# * @author zhangruiqing01(com@baidu.com)
# * @date 2015/10/28 20:15:33
# * @brief-
# *--
# **/
#

import time
import threading
import random

def printf(i):
    randtime = random.randint(1,5)
    for x in xrange(5):
        time.sleep(randtime)
        print "T" + str(i), randtime # print T<threadid> randtime

def test():
    thread_list = []
    for i in xrange(10):
        sthread = threading.Thread(target = printf, args = str(i))
        sthread.setDaemon(True)
        sthread.start()
        thread_list.append(sthread)
    for i in xrange(10):
        thread_list[i].join(1)


if __name__ == '__main__':
    test()