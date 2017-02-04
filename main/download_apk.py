#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import download2

class spider(object):
    def __init__(self):
        print u'开始爬取内容'

    def getsource(self, url):
        html = requests.get(url)
        return html.text

    def changepage(self, url, total_page):
        page_group = []
        for i in range(total_page):
            i += 1
            link = url + str(i)
            page_group.append(link)
        return page_group

    def geteveryapp(self, source):
        everyapp = re.findall(r'.*?&appadb=&url=(.*?)"', source, re.S)
        return everyapp

    def get_app_url(self, source):
        app_url = re.findall(r'<a href="/appdown/(.*?)"', source, re.S)
        return app_url

    def getinfo(self, eachclass):
        info = {}
        str1 = str(re.search('<a href="(.*?)">', eachclass).group(0))
        app_url = re.search('"(.*?)"', str1).group(1)
        appdown_url = app_url.replace('appinfo', 'appdown')
        info['app_url'] = appdown_url
        print appdown_url
        return info

    def saveinfo(self, classinfo):
        f = open('info.txt', 'a')
        for each in classinfo:
            f.writelines(each + '\n')
        f.close()

"""
    根据下载页数来下载apk
"""
def download_all_apk_by_page(page_count):
    appinfo = []
    page_count = 1
    url = 'http://apk.hiapk.com/apps?sort=5&pi='
    appurl = spider()
    all_links = appurl.changepage(url, page_count)
    app_urls = []
    final_urls = []
    for link in all_links:
        print u'正在处理页面' + link
        html = appurl.getsource(link)
        app_urls = appurl.get_app_url(html)

    for app_url in app_urls:
        app_url = 'http://apk.hiapk.com/appdown/' + app_url.__str__()
        final_urls.append(app_url)

    download2.start_download(final_urls)
    appurl.saveinfo(final_urls)
