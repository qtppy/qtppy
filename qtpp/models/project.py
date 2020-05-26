import datetime
from qtpp import db

'''
ondelete:

RESTRICT、NO ACTION：删除，会阻止删除。NO ACTION在MySQL中，与RESTR功能一致。
CASCADE: 数据被删除，关联数据也会被删除。
SET NULL: 数据被删除，关联的数据会设置为null。

Flask中使用ORM时候，如果删除了父记录希望级联删除字对象的话:
# 一的一方：cascade='all, delete-orphan'
    books = db.relationship('Book', backref='device', lazy='dynamic',cascade='all, delete-orphan')
# 多的一方: db.ForeignKey( ondelete='CASCADE')
    device_id = db.Column(db.Integer, db.ForeignKey('persons.id',ondelete='CASCADE'))

# 多 对 多 # cascade="all, delete-orphan",passive_deletes=True

single_parent=True
'''

class Project(db.Model):
    __tablename__ = "project"
    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='项目ID')
    p_name = db.Column(db.String(50), nullable=False, comment='项目名称')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )
    p_creator = db.Column(db.String(50), nullable=False, comment='创建者')
    p_status = db.Column(db.Integer, nullable=False, default=0, comment='项目状态')
    p_desc = db.Column(db.String(150), nullable=False, comment='项目描述')
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid', ondelete='RESTRICT'), comment='用户ID')
    test_suite = db.relationship('TestSuite', backref=db.backref('project'), lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, p_name, p_creator, user_id, p_desc):
        self.p_name = p_name
        self.p_creator = p_creator
        self.user_id = user_id
        self.p_desc = p_desc

    def __repr__(self):
        return "<ProjectID:%r>" % self.p_id



class TestSuite(db.Model):
    __tablename__ = 'p_test_suite'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='测试集ID')
    s_name = db.Column(db.String(50), nullable=False, comment='模块名称或测试集名称')

    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )
    p_creator = db.Column(db.String(50), nullable=False, comment='创建者')
    p_id = db.Column(db.Integer, db.ForeignKey('project.p_id', ondelete='CASCADE'), comment='项目ID')

    def __init__(self, s_name, p_creator, p_id):
        self.s_name = s_name
        self.p_creator = p_creator
        self.p_id = p_id

    def __repr__(self):
        return '<Suite ID:%r>' % self.sid

