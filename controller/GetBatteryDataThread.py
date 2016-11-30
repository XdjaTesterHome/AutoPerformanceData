#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import threading

__author__ = 'zhouliwei'

"""
function: 用于获取电量数据的线程
date:2016/11/25

"""


class GetBatteryDataThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass
