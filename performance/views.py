#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import *
import json
from django.http import HttpResponse
# Create your views here.
import main.MainEntrance as Main


def home(request):
    return render(request, 'home.html')


"""
用于获取fps数据
"""


def get_fps(request):
    fps_list = FpsData().get_all_data()
    return render(request, 'get_fps.html', {'fps_list': json.dumps(fps_list)})


def get_memory(request):
    memory_list = MemoryData().get_all_data()
    return render(request, 'get_memory.html', {'Memory_list': json.dumps(memory_list)})


def get_cpu(request):
    cpu_list = CpuData().get_all_data()
    return render(request, 'get_cpu.html', {'CPU_list': json.dumps(cpu_list)})


def get_flow(request):
    flow_list = FlowData().get_all_data()
    return render(request, 'get_flow.html', {'Flow_list': json.dumps(flow_list)})


def get_kpi(request):
    kpi_list = KpiData().get_all_data()
    return render(request, 'get_kpi.html', {'Kpi_list': json.dumps(kpi_list)})

def get_silent_cpu(request):
    cpu_list = CpuSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'cpu_list': json.dumps(cpu_list)})

def get_silent_flow(request):
    flow_list = FlowSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'flow_list': json.dumps(flow_list)})

def get_power(request):
    return render(request, 'get_power.html')

# get_test方法用于前端网页调试#
def get_test(request):
    if request.method == "POSt":
       import tests
    return render(request, 'test.html')
