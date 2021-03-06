#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

import os, re, time
from LogUtil import LogUtil
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
    获取当前应用版本号信息
    """
    @staticmethod
    def get_verson(package):
        try:
            pattern = re.compile(r"versionName=(.*\d+)")
            out = os.popen("adb shell dumpsys package %s" % package).read()
            version_name = pattern.findall(out)
            return version_name[0]
        except:
            print "当前无应用，或未找到设备"

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


    """
        模拟双击back事件
        注意：keycode_home 3
             keycode_call 5
             keycode_menu 1
    """
    @staticmethod
    def double_click_back():
        try:
            cmd = 'adb shell input keyevent 4'
            i = 0
            while i < 1:
                os.system(cmd)
                i += 1

        except Exception,e:
            LogUtil.log_e(e.message)

    """
        按电源键
    """
    @staticmethod
    def press_power_key():
        try:
            cmd = 'adb shell input keyevent 26'
            os.system(cmd)

        except Exception, e:
            LogUtil.log_e(e.message)

    """
        按手机的物理按键
    """
    @staticmethod
    def press_home():
        try:
            cmd = 'adb shell input keyevent 3'
            os.system(cmd)

        except Exception, e:
            LogUtil.log_e(e.message)


    """
        用于获取指定APP的电量数据
    """
    @staticmethod
    def get_battery_data(pkg_name):
        try:
            if pkg_name is None or pkg_name == '':
                cmd = 'dumpsys batterystats'
            else:
                cmd = 'dumpsys batterystats %s' % pkg_name
            # data = subprocess.check_output(cmd, shell=True)
            data = AdbUtil.exec_adb_shell(cmd)
            if data is not None and data is not '' :
                return data
            else:
                return 0
        except IOError as e:
            LogUtil.log_e('getbatterydata ' + e.message)

    """
        通过uid来查找packageName
    """
    @staticmethod
    def get_package_name_by_uid(uid):
        try:
            cmd = 'adb shell ps | findStr %s' % uid
            results = os.popen(cmd, "r")
            package_name = ''
            while 1:
                line = results.readline()
                if not line: break
                lines = line.split(' ')
                if lines[0] == uid:
                    package_name += lines[len(lines) - 1].strip()
                    package_name += '、'
            package_name_length = len(package_name)
            package_name = package_name[:package_name_length - 3]
            results.close()
            return package_name

        except IOError as e:
            LogUtil.log_e('get packageName by uid' + e.message)

if __name__ == '__main__':
    print AdbUtil().get_verson("com.xdja.safekeyservice")
    pass