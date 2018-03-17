from  flask import session,redirect,url_for
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


