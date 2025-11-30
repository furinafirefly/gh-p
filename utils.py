# coding: utf-8

import re
from subprocess import run as orig_run, TimeoutExpired
from pathlib import Path
import sys
import json
import typing as t

import log as l
import config as c


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

    try:
        result = orig_run(cmd, shell=True, text=True, cwd=Path.cwd(), **args)
    except TimeoutExpired:
        l.e(f'Command {cmd} expired after {timeout} seconds!')
        exit(3)

    if check_err and result.returncode != 0:
        l.e(f'Command {cmd} return isn\'t 0: {result.returncode}')
        if capture:
            print(result.stderr.strip())
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
    r.owner = j.get('headRepositoryOwner', {}).get('login')
    r.repo = j.get('headRepository', {}).get('name')
    return r


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
    if first_arg in c.aliases['checkout']:
        # checkout
        r.cmd = 'checkout'
        l.verbose(f'[parse] set cmd -> checkout')
        if local_flag_help:
            r.flag_help = 'checkout'
            l.verbose('[parse] set flag_help -> checkout')
    elif first_arg in c.aliases['push']:
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


def extract_pr_number_from_branch(name: str) -> int | None:
    for pattern, strict in c.pr_branch_matches:
        regex = pattern.format(
            number=r'(\d+)'
        )

        if regex.endswith('-*'):
            regex = regex[:-2] + r'-\d*[^\d].*'
        elif '*' in regex:
            regex = regex.replace('*', '.*')

        if strict:
            if not regex.startswith('^'):
                regex = f'^{regex}'
            if not regex.endswith('$'):
                regex = f'{regex}$'

        l.v(f'[extract] try {pattern} (strict: {strict}) -> regex: {regex}')

        match = re.search(regex, name)
        if match:
            try:
                l.v(f'[extract] matched: {match.group(1)}')
                return int(match.group(1))
            except (IndexError, ValueError):
                pass

    l.v('[extract] failed to extranch pr from branch name')
    return


def detect_pr_number_from_gh_checkout_ref() -> int | None:
    try:
        curr_commit = run("git rev-parse HEAD", check_err=False).strip()
        if not curr_commit:
            l.verbose(f'[detect] no commit found')
            return
        l.verbose(f'[detect] current commit: {curr_commit}')

        output = run('git for-each-ref --format="%(refname) %(objectname)"')
        for line in output.splitlines():
            if not line.strip():
                continue
            refname, commit = line.strip().split(' ', 1)
            if commit == curr_commit:
                if m := re.search(r'refs/pull/(\d+)/head', refname):
                    l.verbose(f'[detect] found: {m.group(1)}')
                    return int(m.group(1))
    except Exception as e:
        l.verbose(f'[detect] failed: {e}')

    return None


def guess_pr() -> int | None:
    # try to get from ref
    ret = None
    ret = detect_pr_number_from_gh_checkout_ref()
    l.verbose(f'[guess] detect return: {ret}')

    if not ret:
        # try to get from branch
        branch = run("git rev-parse --abbrev-ref HEAD").strip()
        ret = extract_pr_number_from_branch(branch)
        l.verbose(f'[guess] extract return: {ret}')

    return ret
