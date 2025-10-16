#!/bin/bash

echo "📦 准备提交新文件到 Git..."

# 添加所有新文件和修改
git add app/middleware/auth.py
git add app/core/auth_config.py
git add app/core/logging_config.py
git add api/index.py
git add .vercelignore
git add app/main.py
git add app/middleware/__init__.py
git add app/middleware/error_handler.py
git add app/core/dependencies.py
git add app/services/auth_service.py
git add app/services/user_service.py
git add app/api/endpoints/users.py

echo "✅ 文件已添加到暂存区"
echo ""
echo "📝 提交信息："
git commit -m "feat: 添加全局认证中间件和完整日志系统

新增功能：
- 实现类似 Spring Security 的全局认证拦截器
- 支持白名单配置（精确匹配和正则表达式）
- 添加完整的日志记录系统（所有异常都被记录）
- 日志支持多级别（DEBUG/INFO/WARNING/ERROR）
- 日志支持文件输出和控制台输出

修复：
- 修复 Vercel 部署时的模块导入问题
- 更新 api/index.py 以包含新的中间件
- 更新 .vercelignore 配置

相关文档：
- docs/GLOBAL_AUTH.md - 全局认证使用指南
- docs/LOGGING.md - 日志系统使用指南
- DEPLOY_TO_VERCEL.md - Vercel 部署指南
"

echo ""
echo "✅ 提交完成！"
echo ""
echo "🚀 推送到远程仓库："
echo "   git push origin master"
echo ""
echo "📌 推送后 Vercel 会自动部署"
