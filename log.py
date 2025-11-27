# coding: utf-8

from __future__ import annotations
from sys import stderr

# to control verbose()
global is_verbose
is_verbose: bool = False


class c:
    # Colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    WHITE = "\033[97m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def info(msg: str):
    print(f"{c.GREEN}[Info]{c.RESET} {msg}")


def warning(msg: str):
    print(f"{c.YELLOW}[Warning]{c.RESET} {msg}", file=stderr)


def error(msg: str):
    print(f"{c.RED}[Error]{c.RESET} {msg}", file=stderr)


def success(msg: str):
    print(f"{c.GREEN}[Success]{c.RESET} {msg}")


def verbose(msg: str):
    if is_verbose:
        print(f"{c.GREEN}[Verbose]{c.RESET} {msg}")

# idk why i did this
i = info
w = warning
e = error
s = success
v = verbose
