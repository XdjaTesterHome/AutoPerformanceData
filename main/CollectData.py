#!/usr/bin/env python      
# -*- coding: utf-8 -*-
from util.LogUtil import LogUtil
from controller.PerformanceControl import PerformanceControl as control
import common.GlobalConfig as config
from util.AdbUtil import AdbUtil
from util.AndroidUtil import AndroidUtil
from controller.GetKpiDataThread import GetKpiDataThread
from controller.GetCpuDataThread import GetCpuDataThread
from controller.GetFlowDataThread import GetFlowDataThread
from controller.GetFpsDataThread import GetFpsDataThread
from controller.GetMemoryThread import GetMemoryDataThread

import multiprocessing
import time
import subprocess
import re
__author__ = 'zhouliwei'

"""
function: 用于收集数据并进行处理的逻辑
date:2016/11/25

"""


class CollectData(object):
    # 线程id
    MEMORY_THREAD_ID = 101
    CPU_THREAD_ID = 102
    KPI_THREAD_ID = 103
    FLOW_THREAD_ID = 104
    FPS_THREAD_ID = 105
    # 跑monkey的次数
    RUN_MONKEY_COUNT = 100
    # 用于存放计算之后的值[平均fps, 平均jank_count]
    fps_data_dict = {}

    # 用于存放计算之后的cpu值
    cpu_data_dict = {}

    # 用于存放计算之后的kpi值
    kpi_data_dict = {}

    # 用于存放计算之后的memory值
    memory_data_dict = {}

    # 用于存放计算之后的flow值
    flow_data_dict = {}

    package_name = ''

    def __init__(self):
        self.package_name = config.test_package_name
        pass

    """
        用于开始自动收集数据
    """

    def auto_collect_data(self):
        try:
            # # 这里同时启动多个线程，会有问题，后面解决
            # 1. 开始采集kpi数据
            kpi_thread = GetKpiDataThread(CollectData.KPI_THREAD_ID, self.package_name)
            kpi_thread.start()

            #
            # # 2. 开始采集内存数据
            memory_thread = GetMemoryDataThread(CollectData.MEMORY_THREAD_ID)
            memory_thread.start()

            # 3. 开始采集cpu数据
            cpu_thread = GetCpuDataThread(CollectData.CPU_THREAD_ID)
            cpu_thread.start()

            # 4. 开始采集帧率数据
            fps_thread = GetFpsDataThread(CollectData.FPS_THREAD_ID, self.package_name)
            fps_thread.start()

            #
            # # 5. 开始采集流量数据
            flow_thread = GetFlowDataThread(CollectData.FLOW_THREAD_ID, self.package_name)
            flow_thread.start()

            LogUtil.log_i('All thread worked!!')
        except Exception as e:
            LogUtil.log_e('collect data failure ' + e.message)

    """
           用于开始自动收集数据
       """

    def auto_collect_data_process(self):
        try:
            # # 这里同时启动多个线程，会有问题，后面解决
            # 1. 开始采集kpi数据
            kpi_process = multiprocessing.Process(target=CollectData.get_kpi_data(self.package_name))
            kpi_process.start()
            #
            # # 2. 开始采集内存数据
            memory_process = multiprocessing.Process(target=CollectData.get_memory_data(self.package_name))
            memory_process.start()

            # 3. 开始采集cpu数据
            cpu_process = multiprocessing.Process(target=CollectData.get_cpu_data(self.package_name))
            cpu_process.start()

            # 4. 开始采集帧率数据
            fps_process = multiprocessing.Process(target=CollectData.get_fps_data(self.package_name))
            fps_process.start()

            #
            # # 5. 开始采集流量数据
            flow_process = multiprocessing.Process(target=CollectData.get_flow_data(self.package_name))
            flow_process.start()

            # # 创建进程池来执行进程
            # # result = None
            # pool = multiprocessing.Pool(processes=6)
            # result = pool.apply_async(control.run_monkey, (config.test_package_name, CollectData.RUN_MONKEY_COUNT,))
            # for i in range(len(control.METHOD_ARRAY)):
            #     result = pool.apply_async(control.get_data, args=(control.METHOD_ARRAY[i], self.package_name,))
            #
            # # result = pool.apply_async(control.get_kpi_data, (self.package_name,))
            # # result = pool.apply_async(control.get_memory_data, (self.package_name,))
            # # result = pool.apply_async(control.get_cpu_data, (self.package_name,))
            # # result = pool.apply_async(control.get_fps_data, (self.package_name,))
            # # result = pool.apply_async(control.get_flow_data, (self.package_name,))
            # pool.close()
            # pool.join()
            # if result.successful():
            #     LogUtil.log_i('excute success')
            LogUtil.log_i('All process worked!!')
        except Exception as e:
            LogUtil.log_e('collect data failure ' + e.message)



    """
        判断任务是否执行完成
    """

    @staticmethod
    def task_all_finish():
        # flow_task = GetFlowDataThread.task_finish
        # fps_task = GetFpsDataThread.task_finish
        # kpi_task = GetKpiDataThread.task_finish
        # cpu_task = GetCpuDataThread.task_finish
        # memory_task = GetMemoryDataThread.task_finish
        # return flow_task and fps_task and kpi_task and cpu_task and memory_task
        pass

    """
        判断是否符合采集数据的条件
    """

    @staticmethod
    def can_collect_data(package_name):
        # 1. 判断手机是否连接
        mobile_connect = AdbUtil().attach_devices()
        tips = ''
        if not mobile_connect:
            tips = '请连接设备，当前无设备可用'
            return mobile_connect, tips

        # 2. 判断当前进程是否还活着
        process_alive = AndroidUtil.process_alive(package_name)
        if not process_alive:
            tips = 'app进程已被杀死，请打开app后再开始测试'
            return process_alive, tips

        return True, tips

    """
          用于对收集的数据进行预处理
          预处理的规则：对同一类数据，筛选出同一页面的数据，做平均值。
      """

    def pre_process_data(self):
        # 处理收集到的数据
        CollectData.__pre_fps_data(control.fps_datas)
        CollectData.__pre_cpu_data(control.cpu_datas)
        CollectData.__pre_flow_data(control.flow_datas)
        CollectData.__pre_kpi_data(control.kpi_datas)
        CollectData.__pre_memory_data(control.memory_datas)

    """
        用于对收集的fps数据进行处理
        fps采集到的数据格式是：[frame_count, jank_count, fps, current_page]
        处理数据的逻辑：通过current_page来求每个页面的fps平均值
                     通过一个map去存放，key是page_name,value是[fps_data, jank_count]
    """

    @staticmethod
    def __pre_fps_data(fps_datas):
        if len(fps_datas) <= 0:
            return

        for data in fps_datas:
            if len(data) <= 0:
                continue
            now_page_name = data[len(data) - 1]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if CollectData.fps_data_dict.has_key(now_page_name):
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                last_fps_datas = CollectData.fps_data_dict.get(now_page_name)
                now_fps_data = (int(data[2]) + int(last_fps_datas[0])) / 2
                now_jank_count = (int(data[1]) + int(last_fps_datas[1])) / 2
            else:
                if int(data[2]) == 0 and int(data[1]) == 0:
                    continue
                # 不包含当前页面，就直接添加
                now_fps_data = int(data[2])
                now_jank_count = int(data[1])

            CollectData.fps_data_dict[now_page_name] = [now_fps_data, now_jank_count]

    """
        用于对收集的cpu数据进行处理
        cpu采集到的数据格式是：[current_page, cpu值]
        处理数据的逻辑：通过current_page来求每个页面的cpu平均值

    """

    @staticmethod
    def __pre_cpu_data(cpu_datas):
        if len(cpu_datas) < 1:
            return
        for data in cpu_datas:
            if len(data) < 1:
                continue
            now_page_name = data[0]
            # 这里加个逻辑，假如fps和jank_count是0，就不进行计算
            if CollectData.cpu_data_dict.has_key(now_page_name):

                last_cpu_data = CollectData.cpu_data_dict.get(now_page_name)
                now_cpu_data = (int(data[1]) + int(last_cpu_data)) / 2
            else:

                # 不包含当前页面，就直接添加
                now_cpu_data = int(data[1])

            CollectData.fps_data_dict[now_page_name] = now_cpu_data

    """
         对kpi数据进行处理
         收集到的kpi数据格式self.now_page_name, self.jump_page, self.cost_time
     """

    @staticmethod
    def __pre_kpi_data(kpi_datas):
        if len(kpi_datas) < 1:
            return
        now_cost_time = 0
        for kpi_data in kpi_datas:
            if len(kpi_data) < 1:
                continue
            now_page_name = kpi_data[0]
            if CollectData.kpi_data_dict.has_key(now_page_name):
                if kpi_data[2] != '':
                    last_cost_time = CollectData.kpi_data_dict.get(now_page_name, 0)
                    now_cost_time = (int(kpi_data[2]) + int(last_cost_time)) / 2
            else:
                # 不包含就直接添加
                if kpi_data[2] != '':
                    now_cost_time = int(kpi_data[2])
            CollectData.kpi_data_dict[now_page_name] = now_cost_time

    """
        用于预处理内存的数据
        数据格式是[[now_page, last_page, 内存增量]]
    """

    @staticmethod
    def __pre_memory_data(memory_datas):
        if len(memory_datas) < 1:
            return
        now_memory_increase = 0
        last_page_name = ''
        for memory_data in memory_datas:
            if len(memory_data) < 1:
                continue
            now_page_name = memory_data[0]
            if CollectData.memory_data_dict.has_key(now_page_name):
                memory_value = CollectData.memory_data_dict.get(now_page_name)
                # 假如是从同一个页面跳转过来的
                if memory_value[1] == memory_data[1]:
                    if memory_data[2] != '':
                        last_memory_increase = memory_value[0]
                        now_memory_increase = (int(last_memory_increase) + memory_data[2]) / 2
                        last_page_name = memory_value[1]
                else:
                    now_memory_increase = memory_data[2]
                    last_page_name = memory_data[1]
            else:
                if memory_data[2] != '':
                    now_memory_increase = int(memory_data[2])
                last_page_name = memory_data[1]
            CollectData.memory_data_dict[now_page_name] = [now_memory_increase, last_page_name]

    """
        用于处理流量值
        数据格式是：[[now_page, last_page, 流量增量]]
    """
    @staticmethod
    def __pre_flow_data(flow_datas):
        if len(flow_datas) < 1:
            return
        for flow_data in flow_datas:
            if len(flow_data) < 1:
                continue

            now_page_name = flow_data[0]
            if CollectData.flow_data_dict.has_key(now_page_name):
                flow_value = CollectData.flow_data_dict.get(now_page_name)
                # 同样的逻辑，参考内存的计算方式
                if flow_value[1] == flow_data[1]:
                    last_flow = flow_value[0]
                    now_flow = (int(last_flow) + flow_data[2])/2
                    last_page_name = flow_data[1]
                else:
                    now_flow = int(flow_data[2])
                    last_page_name = flow_data[1]
            else:
                now_flow = int(flow_data[2])
                last_page_name = flow_data[1]

            CollectData.flow_data_dict[now_page_name] = [now_flow, last_page_name]

            # 用于存放搜集的数据

    cpu_datas = []
    flow_datas = []
    fps_datas = []
    kpi_datas = []
    memory_datas = []
    battery_datas = []

    METHOD_ARRAY = ['cpu', 'memory', 'kpi', 'fps', 'flow']

    def __init__(self):
        pass

    """
        用于获取cpu数据
    """

    @staticmethod
    def get_cpu_data(package_name, pic_name='cpu'):
        i = 0
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect cpu')
            current_page, cpu_data = AndroidUtil.get_cpu_data(package_name)  # 当前采集到的数据
            if cpu_data >= 50.00:

                AdbUtil.screenshot(pic_name)
            else:
                pass
            CollectData.cpu_datas.append([current_page, cpu_data])
            time.sleep(config.collect_data_interval)  # 设定多久采集一次数据
            i += 1
        LogUtil.log_i('Inspect cpu finish')

    """
        用于获取流量数据
    """

    @staticmethod
    def get_flow_data(package_name, pic_name='flow'):
        # 处理有问题的流量数据，暂定有问题的流量是大于1M时
        def handle_error_data(current_flow):
            if current_flow > 5 * 1024:
                # 异常处理
                AdbUtil.screenshot(pic_name)

        # 死循环，满足条件后跳出
        exec_count = 0
        last_flow_data = 0
        last_page_name = ''
        last_flow = 0
        current_flow_data = 0
        while True:
            LogUtil.log_i('get flow data' + str(exec_count))
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据 返回三个值，接收的流量、发送的流量、流量总数据，单位是KB
            flow_recv, flow_send, flow_total = AndroidUtil.get_flow_data(package_name)
            now_page_name = AndroidUtil.get_cur_activity()

            if exec_count > 0:
                current_flow_data = flow_total - last_flow_data
                if now_page_name != last_page_name:
                    flow_increase = current_flow_data - last_flow
                    last_page_name = now_page_name
                    CollectData.flow_datas.append([now_page_name, last_page_name, flow_increase])
                    handle_error_data(flow_increase)

            # 用于记录每次的流量增量
            last_flow = current_flow_data
            exec_count += 1
            # 用于计算每次采集流量增量
            last_flow_data = flow_total

            # 时间间隔
            time.sleep(config.collect_data_interval)

    """
        用于获取fps数据
        @:param package_name 当前的包名
        @:param pic_name  出问题时保存的图片名称
    """

    @staticmethod
    def get_fps_data(package_name, pic_name='fps'):
        # 处理可能有问题的场景
        def handle_error_data(jank_count, fps):
            # 暂时当fps < 50 或者 jank_count > 10 我们认为是不达标的
            if fps < 50 or jank_count > 10:
                # 截图
                AdbUtil.screenshot(pic_name)
                # 保存日志

        # 死循环，满足条件后跳出
        exec_count = 0
        while True:
            LogUtil.log_i('get fps data')
            # 判断执行了多少次
            if exec_count > config.collect_data_count:
                break

            # 采集数据
            frame_count, jank_count, fps = AndroidUtil.get_fps_data_by_gfxinfo(package_name)
            if frame_count is None and jank_count is None and fps is None:
                exec_count += 1
                continue
            current_page = AndroidUtil.get_cur_activity()
            CollectData.fps_datas.append([frame_count, jank_count, fps, current_page])

            # 处理有问题的数据
            handle_error_data(jank_count, fps)
            exec_count += 1

            # 采集数据时间间隔
            time.sleep(config.collect_data_interval)

    """
        用于获取kpi数据
        @:param package_name 当前的包名
        @:param pic_name  出问题时保存的包名
    """

    @staticmethod
    def get_kpi_data(package_name, pic_name='kpi'):
        # 处理异常的kpi数据,当跳转时间大于3s（暂定）
        def handle_error_data(cost_time):
            if cost_time != '' and cost_time is not None:
                cost_time_value = handle_cost_time(cost_time)
                if cost_time_value > 3000:
                    AdbUtil.screenshot(pic_name)

        # 因为从日志中得到的值都是 +345ms 或者 +1s234ms
        def handle_cost_time(cost_time):
            s_data = 0
            ms_data = 0
            s_result = re.findall(r'\ds', cost_time)
            if len(s_result) > 0:
                s_data = int(s_result[0].split('s')[0]) * 1000
            ms_result = re.findall(r'\d\d\dms', cost_time)
            if len(ms_result) > 0:
                ms_data = int(ms_result[0].split('ms')[0])

            return s_data + ms_data

        # 记录起始时间
        global results
        start_time = time.mktime(time.localtime())
        cmd = 'adb logcat -c && adb logcat -v time -s ActivityManager | findStr %s' % package_name
        try:
            results = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        except Exception as e:
            LogUtil.log_e('get kpi failure ' + e.message)

        # 这里的逻辑是采集一定时间的数据之后，结束进程
        jump_page = ''
        cost_time = ''
        now_page_name = ''
        # 采集数据的次数
        get_count = 0
        while True:
            LogUtil.log_i('get kpi data')
            if get_count > config.collect_data_count:
                if results.poll() is None:
                    print 'results.terminate()'
                    results.stdout.close()
                break
            # 2.读取内容，并分析
            data = results.stdout.readline()
            print data
            # 处理读取到的String
            if data is not None:
                if 'Displayed' in data:
                    # 1. 获取跳转页面的名称及时间，过滤 Displayed
                    result = data.split('Displayed')
                    result = result[1].strip().split(':')
                    if len(result) < 1:
                        jump_page = 'unknow'
                        cost_time = 0
                    else:
                        jump_page = result[0].split('/')[1]
                        cost_time = result[1]

            # 2. 获取从哪个页面跳转
            if 'Moving to STOPPED:' in data:
                now_page = data.split('Moving to STOPPED:')
                now_page = now_page[1].strip().split(' ')
                if len(now_page) > 3:
                    now_page_name = now_page[2].split('/')[1]
                else:
                    now_page_name = 'unknow'

            # 将结果保存到数组中
            if now_page_name is not None and jump_page is not None and cost_time is not None:
                CollectData.kpi_datas.append([now_page_name, jump_page, handle_cost_time(cost_time)])
                handle_error_data(cost_time)
            get_count += 1

    """
        用于获取内存的数据
    """

    @staticmethod
    def get_memory_data(package_name, pic_name='memory'):
        i = 0
        last_page_name = ''
        last_memory_data = 0
        memory_increase = 0
        while i < config.collect_data_count:
            LogUtil.log_i('Inspect memory')
            memory_data = int(AndroidUtil.get_memory_data(package_name))  # 当前采集到的数据
            now_page_name = AndroidUtil.get_cur_activity()
            # 目前暂时粗略的计算增量，当页面不一样时，计算增量
            if now_page_name != last_page_name:
                memory_increase = memory_data - last_memory_data
                if memory_increase < 0:
                    # 对于发生GC的情况，内存增量可能是负值, 暂时先不做处理
                    pass
                CollectData.memory_datas.append([now_page_name, last_page_name, memory_increase])
                last_page_name = now_page_name
            else:
                last_memory_data = memory_data
                i += 1
                continue
            # 内存增量大于某个值就认为是有问题
            if memory_increase >= 10 * 1024:
                AdbUtil.screenshot(pic_name)
                LogUtil.log_i('Inspect memory 12')
            LogUtil.log_i('Inspect memory 13')

            # 设定多久采集一次数据
            time.sleep(config.collect_data_interval)
            i += 1