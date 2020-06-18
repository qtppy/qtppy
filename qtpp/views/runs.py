from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.libs.framework.https import client
'''
用例蓝图与验证蓝图所使用的技术一样。
用例页面应当列出所有的case，允许已登录 用户创建用例，并允许创建者修改和删除用例。
'''
bp = Blueprint('run', __name__, url_prefix='/run')
odb = OperationDB()


@bp.route('/debug', methods=('GET', 'POST'))
@login_required
def debug():
  '''
  执行单个测试用例

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
      axios.post('/run/debug', params)

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

    json = request.json
    
    res = getattr(client, json['method'])(
      json['url']
    )

  #     return jsonify(Const.errcode('0')

  return abort(404)
