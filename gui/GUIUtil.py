#!/usr/bin/env python
# coding=utf-8

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()

"""
    窗口屏幕居中,设置窗口最大,最小尺寸...
    版权所有 2014 yao_yu (http://blog.csdn.net/yao_yu_126)
    本代码以MIT许可协议发布
    2014-04-15  创建
"""
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
