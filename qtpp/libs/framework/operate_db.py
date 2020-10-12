from qtpp import db

class OperationDB:
    """
    必须和表中用同一个db对象，否则增加数据后，查询会有问题：查不到数据
    """
    def __init__(self):
        self.db = db

    def add(self, obj):
        '''
        根据据模型对象，insert数据
        '''
        self.db.session.add(obj)
        self.db.session.commit()


    def query_all(self, table_class):
        '''
        查询模型下所有数据
        '''
        all_data = table_class.query.all()
        return all_data


    def query_all_paginate(self, table_class, page=1, per_page=10):
        '''
        查询分页数据
        page：当前页
        per_page: 分页条数
        '''
        paginate = table_class.query.paginate(page=page, per_page=per_page, error_out=False)

        return paginate


    def query_per(self, table_class, k, v):
        '''
        根据条件，查询模型下第一条数据
        '''
        k = getattr(table_class, k)
        data = table_class.query.filter(k == v).first()
        return data

    def query_per_and_or_(self, table_class, obj):
        '''
        根据条件，查询模型下第一条数据
        '''
        k = getattr(table_class, k)
        data = table_class.query.filter(obj)
        return data

    def query_per_all(self, table_class, k, v):
        '''
        根据条件查询所有数据
        '''
        k = getattr(table_class, k)
        data = table_class.query.filter(k == v).all()
        return data

    def query_per_paginates(self, table_class, page=1, per_page=10, **kwargs):
        '''
        根据条件查询并分页
        page: 当前页
        pre_page: 分页显示条数
        task_filter
        '''
        # k = getattr(table_class, k)
        paginate = table_class.query.filter(*kwargs['task_filter']).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        return paginate


    def query_per_paginate(self, table_class, k, v, page=1, per_page=10):
        '''
        根据条件查询并分页
        page: 当前页
        pre_page: 分页显示条数
        '''
        k = getattr(table_class, k)
        paginate = table_class.query.filter(k == v).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        return paginate


    def update(self, table_class, k, v, **kwargs):
        '''
        根据条件更新数据
        '''
        result = self.query_per(table_class, k, v)

        for k, v in kwargs.items():
            setattr(result, k, v)
        self.db.session.commit()
        return result

    def rollback(self):
        '''回退'''
        self.db.rollback()


    def delete(self, table_class, k, v):
        '''
        根据条件删除数据
        '''
        result = self.query_per(table_class, k, v)
        if result:
            self.db.session.delete(result)
            self.db.session.commit()
        return result