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
    currentPage = models.TextField()
    # 测试页面的帧率
    fps = models.BigIntegerField()
    # 测试页面丢帧数目
    jankCount = models.BigIntegerField()
    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    def __unicode__(self):
        return self.currentPage + '--' + self.packageName

    """
        批量的保存数据
    """

    def save_db_data(self, fps_data_dict, package_name, version_code):

        fps_list_to_insert = []
        fps_keys = fps_data_dict.keys()
        if len(fps_keys) <= 0:
            return
        for key in fps_keys:
            value = fps_data_dict.get(key)
            fps_list_to_insert.append(
                FpsData(currentPage=key, fps=value[0], jankCount=value[1], packageName=package_name,
                        versionCode=version_code))

        FpsData.objects.bulk_create(fps_list_to_insert)

    """
        获取所有的数据
    """

    def get_all_data(self):
        fps_data_list = FpsData.objects.all()
        result_fps_list = []
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.currentPage, fps_data.fps, fps_data.jankCount])
        return result_fps_list


"""
    用于存放cpu数据
"""


class CpuData(models.Model):
    # 当前页面
    currentPage = models.TextField()

    # 平均cpu
    cpu = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    """
          批量的保存数据
    """

    def save_db_data(self, cpu_data_dict, package_name, version_code):
        cpu_list_to_insert = []
        cpu_keys = cpu_data_dict.keys()
        if len(cpu_keys) <= 0:
            return
        for key in cpu_keys:
            value = cpu_data_dict.get(key)
            cpu_list_to_insert.append(
                CpuData(currentPage=key, cpu=value, packageName=package_name,
                        versionCode=version_code))

        CpuData.objects.bulk_create(cpu_list_to_insert)

    """
        获取所有的数据
    """

    def get_all_data(self):
        cpu_data_list = CpuData.objects.all()
        result_cpu_list = []
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list


"""
    用于存放kpi数据
"""


class KpiData(models.Model):
    # 当前页面
    currentPage = models.TextField()

    # 平均cpu
    kpi = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    """
          批量的保存数据
    """

    def save_db_data(self, kpi_data_dict, package_name, version_code):
        kpi_list_to_insert = []
        kpi_keys = kpi_data_dict.keys()
        if len(kpi_keys) <= 0:
            return
        for key in kpi_keys:
            value = kpi_data_dict.get(key)
            kpi_list_to_insert.append(
                KpiData(currentPage=key, kpi=value, packageName=package_name,
                        versionCode=version_code))

        KpiData.objects.bulk_create(kpi_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和kpi数据
    """

    def get_all_data(self):
        kpi_data_list = KpiData.objects.all()
        result_kpi_list = []
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.currentPage, kpi_data.kpi])
        return result_kpi_list


"""
    用于存放memory数据
"""


class MemoryData(models.Model):
    # 当前页面
    currentPage = models.TextField()

    # 上一页面
    lastPage = models.TextField()

    # 平均cpu
    memory_increase = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    """
          批量的保存数据
    """

    def save_db_data(self, memory_data_dict, package_name, version_code):
        memory_list_to_insert = []
        memory_keys = memory_data_dict.keys()
        if len(memory_keys) <= 0:
            return
        for key in memory_keys:
            value = memory_data_dict.get(key)
            memory_list_to_insert.append(
                MemoryData(currentPage=key, lastPage=value[1], memory_increase=value[0], packageName=package_name,
                           versionCode=version_code))

        MemoryData.objects.bulk_create(memory_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和memory数据
    """

    def get_all_data(self):
        memory_data_list = MemoryData.objects.all()
        result_memory_list = []
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.currentPage, memory_data.lastPage, memory_data.memory_increase])
        return result_memory_list


"""
    用于存放flow数据
"""


class FlowData(models.Model):
    # 当前页面
    currentPage = models.TextField()

    # 上一页面
    lastPage = models.TextField()

    # 平均cpu
    flowIncrease = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.TextField()
    # 版本号
    versionCode = models.TextField()

    """
          批量的保存数据
    """

    def save_db_data(self, flow_data_dict, package_name, version_code):
        flow_list_to_insert = []
        flow_keys = flow_data_dict.keys()
        if len(flow_keys) <= 0:
            return
        for key in flow_keys:
            value = flow_data_dict.get(key)
            flow_list_to_insert.append(
                FlowData(currentPage=key, lastPage=value[1], flowIncrease=value[0], packageName=package_name,
                         versionCode=version_code))

        FlowData.objects.bulk_create(flow_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和flow数据
    """

    def get_all_data(self):
        flow_data_list = FlowData.objects.all()
        result_flow_list = []
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.lastPage, flow_data.flowIncrease])
        return result_flow_list
