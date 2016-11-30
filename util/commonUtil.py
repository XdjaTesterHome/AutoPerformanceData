#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os

__author__ = 'zhouliwei'

"""
function: 公共的方法
date:2016/11/24

"""

"""
    获取当前目录
"""


def get_cur_path():
    return os.path.dirname(os.path.abspath("__file__"))

"""
    获取当前目录上层目录
"""
def get_upper_path():
    return os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))
