DEBUG = True
import os

SECRET_KEY = os.urandom(24)

###数据库

# DB_URI = "mysql+pymysql://root:wei3511@127.0.0.1:3306/xmbbs_db?charset=utf8"

DB_URI = "mysql+pymysql://root:wei3511@127.0.0.1:3306/xmbbs_db1?charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

#临时定义后台 session 变量
CMS_USER_ID = "aaaa"

#邮箱配置信息
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL = default False
MAIL_USERNAME = "605882219@qq.com"
MAIL_PASSWORD = 'srfayonbjolhbddd'
MAIL_DEFAULT_SENDER = "605882219@qq.com"

#TLS: 端口是：587
#SSL：端口是：465
#QQ 不支持25端口非加密方式发送
