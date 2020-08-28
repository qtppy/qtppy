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
    s_desc = db.Column(db.String(150), nullable=False, comment='测试集描述')

    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )
    p_creator = db.Column(db.String(50), nullable=False, comment='创建者')
    p_id = db.Column(db.Integer, db.ForeignKey('project.p_id', ondelete='CASCADE'), comment='项目ID')
    suite_case = db.relationship('SuiteCase', backref=db.backref('p_test_suite'), lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, s_name, p_creator, p_id, s_desc=''):
        self.s_name = s_name
        self.p_creator = p_creator
        self.p_id = p_id
        self.s_desc = s_desc

    def __repr__(self):
        return '<Suite ID:%r>' % self.sid


class SuiteCase(db.Model):
    __tablename__ = 'suite_case_interface'
    scid = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, comment='场景用例ID')
    scName = db.Column(db.String(128), nullable=False, comment='用例名称')
    scNo = db.Column(db.Integer, nullable=True, comment='用例在场景中的序顺号')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), comment='创建时间')
    update_time = db.Column(
        db.DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now, 
        comment='更新时间'
        )
    p_creator = db.Column(db.String(20), nullable=False, comment='创建者')
    uid = db.Column(db.Integer, nullable=False, comment='创建者ID')
    scDesc = db.Column(db.String(200), nullable=False, comment="用例描述")
    scMethod = db.Column(db.String(10), nullable=False, comment='请求方式')
    scUrl = db.Column(db.Text, nullable=False, comment='请求地址')
    scHeaders = db.Column(db.Text, nullable=False, comment='请求头信息')
    scBody = db.Column(db.Text, nullable=False, comment='请求主体')
    case_assert = db.relationship('Suite_Case_Assert', backref=db.backref('suite_case_interface'), lazy='dynamic', cascade='all, delete-orphan')
    case_result = db.relationship('Suite_Case_Result', backref=db.backref('suite_case_interface'), lazy='dynamic', cascade='all, delete-orphan')
    case_out_param = db.relationship('Suite_Case_Output_Parameter', backref=db.backref('suite_case_interface'), lazy='dynamic', cascade='all, delete-orphan')
    sid = db.Column(db.Integer, db.ForeignKey('p_test_suite.sid', ondelete='CASCADE'), comment='场景ID')

    def __init__(self, scName, scNo, p_creator, uid, scDesc, scMethod, scUrl, scHeaders, scBody, sid):
        self.scName = scName
        self.scNo = scNo
        self.p_creator = p_creator
        self.uid = uid
        self.scDesc = scDesc
        self.scMethod = scMethod
        self.scUrl = scUrl
        self.scHeaders = scHeaders
        self.scBody = scBody
        self.sid = sid



'''
Case_Assert: 单个case断言表
'''
class Suite_Case_Assert(db.Model):
    __tablename__ = 'suite_case_assert'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='断言ID')
    c_id = db.Column(db.Integer, db.ForeignKey('suite_case_interface.scid', ondelete='CASCADE'), comment='用例ID')
    check_type = db.Column(db.Integer, nullable=False, comment='断言类型')
    check_object = db.Column(db.Text, nullable=False, comment='断言对象')
    check_condition = db.Column(db.Integer, nullable=False, comment='断言条件')
    check_content = db.Column(db.Text, nullable=False, comment='断言内容')
    check_result = db.Column(db.String(20), nullable=False, comment='断言结果')

'''
Case_Result：单个case结果表
'''
class Suite_Case_Result(db.Model):
    __tablename__ = 'suite_case_result'
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='测试结果ID')
    c_id = db.Column(db.Integer, db.ForeignKey('suite_case_interface.scid', ondelete='CASCADE'), comment='用例ID')
    response_header = db.Column(db.Text, nullable=False, comment='响应头信息')
    response_body = db.Column(db.Text, nullable=False, comment='响应body')
    response_cookies = db.Column(db.Text, nullable=False, comment='响应cookie')
    response_datatime = db.Column(db.String(50), comment='响应时间(毫秒)')

'''
Case_Output_Parameter: 输出参数表
'''
class Suite_Case_Output_Parameter(db.Model):
    __tablename__ = 'suite_case_output_parameter'
    o_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='输出参数ID')
    c_id = db.Column(db.Integer, db.ForeignKey('suite_case_interface.scid', ondelete='CASCADE'), comment='用例ID')
    o_name = db.Column(db.String(100), nullable=False, comment='出参名称')
    o_soucre = db.Column(db.Integer, nullable=False, comment='出参来源')
    o_analytical_exp = db.Column(db.Text, nullable=False, comment='解析表达式')
    o_match = db.Column(db.Integer, nullable=False, comment='第几个匹配')