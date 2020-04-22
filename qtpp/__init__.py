import os

from flask import Flask
import setting
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
1、应用工厂
2、QTPPY是一个python包   
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(setting)
    
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'qtppy.sqlite'),
    # )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    '''
    db.init_app(app) # 将上述配置项初始化到flask-sqlachemy配置中并进行相关初始化
    db.create_all() # 初始化数据库，若数据库中没有相应的表，则创建表结构
    '''
    db.init_app(app) 
    db.create_all(app=app)


    # 导入注册蓝图
    from .views import auth
    app.register_blueprint(auth.bp)

    # 与验证蓝图不同，博客蓝图没有 url_prefix 。
    # 因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
    # 用例是 qtppy 的主要 功能，因此把用例索引作为主索引是合理的。
    from .views import case
    app.register_blueprint(case.bp)
    app.add_url_rule('/', endpoint='index')

    return app