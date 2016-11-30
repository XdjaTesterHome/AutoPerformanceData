#!/usr/bin/env python
# -*- coding: utf-8 -*-
from CollectData import CollectData
from PublishData import PublishData
import common.GlobalConfig as config
from controller.RunMonkeyThread import RunMonkeyThread
from util.LogUtil import LogUtil

__author__ = 'zhouliwei'


"""
function: 脚本的主入口
date:2016/11/25

"""

run_monkey_count = 100

"""
    程序的主入口
"""


def main_entrance():
    # 1. 判断是否满足采集数据的条件
    can_collect, tip_message = CollectData.can_collect_data(config.test_package_name)
    if not can_collect:
        print tip_message
        return
    # 2. 开启monkey
    monkey_thread = RunMonkeyThread(config.test_package_name, run_monkey_count)
    monkey_thread.start()

    # 3. 开始采集数据的逻辑
    CollectData().auto_collect_data()

    # 4. 处理采集到的数据
    CollectData().pre_process_data()

    # 5. 对处理之后的数据，写到db中
    PublishData.publish_data()

    # # 4. 数据采集完成后,对采集到的数据处理并上报
    # retry_count = 0
    # while True:
    #     task_finish = CollectData.task_all_finish()
    #     if task_finish or retry_count > config.retry_count:
    #         LogUtil.log_i('task finish')
    #         LogUtil.log_i('begin record data')
    #         # 5. 将数据记录下来
    #         CollectData.record_data()
    #         break
    #     time.sleep(config.collect_data_interval)
    #     retry_count += 1
    LogUtil.log_i('performance data collect success')
main_entrance()
