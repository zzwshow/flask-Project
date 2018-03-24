//监听添加新版块按钮
$(function () {
   $('#add-board-btn').click(function (event) {
       event.preventDefault();
       zlalert.alertOneInput({
           'title':'新增版块',
           'text':"请输入版块名称",
           'confirmText':'确认添加',
           "placeholder":"版块名称",
           "confirmCallback":function (inputValue) {
               zlajax.post({
                  'url':'/cms/aboards/',
                   'data':{
                      'name':inputValue    //inputValue就是输入框输入的内容！
                   },
                   'success':function (data) {
                       if (data['code']===200){
                           window.location.reload();
                       }else {
                           zlalert.alertInfo(data['message']);
                       }
                   }
               });
           }
       });
   });
});

//监听编辑按钮
$(function () {
    $(".edit-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();  //找到编辑按钮的两层父及标签tr

        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');
            
            //zlajax中的弹出框
            zlalert.alertOneInput({
                'title':'编辑版块',
                'text':'请输入新的版块名称',
                'placeholder':name,
                'confirmText':'确认',
                'confirmCallback':function (inputValue) {
                    zlajax.post({
                        'url':"/cms/uboard/",
                        'data':{
                            'board_id':board_id,
                            'name':inputValue
                        },
                        'success':function (data) {
                            if(data['code']===200){
                                window.location.reload();
                            }else {
                                zlalert.alertInfo(data['message']);
                            }
                        }
                    });
                }
            });

    });
});




