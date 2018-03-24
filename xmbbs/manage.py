from  flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from exts import db
from xmbbs import create_app
from apps.cms import models as cms_models  #后台模型
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

from apps.front import models as front_models  #前台模型
from apps.models import BannerModel,BoardModel,PostModel   #轮播图模板
FRONTUser = front_models.FrontUser



app = create_app()
manager = Manager(app)   #将项目app 加入管理器

Migrate(app,db)          #关联app于db

manager.add_command('db',MigrateCommand)  #将MigrateCommond (包含很多迁移子命令)绑定给db


#在角色CMSRole模型中创建初始化几个角色
@manager.command
def create_role():
	#访问者
	visitor = CMSRole(name='访问者',desc='只能显示数据，不能修改')
	visitor.permissions = CMSPermission.VISITOR

	#运营
	operator = CMSRole(name='运营',desc='显示数据，修改个人信息，管理评论，管理帖子，管理前台用户')
	operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

	#管理员
	admin = CMSRole(name='管理员',desc='本系统所有权限')
	admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.CMSUSER

	#开发者
	developer = CMSRole(name='开发者',desc='开发者专用角色')
	developer.permissions = CMSPermission.ALL_permission

	db.session.add_all([visitor,operator,admin,developer])  #以上角色提交到数据库
	db.session.commit()

#定义命令-添加后台用户！
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
	user =CMSUser(username=username,password=password,email=email)
	db.session.add(user)
	db.session.commit()
	print("cms 用户添加成功！")


#定义命令-添加用户到指定角色中去！
@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_role(email,name):
	user = CMSUser.query.filter_by(email=email).first()
	if user:
		role = CMSRole.query.filter_by(name=name).first()
		if role:
			role.users.append(user)  #将用户添加到角色中！
			db.session.commit()
			print("用户%s已经添加到%s角色拉" % (email,name))
		else:
			print("%s 是不存在的角色" % name)
	else:
		print("%s 邮箱用户不存在" % email)



#定义命令-测试用户有权限吗
@manager.command
def test_permission():
	user  = CMSUser.query.first()
	if user.has_permission(CMSPermission.CMSUSER):
		print("这个用户有访问权限")
	else:
		print("这个用户没有访问权限")
		
		
#定义命令-添加前台用户
@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
	user = FRONTUser(telephone=telephone,username=username,password=password)
	db.session.add(user)
	db.session.commit()
	

if __name__ == '__main__':
	manager.run()