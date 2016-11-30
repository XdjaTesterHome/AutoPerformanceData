#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
import time
import common.GlobalConfig as config
from util.AndroidUtil import AndroidUtil
from util.AdbUtil import AdbUtil
from util.LogUtil import LogUtil as log

__author__ = 'zhouliwei'

"""
function: 获取帧率的数据
date:2016/11/24

"""


class GetFpsDataThread(threading.Thread):

    # 存放采集到的帧率数据['frame_count', 'jank_count', 'fps', 'page']
    fps_datas = []

    # 存放有问题的帧率数据['frame_count', 'jank_count', 'fps', 'page', 'pic_name']
    fps_error_datas = []

    # 任务是否完成
    task_finish = False

    def __init__(self, thread_id, package_name):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.package_name = package_name
        self.pic_name = 'fps'
        # 每次采集数据前，先清理上次的数据
        GetFpsDataThread.clear_data()
        GetFpsDataThread.task_finish = False

    """
        采集数据的逻辑
    """
    def run(self):
        # 处理可能有问题的场景
        def handle_error_data(frame_count, jank_count, fps, current_page):
            # 暂时当fps < 50 或者 jank_count > 10 我们认为是不达标的
            if fps < 50 or jank_count > 10:
                # 截图
                AdbUtil.screenshot(self.pic_name)
                # 保存日志

                GetFpsDataThread.fps_error_datas.append([frame_count, jank_count, fps, current_page, self.pic_name])

        # 死循环，满足条件后跳出
        exec_count = 0
        while True:
            log.log_i('get fps data')
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据
            frame_count, jank_count, fps = AndroidUtil.get_fps_data_by_gfxinfo(self.package_name)
            if frame_count is None and jank_count is None and fps is None:
                exec_count += 1
                continue
            current_page = AndroidUtil.get_cur_activity()
            GetFpsDataThread.fps_datas.append([frame_count, jank_count, fps, current_page])

            # 处理有问题的数据
            handle_error_data(frame_count, jank_count, fps, current_page)
            exec_count += 1

            # 采集数据时间间隔
            time.sleep(config.collect_data_interval)
        GetFpsDataThread.task_finish = True

    """
        用于清理数据
    """
    @staticmethod
    def clear_data():
        GetFpsDataThread.fps_datas = []
        GetFpsDataThread.fps_error_datas = []


if __name__ == '__main__':
    GetFpsDataThread('com.xdja.safekeyservice').start()