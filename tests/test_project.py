'''
coverage run -m pytest --capture=no
'''
import pytest


def create_project(client, auth):
    # 创建项目
    auth.login()
    res = client.post(
        '/project/create',
        json={"name": "我的第N个项目"}
    )

    print('新建项目:{}'.format(res['res']))

    return res if "N" in res.json['res']['project_name'] else False



'''
/project/create 创建项目
'''
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

    print('新创建项目ID:{}'.format(p_id_lst))



'''
/project/delete 删除项目
'''
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
    res_project = create_project(client, auth)
    
    res = client.post(
        '/project/delete',
        json=[res_project['res']['p_id']]
    )

    assert res_project['res']['p_id'] in [pid_dict['p_id'] for pid_dict in res['res']['project']]
