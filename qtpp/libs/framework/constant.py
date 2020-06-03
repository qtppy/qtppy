class Const:
    '''
    请求结果定义
    '''
    # errcode list
    ERROR_DICT = {
        '0' : "success",
        '1001' : "尚未登录",
        '1002' : "参数错误",
        '1003' : "用户名或密码不正确"
    }


    # 请求模版.
    SUCCESS_DICT = {
        'errcode': 0,
        'errmsg': 'success',
    }

    @classmethod
    def errcode(cls, code, **kwargs):
        cls.SUCCESS_DICT['errcode'] = int(code)
        cls.SUCCESS_DICT['errmsg'] =  cls.ERROR_DICT[str(code)]

        # 取自定义key
        for key, value in kwargs.items():
            cls.SUCCESS_DICT[key] = value

        return cls.SUCCESS_DICT

    