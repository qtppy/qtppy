from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.libs.framework import libs
from qtpp import setting
from qtpp.models.case import (
    CaseInterface, 
    Case_Assert, 
    Case_Result
)
import os
'''
用例蓝图与验证蓝图所使用的技术一样。
用例页面应当列出所有的case，允许已登录 用户创建用例，并允许创建者修改和删除用例。
'''
bp = Blueprint('case', __name__, url_prefix='/case')
odb = OperationDB()


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    '''
    创建测试用例

    Args:
        name 用例名称
        method 请求方法
        url 请求url地址
        header 请求头部信息
        body 请求体
        desc 用例描述信息
    
    Method: POST

    Fmt: JSON

    Example: 
        axios.post('/case/create', params)

    Returns:
        {
            "name": "测试用例名称",
            "desc": "测试用例描述",
            "creator": "admin"
        }
    '''
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        para_json = request.json

        case_object = CaseInterface(
                para_json['name'],
                g.user.username,
                para_json['method'],
                para_json['url'],
                para_json['header'],
                para_json['body'],
                para_json['desc']
            )

        odb.add(case_object)

        res = {
            "name": case_object.c_name,
            "desc": case_object.c_desc,
            "creator": g.user.username,
            "c_id": case_object.c_id
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/getcaselist', methods=['GET', 'POST'])
@login_required
def get_case_list():
    '''
    获取case信息

    Args:
        page 当前页
        name 按名称获取用例，可选

    Method: POST

    Fmt: JSON

    Example:
        axios.post('/case/getcaselist', params)

    Returns:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": {
                "case": [
                    {
                        "body": "{}",
                        "createtime": "Thu, 11 Jun 2020 14:05:03 GMT",
                        "creator": "admin",
                        "desc": "",
                        "headers": "{}",
                        "id": 1,
                        "method": "post",
                        "name": "/user/account",
                        "url": "http://api.xxxx.acewill.net/user/account"
                    },
                    {
                        "body": "{}",
                        "createtime": "Thu, 11 Jun 2020 14:19:20 GMT",
                        "creator": "admin",
                        "desc": "'这是一个测试用例描述'",
                        "headers": "{}",
                        "id": 2,
                        "method": "post",
                        "name": "/user/account",
                        "url": "http://api.xxxx.acewill.net/user/account"
                    }
                ],
                "next_num": null,
                "page": 1,
                "pages": 1,
                "per_page": 10,
                "prev_num": null,
                "total": 2
            }
        }
    '''
    if request.method == "POST":
        
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        page = request.json.get('page', 1)
        name = request.json.get('name', '')

        if name == '':
            paginate = odb.query_all_paginate(
                CaseInterface,
                page=page
            )
        else:
            paginate = odb.query_per_paginate(
                CaseInterface,
                "c_name",
                name,
                page=int(page)
            )

        res = {
            "page": paginate.page,
            "pages": paginate.pages,
            "next_num": paginate.next_num,
            "per_page": paginate.per_page,
            "prev_num": paginate.prev_num,
            "total": paginate.total,
            "case": [
                {
                    "url": val.c_url,
                    "name": val.c_name,
                    "desc": val.c_desc,
                    "method": val.c_method,
                    "cid": val.c_id,
                    "headers": val.c_headers,
                    "body": val.c_body,
                    "creator": val.p_creator,
                    "createtime": val.create_time
                } for val in paginate.items
            ]
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_case():
    '''
    根据用例ID，删除case

    Args:
        id [1,2,3] 测试用例id

    Method: POST

    Fmt: JSON

    Example:
        axios.post('/case/delete', params)
    
    Returns:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": [
                {
                    "desc": "",
                    "id": 1,
                    "name": "/user/account"
                }
            ]
        }
    '''
    if request.method == 'POST':

        # 验证授权
        if not g.user.uid:
            return jsonify(Const.errcode('1004'))
        
        id_lst = request.json['id']

        # 循环删除case
        res = []
        for id in id_lst:
            dt = odb.delete(CaseInterface, 'c_id', id)
            res.append(
                {
                    "name": dt.c_name,
                    "desc": dt.c_desc,
                    "id": dt.c_id
                }
            )
        return jsonify(Const.errcode('0', res=res))

    return abort(404)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    '''
    根据用例ID，删除case

    Args:
        id [1,2,3] 测试用例id

    Method: POST

    Fmt: JSON

    Example:
        axios.post('/case/delete', params)
    
    Returns:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": [
                {
                    "desc": "",
                    "id": 1,
                    "name": "/user/account"
                }
            ]
        }
    '''
    if request.method == 'POST':

        # 验证授权
        if not g.user.uid:
            return jsonify(Const.errcode('1004'))
        
        file = request.files['file']

        res = {}

        # 文件是否在允许的类型内
        if file and libs.allowed_file(file.filename):
            folder = os.path.join(
                setting.UPLOAD_FOLDER, 
                str(g.user.uid) + g.user.username
            )
            libs.makedirs(folder)

            name = libs.md5_filename(file.filename)

            path = os.path.join(folder, name)
            
            if not libs.is_dirs_exist(path):
                file.save(path)
                res['filename'] = name

                return jsonify(Const.errcode('0', res=res))
            else:
                return jsonify(Const.errcode('1006'))

        return jsonify(Const.errcode('1005'))

    return abort(404)
