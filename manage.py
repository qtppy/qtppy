'''
    # 对数据库的操作
    python manage.py db init
    python manage.py db migrate
    python manage.pydb upgrade

    # 启动项目
    python manage.py runserver
'''

from flask_script import Manager
from flask_migrate import Migrate ,MigrateCommand

from qtpp import create_app
from qtpp.exts import db



app = create_app('dev')

manager = Manager(app)

migrate = Migrate(app, db)

# 增加命令db字符串，为命令行执行时的基础命令，可加参数
manager.add_command('db', MigrateCommand)



@manager.command
def runserver():
    """启动服务"""
    print("renserver")
    app.run()


if __name__ == '__main__':
    manager.run()
