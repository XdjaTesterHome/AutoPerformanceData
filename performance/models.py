#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""
    用于存放fps数据
"""


class FpsData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 包名
    package = models.CharField(max_length=160)

    # 版本号
    version = models.CharField(max_length=160)

    # 测试数据
    testvalue = models.CharField(max_length=50)

    # 日志路径
    logPath = models.CharField(max_length=50)

    # methodTracePath
    methodTracePath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    def __unicode__(self):
        return self.currentPage + '--' + self.packageName

    """
        获取所有的数据
    """

    @staticmethod
    def get_all_data():
        fps_data_list = FpsData.objects.all()
        result_fps_list = [[u'当前页面', u'平均fps值', u'平均丢帧数目']]
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.page, fps_data.testvalue])
        return result_fps_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        fps_data_list = FpsData.objects.filter(package=package_name, version=version)
        result_fps_list = [[u'当前页面', u'平均fps值']]
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.page, fps_data.fps])
        return result_fps_list


"""
    用于存放kpi数据
"""


class KpiData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 包名
    package = models.CharField(max_length=160)

    # 版本
    version = models.CharField(max_length=160)

    # 测试版本
    testvalue = models.CharField(max_length=50)

    # 日志目录
    logPath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    """
        获取所有的数据
        界面暂时只展示页面和kpi数据
    """

    @staticmethod
    def get_all_data():
        kpi_data_list = KpiData.objects.all()
        result_kpi_list = [[u'当前页面', u'加载时间(ms)']]
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.page, kpi_data.testvalue])
        return result_kpi_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        kpi_data_list = KpiData.objects.filter(package=package_name, version=version)
        result_kpi_list = [[u'当前页面', u'加载时间(ms)']]
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.page, kpi_data.testvalue])
        return result_kpi_list


"""
    用于存放flow数据
"""


class FlowData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 平均cpu
    testvalue = models.CharField(max_length=50)

    # 测试应用的包名
    package = models.CharField(max_length=160)
    # 版本号
    version = models.CharField(max_length=160)

    # 日志的路径
    logPath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    """
        获取所有的数据
        界面暂时只展示页面和flow数据
    """

    @staticmethod
    def get_all_data():
        flow_data_list = FlowData.objects.all()
        result_flow_list = [[u'当前页面', u'流量消耗(KB)']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.page, flow_data.testvalue])
        return result_flow_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        flow_data_list = FlowData.objects.filter(package=package_name, version=version)
        result_flow_list = [[u'当前页面', u'流量增量(KB)']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.page, flow_data.testvalue])
        return result_flow_list


"""
    用于存放静默状态flow数据
"""


class FlowSilentData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 平均cpu
    testvalue = models.CharField(max_length=50)

    # 测试应用的包名
    package = models.CharField(max_length=160)
    # 版本号
    version = models.CharField(max_length=160)

    # 保存日志的路径
    logPath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    """
         获取所有的数据
         界面暂时只展示页面和flow数据
     """

    @staticmethod
    def get_all_slient_data():
        flow_data_list = FlowSilentData.objects.all()
        result_flow_list = [[u'当前页面', u'流量值']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.page, flow_data.testvalue])
        return result_flow_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        flow_data_list = FlowSilentData.objects.filter(package=package_name, version=version)
        result_flow_list = [[u'当前页面', u'流量值']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.page, flow_data.testvalue])
        return result_flow_list


"""
    用于存放BatteryData数据
"""


class BatteryData(models.Model):
    # uid
    uid = models.CharField(max_length=11)

    # 当前app的包名
    appPackageName = models.CharField(max_length=128)

    # battery使用情况
    testvalue = models.CharField(max_length=128)

    # 详细使用情况
    detailInfo = models.CharField(max_length=256)

    # 测试应用的包名
    package = models.CharField(max_length=128)
    # 版本号
    version = models.CharField(max_length=128)

    """
        获取所有的数据
        界面暂时只展示页面和flow数据
    """

    @staticmethod
    def get_all_data():
        battery_data_list = BatteryData.objects.all()
        result_battery_list = [[u'Uid', u'应用包名', u'耗电量情况']]
        for battery_data in battery_data_list:
            result_battery_list.append([battery_data.uid, battery_data.appPackageName, battery_data.testvalue])
        return result_battery_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        battery_data_list = BatteryData.objects.filter(package=package_name, version=version)
        result_battery_list = [[u'Uid', u'应用包名', u'耗电量情况']]
        for battery_data in battery_data_list:
            result_battery_list.append([battery_data.uid, battery_data.appPackageName, battery_data.testvalue])
        return result_battery_list


"""
    用于存放测试应用公共数据
"""


class CommonData(models.Model):
    # 测试的包名
    package = models.CharField(max_length=128)

    # 测试的app版本号
    version = models.CharField(max_length=128)

    """
        获取所有的数据
        包名和版本号
    """

    @staticmethod
    def get_all_data():
        common_data_list = CommonData.objects.all()
        result_common_list = []
        for common_data in common_data_list:
            result_common_list.append(
                [common_data.package, common_data.version])
        return result_common_list

    """
        获取所有的packageName
    """

    @staticmethod
    def get_all_package_name():
        common_data_list = CommonData.objects.all()
        result_common_list = []
        for common_data in common_data_list:
            result_common_list.append(common_data.package)
        return result_common_list

    """
        根据包名获取所有的版本信息
    """

    @staticmethod
    def get_all_version_by_package_name(package_name):
        common_versions = CommonData.objects.filter(package=package_name)
        result_common_list = []
        for common_version in common_versions:
            result_common_list.append(common_version.version)

        return result_common_list

    def __unicode__(self):
        return self.package + '-' + self.version

"""
    用于存放memory数据
"""
class MemoryData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 测试应用的包名
    package = models.CharField(max_length=160)
    # 版本号
    version = models.CharField(max_length=160)

    # 平均cpu
    testvalue = models.CharField(max_length=50)

    # 日志的路径
    logPath = models.CharField(max_length=128)

    # methodTrance
    methodTracePath =  models.CharField(max_length=128)

    # memoryDump
    hprofPath = models.CharField(max_length=128)

    # isPass 是否测试通过
    isPass = models.BigIntegerField()

    """
        获取所有的数据
        界面暂时只展示页面和memory数据
    """

    @staticmethod
    def get_all_data():
        memory_data_list = MemoryData.objects.all()
        result_memory_list = [[u'当前页面', u'内存增量(KB)']]
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.page, memory_data.testvalue])
        return result_memory_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        memory_data_list = MemoryData.objects.filter(package=package_name, version=version)
        result_memory_list = [[u'当前页面', u'内存增量(KB)']]
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.page, memory_data.testvalue])
        return result_memory_list
"""
    用于存放cpu数据
"""

class CpuData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)
    # 测试应用的包名
    package = models.CharField(max_length=128)
    # 版本号
    version = models.CharField(max_length=128)

    # 平均cpu
    testvalue = models.CharField(max_length=50)

    # 日志
    logPath = models.CharField(max_length=50)

    # methodTrace
    methodTracePath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    """
        获取所有的数据
    """

    @staticmethod
    def get_all_data():
        cpu_data_list = CpuData.objects.all()
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.page, cpu_data.testvalue])
        return result_cpu_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        cpu_data_list = CpuData.objects.filter(package=package_name, version=version)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.page, cpu_data.testvalue])
        return result_cpu_list
"""
    用于存放静默状态cpu数据
"""
class CpuSilentData(models.Model):
    # 当前页面
    page = models.CharField(max_length=80)

    # 测试应用的包名
    package = models.CharField(max_length=128)
    # 版本号
    version = models.CharField(max_length=128)

    # 平均cpu
    testvalue = models.BigIntegerField()

    # 日志
    logPath = models.CharField(max_length=50)

    # methodTrace
    methodTracePath = models.CharField(max_length=50)

    # 测试是否通过
    isPass = models.BigIntegerField()

    """
        获取所有的数据
    """

    @staticmethod
    def get_all_silent_data():
        cpu_data_list = CpuSilentData.objects.all()
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.page, cpu_data.testvalue])
        return result_cpu_list

    """
        根据packageName和version筛选数据
    """

    @staticmethod
    def get_data_with_pkg_version(package_name, version):
        cpu_data_list = CpuSilentData.objects.filter(package=package_name, version=version)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.page, cpu_data.testvalue])
        return result_cpu_list