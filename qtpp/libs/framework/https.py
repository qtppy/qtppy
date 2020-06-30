import os
import requests
import urllib
from qtpp.libs.framework.asserts import BY_HOW
from qtpp.libs.framework import libs
from qtpp import setting
from flask import g

class client:
    @staticmethod
    def POST(url, data=None, json=None, **kwargs):
        response = requests.post(url, data=data, json=json, **kwargs)
        return response

    @staticmethod
    def GET(url, params=None):
        response = requests.get(url, params=params, **kwargs)
        return response

    @staticmethod
    def urlencoded(values):
        return urllib.parse.urlencode(values)

    @staticmethod
    def data_to_parse(payload, files_list, how, headers):
        """
        转换数据类型

        Args:
            payload 请求数据
            files_list []
            how 请求方式
            headers {} 请求头

        return:
            data 转换后的请求数据
            files [] 请求文件
            headers {} 请求头
        """

        files = []
        data = {}
        # how等于2，form-data格式
        if how == BY_HOW.FORM_DATA:
            
            # form-data格式所有key的value都转成字符串
            for key, value in payload.items():
                data[key] = repr(value) if not isinstance(value, str) else value

            if files_list:
                # 有需要上传的文件
                upload_folder = os.path.join(
                    setting.UPLOAD_FOLDER, 
                    str(g.user.uid) + g.user.username
                )

                files = [
                    (
                        fl['file']['key'], 
                        open(
                            os.path.join(upload_folder, fl['file']['name']), 
                            'rb'
                        )
                    ) 
                    for fl in files_list
                ]

        # x-www-form-urlencoded
        if how == BY_HOW.X_WWW_FORM_URLENCODED:

            headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = client.urlencoded(payload)

        return data, files, headers