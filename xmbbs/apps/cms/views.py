from flask import (
    Blueprint,
    views,
    render_template,
    request, session,
    redirect,
    url_for,
    g
)
from .forms import (
    LoginForm,
    ResetPwdForm,
    RestEmailForm,
    AddBannerForm,
    UpdataBannerForm
)
from .models import CMSUser,CMSPermission
from ..models import BannerModel
from .decorators import Login_Required,permission_required
from exts import db, mail
from flask_mail import Message
from utils import restful,zlcache
import config
import string
import random

bp = Blueprint("cms", __name__, url_prefix="/cms")  # 蓝图url

#首页
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

#CMS后台各模块
@bp.route('/posts/')
@Login_Required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@bp.route('/comments/')
@Login_Required
@permission_required(CMSPermission.COMMENTER)
def commends():
    return render_template('cms/cms_comments.html')

@bp.route('/boards/')
@Login_Required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')

@bp.route('/fusers/')
@Login_Required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@Login_Required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@Login_Required
@permission_required(CMSPermission.ALL_permission)
def croles():
    return render_template('cms/cms_croles.html')



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


#管理轮播图
@bp.route('/banners/')
@Login_Required
def banners():
    banners = BannerModel.query.all()  #找到数据库中所有的轮播图信息！返回给前端
    return render_template('cms/cms_banners.html',banners=banners)


#添加轮播图
@bp.route('/abanners/',methods=["POST"])
@Login_Required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    return restful.parames_error(form.get_error())

#更新修改轮播图信息
@bp.route('/ubanner/',methods=['POST'])
@Login_Required
def ubanner():
    form = UpdataBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.parames_error(message="没有这个轮播图")
    else:
        return restful.parames_error(form.get_error())



##类视图url 添加到蓝图url中
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
###修改密码
bp.add_url_rule('/resetpwd/', view_func=RestPwdView.as_view('resetpwd'))
####修改邮箱
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
