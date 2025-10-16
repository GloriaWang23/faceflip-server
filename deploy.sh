#!/bin/bash

# Face Flip Server - Vercel 部署脚本
# 使用方法: ./deploy.sh

set -e

echo "🚀 Face Flip Server - Vercel 部署脚本"
echo "======================================"

# 检查是否安装了必要的工具
check_dependencies() {
    echo "📋 检查依赖..."
    
    if ! command -v vercel &> /dev/null; then
        echo "❌ Vercel CLI 未安装"
        echo "请运行: npm install -g vercel"
        exit 1
    fi
    
    if ! command -v uv &> /dev/null; then
        echo "❌ uv 未安装"
        echo "请运行: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm 未安装"
        echo "请安装 Node.js 和 npm"
        exit 1
    fi
    
    echo "✅ 所有依赖已安装"
}

# 构建项目
build_project() {
    echo "🔨 构建项目..."
    
    echo "安装后端依赖..."
    uv sync
    
    echo "安装前端依赖..."
    cd ui && npm install && cd ..
    
    echo "构建前端..."
    cd ui && npm run build && cd ..
    
    echo "✅ 构建完成"
}

# 部署到 Vercel
deploy_to_vercel() {
    echo "🚀 部署到 Vercel..."
    
    # 检查是否已登录
    if ! vercel whoami &> /dev/null; then
        echo "请先登录 Vercel:"
        vercel login
    fi
    
    # 部署
    vercel --prod
    
    echo "✅ 部署完成"
}

# 显示环境变量配置提示
show_env_setup() {
    echo ""
    echo "📝 环境变量配置"
    echo "================"
    echo "请在 Vercel Dashboard 的 Settings > Environment Variables 中设置以下变量:"
    echo ""
    echo "必需变量:"
    echo "  SUPABASE_URL=your_supabase_project_url"
    echo "  SUPABASE_KEY=your_supabase_anon_key"
    echo "  ARK_API_KEY=your_ark_api_key"
    echo "  SECRET_KEY=your_jwt_secret_key"
    echo ""
    echo "可选变量:"
    echo "  SUPABASE_SERVICE_ROLE_KEY=your_service_role_key"
    echo "  SUPABASE_STORAGE_BUCKET=faceflip-images"
    echo "  ARK_DEFAULT_PROMPT=your_default_prompt"
    echo ""
    echo "详细配置请参考: docs/VERCEL_DEPLOYMENT.md"
}

# 主函数
main() {
    check_dependencies
    build_project
    deploy_to_vercel
    show_env_setup
    
    echo ""
    echo "🎉 部署完成！"
    echo "请确保在 Vercel Dashboard 中配置了所有必需的环境变量。"
}

# 运行主函数
main "$@"
