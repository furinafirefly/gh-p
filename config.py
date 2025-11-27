# coding: utf-8
# Fork / clone to modify (maybe) useless config

pr_branch_prefix: str = 'gh-pull-'
'''
Controls local branch prefix\n
e.g. `gh-pull` + `#125` -> `gh-pull-125`
'''

temp_remote_name: str = 'gh-pull-temp'
'''
Control remote name (for temp use)
'''

remote_url: str = 'https://github.com/{owner}/{repo}.git'
'''
Custom remote url\n
Placeholder: owner, repo\n
HTTPS: `https://github.com/{owner}/{repo}.git`\n
SSH: `git@github.com:{owner}/{repo}.git`
'''
