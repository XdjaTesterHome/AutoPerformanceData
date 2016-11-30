#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import FpsData
import json
# Create your views here.

def home(request):
    return render(request, 'home.html')

"""
用于获取fps数据
"""


def get_fps(request):
    fps_list = FpsData().get_all_data()
    return render(request, 'get_fps.html', {'fps_list': json.dumps(fps_list)})


def get_memory(request):
    return render(request, 'get_memory.html')

def get_cpu(request):
    return render(request, 'get_cpu.html')

def get_flow(request):
    return render(request, 'get_flow.html')

def get_kpi(request):
    return render(request, 'get_kpi.html')

def get_power(request):
    return render(request, 'get_power.html')