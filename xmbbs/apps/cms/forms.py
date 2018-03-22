from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo,ValidationError
from ..forms import BaseForm
from utils import zlcache
from flask import g

#登陆表单验证
class LoginForm(BaseForm):
	email = StringField(validators=[Email(message="请输入正确的邮箱格式！"),InputRequired(message="请输入邮箱！")])
	password = StringField(validators=[Length(4,20,message="请输入正确的密码！")])
	remember = IntegerField()


#修改密码表单验证
class ResetPwdForm(BaseForm):
	oldpwd = StringField(validators=[Length(4,20,message="旧密码-格式错误！")])
	newpwd = StringField(validators=[Length(4,20,message="新密码-格式错误！")])
	newpwd2 = StringField(validators=[EqualTo("newpwd",message="两次密码不一致！")])

#修改邮箱表单验证
class RestEmailForm(BaseForm):
	email = StringField(validators=[Email(message="您输入的邮箱格式不正确！")])
	captcha = StringField(validators=[Length(min=4,max=4,message="请输入正确的验证码")])

	# 验证邮箱是否和当前登录邮箱一直
	def validate_email(self, field):
		email = field.data
		user = g.cms_user  # 获取当前登录用户信息，可从中获取当前邮箱地址
		# print(user.email)
		if user.email == email:
			raise ValidationError("不能修改为当前正在登录中的邮箱！")

	#定义一个验证码效验方法
	def validate_captcha(self,field):
		#validate_xxxx固定写法，xxxx就是要在次验证的上面定义的属性，field=captcha
		captcha = field.data
		email = self.email.data
		captcha_cache = zlcache.get(email) #从memecached中获取发给用的验证码
		if not captcha_cache or captcha.lower() != captcha_cache.lower(): #不区分用户传过来的大小写
			raise ValidationError("邮箱验证码错误")

#验证添加轮播图的表单
class AddBannerForm(BaseForm):
	name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
	image_url = StringField(validators=[InputRequired(message='请输入轮播图图片')])
	link_url = StringField(validators=[InputRequired(message='请输入轮播图链接')])
	priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])

#更新修改轮播图表单验证
class UpdataBannerForm(AddBannerForm):
	banner_id = IntegerField(validators=[InputRequired(message="请输入轮播图的ID")])




