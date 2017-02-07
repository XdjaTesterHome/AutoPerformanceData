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
            $.each(data['package_name'], function (i, val) {
                var li = document.createElement("li");
                li.setAttribute("id", "newli" + i);
                li.setAttribute("width", 200);
                // li.innerHTML = '<a href="#">' + val + '</a>';
                li.innerHTML = val;
                li.onclick = function () {
                    $("#package_value").text(this.innerHTML).append('<b class="caret"></b>');
                    // 全局包名，通过this()获得
                    var package_name = this.innerHTML;
                    localStorage.setItem("package_name", package_name);
                    // window.global_package_name = this.innerHTML
                    window.location.reload();

                    //根据包名查询版本号
                    var arrversion = []
                    $.getJSON('/performance/getVersion/' + package_name + '/', function (data) {
                    $.each(data['version_list'], function (i,val) {
                        var li = document.createElement("li");
                        li.setAttribute("id", "version" + i);
                        li.innerHTML = val;
                        arrversion.push(val);
                        var version = arrversion[0];
                        localStorage.setItem("version", version);
                        $("#version_value").text(version).append('<b class="caret"></b>');
                        window.location.reload();
                    });});


                };
                $("#choose_package_content").append(li).append('<li class="divider"></li>');
                // $("#choose_package_content").append('<li> <a href="#">' + val + '</a> </li>').append('<li class="divider"></li>');
            })
        }
    );
}

function chooseVersion() {
    $("#choose_version_content").empty();
    var package_name = localStorage.getItem("package_name");
    $.getJSON('/performance/getVersion/' + package_name + '/', function (data) {
        $.each(data['version_list'], function (i,val) {
            var li = document.createElement("li");
            li.setAttribute("id", "version" + i);
            // li.innerHTML = '<a href="#">' + val + '</a>';
            li.innerHTML = val;
            li.onclick = function () {
                $("#version_value").text(this.innerHTML).append('<b class="caret"></b>');
                // 全局包名，通过this()获得
                var version = this.innerHTML;
                localStorage.setItem("version", version);
                // window.global_package_name = this.innerHTML
                window.location.reload();
            };
            $("#choose_version_content").append(li).append('<li class="divider"></li>');
        });
    });
}
function loadData() {
    $('a').css("color","white");
    var package_name = localStorage.getItem("package_name");
    var version_name = localStorage.getItem("version");
    if (package_name != null) {
        $("#package_value").text(package_name).append('<b class="caret"></b>');
        $("#version_value").text(version_name).append('<b class="caret"></b>');
    }
}