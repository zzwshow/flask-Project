from flask import jsonify

#用于接口返回错误或成功时的代码！接口为json格式！
class HttpCode(object):
	ok = 200
	unauththerror =401
	paramserror = 400
	servererror = 500

def restful_result(code,message,data):  #这是个基础方法
	return jsonify({"code":code,"message":message,"data":data or {}})

def success(message="",data=None):   #成功信息
	return restful_result(code=HttpCode.ok,message=message,data=data)

def unauth_error(message=""):         #授权错误
	return restful_result(code=HttpCode.unauththerror,message=message,data=None)

def parames_error(message=""):        #参数错误
	return restful_result(code=HttpCode.paramserror,message=message,data=None)

def server_error(message=''):         #服务器内部错误
	return restful_result(code=HttpCode.servererror,message=message,data=None)


