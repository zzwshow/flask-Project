from flask import (
	Blueprint,
	views,
	render_template,
	make_response
)
from utils.captcha import Captcha
from io import BytesIO
from exts import alidayu



bp = Blueprint("front",__name__)


@bp.route('/')
def index():
	return "front index"

#图形验证码
@bp.route('/captcha/')
def graph_captcha():
	#获取验证码
	text,image = Captcha.gene_graph_captcha()
	#字节流
	out = BytesIO()
	image.save(out,'png')
	out.seek(0)
	resp = make_response(out.read())
	resp.content_type = 'image/png'
	return resp


#注册页面
class SignupView(views.MethodView):
	def get(self):
		return render_template('front/signup.html')
	





bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))