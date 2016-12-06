#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

"""
function: 用于存放性能数据并传递
date:2016/12/5

"""


class GlobalPerformanceData(object):
    # 存放收集到的性能数据
    cpu_datas = []
    flow_datas = []
    fps_datas = []
    kpi_datas = []
    memory_datas = []
    flow_datas_silent = []
    cpu_datas_silent = []

    def __init__(self):
        pass

    @staticmethod
    def append_cpu_datas(data):
        GlobalPerformanceData.cpu_datas.append(data)

    @staticmethod
    def get_cpu_datas():
        return GlobalPerformanceData.cpu_datas

    @staticmethod
    def append_flow_datas(data):
        GlobalPerformanceData.flow_datas.append(data)

    @staticmethod
    def get_flow_datas():
        return GlobalPerformanceData.flow_datas

    @staticmethod
    def append_fps_datas(data):
        GlobalPerformanceData.fps_datas.append(data)

    @staticmethod
    def get_fps_datas():
        return GlobalPerformanceData.fps_datas

    @staticmethod
    def append_kpi_datas(data):
        GlobalPerformanceData.kpi_datas.append(data)

    @staticmethod
    def get_kpi_datas():
        return GlobalPerformanceData.kpi_datas

    @staticmethod
    def append_memory_datas(data):
        GlobalPerformanceData.memory_datas.append(data)

    @staticmethod
    def get_memory_datas():
        return GlobalPerformanceData.memory_datas

    @staticmethod
    def append_silent_flow_datas(data):
        GlobalPerformanceData.flow_datas_silent.append(data)

    @staticmethod
    def get_silent_flow_datas():
        return GlobalPerformanceData.flow_datas_silent

    @staticmethod
    def append_silent_cpu_datas(data):
        GlobalPerformanceData.cpu_datas_silent.append(data)

    @staticmethod
    def get_silent_cpu_datas():
        return GlobalPerformanceData.cpu_datas_silent

    @staticmethod
    def clear_data():
        GlobalPerformanceData.cpu_datas = []
        GlobalPerformanceData.flow_datas = []
        GlobalPerformanceData.fps_datas = []
        GlobalPerformanceData.kpi_datas = []
        GlobalPerformanceData.memory_datas = []

    @staticmethod
    def clear_silent_data():
        GlobalPerformanceData.cpu_datas_silent = []
        GlobalPerformanceData.flow_datas_silent = []
