'''
coverage run -m pytest --capture=no

or

coverage run -m pytest -s

----------------------------------------------------------
-m参数加标记，可以执行测试用例加@pytest.mark.update标记的用例
coverage run -m pytest -s -m update 
'''
import pytest


def create_project(client, auth):
    '''
    创建项目功能函数
    return: json示例

    "res":{
        "project_name": "我的第N+1个项目“,
        "p_id": 1
    }

    '''
    # 创建项目
    auth.login()
    res = client.post(
        '/project/create',
        json={"name": "我的第N个项目"}
    )

    print('\n/project/create :{}'.format(res.json['res']))

    return res.json if "N" in res.json['res']['project_name'] else False



'''
/project/create 创建项目
'''
@pytest.mark.create
def test_create_project(client, auth):
    '''
    desc:创建项目测试用例
    assert: 创建成功接口会返回json串，其中包含项目名称，此处用项目名称断言。
    return: json示例
        {
            "errcode": 0,
            "errmsg": "创建项目成功",
            "res":{
                "project_name": "我的第N+1个项目“,
                "p_id": 1
            }
        }
    '''
    p_id_lst = []
    auth.login()
    for _ in range(2):
        res = client.post(
            '/project/create',
            json={"name": "我的第N个项目"}
        )
        

        assert_result_bool = "N" in res.json['res']['project_name']
        p_id_lst.append(int(res.json['res']['p_id'])) if assert_result_bool else False

        assert assert_result_bool

    print('\n/project/create 新创建项目ID:{}'.format(p_id_lst))



'''
/project/delete 删除项目
'''
@pytest.mark.delete
def test_delete_project(client, auth):
    '''
    删除项目测试函数
    return: json示例
        {
            "errcode": 0,
            "errmsg": "删除成功",
            "res":{
                "project": [
                    {
                        "p_id": 1,
                        "p_name": "我的第1个项目"
                    }，
                    {
                        "p_id": 2,
                        "p_name": "我的第2个项目"
                    }
                ]
            }
        }
    '''
    # 创建项目
    res_project = create_project(client, auth)

    # 级联删除项目
    res = client.post(
        '/project/delete',
        json={'p_id': [res_project['res']['p_id']]}
    )

    print('/project/delete : {}'.format(res.json))
    assert res_project['res']['p_id'] in [pid_dict['p_id'] for pid_dict in res.json['res']['project']]


'''
/project/update根据项目ID更新项目信息
'''
@pytest.mark.update
def test_update_project(client, auth):
    '''
    根据项目ID更新项目信息
    return: json示例
    '''
    new_name = '我更新了项目名称'

    # 创建项目
    res_project = create_project(client, auth)

    res = client.post(
        '/project/update?p_id=%d&name=%s' % (res_project['res']['p_id'], new_name),
    )
    print('/project/update : {}'.format(res.json))

    assert new_name == res.json['res']['project']['new_p_name']


'''
/project/getall/1 or 2获取所有项目或2项目下所有测试集
'''
@pytest.mark.query
@pytest.mark.parametrize("url_index", [1,2])
def test_query_project_or_suite(client, auth, url_index):
    '''
    获取项目或项目下所有测试集

    url: 
        /project/getall/1获取所有项目
        /project/getall/2获取项目下所有测试集
            args: json参数
            {
                "p_id": '项目ID'
            }

    return: json示例
    {
        'errcode': 0, 
        'errmsg': 'SUCCESS', 
        'res': {
            'project': [
                {
                    'p_id': 1, 
                    'p_name': '我的第N+1个项目'
                }, 
                {
                    'p_id': 2, 
                    'p_name': '我的第N+1个项目'
                }
            ]
    }
    '''
    # 创建项目
    res_project = create_project(client, auth)

    res = client.post(
        '/project/getall/{}'.format(url_index),
        json={'p_id': res_project['res']['p_id']}
    )

    print('/project/getall/{} : {}'.format(url_index, res.json))

    assert res.json['errcode'] == 0


'''
/project/suite/create 创建测试集
'''
@pytest.mark.suite_create
def test_create_suite(client, auth):
    '''
    根据项目ID，创建测试集

    args: json示例

    {
        "s_name": "测试集名称",
        "project_id": "项目ID"
    }

    return: json示例
    {
        'errcode': 0, 
        'errmsg': '新建模块成功.', 
        'res': {
            'project_id': 117, 
            'suite_id': 1, 
            'suite_name': '我的第1个测试集'
        }
    }
    '''
    # 创建项目
    res_project = create_project(client, auth)

    res = client.post(
        '/project/suite/create',
        json={
            'project_id': res_project['res']['p_id'],
            's_name': '我的第1个测试集'
        }
    )

    print('/project/suite/create : {}'.format(res.json))

    assert '测试集' in res.json['res']['suite_name']

