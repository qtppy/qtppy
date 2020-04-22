
# session key
SECRET_KEY='dev'


# 数据库配置
# HOST = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'flask2'
# USERNAME = 'root'
# PASSWORD = '123456'

DB_URI = r"sqlite:///D:\test_project\project\qtppy\instance\qtppy.sqlite"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True


# 模式
DEBUG = True