#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common.GlobalConfig as config
import logging,os
import util.commonUtil as common

__author__ = 'zhouliwei'

"""
function: 用于打印日志
date:2016/11/23

"""


class LogUtil(object):

    def __init__(self):
        file_path = os.getcwd() + "\\log"
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=file_path + '\\performance.log',
                            filemode='w')
    """
        用于打印一般信息
    """

    @staticmethod
    def log_i(info):
        if config.log_switch:
            print info
    """
        用于打印错误信息
    """
    @staticmethod
    def log_e(error):
        if config.log_switch:
            # file_path = common.get_upper_path() + "\\log"
            # if not os.path.exists(file_path):
            #     os.makedirs(file_path)
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filemode='w')
            logging.error(error)


if __name__ == '__main__':
    LogUtil.log_e('ddddddd')
    LogUtil.log_i('ddddddd')

