import time
import uuid
import hashlib
import base64
import random

class SYS:
    '''
    系统函数

    type: 
        1 常用函数
        2 加密函数
        3 随机函数
        4 四则运算
    '''
    function_get = [
        {
            "name": '截取字符串',
            "type": 1,
            "value": '例:${sys.substring("text", 0, 1)}'
        },
        {
            "name": '转大写',
            "type": 1,
            "value": '例:${sys.upper_case("text")}'
        },
        {
            "name": '转小写',
            "type": 1,
            "value": '例:${sys.lower_case("text")}'
        },
        {
            "name": '转小写',
            "type": 1,
            "value": '例:${sys.lower_case("text")}'
        },
        {
            "name": '时间戳',
            "type": 1,
            "value": '例:${sys.time_stamp(ms=True)}'
        },
        {
            "name": 'UUID1',
            "type": 1,
            "value": '例:${sys.uuid1()}'
        },
        {
            "name": '32位MD5',
            "type": 2,
            "value": '例:${sys.md5_32("text")}'
        },
        {
            "name": '16位MD5',
            "type": 2,
            "value": '例:${sys.md5_16("text")}'
        },
        {
            "name": 'MD5 Base64编码',
            "type": 2,
            "value": '例:${sys.md5_base64("text")}'
        },
        {
            "name": 'SHA1加密',
            "type": 2,
            "value": '例:${sys.sha1("text")}'
        },
        {
            "name": 'SHA1 256加密',
            "type": 2,
            "value": '例:${sys.sha1_256("text")}'
        },
        {
            "name": 'base64编码',
            "type": 2,
            "value": '例:${sys.base64("text")}'
        },
        {
            "name": '字符串随机',
            "type": 3,
            "value": '例:${sys.random_string(10)}'
        },
        {
            "name": '指定字符串随机',
            "type": 3,
            "value": '例:${sys.random_string(10, "abc")}'
        }
    ]

    @staticmethod
    def substring(text, start=0, end=1):
        '''
        截取字符串

        Args:
            text 原始字符串
            start 第几个位置开始,包含开始位置
            end 截取几个字符串，包含结尾
        
        Explame:
            ret = sys.substring("Thisisstring", 8, 2)
            retrun: tr

        Return: 
            截取字符串
        '''
        start = start -1 if start > 0 else start
        return text[start: start + end]

    @staticmethod
    def upper_case(text):
        '''
        转大写
        '''
        return str(text).upper()

    @staticmethod
    def lower_case(text):
        '''
        转小写
        '''
        return str(text).lower()

    @staticmethod
    def time_stamp(ses=True, ms=False):
        '''
        时间戳
        '''
        return int(time.time()) * 1000 if ms else int(time.time())

    @staticmethod
    def uuid1():
        '''
        uuid1
        '''
        return str(uuid.uuid1()).replace('-', '')
    
    @staticmethod
    def md5_32(text):
        '''
        md5 32位
        '''
        has = hashlib.md5(text.encode('utf8'))
        return has.hexdigest()

    @staticmethod
    def md5_16(text):
        '''
        md5 32位
        '''
        has = hashlib.md5(text.encode('utf8'))
        return has.hexdigest()[8: -8]

    @staticmethod
    def md5_base64(text):
        '''
        base64进行md5加密
        '''
        bs4 = str(base64.b64encode(text.encode("utf-8")), "utf-8")
        has = hashlib.md5(bs4.encode('utf8'))
        return has.hexdigest()

    @staticmethod
    def sha1(text):
        '''
        sha1加密
        '''
        sha1 = hashlib.sha1(text.encode('utf8'))
        return sha1.hexdigest()

    @staticmethod
    def sha1_256(text):
        '''
        sha1加密
        '''
        sha1 = hashlib.sha256(text.encode('utf8'))
        return sha1.hexdigest()

    @staticmethod
    def base64(text):
        '''
        base64编码
        '''
        bs4 = str(base64.b64encode(text.encode("utf-8")), "utf-8")
        return bs4

    @staticmethod
    def random_string(slen, string=''):
        '''
        按指定长度，生成随机字符串

        Args:
            slen int 10
        
        Example:
            ret = random_string(10)
            ret = random_string(10, 'abcd')

        Return:
            YOwdmLPWgj
        '''
        rand_val = 65
        temp = []

        for i in range(slen):
            if string != '':
                randString = random.randrange(0, len(string))
                rand_val = ord(string[randString])
            else:
                while True:
                    rand_val = random.randrange(65, 122)
                    if rand_val > 90 and rand_val < 97:
                        continue
                    break
            temp.append(chr(rand_val))
        return ''.join(temp)


if __name__ == "__main__":
    string = SYS.substring("Thisisstring", 8, 2)
    print(string)

    timestamp = SYS.time_stamp()
    print(timestamp)

    md51 = SYS.md5_16('aaaa')
    print(md51)

    md5base64 = SYS.md5_base64('bbbbb')
    print(md5base64)