
/**
 * Created by lzz on 2016/12/2.
 */
//获取当前页面echarts图表
$(document).ready(function(){

var package_name = localStorage.getItem("package_name");
$.get('/performance/getsilenceflowdata/' + package_name).done(function (data) {
    var flow_list = data["flow_list"]
    // alert(flow_list);
    var flow_data = [];
    for (var i=0;i<flow_list.length-1;i=i+1)
     {

         flow_data.push(flow_list[i+1][1]);

    }
// alert(flow_data);
    if (package_name == "") {
        document.getElementById("p2").innerHTML = "当前未选择包名，请选定包名"
    }
    else  {
//        var cpu_data = [112, 23, 45, 56, 233, 343, 454, 89, 343, 123, 45, 123]//定义展示的测试数据
        var titletext = '流量静默监控信息';
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
                data: ['业务流量消耗']
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
                    name: '流量消耗',
                    type: 'line',
                    stack: '总量',
                    areaStyle: {normal: {opacity: '0.05'}},
                    data: flow_data
                }
            ]

        })
    }

})

});
