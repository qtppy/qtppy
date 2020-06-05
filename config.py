'''
pip install mysql-connector
DRIVER: "mysqlconnector"
'''

from datetime import timedelta
# from redis import StrictRedis

class BaseConfig:
    
    # 调试信息
    DEBUG = False

    SECRET_KEY='dev'

    # 数据库信息
    DIALCT = 'mysql'
    DRIVER = "mysqlconnector"
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DBNAME = 'qtppdb'

    # 数据库URL
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DBNAME)
    
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    # 这需要额外的内存， 如果不必要的可以禁用它。
    # 没有此配置会导致警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False        

    # 控制台输出sql消息:True不输出，False输出,
    # SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True





# 开发环境配置
class DevConfig(BaseConfig):
    DEBUG = True

# 测试环境配置
class TestConfig(BaseConfig):
    SQLALCHEMY_ECHO = False

# 线上环境配置
class ProConfig(BaseConfig):
    pass


# 统一访问入口
config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'pro': ProConfig,
}