


$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();  //阻止默认表单提交事件
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();  //拿到表单数据
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        //csrf 使用
            //1、要在模板的meta标签中渲染一个csrf_token
            //2、在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            "url":"/cms/resetpwd/",
            "data":{
                "oldpwd":oldpwd,
                "newpwd":newpwd,
                "newpwd2":newpwd2
            },
            'success':function (data) {
                //data 是服务器返回的信息，（{code: 200, data: {…}, message: ""}）
                // console.log(data);  //将信息返回到控制台
                // 下面使用sweetalert 来返回
                if (data["code"] === 200){
                    zlalert.alertSuccessToast("恭喜！密码修改成功")
                    //密码修改成功后清空输入框中中的数据
                    oldpwdE.val('');
                    newpwdE.val('');
                    newpwd2E.val('');
                }else{
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }

            },
            'fail':function (error) {
                // console.log(error);
                zlalert.alertNetworkError();

            }
        });
    });
});



