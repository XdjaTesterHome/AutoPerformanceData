#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import re
from Queue import Queue
import threading
import os


class download(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    @staticmethod
    def Schedule(a, b, c):
        '''''
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
       '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print '%.2f%%' % per

    def run(self):
        while True:
            if not self.que.empty():
                print('-----%s------' % (self.name))
                file_names = self.que.get().encode('UTF-8').split('/')
                file_name = file_names[len(file_names) - 1]
                local = os.path.join('/apk', file_name)
                urllib.urlretrieve(self.que.get(), local, download.Schedule)
            else:
                break


def startDown(url_list, decoding=None):
    if not os.path.exists('./apk'):
        os.mkdir('./apk')
    if not decoding:
        decoding = 'utf8'
    que = Queue()
    for l in url_list:
        que.put(l)

    d = download(que)
    d.start()


if __name__ == '__main__':
    url = 'https://class.coursera.org/algo-004/lecture/index'
    rule = '<a target=\"_new\" href=\".*\"'
    startDown(url, rule, 10, 23, -1)
