from flask import redirect,url_for,session
from functools import wraps
import config

#前台登录限制
def Login_Required(func):
	@wraps(func)
	def inner(*args,**kwargs):
		if config.FRONT_USER_ID in session:
			return func(*args,**kwargs)
		else:
			return redirect(url_for("front.signin"))
	return inner

