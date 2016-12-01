#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import common.GlobalConfig as config

__author__ = 'zhouliwei'

"""
    啥都不干，就为了充数
    目前python还有个多线程的问题没有解决
"""


class BlankThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.threadId = thread_id

    def run(self):
        print 'Blank thread'
        # count = 0
        # while True:
        #     if count < config.collect_data_count:
        #         break
        #     print 'blank do nothing'
        #     count += 1
