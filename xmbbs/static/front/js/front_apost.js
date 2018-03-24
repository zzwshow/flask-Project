
//点击发布
$(function () {
    var ue = UE.getEditor('editor',{
        'serverUrl':'/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var boardSelect = $("select[name='board']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();  //获取用户编写的帖子内容包括字体颜色等！

        zlajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'content':content,
                'board_id':board_id
            },
            'success':function (data) {
                if(data['code']===200){
                    zlalert.alertConfirm({
                        'msg':'恭喜帖子发表成功！',
                        'cancelText':'回到首页',
                        'confirmText':'在发一篇',
                        'cancelCallback':function () {
                            window.location = "/"
                        },
                        'confirmCallback':function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                }else {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});


