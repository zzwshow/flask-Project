from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


#定义权限
class CMSPermission(object):
	#所有权限
	ALL_permission = 0b11111111
	#访问者
	VISITOR =        0b00000001
	#管理帖子权限
	POSTER =         0b00000010
	#管理评论权限
	COMMENTER =      0b00000100
	#管理板块权限
	BOARDER =        0b00001000
	#管理前台用户权限
	FRONTUSER =		 0b00010000
	#管理后台用户权限
	CMSUSER =		 0b00100000


#中间表
cms_role_user = db.Table(
	'cms_role_user',
	db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
	db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

#角色表
class CMSRole(db.Model):
	__tablename__ = 'cms_role'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(50),nullable=False)
	desc = db.Column(db.String(200),nullable=True)
	create_time = db.Column(db.DateTime,default=datetime.now)
	permissions = db.Column(db.Integer,default=CMSPermission.VISITOR)

	users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')


#用户表
class CMSUser(db.Model):
	__tablename__ = "cms_user"
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	username = db.Column(db.String(50),nullable=False)
	_password = db.Column(db.String(100),nullable=False)
	email = db.Column(db.String(50),nullable=False,unique=True)
	join_time = db.Column(db.DateTime,default=datetime.now)

	def __init__(self,username,password,email):
		self.username = username
		self.password = password
		self.email = email

	#加密password
	@property   #将类中的方法变为类的属性！外部使用CMSUser.password来获取密码
	def password(self):
		return self._password

	# 上面已经把password变为了属性，我们就可以给属性赋值，CMSUser.password="abc123"
	# @password.setter装饰器可以在复值时给他进行一些处理，如加密
	@password.setter
	def password(self,raw_password):
		#加密密码
		self._password = generate_password_hash(raw_password)

	def check_password(self,raw_password):
		#验证密码
		result = check_password_hash(self.password,raw_password)
		return result


	#定义方法，获取某用户所有权限
	@property
	def permissions(self):
		if not self.roles:
			return 0
		else:
			all_permissions = 0
			for role in self.roles:
				permission = role.permissions  #拿到用户 每个角色中的权限
				all_permissions |= permission  #合并所有权限“|” 或运算
			return all_permissions

	#判断摸个用户是否有某个权限
	def has_permission(self,permission):
		# all_permissions = self.permissions  #调用上面获取权限的方法 获取用户拥有的所有权限
		# result = all_permissions&permission == permission #使用与运算判断用户是否有permission权限
		# return result
		#简化写法
		return self.permissions&permission == permission

	#判断用户是不是开发者
	@property
	def is_developer(self):
		#开发者权限是（CMSPermission.ALL_permission），这里我们调用上面的has_permission方法即可
		return self.has_permission(CMSPermission.ALL_permission)
