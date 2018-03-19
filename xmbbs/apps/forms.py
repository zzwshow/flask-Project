
from flask_wtf import FlaskForm


class BaseForm(FlaskForm):  #表单基类，定义一些通用的方法，供表单验证类继承
	def get_error(self):
		message = self.errors.popitem()[1][0]
		return message

	def validate(self):
		return super(BaseForm, self).validate()

