#!/usr/bin/env python
# -*- coding: utf-8 -*-
from util import AdbUtil
__author__ = 'lzz'

monkey_run = AdbUtil.AdbUtil()

"""
    用于跑monkey
"""


class Monkey(object):

    # run monkey,time为测试monkey时长，pkg为测试包
    @staticmethod
    def run_monkey(time, package_name):
        cmd_memory = "adb shell monkey -p " + package_name + " --throttle 500 --pct-appswitch 70 " + "--ignore-crashes --ignore-timeouts --ignore-native-crashes -v -v -v %s" % str(time)
        monkey_run.exadb(cmd_memory)

if __name__ == "__main__":
    Monkey().run_monkey(10, "com.xdja.safekeyservice")
