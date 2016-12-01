#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
import common.GlobalConfig as config
from util.LogUtil import LogUtil
__author__ = 'lzz'

"""
function: 用于采集cpu数据的逻辑
date:2016/11/23

"""


class GetCpuDataThread(threading.Thread):

    # 用于收集所有的CPU数据
    cpu_datas=[]

    def __init__(self, thread_id, package_name, pic_name='cpu'):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        GetCpuDataThread.clear_data()
        self.pic_name = pic_name
        self.package_name = package_name

    """
        获取cpu数据的逻辑
    """
    def run(self):
        exec_count = 0
        while True:
            LogUtil.log_i('Inspect cpu')
            if exec_count > config.collect_data_count:
                break
            current_page, cpu_datas = AndroidUtil.get_cpu_data(self.package_name)#当前采集到的数据
            if cpu_datas >= 50.00:
                # 对错误进行处理
                AdbUtil.screenshot(self.pic_name)
            else:
                pass
            GetCpuDataThread.cpu_datas.append([current_page, cpu_datas])
            # 设定多久采集一次数据
            time.sleep(config.collect_data_interval)
            exec_count += 1
        LogUtil.log_i('Inspect cpu finish')

    """
        用于清理数据
    """

    @staticmethod
    def clear_data():
        GetCpuDataThread.cpu_datas = []


if __name__ == '__main__':
    res = GetCpuDataThread(1)
    res.start()
