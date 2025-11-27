# coding: utf-8

from subprocess import run as orig_run
from pathlib import Path
import sys
import json
import argparse
import typing as t

import log as l


def run(cmd: str | list[str], check_err: bool = True, timeout: float | None = None, capture: bool = True) -> str:
    '''
    Run command
    '''

    l.v(f'Run command: {cmd}, cwd: {Path.cwd()}, check_err: {check_err}, timeout: {timeout}, capture: {capture}')

    args: dict[str, t.Any] = {}
    if timeout:
        args['timeout'] = timeout
    if capture:
        args['capture_output'] = True
    else:
        args['stdin'] = sys.stdin
        args['stdout'] = sys.stdout
        args['stderr'] = sys.stderr

    result = orig_run(cmd, shell=True, text=True, cwd=Path.cwd(), **args)

    if check_err and result.returncode != 0:
        l.e(f'Command return isn\'t 0: {result.returncode}\n{result.stderr.strip()}')
        exit(result.returncode)

    return result.stdout.strip() if capture else ''


class _get_pr_ret:
    branch: str | None
    owner: str | None
    repo: str | None


def get_pr(pr_num: int) -> _get_pr_ret:
    j: dict = json.loads(run(f"gh pr view {pr_num} --json headRefName,headRepositoryOwner,headRepository"))
    r = _get_pr_ret()
    r.branch = j.get('headRefName')
    r.owner = j.get('headRepositoryOwner')
    r.repo = j.get('headRepository')
    return r


class Old_Args(argparse.Namespace):
    verbose: bool = False
    dry_run: bool = False
    help: bool = False

    pr_number: int | None = None
    force: bool = False
    subcommand: str | None = None
    passthrough: list[str] = []


def old_parse_args() -> Old_Args:
    """
    完全适配 `gh p` 扩展，完美解决：
    - 任意未知子命令自动透传给官方 gh pr
    - gh p checkout 不带参数时显示官方帮助
    - gh p 125 自动识别为 push
    """
    print(sys.argv)
    # 第一步：快速判断是否直接透传
    if len(sys.argv) <= 1:
        # 只有 gh p 或者 gh p -h
        return Old_Args(subcommand='', help=True)

    first_arg = sys.argv[1]

    # 情况1：用户直接输入数字 → 自动当成 push
    if first_arg.isdigit():
        return Old_Args(
            subcommand="push",
            pr_number=int(first_arg),
            force=False,
            verbose=False,
            dry_run=False,
            help=False,
            passthrough=[]
        )

    # 情况2：明确是我们支持的子命令（checkout / push）
    if first_arg in ["checkout", "co", "push", "ps", "-h", "--help"]:
        parser = argparse.ArgumentParser(
            # prog="gh p",
            description="Enhanced PR workflow: checkout & push",
            add_help=False,
        )
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("-f", "--force", action="store_true")
        parser.add_argument("-h", "--help", action="store_true")

        if first_arg in ["checkout", "co"]:
            parser.add_argument("pr_number", type=int, nargs="?")
            args = parser.parse_args()
            args.subcommand = "checkout"
            return args  # type: ignore

        elif first_arg in ["push", "ps"]:
            parser.add_argument("pr_number", type=int, nargs="?")
            args = parser.parse_args()
            args.subcommand = "push"
            return args  # type: ignore

        else:  # -h / --help
            return Old_Args(subcommand="passthrough", passthrough=["--help"])

    # 情况3：其他所有 → 直接透传给官方 gh pr
    else:
        return Old_Args(
            subcommand="passthrough",
            passthrough=sys.argv[1:]  # 把所有参数原样传给 gh pr
        )


def lstget(lst: list, key: int, default: t.Any = None) -> t.Any:
    try:
        return lst[key]
    except IndexError:
        return default


class Args:
    # command
    cmd: t.Literal[
        '',  # passthrough
        'checkout',
        'push'
    ] = ''

    # flags
    flag_help: t.Literal[
        '',  # not asking for help
        'general',
        'checkout',
        'push'
    ] = ''
    flag_verbose: bool = False

    # params / args
    all_others: list[str] = []  # All
    params: list[str] = []  # checkout, push
    args: list[str] = []  # --help, --verbose, -h, -v

    # special
    pr_number: int | None = None  # checkout, push


def parse_args() -> Args:
    r = Args()

    # extract verbose flag
    local_flag_help = False
    for i in sys.argv[1:]:
        if i in ['--verbose', '-v']:
            r.flag_verbose = True
            l.is_verbose = True
            l.verbose('[parse] Verbose mode enabled')
        elif i in ['--help', '-h']:
            local_flag_help = True

        # split params
        if i.startswith('-'):
            r.args.append(i)
        else:
            r.params.append(i)
        r.all_others.append(i)

    l.verbose(f'[parse] args: {r.args}')
    l.verbose(f'[parse] params: {r.params}')
    l.verbose(f'[parse] all_others: {r.all_others}')

    # general help if no args
    if len(r.params) == 0:
        r.flag_help = 'general'
        l.verbose('[parse] set flag_help -> general')
        return r

    # subcommands
    first_arg: str = lstget(r.params, 0, None)
    if first_arg in ['checkout', 'co', 'c']:
        # checkout
        r.cmd = 'checkout'
        l.verbose(f'[parse] set cmd -> checkout')
        if local_flag_help:
            r.flag_help = 'checkout'
            l.verbose('[parse] set flag_help -> checkout')
    elif first_arg in ['push', 'ps', 'p']:
        # push
        r.cmd = 'push'
        l.verbose(f'[parse] set cmd -> push')
        if local_flag_help:
            r.flag_help = 'push'
            l.verbose('[parse] set flag_help -> push')

    # param2 (pr_number)
    num: str = lstget(r.params, 1, '')
    if num.isdigit():
        r.pr_number = int(num)
        l.verbose(f'[parse] set pr_number -> {num}')

    # passthrough if no subcmd
    return r
