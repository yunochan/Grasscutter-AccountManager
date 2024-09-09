import logging
from flask import Flask, render_template
from utils.logger import logger
from routes.accounts import accounts_bp
from routes.permissions import permissions_bp
from routes.status import status_bp
from models import initialize_database, test_mongo_connection

app = Flask(__name__)

# 配置 Flask 和 Werkzeug 的日志处理器
app.logger.handlers = logger.logger.handlers
app.logger.setLevel(logger.logger.level)

# 设置 Werkzeug 使用自定义日志记录器
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers = logger.logger.handlers
werkzeug_logger.setLevel(logger.logger.level)

# 检查 config 配置
test_mongo_connection()

# 注册蓝图
app.register_blueprint(accounts_bp, url_prefix='/accounts')
app.register_blueprint(permissions_bp, url_prefix='/permissions')
app.register_blueprint(status_bp, url_prefix='/server')

# 初始化数据库
initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

# 添加错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 仅用于开发时使用 Flask 内置的服务器
    # 在生产环境中使用 gunicorn
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=33489)
