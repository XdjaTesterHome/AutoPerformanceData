#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import common.GlobalConfig as config
from util.LogUtil import LogUtil
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
from monkey.Monkey import Monkey

import time
import re
import subprocess

__author__ = 'zhouliwei'

"""
function: 主要用于对各种性能数据的采集
date:2016/11/30

"""


class PerformanceControl(object):
    # 用于存放搜集的数据
    cpu_datas = []
    flow_datas = []
    fps_datas = []
    kpi_datas = []
    memory_datas = []
    battery_datas = []

    METHOD_ARRAY = ['cpu', 'memory', 'kpi', 'fps', 'flow', 'monkey']
    SILENT_ARRAY = ['cpu', 'flow']

    def __init__(self):
        pass

    """
        用于获取cpu数据
    """

    @staticmethod
    def get_cpu_data(package_name, pic_name='cpu'):
        i = 0
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect cpu')
            current_page, cpu_data = AndroidUtil.get_cpu_data(package_name)  # 当前采集到的数据
            if cpu_data >= 50.00:

                AdbUtil.screenshot(pic_name)
            else:
                pass
            PerformanceControl.cpu_datas.append([current_page, cpu_data])
            time.sleep(config.collect_data_interval)  # 设定多久采集一次数据
            i += 1
        LogUtil.log_i('Inspect cpu finish')

    """
        用于获取cpu数据
    """

    @staticmethod
    def get_cpu_data_silent(package_name, pic_name='cpu'):
        i = 0
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect cpu')
            current_page, cpu_data = AndroidUtil.get_cpu_data(package_name)  # 当前采集到的数据
            if cpu_data >= 50.00:

                AdbUtil.screenshot(pic_name)
            else:
                pass
            PerformanceControl.cpu_datas.append([current_page, cpu_data])
            time.sleep(config.collect_data_interval)  # 设定多久采集一次数据
            i += 1
        LogUtil.log_i('Inspect cpu finish')


    """
        用于获取流量数据
    """

    @staticmethod
    def get_flow_data(package_name, pic_name='flow'):
        # 处理有问题的流量数据，暂定有问题的流量是大于1M时
        def handle_error_data(current_flow):
            if current_flow > 5 * 1024:
                # 异常处理
                AdbUtil.screenshot(pic_name)

        # 死循环，满足条件后跳出
        exec_count = 0
        last_flow_data = 0
        last_page_name = ''
        last_flow = 0
        current_flow_data = 0
        while True:
            LogUtil.log_i('get flow data' + str(exec_count))
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据 返回三个值，接收的流量、发送的流量、流量总数据，单位是KB
            flow_recv, flow_send, flow_total = AndroidUtil.get_flow_data(package_name)
            now_page_name = AndroidUtil.get_cur_activity()

            if exec_count > 0:
                current_flow_data = flow_total - last_flow_data
                if now_page_name != last_page_name:
                    flow_increase = current_flow_data - last_flow
                    last_page_name = now_page_name
                    PerformanceControl.flow_datas.append([now_page_name, last_page_name, flow_increase])
                    handle_error_data(flow_increase)

            # 用于记录每次的流量增量
            last_flow = current_flow_data
            exec_count += 1
            # 用于计算每次采集流量增量
            last_flow_data = flow_total

            # 时间间隔
            time.sleep(config.collect_data_interval)

    """
        用于获取fps数据
        @:param package_name 当前的包名
        @:param pic_name  出问题时保存的图片名称
    """

    @staticmethod
    def get_fps_data(package_name, pic_name='fps'):
        # 处理可能有问题的场景
        def handle_error_data(jank_count, fps):
            # 暂时当fps < 50 或者 jank_count > 10 我们认为是不达标的
            if fps < 50 or jank_count > 10:
                # 截图
                AdbUtil.screenshot(pic_name)
                # 保存日志

        # 死循环，满足条件后跳出
        exec_count = 0
        while True:
            LogUtil.log_i('get fps data')
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据
            frame_count, jank_count, fps = AndroidUtil.get_fps_data_by_gfxinfo(package_name)
            if frame_count is None and jank_count is None and fps is None:
                exec_count += 1
                continue
            current_page = AndroidUtil.get_cur_activity()
            PerformanceControl.fps_datas.append([frame_count, jank_count, fps, current_page])

            # 处理有问题的数据
            handle_error_data(jank_count, fps)
            exec_count += 1

            # 采集数据时间间隔
            time.sleep(config.collect_data_interval)

    """
        用于获取kpi数据
        @:param package_name 当前的包名
        @:param pic_name  出问题时保存的包名
    """

    @staticmethod
    def get_kpi_data(package_name, pic_name='kpi'):
        # 处理异常的kpi数据,当跳转时间大于3s（暂定）
        def handle_error_data(cost_time):
            if cost_time != '' and cost_time is not None:
                cost_time_value = handle_cost_time(cost_time)
                if cost_time_value > 3000:
                    AdbUtil.screenshot(pic_name)

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
        cmd = 'adb logcat -c && adb logcat -v time -s ActivityManager | findStr %s' % package_name
        try:
            results = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        except Exception as e:
            LogUtil.log_e('get kpi failure ' + e.message)

        # 这里的逻辑是采集一定时间的数据之后，结束进程
        jump_page = ''
        cost_time = ''
        now_page_name = ''
        # 采集数据的次数
        get_count = 0
        while True:
            LogUtil.log_i('get kpi data')
            if get_count > config.collect_data_count:
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
                        jump_page = 'unknow'
                        cost_time = 0
                    else:
                        jump_page = result[0].split('/')[1]
                        cost_time = result[1]

            # 2. 获取从哪个页面跳转
            if 'Moving to STOPPED:' in data:
                now_page = data.split('Moving to STOPPED:')
                now_page = now_page[1].strip().split(' ')
                if len(now_page) > 3:
                    now_page_name = now_page[2].split('/')[1]
                else:
                    now_page_name = 'unknow'

            # 将结果保存到数组中
            if now_page_name is not None and jump_page is not None and cost_time is not None:
                PerformanceControl.kpi_datas.append([now_page_name, jump_page, handle_cost_time(cost_time)])
                handle_error_data(cost_time)
            get_count += 1

    """
        用于获取内存的数据
    """

    @staticmethod
    def get_memory_data(package_name, pic_name='memory'):
        i = 0
        last_page_name = ''
        last_memory_data = 0
        memory_increase = 0
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect memory')
            memory_data = int(AndroidUtil.get_memory_data(package_name))  # 当前采集到的数据
            now_page_name = AndroidUtil.get_cur_activity()
            # 目前暂时粗略的计算增量，当页面不一样时，计算增量
            if now_page_name != last_page_name:
                memory_increase = memory_data - last_memory_data
                if memory_increase < 0:
                    # 对于发生GC的情况，内存增量可能是负值, 暂时先不做处理
                    pass
                PerformanceControl.memory_datas.append([now_page_name, last_page_name, memory_increase])
                last_page_name = now_page_name
            else:
                last_memory_data = memory_data
                i += 1
                continue
            # 内存增量大于某个值就认为是有问题
            if memory_increase >= 10 * 1024:
                AdbUtil.screenshot(pic_name)
                LogUtil.log_i('Inspect memory 12')
            LogUtil.log_i('Inspect memory 13')

            # 设定多久采集一次数据
            time.sleep(config.collect_data_interval)
            i += 1

    """
        用于跑monkey
    """
    def run_monkey(time, package_name):
        LogUtil.log_i('begin exec monkey')
        Monkey.run_monkey(time, package_name)
        LogUtil.log_i('monkey exec success')

    """
        用于处理电量相关的数据
    """

    def get_battery_data(self, package_name, pic_name='battery'):
        pass

    @staticmethod
    def get_data(method_type, package_name):
        print 'exceute get_data' + method_type
        if method_type == PerformanceControl.METHOD_ARRAY[0]:
            PerformanceControl.get_cpu_data(package_name)
        elif method_type == PerformanceControl.METHOD_ARRAY[1]:
            PerformanceControl.get_memory_data(package_name)
        elif method_type == PerformanceControl.METHOD_ARRAY[2]:
            PerformanceControl.get_kpi_data(package_name)
        elif method_type == PerformanceControl.METHOD_ARRAY[3]:
            PerformanceControl.get_fps_data(package_name)
        elif method_type == PerformanceControl.METHOD_ARRAY[4]:
            PerformanceControl.get_flow_data(package_name)
        elif method_type == PerformanceControl.METHOD_ARRAY[5]:
            PerformanceControl.run_monkey(package_name)
