from flask import Blueprint, request, jsonify, send_file
from pymongo import errors
from models import accounts_collection, counters_collection
from utils.tool import generate_random_username, get_next_id
from utils.logger import logger

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/create', methods=['POST'])
def create_accounts():
    data = request.json
    count = data.get('count', 1)

    # 检查数量是否合法
    if not isinstance(count, int) or count < 1 or count > 50000:
        logger.warn("非法的数量: %s", count)
        return jsonify({'status': 'error', 'message': '非法的参数，数量应在1到50000之间'}), 400

    try:
        next_ids = get_next_id('Account', count, counters_collection)
        new_accounts = []
        created_usernames = []

        for next_id in next_ids:
            username = generate_random_username()

            new_account = {
                '_id': next_id,
                'username': username,
                'reservedPlayerId': 0,
                'permissions': [],
                'locale': 'zh_CN',
                'banEndTime': 0,
                'banStartTime': 0,
                'isBanned': False,
                'count': 0
            }

            new_accounts.append(new_account)
            created_usernames.append(username)

        while new_accounts:
            try:
                # 批量插入数据库
                accounts_collection.insert_many(new_accounts, ordered=False)
                logger.info("成功创建%s个账号: %s", count, created_usernames)
                break  
            except errors.BulkWriteError as bwe:
                # 过滤掉因重复键错误而失败的文档
                duplicate_keys = set(err['op']['_id'] for err in bwe.details['writeErrors'])
                new_accounts = [acc for acc in new_accounts if acc['_id'] not in duplicate_keys]
                if not new_accounts:
                    logger.error("批量写入错误: %s", bwe.details)
                    raise  

        with open('account.txt', 'w') as f:
            f.write('\n'.join(created_usernames))

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        logger.error("创建账号时出现异常: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@accounts_bp.route('/download')
def download_accounts():
    try:
        return send_file('account.txt', as_attachment=True)
    except Exception as e:
        logger.error("下载文件出现异常: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@accounts_bp.route('/delete', methods=['POST'])
def delete_account():
    data = request.json
    username = data.get('username')
    if not username:
        logger.warn("删除帐户时缺少用户名")
        return jsonify({'status': 'error', 'message': '用户名不能为空'}), 400

    try:
        result = accounts_collection.delete_one({'username': username})
        if result.deleted_count > 0:
            logger.info('账号删除成功: %s ', username)
            return jsonify({'status': 'success', 'deleted_count': result.deleted_count}), 200
        else:
            logger.warn("未发现账号: %s", username)
            return jsonify({'status': 'error', 'message': f'未找到用户 {username}'}), 404
    except Exception as e:
        logger.error("删除账号时出现异常: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@accounts_bp.route('/ban', methods=['POST'])
def update_ban_status():
    data = request.json
    username = data.get('username')
    is_banned = data.get('isBanned')
    
    if not username or is_banned is None:
        logger.warn("封禁账号缺少用户名")
        return jsonify({'status': 'error', 'message': '用户名不能为空'}), 400
    
    try:
        is_banned = bool(is_banned)
        
        ban_start_time = -1313677 if is_banned else 0
        ban_end_time = 1924876800 if is_banned else 0

        update_fields = {
            'isBanned': is_banned,
            'banStartTime': ban_start_time,
            'banEndTime': ban_end_time
        }
        
        result = accounts_collection.update_one(
            {'username': username},
            {'$set': update_fields}
        )
        
        if result.matched_count > 0:
            logger.info("账号封禁状态已更新: %s, 是否封禁: %s", username, is_banned)
            actionMessage = f"用户 {username} 已被封禁" if is_banned else f"用户 {username} 已解封"
            return jsonify({'status': 'success', 'message': actionMessage }), 200
        else:
            logger.warn("未发现用户: %s", username)
            return jsonify({'status': 'error', 'message': f'未找到用户 {username}'}), 404
    
    except Exception as e:
        logger.error('更新封禁状态出现异常: %s', str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500
