#!/bin/bash

# Face Flip Server 快速设置脚本

echo "🚀 Face Flip Server 快速设置"
echo "================================"
echo ""

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本: $python_version"
echo ""

# 检查是否安装了 UV
echo "📦 检查 UV 包管理器..."
if ! command -v uv &> /dev/null; then
    echo "❌ UV 未安装，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✅ UV 已安装"
fi
echo ""

# 安装依赖
echo "📥 安装项目依赖..."
uv sync
echo "✅ 依赖安装完成"
echo ""

# 创建 .env 文件
if [ ! -f .env ]; then
    echo "📝 创建 .env 配置文件..."
    cat > .env << 'EOF'
# Application Settings
APP_NAME=Face Flip Server
APP_VERSION=0.1.0
DEBUG=True

# Server Settings
HOST=0.0.0.0
PORT=8000

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Supabase Configuration
SUPABASE_URL=
SUPABASE_KEY=

# JWT Settings
SECRET_KEY=change-this-secret-key-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_FOLDER=uploads

# Logging
LOG_LEVEL=INFO
EOF
    echo "✅ .env 文件已创建"
    echo "⚠️  请编辑 .env 文件填写 Supabase 配置"
else
    echo "✅ .env 文件已存在"
fi
echo ""

# 创建上传目录
echo "📁 创建上传目录..."
mkdir -p uploads
echo "✅ 上传目录已创建"
echo ""

# 完成
echo "================================"
echo "✨ 设置完成！"
echo ""
echo "📚 下一步："
echo "  1. 编辑 .env 文件，填写 Supabase 配置"
echo "  2. 运行 'make run' 或 'uv run python run.py' 启动服务器"
echo "  3. 访问 http://localhost:8000/docs 查看 API 文档"
echo ""
echo "🔧 常用命令："
echo "  make run      - 启动开发服务器"
echo "  make test     - 运行测试"
echo "  make format   - 格式化代码"
echo "  make help     - 查看所有命令"
echo ""

