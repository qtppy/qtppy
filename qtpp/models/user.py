from qtpp import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username  = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


