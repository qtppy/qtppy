from .asserts import BY_O
import re
from qtpp.libs.framework import libs

class OutPutParam:
    '''
    输出参数
    '''
    def get_output_variable_value(param_type, var_name, response, exp, match=0):
        '''
        获取出参变量，并返回list

        Args:
            param_type 出参类型
                BODY_TEXT = 0
                BODY_JSON = 1
                HEADER_K_V = 2
                COOKIE_K_V = 3
                STATUS_CODE = 4
            var_name 出参变量名
            response 请求响应对象
            exp 解析表达式
            match 第几个匹配
        
        Example:
            ret = get_output_variable_value(param_type, var_name, response, exp, match=0)

        Return:
            [var, var] 参数变量
        '''
        result = {"var_name" : var_name, "var_value": ''}


        # body文本 param_type等于0，exp进行正则匹配
        if int(param_type) == BY_O.BODY_TEXT:
            body_text = response.text
            # 正则匹配
            pattern = re.compile(exp)
            result_match = pattern.findall(body_text)
            result['var_value'] = result_match if len(result_match) < 1 else result_match[match]

        # body json param_type等于1，exp json解析
        if int(param_type) == BY_O.BODY_JSON:
            result['var_value'] = _parse_exp_json(exp, response.json())

        # headers param_type等于2，exp header dict解析
        if int(param_type) == BY_O.HEADER_K_V:
            result['var_value'] = response.headers[exp]

        # cookies param_type等于3，exp cookie dict解析
        if int(param_type) == BY_O.COOKIE_K_V:
            result['var_value'] = libs.dict_from_cookiejar(
                response.cookies
            )[exp]

        # status_code param_type等于4, 请求状态status_code
        if int(param_type) == BY_O.STATUS_CODE:
            result['var_value'] = response.status_code

        return result


def _parse_exp_json(exp_string, result):
    '''
    解析，解析表达式

    Args:
        exp_string result.errcode
        result 代表response.json

    Example:

        result = {
            "errcode":0,
            "errmsg":["测试1", {"name": [1, {"ak": 47}, 3]}]
        }

        exp_string = "result.errmsg[1].name[1].ak"       
    '''
    exp_string = exp_string.split('.')
    exp_string.pop(0)
    exp_string = '.'.join(exp_string)

    explist = "result['{}".format(exp_string.replace("[", "'][").replace(".", "']['"))

    explist = explist if ']' in explist[-1:] else explist + "']"

    return eval(explist)



        