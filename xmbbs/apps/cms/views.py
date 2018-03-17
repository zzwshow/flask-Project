from flask import (
    Blueprint,
    views,
    render_template,
    request, session,
    redirect,
    url_for,
    g
)
from .forms import LoginForm,ResetPwdForm,RestEmailForm
from .models import CMSUser
from .decorators import Login_Required
from exts import db, mail
from flask_mail import Message
from utils import restful,zlcache
import config
import string
import random

bp = Blueprint("cms", __name__, url_prefix="/cms")  # 蓝图url


@bp.route('/')
@Login_Required
def index():
    return render_template("cms/cms_index.html")


# 注销
@bp.route('/logout/')
@Login_Required
def logout():
    # session.clear()  #清除所有登录的用户
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 个人中心
@bp.route("/profile/")
@Login_Required
def profile():
    return render_template("cms/cms_profile.html")


##登陆类视图
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)  # 验证器获取表单数据
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.password.data
            user = CMSUser.query.filter_by(email=email).first()  # 验证email 是否存在
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id  # 验证成功后添加session 信息！用于以后判断用户是否登陆
                if remember:
                    session.permanent = True  # session 过期时间为31天
                return redirect(url_for('cms.index'))  # 重定向的蓝图主页（一点要加蓝图名字）

            else:
                return self.get(message="邮箱或密码错误")

        else:
            # message = form.errors.popitem()[1][0] #返回任意一项表单验证器定义的错误提示信息！
            message = form.get_error()  # 同上
            return self.get(message=message)


###修改密码类视图
class RestPwdView(views.MethodView):
    decorators = [Login_Required]  # 类视图中使用decorators来添加装饰器（限制登录）

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):  # 检查旧密码是否正确
                user.password = newpwd
                db.session.commit()
                return restful.success("邮箱修改成功")
            else:
                return restful.parames_error("旧密码错误")

        else:
            # message = form.get_error()   #获取表单验证器的错误提示
            # return jsonify({"code":400,"message":message})
            return restful.parames_error(form.get_error())


####修改邮箱
class ResetEmailView(views.MethodView):
    decorators = [Login_Required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = RestEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.parames_error(form.get_error())

#发送邮件验证码
@bp.route("/email_captcha/")
@Login_Required
def Email_captcha():

    email = request.args.get("email")
    if not email:
        return restful.parames_error("请输入邮箱地址！")
    source =  list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,4))       #生成8为的随机字符当做验证码
    message = Message("xmbbs邮箱验证码",recipients=[email],body='您的验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return "服务器异常！"
    #代码走到这里说明验证码已经发送成功了，将验证码写入到memecached中
    zlcache.set(email,captcha) #email当做key, captcha是验证码
    return restful.success("验证码发送成功！")

# 发送测试邮件
# @bp.route('/email/')
# def Send_mail():
#     message = Message("xmbbs邮件测试", recipients=["wei3511@126.com"], body="测试")
#     mail.send(message)
#     return "sucess"



##类视图url 添加到蓝图url中
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
###修改密码
bp.add_url_rule('/resetpwd/', view_func=RestPwdView.as_view('resetpwd'))
####修改邮箱
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
