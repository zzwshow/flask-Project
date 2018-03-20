from flask import (
	Blueprint,
	views,
	render_template,
	request,
	session,
	url_for
)
from .forms import SignupForm,SigninForm
from exts import db
from  utils import restful,safeutils
from .models import FrontUser
import config


bp = Blueprint("front",__name__)


#首页
@bp.route('/')
def index():
	return render_template('front/front_index.html')


#注册页面
class SignupView(views.MethodView):
	def get(self):
		return_to = request.referrer  #获取客户端从哪个页面连接过来的（登陆后还返回哪里页面）
		if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
			return render_template('front/front_signup.html',return_to = return_to)
		else:
			return render_template("front/front_signup.html")

	def post(self):
		form = SignupForm(request.form)
		if form.validate():
			telephone = form.telephone.data
			username = form.username.data
			password = form.password.data
			telephone_db = FrontUser.query.filter_by(telephone=telephone).first()
			if telephone_db:
				return restful.parames_error(message="手机号已存在")
			else:
				user = FrontUser(telephone=telephone,username=username,password=password)
				db.session.add(user)
				db.session.commit()
				return restful.success()
		else:
			print(form.get_error())
			return restful.parames_error(message=form.get_error())


#登陆页面
class SigninView(views.MethodView):
	def get(self):
		return_to = request.referrer
		if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
			return  render_template('front/front_signin.html',return_to=return_to)
		else:
			return render_template('front/front_signin.html')

	def post(self):
		form = SigninForm(request.form)
		if form.validate():
			telephone = form.telephone.data
			password = form.password.data
			remember = form.remember.data
			user = FrontUser.query.filter_by(telephone=telephone).first()
			if user and user.check_password(password):
				session[config.FRONT_USER_ID] = user.id
				if remember:
					session.permanent = True
					return restful.success()
			else:
				return restful.parames_error(message="手机号码或密码错误！")

		else:
			return restful.parames_error(message=form.get_error())



bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))