from  flask import session,redirect,url_for,g
from functools import wraps
import config

#登陆限制
def Login_Required(func):
	@wraps(func)
	def inner(*args,**kwargs):
		if config.CMS_USER_ID in session:
			return func(*args,**kwargs)
		else:
			return redirect(url_for("cms.login"))
	return inner

#后台版块权限限制装饰器
def permission_required(permission):
	def other(func):
		@wraps(func)
		def inner(*args,**kwargs):
			user = g.cms_user
			if user.has_permission(permission):
				return func(*args,**kwargs)
			else:
				return redirect(url_for('cms/index.html'))
		return inner
	return other


