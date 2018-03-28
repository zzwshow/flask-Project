from flask import Blueprint,request,make_response,jsonify
from exts import alidayu
from utils import restful,zlcache
from utils.captcha import Captcha
from .forms import SMSCaptchaForm,UploadForm
from io import BytesIO
import qiniu
from werkzeug.datastructures import CombinedMultiDict #将两个不可变类型组合在一起
from werkzeug.utils import secure_filename  #安全效验文件名
import os
Upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static')


bp = Blueprint("common",__name__,url_prefix="/c")


#发送短信接口（前端get请求）
# @bp.route('/sms_captcha/')
# def sms_captcha():
# 	telephone = request.args.get('telephone')
# 	if not telephone:
# 		return restful.parames_error(message='请传入手机号码')
#
# 	captcha = Captcha.gene_text(number=4)
# 	if alidayu.send_sms(telephone,code=captcha):
# 		return restful.success(message='短信发送成功')
# 	else:
# 		#连接秘钥改了 这里只是测试（全部返回OK）
# 		return restful.parames_error(message='短信发送失败')
# 		#return restful.success("发送成功")
#

##发送短信接口（前端post请求）
@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
	form = SMSCaptchaForm(request.form)
	if form.validate():
		telephone = form.telephone.data
		captcha = Captcha.gene_text(number=4)   #生成4位短信验证码
		print("发送的短信验证码是%s" % captcha)
		if alidayu.send_sms(telephone,code=captcha):
			zlcache.set(telephone,captcha)         #将手机验证码存储到memcached种，telephone为KEY，captcha为值
			return restful.success()
		else:
			#return restful.parames_error("参数错误")
			zlcache.set(telephone, captcha)        ### 为了测试 就算阿里大于发送失败也存储到memcached
			return restful.success()  #用于测这里设置为成功！！！
	else:
		return restful.parames_error(message="参数错误")


#图形验证码
@bp.route('/captcha/')
def graph_captcha():
	#获取验证码
	text,image = Captcha.gene_graph_captcha()
	zlcache.set(text.lower(),text.lower())   #图形验证吗存储到memcached，key和value都是验证码本身并变为小写存储
	#字节流
	out = BytesIO()
	image.save(out,'png')
	out.seek(0)
	resp = make_response(out.read())
	resp.content_type = 'image/png'
	return resp

#七牛静态图片上传接口(将token返回个前端)
# @bp.route('/uptoken/')
# def uptoken():
# 	access_key = "aGsmFPlxj1ahhEh_QaevKtSZila_JA5icJAwkxbw"
# 	secret_key = "Q_6ZaieEOyISuMNSvPBYGYCNGZyvGvGPMXn0QS5e"
# 	q = qiniu.Auth(access_key,secret_key)   #定义一个七牛链接对象
#
# 	bucket = "altzzw"  #七牛中定义的存储空间名
# 	token = q.upload_token(bucket)    #生成token
# 	return jsonify({'uptoken':token})   #以json格式返回token给前端，key必须是“uptoken”

#上传本地文件夹
@bp.route('/upload/')
def upload():
	form = UploadForm(request.files)
	if form.validate():
		banner = request.files.get("banner")
		filename = secure_filename(banner.filename)
		print(filename)
		banner.save(os.path.join(Upload_path,'images'))
		return restful.success()
	else:
		return restful.parames_error(form.get_error())





