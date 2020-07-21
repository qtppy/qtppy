from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.libs.framework import libs
from qtpp.libs.framework.sysfunc import SYS
from qtpp import setting
from qtpp.models.var import (
    Variable
)
import os

'''
用例蓝图与验证蓝图所使用的技术一样。
用例页面应当列出所有的case，允许已登录 用户创建用例，并允许创建者修改和删除用例。
'''
bp = Blueprint('var', __name__, url_prefix='/var')
odb = OperationDB()

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    '''
    增加全局变量

    Args:
        name 变量名称
        value 变量值
    
    Example:
        http://127.0.0.1:5000/var/add

    Return: JSON
        {
            'vid': 1,
            'name': 'name',
            'value': 'value',
            'uid': 1
        }
    '''
    if request.method == 'POST':
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))
        
        name = request.json['name']
        value = request.json['value']

        var_table = Variable(
                name,
                value,
                int(g.user.uid)
            )
        odb.add(var_table)

        res = {
            'vid': var_table.vid,
            'name': var_table.name,
            'value': var_table.value,
            'uid': var_table.uid
        }

        return jsonify(Const.errcode('0', res=res))
    return abort(404)


@bp.route('/getVarByUid', methods=('GET', 'POST'))
@login_required
def get_var():
    '''
    根据用户uid，获取全局变量

    Args: None

    Explame:
        http://127.0.0.1:5000/var/getVarByUid

    Return:
        {
            "errcode": 0,
            "errmsg": "success",
            "res": [
                {
                    "name": "name1",
                    "uid": 1,
                    "value": "value2",
                    "vid": 1
                }
            ]
        }
    '''
    if request.method == 'POST':
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))
        
        result = odb.query_per_all(Variable, 'uid', int(g.user.uid))

        res = [
            {'vid': obj.vid,
            'name': obj.name,
            'value': obj.value,
            'uid': obj.uid} for obj in result
        ]
        return jsonify(
            Const.errcode('0', res=res)
        )

    return abort(404)


@bp.route('/getSystemFunc', methods=['GET', 'POST'])
@login_required
def get_system_function():
    '''
    获取系统函数
    '''
    if request.method == 'POST':
        if not g.user.uid:
            return jsonify(Const.errcode('1001'))
        
        res = SYS.function_get

        return jsonify(Const.errcode('0', res=res))


    return abort(404)