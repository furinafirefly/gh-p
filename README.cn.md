<div align="center">
<h1>gh-p</h1>
<p>GitHub Pull Request 增强工具</p>


[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub CLI](https://img.shields.io/badge/GitHub%20CLI-required-orange.svg)](https://cli.github.com/)

<b>简体中文</b> | <a href="./README.md">English</a>

</div>

## ✨ 功能特性

- **智能 PR Checkout** - 自动将 PR checkout 到格式化的本地分支
- **自动 PR 检测** - 从分支名或 GitHub 引用自动检测 PR 号码
- **无缝推送** - 自动管理远程仓库配置并推送到 PR 分支
- **完全兼容** - 无缝透传所有其他 `gh pr` 命令
- **高度可定制** - 可配置分支命名和远程处理方式

## 🚀 安装

### 依赖项

- Python 3.7+
- GitHub CLI (`gh`)
- Git

### 快速安装

```bash
# Github CLI (gh) install
gh extension install wyf9/gh-p
```

## 使用

### Checkout PR

```bash
gh p checkout 123
# 创建本地分支: gh-pull-123
```

### Push 到 PR

```bash
# 当在分支 'gh-pull-789' 上时
gh p push
# 自动检测 PR #789
```

### 透传命令

```bash
gh p list          # 执行: gh pr list
gh p status        # 执行: gh pr status
gh p review 123    # 执行: gh pr review 123
```

### 帮助

```bash
gh p --help        # 通用帮助
gh p checkout -h   # checkout 命令帮助
gh p push -h       # push 命令帮助
```

## ⚙️ 配置

首先 Clone / Fork 本 Repo,

并编辑 config.py 来自定义行为：

```python
# 本地分支命名
pr_branch_format = 'gh-pull-{number}'

# PR 号码提取模式
pr_branch_matches = [
    ('gh-pull-{number}', True),
    ('gh-{number}', False),
    # 添加您的自定义模式
]

# 远程配置
temp_remote_name = 'gh-pull-temp'
remote_url = 'https://github.com/{owner}/{repo}.git'

# 命令别名
aliases = {
    'checkout': ['checkout', 'co', 'c'],
    'push': ['push', 'p']
}
```

## 📄 协议

MIT License.

Copyright (c) 2025 wyf9, All rights reserved.