import random
import string
import json

# 生成随机的用户名，由2位小写字母和8位数字组成
def generate_random_username():
    letters = ''.join(random.choices(string.ascii_lowercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=8))
    return letters + numbers

# 加载权限文件
def load_permissions():
    try:
        with open('permissions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
# 获取下一个id
def get_next_id(collection_name, count, counters_collection):
    result = counters_collection.find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'count': count}},
        return_document=True
    )
    if result is None:
        counters_collection.insert_one({'_id': collection_name, 'count': count})
        result = counters_collection.find_one_and_update(
            {'_id': collection_name},
            {'$inc': {'count': count}},
            return_document=True
        )
        
    start_id = result['count'] - count
    return [str(start_id + i).zfill(5) for i in range(count)]
