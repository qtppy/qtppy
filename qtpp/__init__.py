import os

from flask import Flask

'''
1、应用工厂
2、QTPPY是一个python包   
'''
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(DebugMode)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'qtppy.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 初始化db
    from . import db
    db.init_app(app)

    # 导入注册蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    # 与验证蓝图不同，博客蓝图没有 url_prefix 。
    # 因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
    # 用例是 qtppy 的主要 功能，因此把用例索引作为主索引是合理的。
    from . import case
    app.register_blueprint(case.bp)
    app.add_url_rule('/', endpoint='index')

    return app