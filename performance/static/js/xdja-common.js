/**
 * Created by zlw on 2016/12/2.
 */

/**
 * 点击选择包名的按钮
 */
function choosepkg() {
    $("#choose_package_content").empty();
    $.getJSON(
        '/performance/getPackageName/',
        function (data) {
            var arr = data['package_name'];

            function arrrepat(arr) {
                var result = [];
                for (var i = 0; i < arr.length; i++) {
                    if (result.indexOf(arr[i]) == -1) {
                        result.push(arr[i])
                    }
                }
                return result;
            }

            var arr1 = arrrepat(arr);
            $.each(arr1, function (i, val) {
                var li = document.createElement("li");
                li.setAttribute("id", "newli" + i);
                // console.log(i);//
                li.setAttribute("width", "200");
                li.innerHTML = val;
                li.onclick = function () {
                    $("#package_value").text(this.innerHTML).append('<b class="caret"></b>');
                    // 全局包名，通过this()获得
                    var package_name = this.innerHTML;
                    localStorage.setItem("package_name", package_name);
                    // window.global_package_name = this.innerHTML
                    window.location.reload();

                    //根据包名查询版本号
                    var arrversion = [];
                    $.getJSON('/performance/getVersion/' + package_name + '/', function (data) {
                        $.each(data['version_list'], function (i, val) {
                            var li = document.createElement("li");
                            li.setAttribute("id", "version" + i);
                            li.innerHTML = val;
                            arrversion.push(val);
                            var version = arrversion[0];
                            localStorage.setItem("version", version);
                            $("#version_value").text(version).append('<b class="caret"></b>');
                            window.location.reload();
                        });
                    });
                };
                $("#choose_package_content").append(li).append('<li class="divider"></li>');
            })
        }
    );
}

function chooseVersion() {
    $("#choose_version_content").empty();
    var package_name = localStorage.getItem("package_name");
    $.getJSON('/performance/getVersion/' + package_name + '/', function (data) {
        $.each(data['version_list'], function (i, val) {
            var li = document.createElement("li");
            li.setAttribute("id", "version" + i);
            li.innerHTML = val;
            li.onclick = function () {
                $("#version_value").text(this.innerHTML).append('<b class="caret"></b>');
                // 全局包名，通过this()获得
                var version = this.innerHTML;
                localStorage.setItem("version", version);
                // window.global_package_name = this.innerHTML
                window.location.reload();
            };
            var checkBox = document.createElement("input");
            checkBox.setAttribute("type", "checkbox");
            checkBox.setAttribute("id", 'version' + i);
            checkBox.onclick = function () {
                checkboxOnclick(this)
            };
            function checkboxOnclick(checkBox) {
                if (checkBox.checked == true) {
                    console.log(i);
                    console.log(li.innerHTML);
                    var version = li.innerHTML;
                    var cpuList = [];
                    $.get('/performance/getCpuData/' + package_name + '/' + version).done(function (data) {
                        cpuList = data['cpu_list'];
                        data_render(cpuList, i);
                    });

                    //Action for checked
                } else {

                    cpuList = [];
                    data_render(cpuList, i);
                    //Action for not checked
                }
            }


            $("#choose_version_content").append(li).append(checkBox).append('<li class="divider" float="left";></li>');
        });

    });
}
function loadData() {
    $('a').css("color", "white");
    var package_name = localStorage.getItem("package_name");
    var version_name = localStorage.getItem("version");
    if (package_name != null) {
        $("#package_value").text(package_name).append('<b class="caret"></b>');
        $("#version_value").text(version_name).append('<b class="caret"></b>');
    }
}


function data_render(cpuList, i) {
    console.log('测试');
    var cpuList = cpuList;
    var ydata = [];
    var xdata = [];
    for (var i = 0; i < cpuList.length; i++) {
        xdata.push(i);
        var mdata = cpuList[i][cpuList[i].length - 1];
        if (isNaN(mdata)) {
            mdata = 0
        }
        ydata.push(mdata);
    }

    var option = {
        title: {
            text: 'Cpu使用情况'
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return params.value[2] + '<br/>' + "cpu占有率：" + params.value[1];
            }
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: ['cpu占有率']
        },
        grid: {
            y2: 80
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: xdata
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value} %'
                }
            }
        ],
        series: [
            {
                name: i,
                type: 'line',
                showAllSymbol: true,
                data: cpuList
            },

        ]
    };

    // 设置chart
    var myChart = echarts.init(document.getElementById('cpu_chart'));

    myChart.setOption(option)

}