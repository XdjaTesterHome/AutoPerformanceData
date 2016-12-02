#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PublishData import PublishData
from PreProcessData import PreProcessData
from util.LogUtil import LogUtil
from util.AndroidUtil import AndroidUtil

import CollectData as Collecter
import common.GlobalConfig as config
__author__ = 'zhouliwei'


"""
function: 脚本的主入口
date:2016/11/25

"""

run_monkey_count = 100

"""
    程序的主入口
"""


def start_test_task():
    # 0. 先将全局结束开始标志重置
    config.run_finish = False
    # 1. 判断是否满足采集数据的条件
    can_collect, tip_message = Collecter.can_collect_data()
    if not can_collect:
        print tip_message
        return
    Collecter.clear_data()

    # 2. 开始采集数据的逻辑
    Collecter.auto_collect_data_process()

    LogUtil.log_i('pre_process_data......')
    # 3. 处理采集到的数据
    PreProcessData().pre_process_data()

    LogUtil.log_i('publish_data......')
    # 4. 对处理之后的数据，写到db中
    PublishData.publish_data()

    LogUtil.log_i('performance data collect success')

"""
    设置任务已经完成
"""
def set_test_finish():

    config.run_finish = True

"""
    设置静默任务已经完成
"""
def set_silent_test_finish():

    config.run_silent_state = config.SlientState.FINISH


def start_silent_test():
    # 1. 判断是否满足采集数据的条件
    can_collect, tip_message = Collecter.can_collect_data()
    if not can_collect:
        print tip_message
        return

    # 2.将标志位设置为start
    config.run_silent_state = config.SlientState.START
    Collecter.clear_data()

    # 3. 应用置于后台，灭屏
    AndroidUtil.make_app_silent()

    Collecter.auto_silent_collect_process()

    LogUtil.log_i('pre_silent_process_data......')
    # 3. 处理采集到的数据
    PreProcessData().pre_silent_process_data()

    LogUtil.log_i('publish_silent_data......')
    # 4. 对处理之后的数据，写到db中
    PublishData.publish_silent_data()

    LogUtil.log_i('silent performance data collect success')

if __name__ == '__main__':

    start_test_task()
