#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views
__author__ = 'zhouliwei'

"""
function:
date:2016/11/29

"""
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^getFps/', views.get_fps, name='fps_info'),
    url(r'^getMem/', views.get_memory, name='memory_info'),
    url(r'^getCpu/', views.get_cpu, name='cpu_info'),
    url(r'^getFlow/', views.get_flow, name='flow_info'),
    url(r'^getKpi/', views.get_kpi, name='kpi_info'),
    url(r'^getPower/', views.get_power, name='battery_info'),
    url(r'^test/', views.get_test, name='test'),#用于前端展示调试界面
    url(r'^startRunTest/', views.start_run_test, name='start_test'),
    url(r'^stopRunTest/', views.stop_run_test, name='stop_test'),
    url(r'^startSilentTest/', views.start_silent_test, name='start_silent_test'),
    url(r'^stopSilentTest/', views.stop_silent_test, name='stop_silent_test'),
    url(r'^getsilencecpu/', views.get_silence_cpu, name='cpu_silence_info'),
    url(r'^getsilenceflow/', views.get_silence_flow, name='flow_silence_info'),
    url(r'^getSilentCpu/', views.get_silent_cpu, name='silent_cpu'),
    url(r'^getSilentFlow/', views.get_silent_flow, name='silent_flow'),
    url(r'^getPackageName/', views.get_test_package_name, name='get_package_name'),
]