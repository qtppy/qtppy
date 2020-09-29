import sys 
from tornado.wsgi import WSGIContainer 
from tornado.httpserver import HTTPServer 
from tornado.ioloop import IOLoop 
from qtpp import create_app  # 这里导入的是flsk项目的运行模块

app = create_app(config_name='pro')

http_server = HTTPServer(WSGIContainer(app)) 
http_server.listen(8088) 
IOLoop.instance().start()