
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
                           zlalert.alertSuccess(data['message']);
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



