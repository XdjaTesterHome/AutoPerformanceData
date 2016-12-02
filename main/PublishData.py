#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os, sys
import django

BaseDir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoPerformanceData.settings")
django.setup()

from performance.models import *
import common.GlobalConfig as config
from util.AndroidUtil import AndroidUtil
from PreProcessData import PreProcessData

__author__ = 'zhouliwei'

"""
function: 用于将收集的数据上报
date:2016/11/25

"""


class PublishData(object):
    # app的版本号
    version_code = ''

    def __init__(self):
        PublishData.version_code = AndroidUtil.get_versioncode(config.test_package_name)

    """
        用于对处理后的数据发布
    """

    @staticmethod
    def publish_data():
        PublishData.__publish_fps_data(PreProcessData.fps_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_cpu_data(PreProcessData.cpu_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_kpi_data(PreProcessData.kpi_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_memory_data(PreProcessData.memory_data_dict, config.test_package_name,
                                          PublishData.version_code)
        PublishData.__publish_flow_data(PreProcessData.flow_data_dict, config.test_package_name,
                                        PublishData.version_code)

    """
        发布静默状态的数据
    """

    @staticmethod
    def publish_silent_data():
        PublishData.__publish_silent_cpu_data(PreProcessData.cpu_silent_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_silent_flow_data(PreProcessData.flow_silent_data_dict, config.test_package_name,
                                               PublishData.version_code)

    """
        将fps数据写入到数据库
    """

    @staticmethod
    def __publish_fps_data(fps_data_dict, package_name, version_code):
        FpsData().save_db_data(fps_data_dict, package_name, version_code)

    """
        将cpu数据保存到数据库
    """

    @staticmethod
    def __publish_cpu_data(fps_data_dict, package_name, version_code):
        CpuData().save_db_data(fps_data_dict, package_name, version_code)

    """
           将kpi数据保存到数据库
    """

    @staticmethod
    def __publish_kpi_data(kpi_data_dict, package_name, version_code):
        KpiData().save_db_data(kpi_data_dict, package_name, version_code)

    """
        将内存数据保存到数据库
    """

    @staticmethod
    def __publish_memory_data(memory_data_dict, package_name, version_code):
        MemoryData().save_db_data(memory_data_dict, package_name, version_code)

    """
        将flow数据保存到数据库
    """

    @staticmethod
    def __publish_flow_data(flow_data_dict, package_name, version_code):
        FlowData().save_db_data(flow_data_dict, package_name, version_code)

    """
         将flow数据保存到数据库
     """

    @staticmethod
    def __publish_silent_flow_data(flow_data_dict, package_name, version_code):
        FlowSilentData().save_db_silent_data(flow_data_dict, package_name, version_code)

    """
          将cpu数据保存到数据库
    """

    @staticmethod
    def __publish_silent_cpu_data(cpu_data_dict, package_name, version_code):
        CpuSilentData().save_db_silent_data(cpu_data_dict, package_name, version_code)

if __name__ == '__main__':
    print AndroidUtil.get_versioncode(config.test_package_name)
