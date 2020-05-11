from qtpp import db

class OperationDB:
    """
    必须和表中用同一个db对象，否则增加数据后，查询会有问题：查不到数据
    """
    def __init__(self):
        self.db = db

    def add(self, obj):
        self.db.session.add(obj)
        self.db.session.commit()

    def query_all(self, table_class):
        all_data = table_class.query.all()
        return all_data

    def query_per(self, table_class, k, v):
        k = getattr(table_class, k)
        data = table_class.query.filter(k == v).first()
        return data

    def update(self, table_class, k, v, **kwargs):
        result = self.query_per(table_class, k, v)
        for g, m in kwargs.items():
            setattr(result, g, m)
        self.db.session.commit()

    def delete(self, table_class, k, v):
        result = self.query_per(table_class, k, v)
        self.db.session.delete(result)
        self.db.session.commit()
        return result