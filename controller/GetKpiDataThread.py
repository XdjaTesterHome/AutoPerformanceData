#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
import subprocess
import common.GlobalConfig as config
from util.LogUtil import LogUtil as log
from util.AdbUtil import AdbUtil
import re

__author__ = 'zhouliwei'

"""
function: 获得kpi相关的数据。
          kpi数据想着是通过 adb logcat -c && adb logcat -v time -s ActivityManager | findStr pkgName获取
date:2016/11/24

"""


class GetKpiDataThread(threading.Thread):
    # 用于收集kpi的数据
    kpi_datas = []

    # 当前页面名称
    now_page_name = ''

    # 跳转页面名称
    jump_page = ''

    # 跳转花费时间
    cost_time = ''

    def __init__(self, thread_id, package_name, pic_name='kpi'):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.package_name = package_name
        self.pic_name = pic_name
        # 每次执行数据先清空之前的数据
        GetKpiDataThread.clear_data()

    """
        循环获取kpi数据的逻辑
    """

    def run(self):
        # 处理异常的kpi数据,当跳转时间大于3s（暂定）
        def handle_error_data():
            if self.cost_time != '' and self.cost_time is not None:
                cost_time_value = handle_cost_time(self.cost_time)
                if cost_time_value > 3000:
                    AdbUtil.screenshot(self.pic_name)
                    GetKpiDataThread.kpi_error_datas.append([self.now_page_name, self.jump_page, self.cost_time, self.pic_name])

        # 因为从日志中得到的值都是 +345ms 或者 +1s234ms
        def handle_cost_time(cost_time):
            s_data = 0
            ms_data = 0
            s_result = re.findall(r'\ds', cost_time)
            if len(s_result) > 0:
                s_data = int(s_result[0].split('s')[0]) * 1000
            ms_result = re.findall(r'\d\d\dms', cost_time)
            if len(ms_result) > 0:
                ms_data = int(ms_result[0].split('ms')[0])

            return s_data + ms_data

        # 记录起始时间
        global results
        start_time = time.mktime(time.localtime())
        cmd = 'adb logcat -c && adb logcat -v time -s ActivityManager | findStr %s' % self.package_name
        try:
            results = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        except Exception as e:
            log.log_e('get kpi failure ' + e.message)

        # 这里的逻辑是采集一定时间的数据之后，结束进程
        exect_count = 0
        while True:
            log.log_i('get kpi data')
            if exect_count > config.collect_data_count:
                if results.poll() is None:
                    print 'results.terminate()'
                    results.stdout.close()
                break
            # 2.读取内容，并分析
            data = results.stdout.readline()
            print data
            # 处理读取到的String
            if data is not None:
                if 'Displayed' in data:
                    # 1. 获取跳转页面的名称及时间，过滤 Displayed
                    result = data.split('Displayed')
                    result = result[1].strip().split(':')
                    if len(result) < 1:
                        self.jump_page = 'unknow'
                        self.cost_time = 0
                    else:
                        self.jump_page = result[0].split('/')[1]
                        self.cost_time = result[1]

            # 2. 获取从哪个页面跳转
            if 'Moving to STOPPED:' in data:
                now_page = data.split('Moving to STOPPED:')
                now_page = now_page[1].strip().split(' ')
                if len(now_page) > 3:
                    self.now_page_name = now_page[2].split('/')[1]
                else:
                    self.now_page_name = 'unknow'

            # 将结果保存到数组中
            if self.now_page_name is not None and self.jump_page is not None and self.cost_time is not None:
                GetKpiDataThread.kpi_datas.append([self.now_page_name, self.jump_page, self.cost_time])
                handle_error_data()

            exect_count += 1

    """
        用于清理数据
    """
    @staticmethod
    def clear_data():
        GetKpiDataThread.kpi_datas = []


if __name__ == '__main__':
    kpi_thread = GetKpiDataThread(102, 'com.xdja.safekeyservice')
    kpi_thread.start()