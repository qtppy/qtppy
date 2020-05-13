from datetime import timedelta
# from redis import StrictRedis

class BaseConfig:
    
    # 调试信息
    DEBUG = True
    SECRET_KEY='dev'

    DIALCT = 'mysql'
    DRIVER = "pymysql"
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DBNAME = 'qtppdb'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DBNAME)
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False        #没有此配置会导致警告

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# 开发环境配置
class DevConfig(BaseConfig):
    pass

# 测试环境配置
class TestConfig(BaseConfig):
    SQLALCHEMY_ECHO = False

# 线上环境配置
class ProConfig(BaseConfig):
    DEBUG = False


# 统一访问入口
config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'pro': ProConfig,
}