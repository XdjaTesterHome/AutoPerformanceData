#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os, sys
import django
BaseDir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoPerformanceData.settings")
django.setup()

from CollectData import CollectData
from performance.models import *
import common.GlobalConfig as config
from util.AndroidUtil import AndroidUtil
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
        PublishData.__publish_fps_data(CollectData.fps_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_cpu_data(CollectData.cpu_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_kpi_data(CollectData.kpi_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_memory_data(CollectData.memory_data_dict, config.test_package_name, PublishData.version_code)
        PublishData.__publish_flow_data(CollectData.flow_data_dict, config.test_package_name, PublishData.version_code)

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
    def __publish_cpu_data(fps_data_fict, package_name, version_code):
        CpuData().save_db_data(fps_data_fict, package_name, version_code)

    """
           将kpi数据保存到数据库
    """

    @staticmethod
    def __publish_kpi_data(kpi_data_fict, package_name, version_code):
        KpiData().save_db_data(kpi_data_fict, package_name, version_code)

    """
        将内存数据保存到数据库
    """

    @staticmethod
    def __publish_memory_data(memory_data_fict, package_name, version_code):
        MemoryData().save_db_data(memory_data_fict, package_name, version_code)

    """
        将flow数据保存到数据库
    """

    @staticmethod
    def __publish_flow_data(flow_data_fict, package_name, version_code):
        MemoryData().save_db_data(flow_data_fict, package_name, version_code)