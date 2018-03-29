from .views import bp
from flask import session,g,render_template
from .models import FrontUser
import config


#前台用户登录限制
@bp.before_request
def my_before_request():
	if config.FRONT_USER_ID in session:
		user_id = session.get(config.FRONT_USER_ID) #从session中取出登录用户的ID
		user = FrontUser.query.get(user_id)  #根据用户ID从数据库中查找这个用户
		if user:
			g.front_user = user  #将user信息绑定给g.front_user对象上，供jinja2 使用
		

#定义一个404页面
@bp.errorhandler
def page_not_found():
	return render_template('front/front_404.html'),404




