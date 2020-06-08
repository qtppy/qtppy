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

'''
create 视图与 register 视图原理相同。
要么显示表单，要么发送内容 已通过验证且内容已加入数据库，或者显示一个出错信息。
先前写的 login_required 装饰器用在了博客视图中，这样用户必须登录以后 才能访问这些视图，
否则会被重定向到登录页面。
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        if not g.user.uid:
            return jsonify(Const.errcode('1001'))

        para_json = request.json

        odb.add(
            CaseInterface(
                para_json['name'],
                g.user.name,
                para_json['method'],
                para_json['url'],
                para_json['header'],
                para_json['body']
            )
        )

        res = {
            "name": para_json['name'],
            "creator": g.user.name 
        }
        return jsonify(Const.errcode('0', res=res))

    return abort(404)
