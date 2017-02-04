#!/usr/bin/env python      
# -*- coding: utf-8 -*-
__author__ = 'zhouliwei'

"""
function:
date:2016/12/16

"""

# !/usr/bin/env python
# encoding=utf-8
# test.py

from multiprocessing import Queue, Process
from Queue import Empty
import urllib
import time
import os
import multiprocessing


def Schedule(a, b, c):
    """''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   """
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print ('%.2f%%' % per)


queue = Queue(1024)


def download(url_list):
    for url in url_list:
        queue.put(url)
    while True:
        try:
            if queue.empty():
                break
            url = queue.get()
            print ('download url: %s' % url)
            # f = urllib.urlopen(url)
            # r = f.read()
            # 这里保存你下载的文件
            file_names = url.split('/')
            file_name = file_names[len(file_names) - 1]
            local = os.path.join('\\apk', file_name)
            urllib.urlretrieve(url, local, Schedule)
            time.sleep(5)

        except Empty:
            break

        except Exception as e:
            print ('download error: %s' % e.message)
            continue


def start_download(url_list):
    thread_pool = multiprocessing.Pool(processes=6)
    for i in range(len(url_list)):
        thread_pool.apply_async(download, args=(url_list,))
    thread_pool.close()
    thread_pool.join()
