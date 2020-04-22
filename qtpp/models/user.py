from qtpp import db
# CREATE TABLE user (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   username TEXT UNIQUE NOT NULL,
#   password TEXT NOT NULL
# );
class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(16), nullable=False)

    def __init__(self,username,password):
        self.username  = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username