import requests
from flask import Blueprint, jsonify
from config import GC_URL
from utils.logger import logger
status_bp = Blueprint('server', __name__)

@status_bp.route('/status')
def check_status():
    try:
        logger.info("检查游戏服务器状态: %s", GC_URL)
        response = requests.get(GC_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        player_count = data['status']['playerCount']
        version = data['status']['version']
        
        return jsonify({'playerCount': player_count, 'version': version})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
