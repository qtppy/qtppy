# QTPPY自动化测试平台

[![Build Status](https://travis-ci.org/HttpTesting/pyhttp.svg?branch=master)](https://travis-ci.org/HttpTesting/pyhttp)
![PyPI - License](https://img.shields.io/pypi/l/HttpTesting)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HttpTesting)


Quality testing platform-python 简称QTPPY，采用前后端分离开发，后端是基于python语言，前端是vue框架开发的HTTP(s)协议接口自动化测试平台。


## 功能描述
QTPPY是一个HTTP(S)接口自动化测试平台,简洁的接口录入，业务场景拟合,统一测试计划中执行，测试报告简单明了，执行数据统计及图表展示功能缺陷分布图。
#### 目的: 
代码质量作为系统稳定性建设的核心的一环，要想提高系统稳定性，根本上要提升代码质量。我们希望通过一些普适性的东西来克服人为因素带来的一些影响，并且可以为以后复用。并且建立一套统一的标准，让提高质量不只是一句口号而是有章可依。
#### 形势: 
站在研发的立场看，自动化测试可以是代码层面简单的功能TestCase，也可以是接口层面的测试。如果要做全面的覆盖，两者对基础设施的要求是一样的,但是站在QA的立场来看，QA关心的是接口层面的返回，代码层面的东西不是特别关心。鉴于两方的述求，我们认为在接口层面做，对双方都有利。
#### 内容梳理:
一个自动化测试的流程应该包含以下几步：初始化基础数据mock所有外部请求发起请求系统处理请求返回结果清理数据涉及的技术点：初始化数据工具，mock server及mock,结果对比，请理数据。我们希望只需要人工准备请求数据，初始化数据，以及返回结果，剩下的事情系统搞定。

## 快速开始
QTPPY采用前后端分离：后端python+flask; 前端vue2.0+elementUI+axios

前端穿越坐标：[点击此处穿越到前端github](https://github.com/qtppy/frontend_qtppy)

### 环境安装

命令行模式下，执行命令

#### 1. 创建虚拟环境:
```virtualenv QTPPY_ENV```

#### 2. 在虚拟环境下，安装python项目依赖包：
```pip install -r requirements.txt```

#### 3. 拉取QTPPY代码库:

``` git clone https://github.com/qtppy/qtppy.git```

#### 4. 创建数据库mysql

执行以下命令:
##### 1.创建库:
```CREATE DATABASE qtppdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;```
##### 2.授权:
```GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON 数据库名.* TO 数据库名@localhost IDENTIFIED BY '密码';```
##### 3.项目根目录执行命令，创建表
###### 1).项目目录下config.py修改数据库实例配置
```
class BaseConfig:
    # 调试信息
    DEBUG = False

    SECRET_KEY='dev'

    # 数据库信息
    DIALCT = 'mysql'
    DRIVER = "mysqlconnector"
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DBNAME = 'qtppdb'
```
###### 2).初始化db migrate.py文件，如果报错，项目目录下migrations目录整个删除
```python manage.py db init```
###### 3).生成表结构
```python manage.py db migrate```
###### 4).数据库中创建表
```python manage.py db upgrade```

#### 4. 运行代码
进入到代码qtppy目录，执行命令，启动项目 ``` python manage.py runserver ```
```
看到以下内容项目运行成功:
* Serving Flask app "qtpp"
* Environment: development
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
## UI界面
#### 主页：

#### 项目管理:

#### 用例管理:

#### 场景管理:

#### 测试计划:

