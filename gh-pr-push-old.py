#!/usr/bin/env python3
"""
gh p push - 一键把本地 commit 推送到 PR 贡献者的分支

用法（两种都行，随你喜欢）：
  gh p push 125          # 自动 checkout + push（最常用）
  gh p push              # 当前分支必须是 gh pr checkout 拉下来的

支持：
  gh p push 125 --force
  gh p push --force     # 当前分支强制推
"""

import os
import sys
import subprocess
import json
import re
import shutil
from pathlib import Path


def run(cmd: str, check=True):
    """运行命令，返回 stdout，失败时抛异常或直接 exit"""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=Path.cwd()
    )
    if check and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def gh_pr_view(pr_number: str):
    """获取 PR 详细信息"""
    return json.loads(run(f"gh pr view {pr_number} --json headRefName,headRepositoryOwner,headRepository"))


def get_current_tracking_ref():
    """返回当前分支的 upstream ref，例如：origin/pull/125/head"""
    try:
        return run("git rev-parse --abbrev-ref --symbolic-full-name @{u}")
    except:
        return ""


def extract_pr_number_from_ref(ref: str) -> str | None:
    m = re.search(r"/(pull/)?(\d+)/head", ref)
    return m.group(2) if m else None


def main():
    args = sys.argv[1:]
    force = "--force" if "--force" in args or "-f" in args else ""

    # ------------------- 情况1：用户传了数字 -------------------
    if args and args[0].isdigit():
        pr_number = args[0]
        print(f"Checking out PR #{pr_number} ...")
        run(f"gh pr checkout {pr_number}")

    # ------------------- 情况2：没传参数 → 尝试自动识别 -------------------
    elif not args:
        tracking = get_current_tracking_ref()
        detected = extract_pr_number_from_ref(tracking)
        if detected:
            pr_number = detected
            print(f"Detected current branch belongs to PR #{pr_number}")
        else:
            print("Error: No PR number provided and cannot detect from current branch.")
            print("Usage:")
            print("  gh p push 125          # recommended")
            print("  gh p push              # only works after 'gh p checkout'")
            sys.exit(1)
    else:
        print("Usage: gh p push [<pr-number>] [--force]")
        sys.exit(1)

    # ------------------- 获取 PR 信息 -------------------
    print(f"Fetching PR #{pr_number} info...")
    info = gh_pr_view(pr_number)

    branch = info["headRefName"]
    owner = info["headRepositoryOwner"]["login"]
    repo = info["headRepository"]["name"]

    remote_name = "pr-contributor"
    remote_url = f"https://github.com/{owner}/{repo}.git"

    # ------------------- 配置 remote -------------------
    current_url = ""
    if shutil.which("git"):  # 安全检查
        try:
            current_url = run(f"git remote get-url {remote_name}", check=False)
        except:
            pass

    if current_url != remote_url:
        run(f"git remote remove {remote_name}", check=False)
        run(f"git remote add {remote_name} {remote_url}")
        print(f"Remote '{remote_name}' → {owner}/{repo}")
    else:
        print(f"Remote '{remote_name}' already points to {owner}/{repo}")

    # ------------------- 推 送 -------------------
    print(f"Pushing to {owner}:{branch} {force}...")
    push_result = run(f"git push {remote_name} HEAD:{branch} {force}")
    print(push_result)

    print("\nSuccess")


if __name__ == "__main__":
    main()
