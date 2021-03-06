//提交新添加的轮播图数据到后台
$(function () {
    $("#save-banner-btn").click(function (event) {
       event.preventDefault();
       var self = $(this);
       var dialog = $("#banner-dialog");
       var nameInput = $("input[name='name']");
       var imageInput = $("input[name='image_url']");
       var linkInput = $("input[name='link_url']");
       var priorityInput = $("input[name='priority']");
       var submitType = self.attr('data-type');
       var bannerId = self.attr('data-id');

       var name = nameInput.val();
       var image_url = imageInput.val();
       var link_url = linkInput.val();
       var priority = priorityInput.val();
       if (!name || !image_url || !link_url || !priority){
           zlalert.alertInfoToast("请输入完整的轮播图数据！");
           return;
       }
       var url = "";
       if(submitType === "update"){
           url = "/cms/ubanners/";
       }else{
           url = "/cms/abanners/";
       }

       zlajax.post({
           'url':url,
           'data':{
               'name':name,
               'image_url':image_url,
               'link_url':link_url,
               'priority':priority,
               'banner_id':bannerId
           },
           'success':function (data) {
               dialog.modal('hide');      //隐藏弹出窗
               if (data['code']===200){
                   //重新加载整个页面
                   window.location.reload();
               }else {
                   zlalert.alertInfo(data['message']);
               }
           },
           'fail':function () {
                zlalert.alertNetworkError()
           }
       });
    });

});

//监视点击编辑后做什么操作
$(function () {
    $(".edit-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");     //显示弹出窗

        //获取数据
        var tr = self.parent().parent();   //前端页面将属性绑定在了tr标签上
        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');
        //获取表单字段
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");   //找到保存按钮

        //将数据添加进表单中前端显示
        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type","update");
        saveBtn.attr("data-id",tr.attr("data-id"))

    });

});

//删除轮播图按钮
$(function () {
   $('.del-banner-btn').click(function (event) {
      event.preventDefault();
      var self = $(this);
      var tr = self.parent().parent();
      var banner_id = tr.attr('data-id');

      zlalert.alertConfirm({
          'msg':'您确定要删除这个轮播图吗？',
          'confirmCallback':function(){
              zlajax.post({
                 'url':"/cms/debanner/",
                  'data':{
                     'banner_id':banner_id
                  },
                  'success':function (data) {
                     if(data["code"]===200){
                         window.location.reload();
                     }else{
                         zlalert.alertInfo(data['message']);
                     }

                  }
              });
          }

      });

   });
});












