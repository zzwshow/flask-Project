from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp  as front_bp
from exts import db
from exts import mail
from flask_wtf import CSRFProtect
import config


def create_app():
	app = Flask(__name__)
	app.config.from_object(config)  #加载配置文件
	db.init_app(app) #初始化app
	mail.init_app(app)
	app.register_blueprint(cms_bp)   #注册蓝图
	app.register_blueprint(common_bp)
	app.register_blueprint(front_bp)
	CSRFProtect(app)   #使用CSRF 保护app
	return app




if __name__ == '__main__':
	app = create_app()
	app.run(port=8000)
