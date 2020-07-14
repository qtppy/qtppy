import datetime
from qtpp import db

'''
_Case: case基本model __abstract__
'''
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
    c_desc = db.Column(db.String(200), nullable=False, comment="用例描述")

'''
CaseInterface：接口测试用例表
'''
class CaseInterface(_Case):
    __tablename__ = 'case_interface'
    c_method = db.Column(db.String(10), nullable=False, comment='请求方式')
    c_url = db.Column(db.Text, nullable=False, comment='请求地址')
    c_headers = db.Column(db.Text, nullable=False, comment='请求头信息')
    c_body = db.Column(db.Text, nullable=False, comment='请求主体')
    case_assert = db.relationship('Case_Assert', backref=db.backref('case_interface'), lazy='dynamic', cascade='all, delete-orphan')
    case_result = db.relationship('Case_Result', backref=db.backref('case_interface'), lazy='dynamic', cascade='all, delete-orphan')
    case_out_param = db.relationship('Case_Output_Parameter', backref=db.backref('case_interface'), lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, creator, method, url, header, body, desc):
        self.c_name = name
        self.p_creator = creator
        self.c_method = method
        self.c_url = url
        self.c_headers = repr(header)
        self.c_body = repr(body)
        self.c_desc = repr(desc)

    def __repr__(self):
        return '<CASE ID:%r>' % self.c_id

'''
Case_Assert: 单个case断言表
'''
class Case_Assert(db.Model):
    __tablename__ = 'case_assert'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='断言ID')
    c_id = db.Column(db.Integer, db.ForeignKey('case_interface.c_id', ondelete='CASCADE'), comment='用例ID')
    check_type = db.Column(db.Integer, nullable=False, comment='断言类型')
    check_object = db.Column(db.Text, nullable=False, comment='断言对象')
    check_condition = db.Column(db.Integer, nullable=False, comment='断言条件')
    check_content = db.Column(db.Text, nullable=False, comment='断言内容')
    check_result = db.Column(db.String(20), nullable=False, comment='断言结果')

'''
Case_Result：单个case结果表
'''
class Case_Result(db.Model):
    __tablename__ = 'case_result'
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='测试结果ID')
    c_id = db.Column(db.Integer, db.ForeignKey('case_interface.c_id', ondelete='CASCADE'), comment='用例ID')
    response_header = db.Column(db.Text, nullable=False, comment='响应头信息')
    response_body = db.Column(db.Text, nullable=False, comment='响应body')
    response_cookies = db.Column(db.Text, nullable=False, comment='响应cookie')
    response_datatime = db.Column(db.String(50), comment='响应时间(毫秒)')

'''
Case_Output_Parameter: 输出参数表
'''
class Case_Output_Parameter(db.Model):
    __tablename__ = 'case_output_parameter'
    o_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='输出参数ID')
    c_id = db.Column(db.Integer, db.ForeignKey('case_interface.c_id', ondelete='CASCADE'), comment='用例ID')
    o_name = db.Column(db.String(100), nullable=False, comment='出参名称')
    o_soucre = db.Column(db.Integer, nullable=False, comment='出参来源')
    o_analytical_exp = db.Column(db.Text, nullable=False, comment='解析表达式')
    o_match = db.Column(db.Integer, nullable=False, comment='第几个匹配')