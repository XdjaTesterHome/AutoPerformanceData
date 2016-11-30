#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import os, re, time
import subprocess
PATH = lambda p: os.path.abspath(p)
"""
function: 处理和adb命令相关的工具类
date:2016/11/23

"""


class AdbUtil(object):
    def __init__(self):
        pass

    """
        执行adb命令,执行完整的adb命令，如adb devices
    """

    def exadb(self,commands):
        command_result = ''
        results = os.popen(commands, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result



    @staticmethod
    def exec_adb(commands):
        command_result = ''
        cmd = 'adb %s' % commands
        results = os.popen(cmd, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    """
    执行adb shell命令
    """

    @staticmethod
    def exec_adb_shell(command):
        command_result = ''
        cmd = 'adb shell %s' % command
        results = os.popen(cmd, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    """
        检查设备是否连接
    """

    @staticmethod
    def attach_devices():
        result = AdbUtil.exec_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        flag = [device for device in devices if len(device) > 2]
        if flag:
            return True
        else:
            return False

    """
        接收cmd命令输出的结果，lzz
    """
    def exccmd(self,cmd):
        try:
            return os.popen(cmd).read()
        except Exception:
            return None
    """
        检查设备是否连接，并返回设备ID，用于后期执行多线程操作，同时操作多台设备。
    """
    def finddevices(self):
        rst = AdbUtil.exccmd('adb devices')
        devices = re.findall(r'(.*?)\s+device',rst)
        if len(devices) > 1:
            deviceIds = devices[1:]
            print ('共找到%s个手机'%str(len(devices)-1))
            for i in deviceIds:
                print ('设备ID为%s'%i)
            return deviceIds
        else:
            print('没有找到手机，请检查')
            return
    """
       获取手机屏幕截屏
    """
    @staticmethod
    def screenshot(pic_name):
        path = PATH(os.getcwd() + "/screenshot")
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        pic_name  = pic_name + '_' + timestamp
        os.popen("adb wait-for-device")
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        if not os.path.isdir(PATH(os.getcwd() + "/screenshot")):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path + "/" + pic_name + ".png"))
        os.popen("adb shell rm /data/local/tmp/tmp.png")

    """
       卸载apk
    """
    @staticmethod
    def uninstall_apk(package_name):
        result = AdbUtil.exec_adb("uninstall %s" % package_name)
        if 'Faliure' in result:
            return False
        else:
            return True

    """
       安装apk
    """
    @staticmethod
    def install_apk(apk_path):
        result = AdbUtil.exec_adb('install -rf %s' % apk_path)
        if 'Success' in result:
            return True
        else:
            return False

    #获取当前应用pid和包名#
    def getCurrentPID(self):
        _result = os.popen('adb shell dumpsys activity top | findstr ACTIVITY').read().strip()
        _resultPid = re.findall(u'pid=(\d+)', _result)[0]
        _resultPName = re.findall(u'(com.\w+.\w+)',_result)[0]
        return [_resultPid,_resultPName]

    """
        获取应用的pid
    """
    @staticmethod
    def get_pid(package_name):
        try:
            cmd = "ps | grep %s  | awk '{print $2}'" % package_name
            result = AdbUtil.exec_adb_shell(cmd)
            result = result.strip()

        except Exception, e:
            print e
            result = 0
        return result

    """
        获取app的uid
    """
    @staticmethod
    def get_uid(package_name):
        try:
            pid = AdbUtil.get_pid(package_name)
            pid = pid.split('\n')[0]

            cmd = 'cat /proc/'+ str(pid) + '/status | grep Uid'
            result = AdbUtil.exec_adb_shell(cmd)
            result = result.split('\t')[1]

        except Exception, e:
            print e
            result = 0
        return result


if __name__ == '__main__':
    print AdbUtil().get_pid("com.xdja.safekeyservice")
    pass