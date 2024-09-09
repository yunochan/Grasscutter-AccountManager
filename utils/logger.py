import logging
import os
import glob
import re
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name='app', log_dir='log', log_prefix='app', log_level=logging.DEBUG, max_log_size=10*1024*1024, backup_count=10):
        """
        初始化 Logger 对象。

        :param name: 日志记录器的名称
        :param log_dir: 日志目录
        :param log_prefix: 日志文件名前缀
        :param log_level: 日志级别
        :param max_log_size: 单个日志文件的最大大小（字节）
        :param backup_count: 保留的旧日志文件的数量
        """
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # 防止重复添加处理器
        if not self.logger.handlers:
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            # 创建旋转文件处理器
            log_file = self.get_next_log_file(log_dir, log_prefix)
            rotating_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_log_size,
                backupCount=backup_count
            )

            # 设置格式化器
            console_formatter = self.ColoredFormatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # 将格式化器添加到处理器
            console_handler.setFormatter(console_formatter)
            rotating_handler.setFormatter(file_formatter)

            # 将处理器添加到日志记录器
            self.logger.addHandler(console_handler)
            self.logger.addHandler(rotating_handler)

    def get_next_log_file(self, log_dir, log_prefix):
        """
        获取下一个日志文件名。

        :param log_dir: 日志目录
        :param log_prefix: 日志文件名前缀
        :return: 下一个日志文件名
        """
        # 获取当前日期
        date_str = self.get_current_date()
        
        # 构建日志文件的基本模式
        base_pattern = os.path.join(log_dir, f'{date_str}-{log_prefix}-*.log')

        # 查找所有匹配的日志文件
        existing_files = glob.glob(base_pattern)
        
        # 提取文件名中的序号
        max_index = 0
        for file in existing_files:
            match = re.search(rf'{date_str}-{log_prefix}-(\d+)\.log$', file)
            if match:
                index = int(match.group(1))
                if index > max_index:
                    max_index = index
        
        # 生成下一个日志文件名
        next_index = max_index + 1
        return os.path.join(log_dir, f'{date_str}-{log_prefix}-{next_index}.log')

    def get_current_date(self):
        """
        获取当前日期，格式为 YYYY-MM-DD。

        :return: 当前日期字符串
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    class ColoredFormatter(logging.Formatter):
        """自定义的日志格式化器，添加颜色代码"""

        COLORS = {
            'DEBUG': '\033[32m',   # 青色
            'INFO': '\033[34m',    # 蓝色
            'WARNING': '\033[33m', # 黄色
            'ERROR': '\033[31m',   # 红色
        }

        RESET = '\033[0m'

        def format(self, record):
            log_message = super().format(record)

            # 分离出时间、级别和消息
            time_str = f'\033[36m[{self.formatTime(record, self.datefmt)}]\033[0m'
            level_str = f'{self.COLORS.get(record.levelname, self.RESET)}[{record.levelname}]{self.RESET}'
            message_str = record.getMessage()

            return f'{time_str} {level_str} {message_str}'

    def debug(self, message, *args):
        """记录 debug 级别日志"""
        self.logger.debug(message, *args)

    def info(self, message, *args):
        """记录 info 级别日志"""
        self.logger.info(message, *args)

    def warn(self, message, *args):
        """记录 warn 级别日志"""
        self.logger.warning(message, *args)

    def error(self, message, *args):
        """记录 error 级别日志"""
        self.logger.error(message, *args)

logger = Logger(name='app', log_dir='log', log_prefix='app')
