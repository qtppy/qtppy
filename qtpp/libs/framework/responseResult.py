from .asserts import BY_O, BY_C, BY_T
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
            result['var_value'] = OutPutParam._parse_exp_json(exp, response.json())

        # headers param_type等于2，exp header dict解析
        if int(param_type) == BY_O.HEADER_K_V:
            result['var_value'] = response.headers.get(exp, 'key Error!')

        # cookies param_type等于3，exp cookie dict解析
        if int(param_type) == BY_O.COOKIE_K_V:
            result['var_value'] = libs.dict_from_cookiejar(
                response.cookies
            ).get(exp, 'Key Error!')

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


class Check_Result:
    '''
    断言结果
    '''
    @staticmethod
    def get_check_result(**kwargs):
        # 响应header
        if kwargs['checkType'] == BY_T.RES_HEADER:
            # 转换value
            check_obj = Check_Result.convert_type(
                kwargs['response'].headers.get(kwargs['check_object'], 0)
            )
            result = Check_Result.__check_condition(
                kwargs['checkType'],
                check_obj,
                kwargs['chk_cd'],
                kwargs['check_content']
            )
        
        # 响应状态码
        if kwargs['checkType'] == BY_T.RES_STATUS:
            check_obj = str(kwargs['response'].status_code)
            result = Check_Result.__check_condition(
                kwargs['checkType'],
                check_obj,
                kwargs['chk_cd'],
                kwargs['check_content']                
            )
        
        # 响应body
        if kwargs['checkType'] == BY_T.RES_BODY:
            check_obj = kwargs['response'].text
            result = Check_Result.__check_condition(
                kwargs['checkType'],
                check_obj,
                kwargs['chk_cd'],
                kwargs['check_content']
            )

        # 出参断言
        if kwargs['checkType'] == BY_T.REFER:
            check_obj = kwargs['REFER']
            result = Check_Result.__check_condition(
                kwargs['checkType'],
                check_obj,
                kwargs['chk_cd'],
                kwargs['check_content']
            )

        return result

            
    @staticmethod
    def __check_condition(check_type, check_object, chk_cd, check_content, **kwargs):
        ''''''
        result = {
                    "check_object": check_object,
                    "check_content": check_content,
                    "check_result": ''
                }
        check_content = Check_Result.convert_type(check_content)
        check_object = Check_Result.convert_type(check_object)
        result['check_result'] = (True if check_object > check_content else False) \
            if chk_cd == BY_C.GREATER_THEN else result['check_result']

        result['check_result'] = (True if check_object == check_content else False) \
            if chk_cd == BY_C.EQUAL_TO else result['check_result']

        result['check_result'] = (True if check_object < check_content else False) \
            if chk_cd == BY_C.LESS_THAN else result['check_result']

        result['check_result'] = (True if check_object != check_content else False) \
            if chk_cd == BY_C.UNEQUAL_TO else result['check_result']

        result['check_result'] = (True if check_content in check_object else False) \
            if chk_cd == BY_C.CONTAIN else result['check_result']
        result['check_result'] = (True if check_content not in str(check_object) else False) \
            if chk_cd == BY_C.DO_NOT_CONTAIN else result['check_result']
        return result  

    @staticmethod
    def convert_type(string):
        try:
            return int(string)
        except:
            try:
                return float(string)
            except:
                string = str(string).replace(' ', '')
                return string
            