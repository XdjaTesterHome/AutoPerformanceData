/**
 * Created by zlw on 2016/12/2.
 */


var m = [[],[],[],[]]; //定义全局变量，并初始化为空数组。
var verchecked0, verchecked1, verchecked2,verchecked3;
var verchecked=[];
var i;
/**
 * vercheck用于记录当前版本是否被选中
 */
function vercheck(verchecked,i,xx){
    verchecked0 = document.getElementById("version0");
    verchecked1 = document.getElementById("version1");
    verchecked2 = document.getElementById("version2");
    verchecked3 = document.getElementById("version3");

    verchecked = [verchecked0,verchecked1,verchecked2,verchecked3];
    for(var j=0;j < 4;j++){
        if(j ==i){
            verchecked[j].checked=xx;
        }else{
            // verchecked[j].checked=false;
        }
    }
    return verchecked;
}

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

/**
 * 点击选择版本号的监控方法
 */
function chooseVersion() {
    $("#choose_version_content").empty();
    var package_name = localStorage.getItem("package_name");
    $.getJSON('/performance/getVersion/' + package_name + '/', function (data) {
        $.each(data['version_list'], function (i, val) {
            i = i;//全局变量赋值
            var li = document.createElement("li");
            li.setAttribute("id", "version" + i+6);
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
            if(verchecked.length>0){
                if (verchecked[i].checked ==true){
                checkBox.setAttribute("checked",'checked');
                }
            }


            checkBox.onclick = function () {
                checkboxOnclick(this,i,package_name,li);//解决办法是以参数形式传递
            };


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




/**
 * 根据版本号和包名，处理得到的CPUJSON数据
 */
function handedata(arrdata){
    var d = [];
    for (var i = 0; i < arrdata.length; i++) {
        var value = arrdata[i][1];
        if (isNaN(value)) {
            value = 0;
        }
        d.push(value)
    }
    return d;

}

function allcheck(m,i,list,option,chart){
    m[i]= list;
    var Series = [];
    var Item = function() {
        return {
            name: '',
            type: 'line',
            showAllSymbol: true,
            data: []
        }
    };
    for(var j=0;j < 4;j++){
            var it = new Item();
            it.name = j;
            it.data = m[j];
            Series.push(it);
        }
    var myChart = echarts.init(document.getElementById(chart));
    option.series = Series; // 设置图表
    myChart.setOption(option);// 重新加载图表
    return m;
}