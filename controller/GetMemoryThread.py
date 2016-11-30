#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
from util.LogUtil import LogUtil
import common.GlobalConfig as config
__author__ = 'lzz'


"""
function: 采集内存数据的逻辑
date:2016/11/23

"""
AdbUtil = AdbUtil()
AndroidUtil = AndroidUtil()


class GetMemoryDataThread(threading.Thread):
    # 用于收集所有的内存数据
    memory_datas=[]

    def __init__(self, thread_id, package_name, pic_name='memory'):
        threading.Thread.__init__(self)
        self.threadId = thread_id

        GetMemoryDataThread.clear_data()
        self.pic_name = pic_name
        self.package_name = package_name

    """
        采集内存数据的逻辑
    """
    def run(self):
        exec_count=0
        last_page_name = ''
        last_memory_data = 0
        try:
            while True:
                LogUtil.log_i('Inspect memory')
                if exec_count > config.collect_data_count:
                    break
                memory_data = int(AndroidUtil.get_memory_data(self.package_name))#当前采集到的数据
                now_page_name = AndroidUtil.get_cur_activity()
                # 目前暂时粗略的计算增量，当页面不一样时，计算增量
                if now_page_name != last_page_name:
                    memory_increase = memory_data - last_memory_data
                    if memory_increase < 0:
                        # 对于发生GC的情况，内存增量可能是负值, 暂时先不做处理
                        pass
                    GetMemoryDataThread.memory_datas.append([now_page_name, last_page_name, memory_increase])
                    last_page_name = now_page_name
                else:
                    last_memory_data = memory_data
                    exec_count += 1
                    continue

                # 内存增量大于某个值就认为是有问题
                if memory_increase >= 10 * 1024:
                    AdbUtil.screenshot(self.pic_name)
                    LogUtil.log_i('Inspect memory 12')
                LogUtil.log_i('Inspect memory 13')

                # 设定多久采集一次数据
                time.sleep(config.collect_data_interval)
                exec_count += 1
        except Exception as e:
            LogUtil.log_e('get cpu error'+e.message)

    """
        用于清理数据
    """

    @staticmethod
    def clear_data():
        GetMemoryDataThread.memory_datas = []

if __name__ == '__main__':
    res = GetMemoryDataThread(1)
    print res.start()
    res.join()#子线程执行完毕，才能执行主线程