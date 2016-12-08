#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import os

__author__ = 'zhouliwei'

"""
执行adb shell命令
"""


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
    用于读取application 的路径
    如果没有，就将已经存在的Application配置进去
"""


def get_application_path(file_name):
    package_name = ''
    application_name = ''
    parent_path = ''
    # 获取代码所在的主目录
    main_path = search_file_path(os.path.abspath('.'), 'AndroidManifest.xml', 'android.intent.category.LAUNCHER')
    if main_path is not None:
        parent_path = os.path.abspath(os.path.join(main_path, os.path.pardir))

    # 解析AndroidManifest.xml文件
    DOMTree = xml.dom.minidom.parse(file_name)
    collection = DOMTree.documentElement
    if collection.hasAttribute("package"):
        package_name = collection.getAttribute("package")

    apps = collection.getElementsByTagName("application")
    for application in apps:
        if application.hasAttribute('android:name'):
            application_name = application.getAttribute('android:name')
        else:

            # 如果还没有配置Application，就将本地的Application copy到 package路径下。
            package_path = package_name.replace('.', '\\')
            package_path = parent_path + "\\java\\" + package_path
            os.system('cp LeakCanaryApplication.java %s\\LeakCanaryApplication.java' % package_path)
            return package_path + "\\LeakCanaryApplication.java"

    # 拼接application的路径
    if package_name not in application_name:
        application_name = package_name + application_name

    application_path = application_name.replace('.', '\\')
    package_path = parent_path + "\\java\\" + application_path
    return package_path + '.java'

"""
    用于查找主配置AndroidManifest.xml所在的路径
"""
def search_file_path(path, file_name, keyword):
    for filename in os.listdir(path):
        if filename.startswith('.') or filename == 'build':
            continue
        fp = os.path.join(path, filename)
        if os.path.isfile(fp):
            if file_name in fp:
                with open(fp, 'r') as f:
                    for line in f:
                        if keyword in line:
                            return fp

        elif os.path.isdir(fp):
            my_path = search_file_path(fp, file_name, keyword)
            if my_path is not None:
                return my_path


def main():
    # 1. 获取application所在的路径
    application_path = get_application_path('./app/src/main/AndroidManifest.xml')
    # 2. 将Leakcanary的代码插入到Application中
    os.system("sed -i '/super.onCreate()/a\\LeakCanary.install(this);' %s" % application_path)
    os.system("sed -i '/super.onCreate()/a\\LeakCanaryInternals.setEnabled(this, DisplayLeakActivity.class, false);' %s"% application_path)
    os.system("sed -i '/package/a\\import com.squareup.leakcanary.LeakCanary;' %s" % application_path)
    os.system("sed -i '/package/a\\import com.squareup.leakcanary.internal.DisplayLeakActivity;' %s" % application_path)
    os.system("sed -i '/package/a\\import com.squareup.leakcanary.internal.LeakCanaryInternals;' %s" % application_path)

    # package_name='xdja.com.demospace'
    # # package_path = package_name.replace('.', '\\')
    # # path = os.path.join(os.path.abspath('.'), 'app\'package_path)
    # # os.system('cp LeakCanaryApplication.java %s' % path)
    # path = search_file_path(os.path.abspath('.'), 'AndroidManifest.xml', 'android.intent.category.LAUNCHER')
    # parent_path = os.path.abspath(os.path.join(path, os.path.pardir))
    # package_path = package_name.replace('.', '\\')
    # package_path = parent_path + "\\java\\" + package_path
    # os.system('cp LeakCanaryApplication.java %s\\LeakCanaryApplication.java' % package_path)
main()
