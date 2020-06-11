from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.models.case import CaseInterface
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

        odb.add(
            CaseInterface(
                para_json['name'],
                g.user.username,
                para_json['method'],
                para_json['url'],
                para_json['header'],
                para_json['body'],
                para_json['desc']
            )
        )

        res = {
            "name": para_json['name'],
            "desc": para_json['desc'],
            "creator": g.user.username
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)


@bp.route('/getcaselist', methods=['GET', 'POST'])
@login_required
def get_case_list():
    '''
    获取case信息
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
                    "id": val.c_id,
                    "headers": val.c_headers,
                    "body": val.c_body,
                    "creator": val.p_creator,
                    "createtime": val.create_time
                } for val in paginate.items
            ]
        }

        return jsonify(Const.errcode('0', res=res))

    return abort(404)
