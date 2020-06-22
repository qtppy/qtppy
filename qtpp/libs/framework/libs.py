import os
import hashlib
from qtpp import setting

def parse_string_eval(string):
    '''
    解析字符串为原始类型

    Args: 
        string 要解析的字符串
    
    Example:
        string = '{"cno": "213847244982000189442601", "shop_id":"1429830612"}'
        ret =  parse_string_eval(string)
    
    Return:
        可以解析原始类型返回原始类型对象，否则返回原字符串对象
    '''
    try:
       parse_type = eval(string)
    except (SyntaxError, TypeError, ValueError, NameError):
        return string

    return parse_type


def is_parse_raw_type(string):
    '''
    解析字符串为原始类型

    Args:
        string 要解析的字符串

    Example:
        string = '{"cno": "213847244982000189442601", "shop_id":"1429830612"}'
        bool = is_parse_raw_type(string)
    
    Return:
        对象可以解析为原始类型，返回True,否则返回False
    '''
    try:
        parse_type = eval(string)
    except (SyntaxError, TypeError, ValueError, NameError):
        return False

    return True


def allowed_file(filename):
    '''
    判断文件后缀是否在列表中

    Args:
        filename 文件名称，带扩展名

    Example: 
        bool = allowed_file('test.csv')

    Return:
        True or False
    '''
    # 上传文件
    ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'txt', 'xls', 'xlsx', 'csv']

    return '.' in filename and filename.rsplit('.', 1)[-1] in setting.ALLOW_EXTENSIONS

def is_dirs_exist(forder):
    '''
    目录是否存在

    Args:
        forder 文件夹路径

    Example:
        bool = is_dirs_exist('/xxxx/xxxx')

    Return:
        True or False
    '''
    return False if not os.path.exists(forder) else True


def makedirs(forder):
    '''
    创建文件夹

    Args：
        forder 文件夹路径

    Example:
        bool = makedirs(/xxxx/xxx)

    Return:
        null
    '''
    if not is_dirs_exist(forder):
        os.makedirs(forder)

def md5_filename(filename):
    '''
    生成md5文件名

    Args:
        filename 文件名带扩展名
    
    Example:
        md5 = md5_filename('filename.csv')

    Return:
        md5 文件名
        8f60123d6e48c910d0e6ac8086a6032d.csv
    '''
    suffix =  os.path.splitext(filename)[1]

    return '{}{}'.format(
        hashlib.md5(filename.encode('utf-8')).hexdigest(), 
        suffix
    )