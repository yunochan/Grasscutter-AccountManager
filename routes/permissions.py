from flask import Blueprint, request, jsonify
from models import accounts_collection
from utils.tool import load_permissions
from utils.logger import logger

permissions_bp = Blueprint('permissions', __name__)

@permissions_bp.route('/list')
def get_permissions():
    try:
        permissions = load_permissions()
        logger.info("权限列表检索成功")
        return jsonify({'permissions': permissions})
    except Exception as e:
        logger.error("权限列表索引异常: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@permissions_bp.route('/update', methods=['POST'])
def update_permissions():
    data = request.json
    username = data.get('username')
    selected_permissions = data.get('permissions', [])
    action = data.get('action')

    if not username or not isinstance(selected_permissions, list) or action not in ['add', 'remove']:
        logger.warn("非法输入: username=%s, permissions=%s, action=%s", username, selected_permissions, action)
        return jsonify({'status': 'error', 'message': '非法输入'}), 400

    available_permissions = load_permissions()
    invalid_permissions = [perm for perm in selected_permissions if perm not in available_permissions]
    if invalid_permissions:
        logger.warn("非法的权限参数: %s", ', '.join(invalid_permissions))
        return jsonify({'status': 'error', 'message': f'非法的权限参数: {", ".join(invalid_permissions)}'}), 400

    try:
        account = accounts_collection.find_one({'username': username})
        if not account:
            logger.warn("未发现账号: %s", username)
            return jsonify({'status': 'error', 'message': '未找到账号'}), 404

        if action == 'add':
            updated_permissions = list(set(account.get('permissions', []) + selected_permissions))
            logger.info("账号: %s, 添加权限: [%s]", username, selected_permissions)
        elif action == 'remove':
            updated_permissions = [perm for perm in account.get('permissions', []) if perm not in selected_permissions]
            logger.info("账号: %s, 移除权限: [%s]", username, selected_permissions)

        accounts_collection.update_one(
            {'username': username},
            {'$set': {'permissions': updated_permissions}}
        )
        actionMessage = f"已为用户 {username} 添加 {selected_permissions} 权限" if action == 'add' else f"已移除用户 {username} 的 {selected_permissions} 权限"
        return jsonify({'status': 'success','message': actionMessage }), 200

    except Exception as e:
        logger.error("更新权限状态出现异常: %s", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500
