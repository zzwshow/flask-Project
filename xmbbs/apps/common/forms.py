from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp,InputRequired
import hashlib

class SMSCaptchaForm(BaseForm):
	salt = "qkasdfwermnkskjak%#$@"  #加盐字符串
	telephone = StringField(validators=[Regexp(r'1[1345789]\d{9}')])
	timestamp = StringField(validators=[Regexp(r'\d{13}')])
	sign = StringField(validators=[InputRequired()])

	def validate(self):
		result = super(SMSCaptchaForm, self).validate()
		if not result:
			return False

		telephone = self.telephone.data
		timestamp = self.timestamp.data
		sign = self.sign.data

		#md5(telephone+timestamp+salt)
		#md5函数必须传一个bytes类型的字符串进去
		sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()
		print('客户端传进来的sgin：%s' %sign)
		print('服务器生成的sgin：%s' %sign2)
		if sign == sign2:
			return True
		else:
			return False

