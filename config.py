from pymongo import MongoClient

# MongoDB 配置
USERNAME = "root"
PASSWORD = "123456"
HOST = '127.0.0.1'
PORT = 27017
DATABASE_NAME = 'grasscutter'
AUTHORIZATION = False  # If authentication is required, set to True

# Grasscutter 服务器地址
PUBLICADDRESS = '127.0.0.1'
BINPORT = 27017

# 构建 MongoDB 数据库 url
if AUTHORIZATION:
    client = MongoClient(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        authSource='admin'  # 根据需要更改 authSource
    )
else:
    client = MongoClient(host=HOST, port=PORT)
    
# 构建请求 url
GC_URL = f'http://{PUBLICADDRESS}:{BINPORT}/status/server'




