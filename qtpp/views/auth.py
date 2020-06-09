import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)
from werkzeug.security import check_password_hash, generate_password_hash


from qtpp import db
from qtpp.libs.framework.operate_db import OperationDB
from qtpp.libs.framework.constant import Const

from qtpp.models.user import User

'''
这里创建了一个名称为 'auth' 的 Blueprint 。和应用对象一样， 
蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 
url_prefix 会添加到所有与该蓝图关联的 URL 前面。
'''
bp = Blueprint('auth', __name__, url_prefix='/auth')
odb = OperationDB()

''' 
认证蓝图将包括注册新用户、登录和注销视图。
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    当用访问 /auth/register URL 时， register 视图会返回用于填写注册 内容的表单的 HTML 。
    当用户提交表单时，视图会验证表单内容，然后要么再次 显示表单并显示一个出错信息，
    要么创建新用户并显示登录页面。
    '''
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        # 带有 ? 占位符 的 SQL 查询语句。占位符可以代替后面的元组参数中相应的值。
        # 使用占位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击 。
        # fetchone() 根据查询返回一个记录行。 如果查询没有结果，则返回 None 。
        # 后面还用到 fetchall() ，它返回包括所有结果的列表。
        # 使用 generate_password_hash() 生成安全的哈希值并储存 到数据库中。
        #  url_for() 根据登录视图的名称生成相应的 URL

        
        if not (username and password) :
            return jsonify(Const.errcode('1004'))

        if odb.query_per(User, 'username', username) is not None:
            return jsonify(Const.errcode('1005', res={"username": username}))


        odb.add(User(username, generate_password_hash(password)))

        return jsonify(Const.errcode('0', res={"username": username}))

    return abort(404)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        error = None

        user = odb.query_per(User, 'username', username)

        # check_password_hash() 以相同的方式哈希提交的 密码并安全的比较哈希值。
        # 如果匹配成功，那么密码就是正确的。
        # session 是一个 dict ，它用于储存横跨请求的值。
        # 当验证 成功后，用户的 id 被储存于一个新的会话中。
        # 会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它。 
        # Flask 会安全对数据进行 签名 以防数据被篡改。

        if (user is None) or (not check_password_hash(user.password, password)):
            return jsonify(Const.errcode('1003'))

        if error is None:
            session.clear()
            session['user_id'] = user.uid
            session['user_name'] = user.username

            res = {
                "user_id": user.uid,
                "name": user.username
            }

            return jsonify(Const.errcode('0', res=res))

        # flash(error)

    return abort(404)


'''
bp.before_app_request() 注册一个 在视图函数之前运行的函数，不论其 URL 是什么。 
load_logged_in_user 检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，
然后储存在 g.user 中。 g.user 的持续时间比请求要长。 如果没有用户 id ，或者 id 不存在，
那么 g.user 将会是 None 。
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = odb.query_per(User, 'uid', user_id)


'''
注销的时候需要把用户 id 从 session 中移除。 
然后 load_logged_in_user 就不会在后继请求中载入用户了。
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


'''
用户登录以后才能创建、编辑和删除。
在每个视图中可以使用 装饰器 来完成这个工作。
装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。
新的函数检查用户 是否已载入。如果已载入，那么就继续正常执行原视图，
否则就重定向到登录页面。 我们会在应用视图中使用这个装饰器。
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view