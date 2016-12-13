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
    currentPage = models.CharField(max_length=128)
    # 测试页面的帧率
    fps = models.BigIntegerField()
    # 测试页面丢帧数目
    jankCount = models.BigIntegerField()
    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

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
        result_fps_list = [[u'当前页面', u'平均fps值', u'平均丢帧数目']]
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.currentPage, fps_data.fps, fps_data.jankCount])
        return result_fps_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        fps_data_list = FpsData.objects.filter(packageName=package_name)
        result_fps_list = [[u'当前页面', u'平均fps值', u'平均丢帧数目']]
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.currentPage, fps_data.fps, fps_data.jankCount])
        return result_fps_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        fps_data_list = FpsData.objects.filter(packageName=package_name, versionCode=version)
        result_fps_list = [[u'当前页面', u'平均fps值', u'平均丢帧数目']]
        for fps_data in fps_data_list:
            result_fps_list.append([fps_data.currentPage, fps_data.fps, fps_data.jankCount])
        return result_fps_list


"""
    用于存放cpu数据
"""


class CpuData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    cpu = models.FloatField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

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
            cpu_data = CpuData.objects.filter(currentPage=key)
            if len(cpu_data) > 0:
                cpu_data.update(cpu=value)
            else:
                cpu_list_to_insert.append(
                    CpuData(currentPage=key, cpu=value, packageName=package_name,
                            versionCode=version_code))

        CpuData.objects.bulk_create(cpu_list_to_insert)

    """
        获取所有的数据
    """

    def get_all_data(self):
        cpu_data_list = CpuData.objects.all()
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        cpu_data_list = CpuData.objects.filter(packageName=package_name)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        cpu_data_list = CpuData.objects.filter(packageName=package_name, versionCode=version)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list


"""
    用于存放kpi数据
"""


class KpiData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    kpi = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

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
            kpi_data = KpiData.objects.filter(currentPage=key)
            if len(kpi_data) > 1:
                kpi_data.update(kpi=value)
            else:
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
        result_kpi_list = [[u'当前页面', u'加载时间(ms)']]
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.currentPage, kpi_data.kpi])
        return result_kpi_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        kpi_data_list = KpiData.objects.filter(packageName=package_name)
        result_kpi_list = [[u'当前页面', u'加载时间(ms)']]
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.currentPage, kpi_data.kpi])
        return result_kpi_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        kpi_data_list = KpiData.objects.filter(packageName=package_name, versionCode=version)
        result_kpi_list = [[u'当前页面', u'加载时间(ms)']]
        for kpi_data in kpi_data_list:
            result_kpi_list.append([kpi_data.currentPage, kpi_data.kpi])
        return result_kpi_list


"""
    用于存放memory数据
"""


class MemoryData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    memory_increase = models.FloatField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

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
                MemoryData(currentPage=key, memory_increase=value, packageName=package_name,
                           versionCode=version_code))

        MemoryData.objects.bulk_create(memory_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和memory数据
    """

    def get_all_data(self):
        memory_data_list = MemoryData.objects.all()
        result_memory_list = [[u'当前页面', u'内存增量(KB)']]
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.currentPage, memory_data.memory_increase])
        return result_memory_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        memory_data_list = MemoryData.objects.filter(packageName=package_name)
        result_memory_list = [[u'当前页面', u'内存增量(KB)']]
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.currentPage, memory_data.memory_increase])
        return result_memory_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        memory_data_list = MemoryData.objects.filter(packageName=package_name, versionCode=version)
        result_memory_list = [[u'当前页面', u'内存增量(KB)']]
        for memory_data in memory_data_list:
            result_memory_list.append([memory_data.currentPage, memory_data.memory_increase])
        return result_memory_list


"""
    用于存放flow数据
"""


class FlowData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    flowIncrease = models.FloatField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

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
                FlowData(currentPage=key, flowIncrease=value, packageName=package_name,
                         versionCode=version_code))

        FlowData.objects.bulk_create(flow_list_to_insert)

    """
          批量的保存数据
    """

    def save_db_data_silent(self, flow_data_dict, package_name, version_code):
        flow_list_to_insert = []
        flow_keys = flow_data_dict.keys()
        if len(flow_keys) <= 0:
            return
        for key in flow_keys:
            value = flow_data_dict.get(key)
            flow_list_to_insert.append(
                FlowData(currentPage=key, flowIncrease=value, packageName=package_name,
                         versionCode=version_code))

        FlowData.objects.bulk_create(flow_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和flow数据
    """

    def get_all_data(self):
        flow_data_list = FlowData.objects.all()
        result_flow_list = [[u'当前页面', u'流量消耗(KB)']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flowIncrease])
        return result_flow_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        flow_data_list = FlowData.objects.filter(packageName=package_name)
        result_flow_list = [[u'当前页面', u'流量增量(KB)']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flowIncrease])
        return result_flow_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        flow_data_list = FlowData.objects.filter(packageName=package_name, versionCode=version)
        result_flow_list = [[u'当前页面', u'流量增量(KB)']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flowIncrease])
        return result_flow_list


"""
    用于存放静默状态cpu数据
"""


class CpuSilentData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    cpu = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

    """
          批量的保存数据
    """

    def save_db_silent_data(self, cpu_data_dict, package_name, version_code):
        cpu_list_to_insert = []
        if len(cpu_data_dict) <= 0:
            return
        for value in cpu_data_dict:
            cpu_list_to_insert.append(
                CpuSilentData(currentPage=value[0], cpu=value[1], packageName=package_name,
                              versionCode=version_code))

        CpuSilentData.objects.bulk_create(cpu_list_to_insert)

    """
        获取所有的数据
    """

    def get_all_silent_data(self):
        cpu_data_list = CpuSilentData.objects.all()
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        cpu_data_list = CpuSilentData.objects.filter(packageName=package_name)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        cpu_data_list = CpuSilentData.objects.filter(packageName=package_name, versionCode=version)
        result_cpu_list = [[u'当前页面', u'平均cpu占有率']]
        for cpu_data in cpu_data_list:
            result_cpu_list.append([cpu_data.currentPage, cpu_data.cpu])
        return result_cpu_list


"""
    用于存放静默状态flow数据
"""


class FlowSilentData(models.Model):
    # 当前页面
    currentPage = models.CharField(max_length=128)

    # 平均cpu
    flow = models.BigIntegerField()

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

    """
          批量的保存数据
    """

    def save_db_silent_data(self, flow_data_dict, package_name, version_code):
        flow_list_to_insert = []
        if len(flow_data_dict) <= 0:
            return
        for value in flow_data_dict:
            flow_list_to_insert.append(
                FlowSilentData(currentPage=value[0], flow=value[1], packageName=package_name,
                               versionCode=version_code))

        FlowSilentData.objects.bulk_create(flow_list_to_insert)

    """
         获取所有的数据
         界面暂时只展示页面和flow数据
     """

    def get_all_slient_data(self):
        flow_data_list = FlowSilentData.objects.all()
        result_flow_list = [[u'当前页面', u'流量值']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flow])
        return result_flow_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        flow_data_list = FlowSilentData.objects.filter(packageName=package_name)
        result_flow_list = [[u'当前页面', u'流量值']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flow])
        return result_flow_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        flow_data_list = FlowSilentData.objects.filter(packageName=package_name, versionCode=version)
        result_flow_list = [[u'当前页面', u'流量值']]
        for flow_data in flow_data_list:
            result_flow_list.append([flow_data.currentPage, flow_data.flow])
        return result_flow_list


"""
    用于存放flow数据
"""


class BatteryData(models.Model):
    # uid
    uid = models.CharField(max_length=128)

    # 当前app的包名
    appPackageName = models.CharField(max_length=128)

    # battery使用情况
    batteryUse = models.CharField(max_length=128)

    # 测试应用的包名
    packageName = models.CharField(max_length=128)
    # 版本号
    versionCode = models.CharField(max_length=128)

    """
          批量的保存数据
    """

    def save_db_data(self, battery_data_dict, package_name, version_code):
        battery_list_to_insert = []
        if len(battery_data_dict) <= 0:
            return
        for battery_data in battery_data_dict:
            battery_list_to_insert.append(
                BatteryData(uid=battery_data[0], appPackageName=battery_data[1], batteryUse=battery_data[2],
                            packageName=package_name,
                            versionCode=version_code))

        BatteryData.objects.bulk_create(battery_list_to_insert)

    """
        获取所有的数据
        界面暂时只展示页面和flow数据
    """

    def get_all_data(self):
        battery_data_list = BatteryData.objects.all()
        result_battery_list = [[u'Uid', u'应用包名', u'耗电量情况']]
        for battery_data in battery_data_list:
            result_battery_list.append([battery_data.uid, battery_data.appPackageName, battery_data.batteryUse])
        return result_battery_list

    """
        根据packageName来获取数据
    """

    def get_data_by_package_name(self, package_name):
        battery_data_list = BatteryData.objects.filter(packageName=package_name)
        result_battery_list = [[u'Uid', u'应用包名', u'耗电量情况']]
        for battery_data in battery_data_list:
            result_battery_list.append([battery_data.uid, battery_data.appPackageName, battery_data.batteryUse])
        return result_battery_list

    """
        根据packageName和version筛选数据
    """

    def get_data_with_pkg_version(self, package_name, version):
        battery_data_list = BatteryData.objects.filter(packageName=package_name, versionCode=version)
        result_battery_list = [[u'Uid', u'应用包名', u'耗电量情况']]
        for battery_data in battery_data_list:
            result_battery_list.append([battery_data.uid, battery_data.appPackageName, battery_data.batteryUse])
        return result_battery_list


"""
    用于存放测试应用公共数据
"""


class CommonData(models.Model):
    # 测试的包名
    packageName = models.CharField(max_length=128)

    # 测试的app版本号
    packageVersion = models.CharField(max_length=128)

    # 电量数据文件
    batteryFilePath = models.FileField(upload_to='upload/')

    def save_data(self, common_data_list):
        try:
            common_data_insert_list = []

            if len(common_data_list) < 1:
                return
            for common_data in common_data_list:
                search_list = CommonData.objects.filter(packageName=common_data[0], packageVersion=common_data[1])
                if search_list is None or len(search_list) < 1:
                    if len(common_data) < 1:
                        continue
                    common_data_insert_list.append(CommonData(packageName=common_data[0], packageVersion=common_data[1],
                                                              batteryFilePath=common_data[2]))
            if len(common_data_insert_list) > 0:
                CommonData.objects.bulk_create(common_data_insert_list)
        except Exception as e:
            print e

    def get_all_data(self):
        common_data_list = CommonData.objects.all()
        result_common_list = []
        for common_data in common_data_list:
            result_common_list.append(
                [common_data.packageName, common_data.packageVersion, common_data.batteryFilePath])
        return result_common_list

    """
        获取所有的packageName
    """

    def get_all_package_name(self):
        common_data_list = CommonData.objects.all()
        result_common_list = []
        for common_data in common_data_list:
            result_common_list.append(common_data.packageName)
        return result_common_list

    """
        根据包名获取所有的版本信息
    """

    def get_all_version_by_package_name(self, package_name):
        common_versions = CommonData.objects.filter(packageName=package_name)
        result_common_list = []
        for common_version in common_versions:
            result_common_list.append(common_version.packageVersion)

        return result_common_list

    def __unicode__(self):
        return self.packageName + '-' + self.packageVersion


class LeakMemory(models.Model):
    # 泄露的包名
    packageName = models.CharField(max_length=128)

    # 泄露的类名
    className = models.CharField(max_length=128)

    # 泄露的详情
    leakDetail = models.CharField(max_length=255)
    # 测试的app版本号
    packageVersion = models.CharField(max_length=128)

    """
        根据包名获取所有的版本信息
    """

    def get_leak_by_package_and_version(self, package_name, version_name):
        leak_datas = LeakMemory.objects.filter(packageName=package_name, packageVersion=version_name)
        result_leak_list = []
        for leak_data in leak_datas:
            result_leak_list.append([package_name, leak_data.className, leak_data.leakDetail, leak_data.packageVersion])

        return result_leak_list

    def __unicode__(self):
        return self.packageName + '-' + self.packageVersion + '-' + self.leakDetail


if __name__ == '__main__':
    MemoryData().get_data_by_package_name('com.')
