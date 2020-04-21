from datetime import timedelta

# app.config[] dict
app_config = {
    "DEBUG": None,   # debug模式的设置,开发环境用，自动重启项目，日志级别低，报错在前端显示具体代码
    "TESTING": False,  #测试模式的设置，无限接近线上环境，不会重启项目，日志级别较高，不会在前端显示错误
    "SESSION_COOKIE_NAME": "session",           #cookies中存储的session字符串的键
    "JSONIFY_MIMETYPE": "application/json",     #设置jsonify响应时返回的contentype类型
    "PERMANENT_SESSION_LIFETIME": timedelta(days=31),   #session有效期时间的设置
}