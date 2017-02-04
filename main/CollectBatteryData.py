#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os, sys,re
import django

BaseDir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(BaseDir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoPerformanceData.settings")
django.setup()

from util.AdbUtil import AdbUtil
from util.LogUtil import LogUtil
import common.GlobalConfig as config
from performance.models1 import BatteryData
import util.UploadFileUtil as loadFile
__author__ = 'zhouliwei'

"""
function: 用于收集电量数据
date:2016/12/6
"""

package_name = config.test_package_name
battery_excel_data = []
data_folder = os.path.abspath(os.path.join(os.path.dirname('__file__'), os.path.pardir)) + '\\TestResultData'
"""
    用于收集电量的数据
"""


def get_battery_data():

    # 创建存放测试数据本地目录
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    battery_data = AdbUtil.get_battery_data(package_name)
    # print "battery_data0:", battery_data
    # 现将结果写入到txt中
    fo = open(data_folder + '/batterystats.txt', 'wb')
    fo.write(battery_data)
    fo.close()

    # 解析采集的电量数据
    # 思路是：每种数据之间会有空格分隔，以空格作为分隔
    battery_data = battery_data.split('Estimated power use (mAh):')[1].strip()
    # print "battery_data0:",battery_data
    # battery_data = battery_data.split('\r\n')
    battery_data = battery_data.split('\r\n')
    # pattern = re.compile(r'.*', re.DOTALL)
    # match = pattern.findall(battery_data)
    # print "battery_data:", battery_data

    pkg_name = ''
    compute_drain = ''
    actual_drain = ''

    for i in range(len(battery_data)):
        # 处理整体电流情况
        if i == 0:
            battery_total_data = battery_data[i]
            battery_total_datas = battery_total_data.split(',')
            compute_drain = battery_total_datas[1]
            actual_drain = battery_total_datas[2]
            continue
        # 处理单个uid消耗电量的情况
        battery_str = battery_data[i]
        if battery_str is None or battery_str == '':
            break
        battery_strs = battery_str.split(': ')
        uid = battery_strs[0].strip()
        # 处理uid，查找出packagename
        if uid is not None and 'Uid' in uid:
            uid_uid = uid.split(' ')[1]
            # print "uid_uid:",uid_uid
            if 'u0' in uid_uid:
                uid_uid = 'u0_' + uid_uid[2:]
                # uid_uid = 'u0_' + uid_uid[1:]
                # print "uid_uid1:", uid_uid
                pkg_name = AdbUtil.get_package_name_by_uid(uid_uid)
        battery_str_data = battery_strs[1]
        battery_excel_data.append([uid, pkg_name, battery_str_data])
        pkg_name = ''
        i += 1
    # return compute_drain, actual_drain, battery_excel_data
    return battery_excel_data

def publish_battery_data():
    if len(battery_excel_data) < 1:
        return
    version_code = AdbUtil.get_verson(package_name)
    BatteryData().save_db_data(battery_excel_data, package_name,version_code)


if __name__ == '__main__':
    # LogUtil.log_i('begin collect battery data.....')
    print (get_battery_data())
    # LogUtil.log_i('begin save battery data.....')
    # publish_battery_data()
    # LogUtil.log_i('upload battery data.....')
    #
    # loadFile.upload_file(data_folder+'\\batterystats.txt', package_name, AdbUtil.get_verson(package_name))
    # LogUtil.log_i('finish collect battery data.....')
