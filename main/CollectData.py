#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from util.LogUtil import LogUtil
from controller.PerformanceControl import PerformanceControl as control
import common.GlobalConfig as config
from util.AdbUtil import AdbUtil
from util.AndroidUtil import AndroidUtil
import multiprocessing

__author__ = 'zhouliwei'

"""
function: 用于收集数据并进行处理的逻辑
date:2016/11/25

"""


class CollectData(object):
    # 线程id
    MEMORY_THREAD_ID = 101
    CPU_THREAD_ID = 102
    KPI_THREAD_ID = 103
    FLOW_THREAD_ID = 104
    FPS_THREAD_ID = 105

    # 用于存放计算之后的值[平均fps, 平均jank_count]
    fps_data_dict = {}

    # 用于存放计算之后的cpu值
    cpu_data_dict = {}

    # 用于存放计算之后的kpi值
    kpi_data_dict = {}

    # 用于存放计算之后的memory值
    memory_data_dict = {}

    # 用于存放计算之后的flow值
    flow_data_dict = {}

    def __init__(self):
        self.package_name = config.test_package_name
        pass

    """
        用于开始自动收集数据
    """

    def auto_collect_data(self):
        try:
            # # 这里同时启动多个线程，会有问题，后面解决
            # 1. 开始采集kpi数据
            kpi_process = multiprocessing.Process(target=lambda: control.get_kpi_data(self.package_name))
            kpi_process.start()

            #
            # # 2. 开始采集内存数据
            memory_process = multiprocessing.Process(target=lambda: control.get_memory_data(self.package_name))
            memory_process.start()

            # 3. 开始采集cpu数据
            cpu_process = multiprocessing.Process(target=lambda: control.get_cpu_data(self.package_name))
            cpu_process.start()

            # 4. 开始采集帧率数据
            fps_process = multiprocessing.Process(target=lambda: control.get_fps_data(self.package_name))
            fps_process.start()

            #
            # # 5. 开始采集流量数据
            flow_process = multiprocessing.Process(target=lambda: control.get_flow_data(self.package_name))
            flow_process.start()

            LogUtil.log_i('All thread worked!!')
        except Exception as e:
            LogUtil.log_e('collect data failure ' + e.message)

    """
        判断任务是否执行完成
    """

    @staticmethod
    def task_all_finish():
        # flow_task = GetFlowDataThread.task_finish
        # fps_task = GetFpsDataThread.task_finish
        # kpi_task = GetKpiDataThread.task_finish
        # cpu_task = GetCpuDataThread.task_finish
        # memory_task = GetMemoryDataThread.task_finish
        # return flow_task and fps_task and kpi_task and cpu_task and memory_task
        pass

    """
        判断是否符合采集数据的条件
    """

    @staticmethod
    def can_collect_data(package_name):
        # 1. 判断手机是否连接
        mobile_connect = AdbUtil().attach_devices()
        tips = ''
        if not mobile_connect:
            tips = '请连接设备，当前无设备可用'
            return mobile_connect, tips

        # 2. 判断当前进程是否还活着
        process_alive = AndroidUtil.process_alive(package_name)
        if not process_alive:
            tips = 'app进程已被杀死，请打开app后再开始测试'
            return process_alive, tips

        return True, tips

    """
          用于对收集的数据进行预处理
          预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
      """

    def pre_process_data(self):
        # 处理收集到的数据
        CollectData.__pre_fps_data(control.fps_datas)
        CollectData.__pre_cpu_data(control.cpu_datas)
        CollectData.__pre_flow_data(control.flow_datas)
        CollectData.__pre_kpi_data(control.kpi_datas)
        CollectData.__pre_memory_data(control.memory_datas)

    """
        用于对收集的fps数据进行处理
        fps采集到的数据格式是：[frame_count, jank_count, fps, current_page]
        处理数据的逻辑：通过current_page来求每个页面的fps平均值
                     通过一个map去存放，key是page_name,value是[fps_data, jank_count]
    """

    @staticmethod
    def __pre_fps_data(fps_datas):
        if len(fps_datas) <= 0:
            return

        for data in fps_datas:
            if len(data) <= 0:
                continue
            now_page_name = data[len(data) - 1]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if CollectData.fps_data_dict.has_key(now_page_name):
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                last_fps_datas = CollectData.fps_data_dict.get(now_page_name)
                now_fps_data = (int(data[2]) + int(last_fps_datas[0])) / 2
                now_jank_count = (int(data[1]) + int(last_fps_datas[1])) / 2
            else:
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                # 不包含当前页面，就直接添加
                now_fps_data = int(data[2])
                now_jank_count = int(data[1])

            CollectData.fps_data_dict[now_page_name] = [now_fps_data, now_jank_count]

    """
        用于对收集的cpu数据进行处理
        cpu采集到的数据格式是：[current_page, cpu值]
        处理数据的逻辑：通过current_page来求每个页面的cpu平均值

    """

    @staticmethod
    def __pre_cpu_data(cpu_datas):
        if len(cpu_datas) < 1:
            return
        for data in cpu_datas:
            if len(data) < 1:
                continue
            now_page_name = data[0]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if CollectData.cpu_data_dict.has_key(now_page_name):

                last_cpu_data = CollectData.cpu_data_dict.get(now_page_name)
                now_cpu_data = (int(data[1]) + int(last_cpu_data)) / 2
            else:

                # 不包含当前页面，就直接添加
                now_cpu_data = int(data[1])

            CollectData.fps_data_dict[now_page_name] = now_cpu_data

    """
        对kpi数据进行处理
        收集到的kpi数据格式self.now_page_name, self.jump_page, self.cost_time
    """

    @staticmethod
    def __pre_kpi_data(kpi_datas):
        if len(kpi_datas) < 1:
            return
        for kpi_data in kpi_datas:
            if len(kpi_data) < 1:
                continue
            now_page_name = kpi_data[0]
            if CollectData.kpi_data_dict.has_key(now_page_name):
                last_cost_time = CollectData.kpi_data_dict.get(now_page_name, 0)
                now_cost_time = (int(kpi_data[2]) + int(last_cost_time)) / 2
            else:
                # 不包含就直接添加
                now_cost_time = int(kpi_data[2])
            CollectData.kpi_data_dict[now_page_name] = now_cost_time

    """
        用于预处理内存的数据
        数据格式是[[now_page, last_page, 内存增量]]
    """

    @staticmethod
    def __pre_memory_data(memory_datas):
        if len(memory_datas) < 1:
            return

        for memory_data in memory_datas:
            if len(memory_data) < 1:
                continue
            now_page_name = memory_data[0]
            if CollectData.memory_data_dict.has_key(now_page_name):
                memory_value = CollectData.memory_data_dict.get(now_page_name)
                # 假如是从同一个页面跳转过来的
                if memory_value[1] == memory_data[1]:
                    last_memory_increase = memory_value[0]
                    now_memory_increase = (int(last_memory_increase) + memory_data[2]) / 2
                    last_page_name = memory_value[1]
                else:
                    now_memory_increase = memory_data[2]
                    last_page_name = memory_data[1]
            else:
                now_memory_increase = int(memory_data[2])
                last_page_name = memory_data[1]
            CollectData.memory_data_dict[now_page_name] = [now_memory_increase, last_page_name]

    """
        用于处理流量值
        数据格式是：[[now_page, last_page, 流量增量]]
    """
    @staticmethod
    def __pre_flow_data(flow_datas):
        if len(flow_datas) < 1:
            return
        for flow_data in flow_datas:
            if len(flow_data) < 1:
                continue

            now_page_name = flow_data[0]
            if CollectData.flow_data_dict.has_key(now_page_name):
                flow_value = CollectData.flow_data_dict.get(now_page_name)
                # 同样的逻辑，参考内存的计算方式
                if flow_value[1] == flow_data[1]:
                    last_flow = flow_value[0]
                    now_flow = (int(last_flow) + flow_data[2])/2
                    last_page_name = flow_data[1]
                else:
                    now_flow = int(flow_data[2])
                    last_page_name = flow_data[1]
            else:
                now_flow = int(flow_data[2])
                last_page_name = flow_data[1]

            CollectData.flow_data_dict[now_page_name] = [now_flow, last_page_name]

