from flask import (
	Blueprint,
	views,
	render_template
)

bp = Blueprint("front",__name__,url_prefix='/front')


@bp.route('/')
def index():
	return "front index"


#注册页面
class SignupView(views.MethodView):
	def get(self):
		return render_template('front/signup.html')
	



bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))