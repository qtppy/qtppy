from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.models.project import Project, TestSuite


bp = Blueprint('project', __name__, url_prefix='/project')
odb = OperationDB()



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_project():
    '''
    创建项目
    '''
    if request.method == 'POST':
        project_name = request.form['name']

        error = None
        
        if not g.user.uid:
            error = 'is not required.'
        
        if error is not None:
            # flash(error)
            return jsonify(Const.NOT_LOGIN_DICT)

        else:
            projects = Project(project_name, g.user.username, g.user.uid)
            odb.add(projects)

            
            Const.SUCCESS_DICT['errmsg'] = '创建项目成功.'
            Const.SUCCESS_DICT['res'] = {
                "project_name": project_name, 
                "p_id": projects.p_id
            }
            return jsonify(Const.SUCCESS_DICT)
 

    return abort(404)


@bp.route('/getall/<int:id>', methods=('GET', 'POST'))
@login_required
def get_project_or_suite_list(id):
    '''
    获取项目列表
    '''
    if request.method == 'POST':
        error = None

        if not g.user.uid:
            error = 'is not required.'
        
        if error is not None:
            return jsonify(Const.NOT_LOGIN_DICT)
        else:
            '''
            true获取项目内容，false获取测试集内容
            true_bool = (项目ID, 项目名称, 项目model对象， 用户ID字段，用户ID)
            false_bool = (测试集ID， 测试集名称，测试集model对象，项目ID字段，项目ID)
            '''
            true_bool = ('p_id', 'p_name', 'Project', 'user_id', g.user.uid)
            false_bool = ('sid', 's_name', 'TestSuite', 'p_id', int(request.form['p_id']))
            
            # id为1获取项目，否则获取测试集
            args = true_bool if id == 1 else false_bool

            #通过args[2] 来选择数据模型对象
            all_data = odb.query_all(eval(args[2]))

            Const.SUCCESS_DICT['errmsg'] = 'SUCCESS'
            Const.SUCCESS_DICT['res'] = {
                "project": [
                    {'%s'%args[0]:getattr(i, args[0]), "%s"%args[1]:getattr(i, args[1])} 
                    for i in all_data 
                        if getattr(i, args[3]) == args[4]
                    ]
            }

            return jsonify(Const.SUCCESS_DICT)

    return abort(404)


@bp.route('/suite/getlist', methods=('GET', 'POST'))
@login_required
def get_suite_by_pid():
    '''
    根据项目id获取，该项目下的所有测试集
    '''
    if request.method == 'GET':
        error = None
        if not g.user.uid:
            error = 'is not required.'

        if error is not None:
            return jsonify(Const.NOT_LOGIN_DICT)
        else:
            pid = request.args['pid']
            suite_data = odb.query_per(TestSuite, 'p_id', int(pid))

            Const.SUCCESS_DICT['errmsg'] = 'SUCCESS'
            Const.SUCCESS_DICT['res'] = {
                "suite":{
                    "sid": suite_data.sid,
                    "s_name": suite_data.s_name
                }
            }
            return jsonify(Const.SUCCESS_DICT)

    return abort(404)


@bp.route('/suite/create', methods=('GET', 'POST'))
@login_required
def create_suite():
    '''
    创建测试集
    '''
    if request.method == 'POST':

        error = None

        if not g.user.uid:
            error = '尚未登录.'

        if error is not None:
            return jsonify(
                {"errcode": 1001, "errmsg": error}
            )
        else:
            suite_name = request.form['s_name']
            project_id = request.form['project_id']

            test_suite = TestSuite(
                    suite_name, 
                    g.user.username, 
                    project_id
            )
            odb.add(test_suite)

            return jsonify(
                {
                    "errcode": 0, 
                    "errmsg": "新建模块成功.", 
                    'res':{"suite_id": test_suite.sid, "suite_name": suite_name, "project_id": project_id}
                }
            )
    return abort(404)