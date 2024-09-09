#!/bin/bash

# 查找所有 Python 3 路径
PYTHON_PATHS=$(ls /usr/bin/python3.* 2>/dev/null)
if [ -z "$PYTHON_PATHS" ]; then
    echo "未安装 Python3 退出程序"
    exit 1
fi

# 提取最高版本号
PYTHON_VERSION=$(echo "$PYTHON_PATHS" | grep -Eo '[0-9]+\.[0-9]+' | sort -V | tail -n 1)

# Python 执行路径
PYTHON_EXEC="/usr/bin/python$PYTHON_VERSION"

# 检查并安装虚拟环境包
if ! dpkg -l | grep -q "python$PYTHON_VERSION-venv"; then
    echo "安装 python$PYTHON_VERSION-venv 包..."
    sudo apt-get update
    sudo apt-get install -y python$PYTHON_VERSION-venv
else
    echo "python$PYTHON_VERSION-venv 已安装"
fi

# 设置虚拟环境名称
VENV_NAME="gcweb"
# 设置虚拟环境路径
VENV_PATH="./$VENV_NAME"

# 创建虚拟环境
if [ ! -d "$VENV_PATH" ]; then
    echo "创建虚拟环境 $VENV_NAME ..."
    $PYTHON_EXEC -m venv $VENV_PATH
else
    echo "虚拟环境 $VENV_NAME 已存在，跳过创建。"
fi

# 激活虚拟环境
source $VENV_PATH/bin/activate

# 升级 pip 和安装依赖
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 检查是否已有 gunicorn 实例在运行
echo "检查是否已有 gunicorn 实例在运行 ..."
PID=$(lsof -i:33489 -t)
if [ ! -z "$PID" ]; then
    echo "正在运行的 gunicorn 实例，PID: $PID"
    kill -9 $PID
    echo "已杀死gunicorn 实例"
fi

# 启动应用
echo "启动 GC-WebAccount ..."
gunicorn -w 4 -b 0.0.0.0:33489 main:app -D --access-logfile log/gcweb.log --error-logfile log/gcweb.error.log
