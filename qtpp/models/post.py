from qtpp import db


# CREATE TABLE post (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   author_id INTEGER NOT NULL,
#   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   title TEXT NOT NULL,
#   body TEXT NOT NULL,
#   FOREIGN KEY (author_id) REFERENCES user (id)
# );

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(100), nullable=False)

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return '<Category %r>' % self.title