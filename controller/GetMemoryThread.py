#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'lzz'

import  threading
import time
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
"""
function: 采集内存数据的逻辑
date:2016/11/23

"""
AdbUtil = AdbUtil()
AndroidUtil = AndroidUtil()


class GetMemoryDataThread(threading.Thread):
    
    times=30 #收集数据条数为30次
#     cycletime=60*60*4 #测试持续时长为4H
    cycletime=5*60 #测试持续时长为5min
    interval = cycletime/times#收集1次所需要的时间，单位为s
    Memorydata=[]#用于收集所有的内存数据
    Memoryerror=[]#用于手机内存占用过高的数据。

    # 任务是否完成
    task_finish = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        GetMemoryDataThread.task_finish = False
        GetMemoryDataThread.clear_data()

    """
        采集内存数据的逻辑
    """
    def run(self):
        i=0
        pkgName = config.test_package_name
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect memory')
            memorydata = int(AndroidUtil.get_memory_data(pkgName))#当前采集到的数据
            if memorydata >= 50*1024:
                memoryerror = memorydata
                self.Memoryerror.append(memoryerror)
                AdbUtil.screenshot()
                LogUtil.log_i('Inspect memory 12')
            LogUtil.log_i('Inspect memory 13')
            self.Memorydata.append(memorydata)
            # time.sleep(self.interval)#设定多久采集一次数据
            i += 1

        GetMemoryDataThread.task_finish = True
        print self.Memoryerror, self.Memorydata

    """
        用于清理数据
    """

    @staticmethod
    def clear_data():
        GetMemoryDataThread.Memorydata = []
        GetMemoryDataThread.Memoryerror = []

if __name__ == '__main__':
    res = GetMemoryDataThread(1)
    print res.start()
    res.join()#子线程执行完毕，才能执行主线程
    print res.Memorydata, res.Memoryerror  #这个就是主线程