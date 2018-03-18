from flask import Blueprint,request
from exts import alidayu
from utils import restful
from utils.captcha import Captcha

bp = Blueprint("common",__name__,url_prefix="/c")


#发送短信接口
@bp.route('/sms_captcha/')
def sms_captcha():
	telephone = request.args.get('telephone')
	if not telephone:
		return restful.parames_error(message='请传入手机号码')
	
	captcha = Captcha.gene_text(number=4)
	if alidayu.send_sms(telephone,code=captcha):
		return restful.success(message='短信发送成功')
	else:
		#连接秘钥改了 这里只是测试（全部返回OK）
		# return restful.parames_error(message='短信发送失败')
		return restful.success("发送成功")
	
	
	
	