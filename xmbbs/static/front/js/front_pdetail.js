$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl':'/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});


//点击发表评论提交后台
$(function () {
   $('#comment-btn').click(function (event) {
       event.preventDefault();
       var loginTag = $("#login-tag").attr("data-is-login"); //拥挤判断用户是否在登录状态
       if(!loginTag){
           window.location = '/signin/';

       }else {
           var content = window.ue.getContent(); //获取评论内容
           var post_id = $("#post-content").attr("data-id") //拿到帖子ID
           zlajax.post({
               'url':'/acomment/',
               'data':{
                   'content':content,
                   'post_id':post_id
               },
               'success':function (data) {
                   if(data['code']===200){
                       zlalert.alertSuccess();
                   }else {
                       zlalert.alertInfo(data['message']);
                   }

               }
           });
       }

   });
});