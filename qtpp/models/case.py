import datetime
from qtpp import db


class Case(db.Model):
    __abstract__ = True
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用例ID')
    c_name = db.Column(db.String(128), nullable=False, comment='用例名称')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )


class CaseInterface(Case):
    __tablename__ = 'case_interface'
    c_method = db.Column(db.String(10), nullable=False, comment='请求方式')
    c_url = db.Column(db.Text, nullable=False, comment='请求地址')
    c_headers = db.Column(db.Text, nullable=False, comment='请求头信息')
    c_body = db.Column(db.Text, nullable=False, comment='请求主体')
    sid = db.Column(db.Integer, db.ForeignKey(''), comment='测试集')

    suites = db.relationship('TestSuite', secondary='suite_case', backref='caseInterfaces')


suite_case = db.Table(
    'suite_case',
    db.Column('c_id', db.Integer, db.ForeignKey('case_interface.c_id'), comment='用例ID'),
    db.Column('sid', db.Integer, db.ForeignKey('p_test_suite.sid'), comment='测试集ID')
    )