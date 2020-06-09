import datetime
from qtpp import db


class _Case(db.Model):
    __abstract__ = True
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用例ID')
    c_name = db.Column(db.String(128), nullable=False, comment='用例名称')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )
    p_creator = db.Column(db.String(20), nullable=False, comment='创建者')


class CaseInterface(_Case):
    __tablename__ = 'case_interface'
    c_method = db.Column(db.String(10), nullable=False, comment='请求方式')
    c_url = db.Column(db.Text, nullable=False, comment='请求地址')
    c_headers = db.Column(db.Text, nullable=False, comment='请求头信息')
    c_body = db.Column(db.Text, nullable=False, comment='请求主体')
    c_params = db.Column(db.Text, nullable=False, comment='url参数')
    c_req_fmt = db.Column(db.Text, nullable=False, comment='请求格式')

    def __init__(self, name, creator, method, url, header, body, params, c_req_fmt):
        self.c_name = name
        self.p_creator = creator
        self.c_method = method
        self.c_url = url
        self.c_headers = header
        self.c_body = body
        self.c_params = params
        self.c_req_fmt = c_req_fmt

    def __repr__(self):
        return '<CASE ID:%r>' % self.c_id