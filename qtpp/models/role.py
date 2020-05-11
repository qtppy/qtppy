import datetime
from qtpp import db

class Role(db.Model):
    
    __tablename__='role'
    r_id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    r_name=db.Column(db.String(10))
    users=db.relationship('User',backref='role')


#角色和权限的(多对多的)关联表
#r_p为关联表的表名
r_p=db.Table(
    'r_p',
    db.Column('role_id',db.Integer,db.ForeignKey('role.r_id'), primary_key=True),
    db.Column('permission_id',db.Integer,db.ForeignKey('permission.p_id'), primary_key=True)
)


#权限模型表
class Permission(db.Model):
    __tablename__='permission'
    p_id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    p_name=db.Column(db.String(16), unique=True)
    p_er=db.Column(db.String(16), unique=True)
    #添加多对多的反向引用,必须使用secondary指定中间关联表
    #用权限查询角色时用查询到的权限对象：“权限对象.roles.all()”得到其对应的所有角色
    roles=db.relationship('Role', secondary=r_p, backref=db.backref('permission', lazy=True))
    #db.backref('permission', 中的permission用来反向关联，用角色查询其对应的所有权限。用查询到的 '角色对象.permission.all()'得到。
    ###relationship可以放到任意一个类中都行，与之相反。###