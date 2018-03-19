from flask import (
	Blueprint,
	views,
	render_template,
	request
)
from .forms import SignupForm
from exts import db
from  utils import restful,safeutils
from .models import FrontUser


bp = Blueprint("front",__name__)


@bp.route('/')
def index():
	return render_template('front/front_index.html')

@bp.route('/test/')
def test():
	return render_template('front/front_test.html')


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
			user = FrontUser(telephone=telephone,username=username,password=password)
			db.session.add(user)
			db.session.commit()
			return restful.success()
		else:
			print(form.get_error())
			return restful.parames_error(message=form.get_error())






bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))