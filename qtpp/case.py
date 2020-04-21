from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from qtpp.auth import login_required
from qtpp.db import get_db

'''
用例蓝图与验证蓝图所使用的技术一样。
用例页面应当列出所有的case，允许已登录 用户创建用例，并允许创建者修改和删除用例。
'''
bp = Blueprint('case', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('case/index.html', posts=posts)


'''
create 视图与 register 视图原理相同。
要么显示表单，要么发送内容 已通过验证且内容已加入数据库，或者显示一个出错信息。
先前写的 login_required 装饰器用在了博客视图中，这样用户必须登录以后 才能访问这些视图，
否则会被重定向到登录页面。
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


'''
update 和 delete 视图都需要通过 id 来获取一个 post ，并且 检查作者与登录用户是否一致。
为避免重复代码，可以写一个函数来获取 post ， 并在每个视图中调用它。
abort() 会引发一个特殊的异常，返回一个 HTTP 状态码。它有一个可选参数， 
用于显示出错信息，若不使用该参数则返回缺省出错信息。 
404 表示“未找到”， 403 代表“禁止访问”。（ 401 表示“未授权”，但是我们重定向到登录 页面来代替返回这个状态码）
check_author 参数的作用是函数可以用于在不检查作者的情况下获取一个 post 。
这主要用于显示一个独立的用例页面的情况，因为这时用户是谁没有关系， 用户不会修改用例。
'''
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('case.index'))

    return render_template('case/update.html', post=post)


'''
删除视图没有自己的模板。删除按钮已包含于 update.html 之中，该按钮指向 /<id>/delete URL 。
既然没有模板，该视图只处理 POST 方法并重定向到 index 视图。
'''
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('case.index'))