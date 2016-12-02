#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import CollectData as collect
__author__ = 'zhouliwei'

"""
function:
date:2016/12/1

"""


class PreProcessData(object):
    # 用于存放计算之后的值[平均fps, 平均jank_count]
    fps_data_dict = {}

    # 用于存放计算之后的cpu值
    cpu_data_dict = {}
    cpu_silent_data_dict = {}

    # 用于存放计算之后的kpi值
    kpi_data_dict = {}

    # 用于存放计算之后的memory值
    memory_data_dict = {}

    # 用于存放计算之后的flow值
    flow_data_dict = {}
    flow_silent_data_dict = {}

    def __init__(self):
        pass

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
            if PreProcessData.fps_data_dict.has_key(now_page_name):
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                last_fps_datas = PreProcessData.fps_data_dict.get(now_page_name)
                now_fps_data = (int(data[2]) + int(last_fps_datas[0])) / 2
                now_jank_count = (int(data[1]) + int(last_fps_datas[1])) / 2
            else:
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                # 不包含当前页面，就直接添加
                now_fps_data = int(data[2])
                now_jank_count = int(data[1])

            PreProcessData.fps_data_dict[now_page_name] = [now_fps_data, now_jank_count]

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
            if PreProcessData.cpu_data_dict.has_key(now_page_name):

                last_cpu_data = PreProcessData.cpu_data_dict.get(now_page_name)
                now_cpu_data = (int(data[1]) + int(last_cpu_data)) / 2
            else:

                # 不包含当前页面，就直接添加
                now_cpu_data = int(data[1])

            PreProcessData.cpu_data_dict[now_page_name] = now_cpu_data

    """
         对kpi数据进行处理
         收集到的kpi数据格式self.now_page_name, self.jump_page, self.cost_time
     """

    @staticmethod
    def __pre_kpi_data(kpi_datas):
        if len(kpi_datas) < 1:
            return
        now_cost_time = 0
        for kpi_data in kpi_datas:
            if len(kpi_data) < 1:
                continue
            now_page_name = kpi_data[0]
            if PreProcessData.kpi_data_dict.has_key(now_page_name):
                if kpi_data[2] != '' and kpi_data[0] != '':
                    last_cost_time = PreProcessData.kpi_data_dict.get(now_page_name, 0)
                    now_cost_time = (int(kpi_data[2]) + int(last_cost_time)) / 2
            else:
                # 不包含就直接添加
                if kpi_data[2] != '' and kpi_data[0] != '':
                    now_cost_time = int(kpi_data[2])
            PreProcessData.kpi_data_dict[now_page_name] = now_cost_time

    """
        用于预处理内存的数据
        数据格式是[[now_page, last_page, 内存增量]]
    """

    @staticmethod
    def __pre_memory_data(memory_datas):
        if len(memory_datas) < 1:
            return
        now_memory_increase = 0
        last_page_name = ''
        for memory_data in memory_datas:
            if len(memory_data) < 1:
                continue
            now_page_name = memory_data[0]
            if PreProcessData.memory_data_dict.has_key(now_page_name):
                memory_value = PreProcessData.memory_data_dict.get(now_page_name)
                if memory_data[1] == memory_value[1]:
                    if memory_data[2] != '':
                        last_memory_increase = memory_value[0]
                        now_memory_increase = (int(last_memory_increase) + memory_data[2]) / 2.0
                        last_page_name = memory_value[1]
                else:
                    now_memory_increase = memory_data[2]
                    last_page_name = memory_data[1]
            else:
                if memory_data[2] != '':
                    now_memory_increase = int(memory_data[2])
                last_page_name = memory_data[1]
            PreProcessData.memory_data_dict[now_page_name] = [now_memory_increase, last_page_name]

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
            if PreProcessData.flow_data_dict.has_key(now_page_name):
                flow_value = PreProcessData.flow_data_dict.get(now_page_name)
                # 同样的逻辑，参考内存的计算方式
                if flow_value[1] == flow_data[1]:
                    last_flow = flow_value[0]
                    now_flow = (int(last_flow) + flow_data[2]) / 2
                    last_page_name = flow_data[1]
                else:
                    now_flow = int(flow_data[2])
                    last_page_name = flow_data[1]
            else:
                now_flow = int(flow_data[2])
                last_page_name = flow_data[1]

            PreProcessData.flow_data_dict[now_page_name] = [now_flow, last_page_name]

    """
        用于处理流量值
        数据格式是：[[now_page, last_page, 流量增量]]
    """

    @staticmethod
    def __pre_silent_flow_data(flow_datas):
        if len(flow_datas) < 1:
            return
        for flow_data in flow_datas:
            if len(flow_data) < 1:
                continue

            now_page_name = flow_data[0]
            if PreProcessData.flow_silent_data_dict.has_key(now_page_name):
                flow_value = PreProcessData.flow_silent_data_dict.get(now_page_name)
                # 同样的逻辑，参考内存的计算方式
                last_flow = flow_value[0]
                now_flow = (int(last_flow) + flow_data[1]) / 2
            else:
                now_flow = int(flow_data[1])

            PreProcessData.flow_silent_data_dict[now_page_name] = now_flow

    """
        用于对收集的cpu数据进行处理
        cpu采集到的数据格式是：[current_page, cpu值]
        处理数据的逻辑：通过current_page来求每个页面的cpu平均值

    """

    @staticmethod
    def __pre_silent_cpu_data(cpu_datas):
        if len(cpu_datas) < 1:
            return
        for data in cpu_datas:
            if len(data) < 1:
                continue
            now_page_name = data[0]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if PreProcessData.cpu_silent_data_dict.has_key(now_page_name):

                last_cpu_data = PreProcessData.cpu_silent_data_dict.get(now_page_name)
                now_cpu_data = (int(data[1]) + int(last_cpu_data)) / 2
            else:

                # 不包含当前页面，就直接添加
                now_cpu_data = int(data[1])

            PreProcessData.cpu_silent_data_dict[now_page_name] = now_cpu_data


    """
          用于对收集的数据进行预处理
          预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
    """
    def pre_process_data(self):
        # 处理收集到的数据
        PreProcessData.__pre_fps_data(collect.fps_datas)
        PreProcessData.__pre_cpu_data(collect.cpu_datas)
        PreProcessData.__pre_flow_data(collect.flow_datas)
        PreProcessData.__pre_kpi_data(collect.kpi_datas)
        PreProcessData.__pre_memory_data(collect.memory_datas)

    """
          用于对收集的数据进行预处理
          预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
    """
    def pre_silent_process_data(self):
        # 处理收集到的数据
        PreProcessData.__pre_silent_cpu_data(collect.cpu_datas)
        PreProcessData.__pre_silent_flow_data(collect.flow_datas)
