#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PublishData import PublishData
from PreProcessData import PreProcessData
from util.LogUtil import LogUtil

import CollectData as Collecter

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
    can_collect, tip_message = Collecter.can_collect_data()
    if not can_collect:
        print tip_message
        return

    # 2. 开始采集数据的逻辑
    Collecter.auto_collect_data_process()

    LogUtil.log_i('pre_process_data......')
    # 3. 处理采集到的数据
    PreProcessData().pre_process_data()

    LogUtil.log_i('publish_data......')
    # 4. 对处理之后的数据，写到db中
    PublishData.publish_data()

    LogUtil.log_i('performance data collect success')

if __name__ == '__main__':
    main_entrance()
