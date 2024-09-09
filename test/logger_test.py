import sys
import os
import time
# 添加项目根目录到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import Logger

def main():
    # 创建 Logger 实例
    log_file = 'log/app.log'
    logger = Logger(log_file=log_file)

    while True:
        # 记录各种级别的日志
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warn("This is a warning message.")
        logger.error("This is an error message.")

        # 等待 5 秒
        time.sleep(5)


if __name__ == "__main__":
    main()
