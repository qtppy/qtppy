from datetime import timedelta
# from redis import StrictRedis

class BaseConfig:
    
    # 调试信息
    DEBUG = True
    SECRET_KEY='dev'

    DB_URI = r"sqlite:///D:\test_project\project\qtppy\instance\qtppy.sqlite"

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


# 开发环境配置
class DevConfig(BaseConfig):
    pass

# 测试环境配置
class TestConfig(BaseConfig):
    pass

# 线上环境配置
class ProConfig(BaseConfig):
    DEBUG = False


# 统一访问入口
config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'pro': ProConfig,
}