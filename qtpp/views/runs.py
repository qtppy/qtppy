import os
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from qtpp.views.auth import login_required

from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const
from qtpp.libs.framework.https import client
from qtpp.libs.framework.asserts import BY_HOW
from qtpp.libs.framework.responseResult import OutPutParam
from qtpp.libs.framework import libs
from qtpp import setting
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

    req_json = request.json

    '''
    Var:
        data_dict: dict类型data数据组合
        files_list: form-data类型时files文件
        how: form-data; x-xxx-form-urlencoded; raw类型
        url: 请求url地址
        headers:请求头信息
    '''
    body = req_json['body']['body']
    data_dict = body['data']
    files_list = body['files']
    how = req_json['body']['how']
    url = req_json['url']
    headers = req_json['header']
    method = req_json['method']
    outParam_list = req_json['outParam']

    data_dict, files, headers = client.data_to_parse(data_dict, files_list, how, headers)

    response = getattr(client, method)(
      url,
      data=data_dict,
      headers=headers,
      files=files
    )

    # 出参内容
    ret_out_param = []
    for param in outParam_list:
        ret_out_param.append(
            OutPutParam.get_output_variable_value(
                param['source'],
                param['name'],
                response,
                param['exp'],
                param['match']
            )
        )

    content_type = response.headers.get("Content-Type", '')

    # 根据响应头，如果content-type类型是json返回json格式，否则返回text格式
    res_data = response.json() if 'json' in content_type else response.text

    res_dt = {
        "headers": dict(response.headers),
        "url": response.url,
        "data": res_data,
        "cookies": libs.dict_from_cookiejar(
            response.cookies
        ),
        "ok": response.ok,
        "encoding": response.encoding,
        "reason": response.reason,
        "status_code": response.status_code,
        "elapsed": int(response.elapsed.total_seconds() * 1000),
        "out_param_list": ret_out_param
    }

    return jsonify(Const.errcode('0', res=res_dt))


  return abort(404)
