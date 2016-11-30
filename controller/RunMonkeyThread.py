#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading
from monkey.Monkey import Monkey
from util.LogUtil import LogUtil as log

__author__ = 'zhouliwei'

"""
function: 用于跑monkey的线程
date:2016/11/25

"""


class RunMonkeyThread(threading.Thread):
    """
        @:param package_name 要跑monkey的包名
        @:param time   跑monkey的次数
    """

    def __init__(self, package_name, time):
        threading.Thread.__init__(self)
        self.package_name = package_name
        self.time = time

    def run(self):
        log.log_i('begin exec monkey')
        Monkey.run_monkey(self.time, self.package_name)
        log.log_i('monkey exec success')

