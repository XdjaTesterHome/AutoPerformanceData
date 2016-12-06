#!/usr/bin/env python      
# -*- coding: utf-8 -*-
import os
import urllib2
import requests
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

__author__ = 'zhouliwei'

"""
function: 用于上传和下载文件
date:2016/12/6

"""
def upload_file(file_path, package_name, package_version):
    url = 'http://127.0.0.1:8000/performance/upload/'
    files = {'file': open(file_path, 'rb')}
    data = {'enctype': 'multipart/form-data', 'name': 'battery_file'}
    response = requests.post(url, files=files, data=data)
    print response.text
    json = response.json()
    print json