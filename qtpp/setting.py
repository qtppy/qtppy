import os, sys

# 文件上传配置

# 允许上传的文件类型
ALLOW_EXTENSIONS = [
    'png', 
    'jpg', 
    'jpeg', 
    'txt', 
    'xls', 
    'xlsx', 
    'csv'
]

# 文件上传目录
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'upload'
)