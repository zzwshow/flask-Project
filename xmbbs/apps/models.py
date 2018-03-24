
from exts import db
from datetime import datetime

#轮播图模板
class BannerModel(db.Model):
	__tablename__  = 'banner'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(255),nullable=False)
	image_url = db.Column(db.String(255),nullable=False)
	link_url = db.Column(db.String(255),nullable=False)
	priority = db.Column(db.Integer,default=0)
	create_time = db.Column(db.DateTime,default=datetime.now)


#版块模型
class BoardModel(db.Model):
	__tablename__ = "board"
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(20),nullable=False)
	create_time = db.Column(db.DateTime,default=datetime.now)


#帖子模型
class PostModel(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	title = db.Column(db.String(200),nullable=False)
	content = db.Column(db.Text,nullable=False)
	create_time = db.Column(db.DateTime,default=datetime.now)
	board_id = db.Column(db.Integer,db.ForeignKey('board.id')) #定义外键
	board = db.relationship("BoardModel",backref='posts') #定义关系
	
