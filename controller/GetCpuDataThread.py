#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'lzz'
import  threading
import time
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
import common.GlobalConfig as config
from util.LogUtil import LogUtil
"""
function: 用于采集cpu数据的逻辑
date:2016/11/23

"""
AdbUtil = AdbUtil()
AndroidUtil = AndroidUtil()
class GetCpuDataThread(threading.Thread):
    times=30 #收集数据条数为30次
#     cycletime=60*60*4 #测试持续时长为4H
    cycletime=5*60 #测试持续时长为5min
    interval = cycletime/times#收集1次所需要的时间，单位为s
    CPUdata=[]#用于收集所有的CPU数据
    CPUerror=[]#用于手机CPU占用过高的数据。

    # 任务是否完成
    task_finish = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        GetCpuDataThread.task_finish = False
        GetCpuDataThread.clear_data()

    """
        获取cpu数据的逻辑
    """
    def run(self):
        i = 0
        pkgName = config.test_package_name
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect cpu')
            current_page, cpudata = AndroidUtil.get_cpu_data(pkgName)#当前采集到的数据
            if cpudata >= 50.00:
                self.CPUerror.append([current_page, cpudata])
                AdbUtil.screenshot('cpu')
            else:
                pass
            self.CPUdata.append([current_page, cpudata])
            time.sleep(config.collect_data_interval)#设定多久采集一次数据
            i += 1
        print "CPUerror:",self.CPUerror,"CPUdata:", self.CPUdata
        GetCpuDataThread.task_finish = True
        LogUtil.log_i('Inspect cpu finish')

    """
        用于清理数据
    """

    @staticmethod
    def clear_data():
        GetCpuDataThread.CPUdata = []
        GetCpuDataThread.CPUerror = []


if __name__ == '__main__':
    res = GetCpuDataThread(1)
    res.start()
