class BY_C:
    '''
    断言条件
    '''
    GREATER_THEN = 0 # 大于 greater then
    GREATER_THEN_OR_EQUAL = 1 # 大于等于 is equal or greater then
    LESS_THAN = 2 # 小于 less than
    LESS_THAN_OR_EQUAL_TO = 3 # 小于等于 less than or equal to
    EQUAL_TO = 4 # 等于 equal to
    UNEQUAL_TO = 5 # 不等于 unequal to
    CONTAIN = 6 # 包含 contain
    DO_NOT_CONTAIN = 7 # 不包含 do not contain
    BELONG_TO = 8 # 属于belong to
    NOT_BELONG_TO = 9 # 不属于 not belong to
    EXIST = 10 # 存在 exist
    NOT_EXIST = 11 # 不存在 not exist
    REGEX_MATCH = 12  #正则匹配  regex match

    
class BY_T:
    '''
    断言类型
    '''
    RES_HEADER = 0 # 响应header
    RES_STATUS = 1 # 响应状态码
    RES_BODY = 2 # 响应body
    REFER = 3 # 出参


class BY_M:
    '''
    请求method映射关系
    '''
    @staticmethod
    def map(val):
        method = {
            "GET": 0,
            "POST": 1,
            "PUT": 2,
            "PATCH": 3,
            "DELETE": 4,
            "COPY": 5,
            "HEAD": 6,
            "OPTIONS": 7,
            "LINK": 8,
            "UNLINK": 9,
            "PURGE": 10,
            "LOCK": 11,
            "UNLOCK": 12,
            "PROPFIND": 13,
            "VIEW": 14
        }
        for key, value in method.items():
            if value == int(val):
                return key



