from flask import session,g
from .models import CMSUser,CMSPermission
from .views import bp
import config


#在返回cms主页前将用户信息绑定到g对象上供前端模板使用
@bp.before_request
def before_request():
	if config.CMS_USER_ID in session:
		user_id = session.get(config.CMS_USER_ID)
		user = CMSUser.query.get(user_id)
		if user:
			g.cms_user = user


#使用上下文处理器将CMSPermission返回，可以在前端bp蓝图下的任意模板中调用！
@bp.context_processor
def cms_context_processor():
	return {'CMSPermission':CMSPermission}