from pymongo import errors
from config import client, DATABASE_NAME
from utils.logger import logger
import sys

# 访问数据库
db = client[DATABASE_NAME]
accounts_collection = db['accounts']
counters_collection = db['counters']

def test_mongo_connection():
    try:
        collections = db.list_collection_names()
        logger.debug("Collections: %s", collections) 

    except errors.ServerSelectionTimeoutError:
        logger.error("连接超时: 无法连接到 MongoDB 服务器")
        sys.exit(1)
    except errors.PyMongoError as e:
        logger.error("连接数据库时发生错误: %s",e)
        sys.exit(1)
    except Exception as e:
        logger.error("发生意外错误: %s", e)
        sys.exit(1)
                      
def initialize_database():
    try:
        if 'counters' not in db.list_collection_names():
            db.create_collection('counters')
            logger.warn("未找到counters集合，进行初始化...")
        if not counters_collection.find_one({'_id': 'Account'}):
            counters_collection.insert_one({
                '_id': 'Account',
                'count': 10001
            })
            logger.info("正在初始化Account文档...")
            
        if not counters_collection.find_one({'_id': 'Player'}):
            counters_collection.insert_one({
                '_id': 'Player',
                'count': 10001
            })
            logger.info("正在初始化Player文档...")
            
    except errors.PyMongoError as e:
         logger.error("counters集合初始化失败", e)
