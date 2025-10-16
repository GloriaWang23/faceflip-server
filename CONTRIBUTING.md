# 贡献指南

感谢您对 Face Flip Server 项目的关注！我们欢迎任何形式的贡献。

## 🚀 开始之前

在开始贡献之前，请确保：

1. 已经阅读了项目的 README.md
2. 了解项目的基本架构和设计理念
3. 熟悉 Python 和 FastAPI 框架

## 📋 贡献流程

### 1. Fork 项目

首先 fork 本项目到您的 GitHub 账户。

### 2. 克隆项目

```bash
git clone https://github.com/your-username/face-flip-server.git
cd face-flip-server
```

### 3. 创建分支

为您的功能或修复创建一个新分支：

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 4. 设置开发环境

```bash
# 运行设置脚本
bash setup.sh

# 或手动安装
uv sync --extra dev
```

### 5. 进行更改

- 遵循项目的代码风格
- 添加必要的测试
- 更新相关文档

### 6. 代码质量检查

在提交前，请运行以下检查：

```bash
# 格式化代码
make format

# 检查代码规范
make lint

# 运行测试
make test
```

### 7. 提交更改

```bash
git add .
git commit -m "feat: 添加新功能描述"
```

提交信息格式：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 其他修改

### 8. 推送到 GitHub

```bash
git push origin feature/your-feature-name
```

### 9. 创建 Pull Request

在 GitHub 上创建 Pull Request，并描述：
- 更改的内容
- 为什么需要这个更改
- 如何测试这些更改

## 📝 代码规范

### Python 代码风格

- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化（行长度：100）
- 使用 Ruff 进行代码检查
- 使用类型注解

### 项目结构规范

- API 端点放在 `app/api/endpoints/`
- 业务逻辑放在 `app/services/`
- 数据模型放在 `app/models/`
- Pydantic schemas 放在 `app/schemas/`
- 工具函数放在 `app/utils/`

### 测试规范

- 每个新功能都应该有对应的测试
- 测试文件放在 `tests/` 目录
- 测试函数以 `test_` 开头
- 保持测试简洁和可读

## 🐛 报告 Bug

如果您发现 bug，请创建 Issue 并包含：

- Bug 的详细描述
- 复现步骤
- 期望的行为
- 实际的行为
- 环境信息（操作系统、Python 版本等）
- 相关的日志或截图

## 💡 功能建议

如果您有新功能建议：

1. 先检查是否已有类似的 Issue
2. 创建新的 Issue 详细描述您的想法
3. 说明这个功能的用途和价值
4. 如果可能，提供实现思路

## 📧 联系方式

如有问题，可以通过以下方式联系：

- 创建 GitHub Issue
- 发送邮件到维护者

## 📄 许可证

通过贡献代码，您同意您的贡献将使用与本项目相同的 MIT 许可证。

---

再次感谢您的贡献！🎉

