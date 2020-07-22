from qtpp import db

class Variable(db.Model):
    """
    变量表
    """
    __tablename__ = 'variableglobal'
    vid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    uid = db.Column(
        db.Integer, 
        db.ForeignKey('user.uid', ondelete='CASCADE'), 
        comment='用户ID'
    )

    def __init__(self, name, value, uid):
        self.name = name
        self.value = value
        self.uid = uid


