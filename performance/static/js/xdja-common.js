/**
 * Created by zlw on 2016/12/2.
 */
//获取当前包名和Activity
$("#choose_package").click(function (event) {
    event.preventDefault();
    alert("11");
    $.getJSON(
        '/performance/getPackageName/',
        function (data) {
            $.each(data['package_name'], function (i, val) {
                alert("22")
                $("#choose_package_content").append('<li> <a href="#">' + val + '</a> </li>')
            })
        }
    );
    return false;
});

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
                li.setAttribute("id", "newli"+ i);
                li.setAttribute("width", 200);
                // li.innerHTML = '<a href="#">' + val + '</a>';
                li.innerHTML = val;
                li.onclick = function () {
                    $("#package_value").text(this.innerHTML).append('<b class="caret"></b>');
                    // 全局包名，通过this()获得
                    global_package_name = this.innerHTML
                };
                $("#choose_package_content").append(li).append('<li class="divider"></li>');
                // $("#choose_package_content").append('<li> <a href="#">' + val + '</a> </li>').append('<li class="divider"></li>');
            })
        }
    );
}