import os

from flask import Flask
from config import config_dict
from qtpp.exts import db

'''
1、应用工厂
2、QTPPY是一个python包   
'''
def create_app(config_name='dev'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)


    # 根据传入的环境名称获取配置
    config = config_dict.get(config_name)

    # 加载配置A
    app.config.from_object(config)

    '''
    db.init_app(app) # 将上述配置项初始化到flask-sqlachemy配置中并进行相关初始化
    '''
    db.init_app(app) 

    # 导入注册蓝图
    from .views import auth
    app.register_blueprint(auth.bp)

    # 与验证蓝图不同，博客蓝图没有 url_prefix 。
    # 因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
    # 用例是 qtppy 的主要 功能，因此把用例索引作为主索引是合理的。
    from .views import case
    app.register_blueprint(case.bp)
    app.add_url_rule('/', endpoint='index')

    #导入项目蓝图
    from .views import project
    app.register_blueprint(project.bp)

    return app