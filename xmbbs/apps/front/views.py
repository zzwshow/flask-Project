from flask import (
	Blueprint,
	views,
	render_template,
	request,
	session,
	url_for,
	redirect,
	g
)
from .forms import SignupForm,SigninForm,AddPostForm
from exts import db
from  utils import restful,safeutils
from .models import FrontUser
import config
from ..models import BannerModel,BoardModel,PostModel
from .decorators import Login_Required
from flask_paginate import Pagination,get_page_parameter #分页工具

bp = Blueprint("front",__name__)


#首页
@bp.route('/')
def index():
	#显示四个轮播图
	banner = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
	boards = BoardModel.query.all()   #所有版块
	# posts = PostModel.query.all()  #所有帖子
	page = request.args.get(get_page_parameter(),type=int,default=1) #获取当前在第几页
	start = (page-1)*config.PRE_PAGE
	end = start +config.PRE_PAGE
	posts = PostModel.query.slice(start,end)
	pagination = Pagination(bs_version=3,page=page,total=PostModel.query.count()) #分页
	context = {
		'banners':banner,
		'boards':boards,
		'posts':posts,
		'pagination':pagination
	}
	return render_template('front/front_index.html',**context)


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
			password = form.password1.data
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
				# 用户登录之后将user.id 赋值给config文件中的变量FRONT_USER_ID,并传入session中！
				session[config.FRONT_USER_ID] = user.id
				if remember:
					session.permanent = True
					return restful.success()
			else:
				return restful.parames_error(message="手机号码或密码错误！")

		else:
			return restful.parames_error(message=form.get_error())

#用户注销
@bp.route('/logout/')
@Login_Required
def logout():
	del session[config.FRONT_USER_ID]
	return redirect(url_for('front.signin'))


#类视图注册路由
bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))

#发布帖子
@bp.route('/apost/',methods=['GET','POST'])
@Login_Required
def apost():
	if request.method == 'GET':
		board = BoardModel.query.all()  #获取所有版块，返回给前端！
		content = {
			'boards':board
		}
		return render_template('front/front_apost.html',**content)
	else:
		form = AddPostForm(request.form)
		if form.validate():
			title = form.title.data
			content = form.content.data
			board_id = form.board_id.data  #判断这个版块ID 是否存在！
			board = BoardModel.query.get(board_id)
			if not board:
				return restful.parames_error(message="没有这个版块！")
			else:
				post = PostModel(title=title,content=content)
				post.board = board   #将帖子加入到相应的版块中
				post.author = g.front_user
				db.session.add(post)
				db.session.commit()
				return restful.success()
		else:
			return restful.parames_error(message=form.get_error())


