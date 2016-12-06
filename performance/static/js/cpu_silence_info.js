
/**
 * Created by lzz on 2016/12/2.
 */
//获取当前页面echarts图表
$(document).ready(function(){

var package_name = localStorage.getItem("package_name");
$.get('/performance/getsilencecpudata/' + package_name).done(function (data) {
    var cpu_list = data["cpu_list"]
    alert(cpu_list);
    var cpu_data = [];
    for (var i=0;i<cpu_list.length-1;i=i+1)
     {

         cpu_data.push(cpu_list[i+1][1]);

    }
alert(cpu_data);
    if (package_name == "") {
        document.getElementById("p2").innerHTML = "当前未选择包名，请选定包名"
    }
    else  {
//        var cpu_data = [112, 23, 45, 56, 233, 343, 454, 89, 343, 123, 45, 123]//定义展示的测试数据
        var titletext = 'CPU静默监控信息';
        var pversion = "3.3.13.2314";
        var myChart = echarts.init(document.getElementById('main'), 'dark');  //创建echarts图表
        myChart.hideLoading();  //设置为隐藏载入
        myChart.setOption({
            title: {
                text: titletext + " 应用版本号：" + pversion
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['CPU占用率']
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    data: []
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: 'CPU占用量',
                    type: 'line',
                    stack: '总量',
                    areaStyle: {normal: {opacity: '0.05'}},
                    data: cpu_data
                }
            ]

        })
    }

})

});
