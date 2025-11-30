<div align="center">
<h1>gh-p</h1>
<p>GitHub Pull Request Enhanced Tool</p>


[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub CLI](https://img.shields.io/badge/GitHub%20CLI-required-orange.svg)](https://cli.github.com/)

<b>English</b> | <a href="./README.cn.md">简体中文</a>

</div>

## ✨ Features

- **Smart PR Checkout** - Automatically checkout PRs to formatted local branches
- **Auto PR Detection** - Detect PR numbers from branch names or GitHub references
- **Seamless Push** - Push to PR branches with automatic remote management
- **Full Compatibility** - Passthrough all other `gh pr` commands unchanged
- **Customizable** - Highly configurable branch naming and remote handling

## 🚀 Installation

### Prerequisites

- Python 3.7+
- GitHub CLI (`gh`) installed and authenticated
- Git

### Quick Install

```bash
# Github CLI (gh) install
gh extension install wyf9/gh-p
```

## Usage

### Checkout a PR

```bash
gh p checkout 123
# Creates local branch: gh-pull-123
```

### Push to a PR

```bash
# When on branch 'gh-pull-789'
gh p push
# Automatically detects PR #789
```

### Pass-through commands

```bash
gh p list          # Runs: gh pr list
gh p status        # Runs: gh pr status
gh p review 123    # Runs: gh pr review 123
```

### Help

```bash
gh p --help        # General help
gh p checkout -h   # Checkout command help
gh p push -h       # Push command help
```

## ⚙️ Configuration

Clone / Fork this repo first,

then edit config.py to customize behavior:

```python
# Local branch naming
pr_branch_format = 'gh-pull-{number}'

# PR number extraction patterns
pr_branch_matches = [
    ('gh-pull-{number}', True),
    ('gh-{number}', False),
    # Add your custom patterns
]

# Remote configuration
temp_remote_name = 'gh-pull-temp'
remote_url = 'https://github.com/{owner}/{repo}.git'

# Command aliases
aliases = {
    'checkout': ['checkout', 'co', 'c'],
    'push': ['push', 'p']
}
```

## 📄 License

MIT License.

Copyright (c) 2025 wyf9, All rights reserved.