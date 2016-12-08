#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
import tests as te
from models import *
import json
import os
from models import CommonData

def home(request):
    return render(request, 'home.html')


"""
用于获取fps数据
"""


def get_fps(request):
    fps_list = FpsData().get_all_data()
    return render(request, 'get_fps.html', {'fps_list': json.dumps(fps_list)})

def get_fps_data(request, package_name, version_name):
    # print 'package_name' + package_name
    if package_name != '':
        fps_list = FpsData().get_data_with_pkg_version(package_name, version_name)
    else:
        fps_list = FpsData().get_all_data()
    fps_json_list = {'fps_list': fps_list}
    return JsonResponse(fps_json_list)

def get_memory(request):
    memory_list = MemoryData().get_all_data()
    return render(request, 'get_memory.html', {'Memory_list': json.dumps(memory_list)})

def get_memory_data(request, package_name, version_name):
    if package_name != '':
        memory_list = MemoryData().get_data_with_pkg_version(package_name, version_name)
    else:
        memory_list = MemoryData().get_all_data()

    memory_json_list = {'memory_list': memory_list}
    return JsonResponse(memory_json_list)

def get_cpu(request):
    cpu_list = CpuData().get_all_data()
    return render(request, 'get_cpu.html', {'CPU_list': json.dumps(cpu_list)})

def get_cpu_data(request, package_name, version_name):
    if package_name != '':
        cpu_list = CpuData().get_data_with_pkg_version(package_name, version_name)
    else:
        cpu_list = CpuData().get_all_data()
    cpu_json_list = {'cpu_list': cpu_list}
    return JsonResponse(cpu_json_list)

def get_flow(request):
    flow_list = FlowData().get_all_data()
    return render(request, 'get_flow.html', {'Flow_list': json.dumps(flow_list)})

def get_flow_data(request, package_name, version_name):
    if package_name != '':
        flow_list = FlowData().get_data_with_pkg_version(package_name, version_name)
    else:
        flow_list = FlowData().get_all_data()
    flow_json_list = {"flow_list": flow_list}
    return JsonResponse(flow_json_list)

def get_kpi(request):
    kpi_list = KpiData().get_all_data()
    return render(request, 'get_kpi.html', {'Kpi_list': json.dumps(kpi_list)})

def get_kpi_data(request, package_name, version_name):
    if package_name != '':
        kpi_list = KpiData().get_data_with_pkg_version(package_name, version_name)
    else:
        kpi_list = KpiData().get_all_data()
    kpi_json_list = {'kpi_list': kpi_list}
    return JsonResponse(kpi_json_list)

def get_silent_cpu(request):
    cpu_list = CpuSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'cpu_list': json.dumps(cpu_list)})

def get_silent_cpu_data(request, package_name, version_name):
    if package_name != '':
        cpu_list = CpuSilentData().get_data_with_pkg_version(package_name, version_name)
    else:
        cpu_list = CpuSilentData().get_all_data()
    cpu_json_list = {'cpu_list': cpu_list}
    return JsonResponse(cpu_json_list)

def get_silent_flow(request):
    flow_list = FlowSilentData().get_all_data()
    return render(request, 'get_kpi.html', {'flow_list': json.dumps(flow_list)})

def get_silent_flow_data(request, package_name, version_name):
    if package_name != '':
        flow_list = FlowSilentData().get_data_with_pkg_version(package_name, version_name)
    else:
        flow_list = FlowSilentData().get_all_data()
    flow_json_list = {'flow_list': flow_list}
    return JsonResponse(flow_json_list)

def get_power(request):
    return render(request, 'get_power.html')
def get_power_data(request, package_name, version_name):
    if package_name != '':
        battery_list = BatteryData().get_data_with_pkg_version(package_name, version_name)
    else:
        battery_list = BatteryData().get_all_data()
    battery_json_list = {'battery_list': battery_list}
    return JsonResponse(battery_json_list)

def get_silence_cpu(request):
    return render(request, 'cpu_silence_info.html')

def get_silence_flow(request):
    return render(request, 'flow_silence_info.html')

"""
    用于获取所有的包名信息
"""
def get_test_package_name(request):
    package_list = CommonData().get_all_package_name()
    data = {'package_name': package_list}
    return JsonResponse(data)
"""
    根据包名来查找version
"""
def get_test_package_version(request, package_name):
    version_list = CommonData().get_all_version_by_package_name(package_name)
    data = {'version_list': version_list}
    return JsonResponse(data)

# get_test方法用于前端网页调试#
def get_test(request):
    # if request.method == "POSt":
    #     p = te.test()
    #     return HttpResponse(int(p))
    # else:
        return render(request, 'test.html')

def upload_file(request):
    # if not request.user.is_superuser:
    #     # 判断是否为管理员，只有管理员才有权限访问upload.html页面
    #     return HttpResponse(True)
    # else:
    if request.method == 'POST':
        f = request.FILES.get('file')
        handle_upload_file(f)
    else:
        pass
    return HttpResponse(True)

def handle_upload_file(f):
    try:

        f_path = '/upload/' + f.name
        if not os.path.exists(f_path):
            os.mkdir(f_path)
        with open(f_path, 'wb+') as info:
            print f.name
            for chunk in f.chunks():
                info.write(chunk)
        return f
    except Exception as e:
        print e
