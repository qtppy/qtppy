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
        project_name = request.json['p_name']
        p_desc = request.json['p_desc']
     
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        projects = Project(project_name, g.user.username, g.user.uid, p_desc)
        odb.add(projects)

        res = {
            "project_name": project_name, 
            "p_id": projects.p_id,
            "p_desc": projects.p_desc,
            "p_creator": projects.p_creator,
            "p_status": projects.p_status,
            "p_createtime": projects.create_time
        }
        return jsonify(Const.errcode('0', res=res))
 

    return abort(404)


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete_project():
    '''
    删除项目,级联测试集也会删除
    args:
        p_id: 项目ID
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1101'))

        # 获取参数p_id
        p_id_lst = request.json


        del_res = []
        for p_id in p_id_lst['p_id']:
            dt = odb.delete(Project, 'p_id', int(p_id))
            del_res.append({"p_id": p_id, "p_name": dt.p_name})

        res = {
            'project': del_res
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update_project_info():
    '''
    更新项目
    method: post
    params: p_id, name
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        params =  request.json

        # 按照项目ID，更新项目名称
        dt = odb.update(
            Project, 
            'p_id', 
            params['p_id'], 
            p_name=params['p_name'],
            p_desc=params['p_desc']
        )

        res = {
            'project': {
                "p_id": dt.p_id,
                "new_p_name": dt.p_name
            }
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/getAllList', methods=['GET', 'POST'])
@login_required
def get_all_project_list():
    '''
    获取所有项目
    Args: 
        page: url params请求参数, 不传默认为1
        p_name: 项目名称查询
    return:
        {
            "errcode": 0,
            "errmsg": "SUCCESS",
            "res": {
                "next_page": 3,
                "page": 2,
                "pages": 4,
                "per_page": 10,
                "prev_num": 1,
                "project": [
                    {
                        "create_time": "Tue, 26 May 2020 17:30:32 GMT",
                        "p_d": "xzdylyh",
                        "p_desc": "这是项目描述，我最多支持150字符",
                        "p_id": 11,
                        "p_name": "我的第1个项目",
                        "p_status": 0
                    },
                    {
                        "create_time": "Tue, 26 May 2020 17:35:20 GMT",
                        "p_d": "xzdylyh",
                        "p_desc": "这是项目描述，我最多支持150字符",
                        "p_id": 12,
                        "p_name": "我的第1个项目",
                        "p_status": 0
                    }
                ],
                "total": 39
            }
        }  
    '''
    if request.method == 'POST':
        if not g.user.uid:
            return Const.errcode('1001')

        dt = odb.query_per_all(Project, 'p_creator', g.user.username)

        # response数据组装
        res = {
            "project": [{
                "create_time": item.create_time, 
                "p_id": item.p_id, 
                "p_name": item.p_name,
                "p_desc": item.p_desc,
                "p_status": item.p_status,
                "p_creator": item.p_creator
            } for item in dt]
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/getlist', methods=['GET', 'POST'])
@login_required
def get_project_list():
    '''
    获取所有项目信息,带分页

    Args: 
        page: url params请求参数, 不传默认为1
        p_name: 项目名称查询
    return:
        {
            "errcode": 0,
            "errmsg": "SUCCESS",
            "res": {
                "next_page": 3,
                "page": 2,
                "pages": 4,
                "per_page": 10,
                "prev_num": 1,
                "project": [
                    {
                        "create_time": "Tue, 26 May 2020 17:30:32 GMT",
                        "p_d": "xzdylyh",
                        "p_desc": "这是项目描述，我最多支持150字符",
                        "p_id": 11,
                        "p_name": "我的第1个项目",
                        "p_status": 0
                    },
                    {
                        "create_time": "Tue, 26 May 2020 17:35:20 GMT",
                        "p_d": "xzdylyh",
                        "p_desc": "这是项目描述，我最多支持150字符",
                        "p_id": 12,
                        "p_name": "我的第1个项目",
                        "p_status": 0
                    }
                ],
                "total": 39
            }
        }      
    '''
    if request.method == 'POST':

        # 是否登录授权
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        # 请求url参数page
        page = request.json.get('page', 1)
        p_name = request.json.get('p_name', '')
        p_id = request.json.get('p_id', '')

        # 可按pid与name查询，pid优先
        if p_id:
            paginate = odb.query_per_paginate(Project, 'p_id', p_id, page=int(page))

        elif p_name:
            paginate = odb.query_per_paginate(Project, 'p_name', p_name, page=int(page))       
        else:
            paginate = odb.query_all_paginate(
                Project, 
                page=int(page)
            )

        # response数据组装
        res = {
            "prev_num": paginate.prev_num,
            "per_page": paginate.per_page,
            "pages": paginate.pages,
            "total": paginate.total,
            "page": paginate.page,
            "next_page": paginate.next_num,
            "project": [{
                "create_time": item.create_time, 
                "p_id": item.p_id, 
                "p_name": item.p_name,
                "p_desc": item.p_desc,
                "p_status": item.p_status,
                "p_creator": item.p_creator
            } for item in paginate.items]
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/suite/getAllList', methods=('GET', 'POST'))
@login_required
def get_all_suite_list():
    '''
    获取所有测试集

    Args:
        page: 当前页码，不传默认为1

    return:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": {
                "next_page": 2,
                "page": 1,
                "pages": 2,
                "per_page": 10,
                "prev_num": null,
                "project": [
                    {
                        "create_time": "Tue, 02 Jun 2020 17:06:50 GMT",
                        "p_creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 1
                    },
                    {
                        "create_time": "Tue, 02 Jun 2020 17:08:35 GMT",
                        "p_creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 2
                    }
                ],
                "total": 11
            }
        }
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        page = request.args.get('page', 1)

        # 分页展示
        paginate = odb.query_all_paginate(
            TestSuite, 
            page=int(page)
        )

        res = {
            "prev_num": paginate.prev_num,
            "per_page": paginate.per_page,
            "pages": paginate.pages,
            "total": paginate.total,
            "page": paginate.page,
            "next_page": paginate.next_num,
            "project": [{
                "create_time": item.create_time, 
                "sid": item.sid,
                "s_name": item.s_name,
                "p_id": item.p_id,
                "p_creator": item.p_creator
            } for item in paginate.items]
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/suite/getlistbyId', methods=('GET', 'POST'))
@login_required
def get_all_suite_by_pid():
    '''
    根据项目id获取，该项目下的所有测试集

    Args: params参数
        p_id: 项目ID

    Return:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": {
                "count": 10,
                "next_page": 2,
                "page": 1,
                "pages": 2,
                "per_page": 10,
                "prev_num": null,
                "suite": [
                    {
                        "create_time": "Tue, 02 Jun 2020 17:06:50 GMT",
                        "creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 1
                    },
                    {
                        "create_time": "Tue, 02 Jun 2020 17:08:35 GMT",
                        "creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 2
                    }
                ],
                "total": 11
            }
        }
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        pid = request.json['p_id']


  
        dt_lst = odb.query_per_all(
            TestSuite, 
            'p_id', 
            int(pid)
        )

        res = {
            "suite":[{
                "sid": sd.sid,
                "s_name": sd.s_name,
                "create_time": sd.create_time,
                "creator": sd.p_creator,
                "p_id": sd.p_id
            } for sd in dt_lst],
            "count": len(dt_lst)
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/suite/getlist', methods=('GET', 'POST'))
@login_required
def get_suite_by_pid():
    '''
    根据项目id获取，该项目下的所有测试集

    Args: params参数
        p_id: 项目ID
        page: 页码，不传默认为1

    Return:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": {
                "count": 10,
                "next_page": 2,
                "page": 1,
                "pages": 2,
                "per_page": 10,
                "prev_num": null,
                "suite": [
                    {
                        "create_time": "Tue, 02 Jun 2020 17:06:50 GMT",
                        "creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 1
                    },
                    {
                        "create_time": "Tue, 02 Jun 2020 17:08:35 GMT",
                        "creator": "xzdylyh",
                        "p_id": 2,
                        "s_name": "我的测试集",
                        "sid": 2
                    }
                ],
                "total": 11
            }
        }
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        pid = request.args.get('p_id', False)
        if not pid:
            return jsonify(Const.errcode('1002'))

        else:
            # 分页
            paginate = odb.query_per_paginate(
                TestSuite, 
                'p_id', 
                int(pid), 
                page=int(request.args.get('page', 1)),
            )

            res = {
                "prev_num": paginate.prev_num,
                "per_page": paginate.per_page,
                "pages": paginate.pages,
                "total": paginate.total,
                "page": paginate.page,
                "next_page": paginate.next_num,
                "suite":[{
                    "sid": sd.sid,
                    "s_name": sd.s_name,
                    "create_time": sd.create_time,
                    "creator": sd.p_creator,
                    "p_id": sd.p_id
                } for sd in paginate.items],
                "count": len(paginate.items)
            }
            return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/suite/create', methods=('GET', 'POST'))
@login_required
def create_suite():
    '''
    创建测试集

    Args: json
        s_name: 测试集名称
        project_id: 项目ID
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        req_args = request.json

        test_suite = TestSuite(
                req_args['s_name'], 
                g.user.username, 
                req_args['project_id'],
                req_args['s_desc']
        )
        # 新增测试集，同步更新项目状态
        odb.add(test_suite)
        odb.update(Project, 'p_id', req_args['project_id'], p_status=1)

        res = {
            "suite_id": test_suite.sid, 
            "suite_name": req_args['s_name'], 
            "description": req_args['s_desc'],
            "project_id": req_args['project_id'],
            "create_time": test_suite.create_time,
            "creator": test_suite.p_creator
        }


        return jsonify(Const.errcode('0', res=res))

    return abort(404)

@bp.route('/suite/getSuitebySid', methods=('GET', 'POST'))
@login_required
def get_suite_by_sid():
    '''
    根据sid获取测试集数据
    '''
    if request.method == 'POST':
        
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))
        
        sid = request.json['sid']
        dt = odb.query_per(TestSuite, 'sid', int(sid))

        res = {
            'sid': dt.sid,
            's_name': dt.s_name,
            's_desc': dt.s_desc
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)

@bp.route('/suite/delete', methods=('GET', 'POST'))
@login_required
def delete_suite():
    '''
    根据测试集ID，删除测试集

    Args: JSON
        sid: 测试集ID
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        s_id_lst = request.json

        del_res = []
        for sid in s_id_lst['sid']:

            dt = odb.delete(TestSuite, 'sid', int(sid))
            del_res.append({"sid": int(sid), "s_name": dt.s_name, "p_id": dt.p_id})

        res = {
            'suite': del_res
        }
        return jsonify(Const.errcode('0', res=res))

    
    return abort(404)


@bp.route('/suite/update', methods=['GET', 'POST'])
@login_required
def suite_update():
    '''
    更新测试集信息

    Args: JSON
        sid:测试集id

    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))
        
        req_data_json = request.json

        suite_dt = odb.update(
            TestSuite, 
            'sid', 
            int(req_data_json['sid']),
            s_name=req_data_json['s_name'],
            s_desc=req_data_json['s_desc']
        )

        res = {
            'suite': {
                "sid": suite_dt.sid,
                "new_s_name": suite_dt.s_name,
                "p_id": suite_dt.p_id
            }
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)