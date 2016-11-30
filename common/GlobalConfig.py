#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

"""
function: 全局的配置信息
date:2016/11/23

"""

# 全局日志的开关
log_switch = True

# 采集数据时长
collect_data_time = 10

# 采集数据次数
collect_data_count = 10

# 采集数据的时间间隔
collect_data_interval = collect_data_count / collect_data_time

# 循环采集数据重试的次数
retry_count = 100

# 要测试的App的包名
test_package_name = 'com.xdja.safekeyservice'
