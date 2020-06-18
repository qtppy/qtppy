class SYS:
    '''
    系统函数
    '''

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
    

if __name__ == "__main__":
    string = sys.substring("Thisisstring", 8, 2)
    print(string)