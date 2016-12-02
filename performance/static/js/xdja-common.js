/**
 * Created by zlw on 2016/12/2.
 */
   //获取当前包名和Activity
    $("#choose_package").click(function (event) {
        event.preventDefault();
        alert("11")
        $.getJSON(
            '/performance/getPackageName/',
            function (data) {
                $.each(data['package_name'], function (i, val) {
                    alert("22")
                    $("#choose_package_content").append('<li> <a href="#">'+val+'</a> </li>')
                })
            }
        )
        return false;
    });