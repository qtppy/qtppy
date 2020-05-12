import pytest


def test_create_project(client, auth):
    '''
    创建项目
    '''
    auth.login()
    res = client.post(
        '/project/create',
        json={"name": "我的第N+1个项目"}
    )
    assert "N+1" in res.json['res']['project_name']

