#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import common.GlobalConfig as config
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
import time
from util.LogUtil import LogUtil as log

__author__ = 'zhouliwei'

"""
function: 用于获取流量数据的线程
date:2016/11/24

"""


class GetFlowDataThread(threading.Thread):

    # 用于存放采集到的流量数据
    flow_datas = []

    # 记录上一次的total流量值
    last_flow_data = 0

    # 当前时间段的流量值
    current_flow_data = 0

    # 用于存放采集到的有问题的流量数据
    flow_error_datas = [['flow_data', 'current_page', 'pic_name']]

    # 任务是否完成
    task_finish = False

    def __init__(self, thread_id, package_name):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.package_name = package_name
        self.pic_name = 'flow'
        # 每次开启线程，清理上次的数据
        GetFlowDataThread.clear_data()
        GetFlowDataThread.task_finish = False

    """
        用于采集流量数据
    """
    def run(self):
        # 处理有问题的流量数据，暂定有问题的流量是大于1M时
        def handle_error_data(current_flow):
            if current_flow > 1 * 1024:
                current_page = AndroidUtil.get_cur_activity()
                AdbUtil.screenshot(self.pic_name)
                GetFlowDataThread.flow_error_datas.append([current_flow, current_page, self.pic_name])

        # 死循环，满足条件后跳出
        exec_count = 0
        last_page_name = ''
        last_flow_data = 0

        while True:
            log.log_i('get flow data' + str(exec_count))
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据 返回三个值，接收的流量、发送的流量、流量总数据，单位是KB
            flow_recv, flow_send, flow_total = AndroidUtil.get_flow_data(self.package_name)

            if exec_count > 0:
                self.current_flow_data = flow_total - self.last_flow_data
                GetFlowDataThread.flow_datas.append(self.current_flow_data)
                handle_error_data(self.current_flow_data)

            exec_count += 1
            self.last_flow_data = flow_total

            # 时间间隔
            time.sleep(config.collect_data_interval)

        GetFlowDataThread.task_finish = True

    """
        清理数据
    """
    @staticmethod
    def clear_data():
        GetFlowDataThread.flow_datas = []
        GetFlowDataThread.flow_error_datas = [['flow_data', 'current_page', 'pic_name']]


if __name__ == '__main__':
    for i in (0,1):
        GetFlowDataThread(102, 'com.xdja.safekeyservice').start()







