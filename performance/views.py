#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import *
import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
import main.MainEntrance as Main
import tests as te



def home(request):
    return render(request, 'home.html')


"""
用于获取fps数据
"""


def get_fps(request):
    package_name = request.GET.get('package_name')
    # print 'package_name' + package_name
    if package_name != '':
        fps_list = FpsData().get_data_by_package_name(package_name)
    else:
        fps_list = FpsData().get_all_data()
    return render(request, 'get_fps.html', {'fps_list': json.dumps(fps_list)})


def get_memory(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        memory_list = MemoryData().get_data_by_package_name(package_name)
    else:
        memory_list = MemoryData().get_all_data()
    return render(request, 'get_memory.html', {'Memory_list': json.dumps(memory_list)})


def get_cpu(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        cpu_list = CpuData().get_data_by_package_name(package_name)
    else:
        cpu_list = CpuData().get_all_data()
    return render(request, 'get_cpu.html', {'CPU_list': json.dumps(cpu_list)})


def get_flow(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        flow_list = FlowData().get_data_by_package_name(package_name)
    else:
        flow_list = FlowData().get_all_data()
    return render(request, 'get_flow.html', {'Flow_list': json.dumps(flow_list)})


def get_kpi(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        kpi_list = KpiData().get_data_by_package_name(package_name)
    else:
        kpi_list = KpiData().get_all_data()
    return render(request, 'get_kpi.html', {'Kpi_list': json.dumps(kpi_list)})


def get_silent_cpu(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        cpu_list = CpuSilentData().get_data_by_package_name(package_name)
    else:
        cpu_list = CpuSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'cpu_list': json.dumps(cpu_list)})


def get_silent_flow(request):
    package_name = request.GET.get('package_name')
    if package_name != '':
        flow_list = FlowSilentData().get_data_by_package_name(package_name)
    else:
        flow_list = FlowSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'flow_list': json.dumps(flow_list)})


def get_power(request):
    return render(request, 'get_power.html')

def get_silence_cpu(request):
    return render(request, 'cpu_silence_info.html')

def get_silence_flow(request):
    return render(request, 'flow_silence_info.html')

#get_test方法用于前端网页调试#

def get_test_package_name(request):
    data = {'package_name': ['com.xdja.HDSafeEMailClient', 'com.xdja.safekeyservice']}
    return JsonResponse(data)


# get_test方法用于前端网页调试#
def get_test(request):
    # if request.method == "POSt":
    #     p = te.test()
    #     return HttpResponse(int(p))
    # else:
        return render(request, 'test.html')



"""
    开始进行测试
"""


def start_run_test(request):
    # 开始进行测试
    Main.start_test_task()
    return render(request, 'get_fps.html')
    # return HttpResponse('True'), render(request, 'get_fps.html')


"""
    停止进行测试
"""


def stop_run_test(request):
    # 开始进行测试
    Main.set_test_finish()
    return render(request, 'get_fps.html')
    # return HttpResponse('True'), render(request, 'get_fps.html')

"""
    开始进行测试
"""


def start_silent_test(request):
    # 开始进行测试
    Main.start_silent_test()

    return HttpResponse('True')

"""
    开始进行测试
"""


def stop_silent_test(request):
    # 开始进行测试
    Main.set_silent_test_finish()

    return HttpResponse('True')
    if request.method == "POSt":
        import tests
    return render(request, 'test.html')
