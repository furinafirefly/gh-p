# coding: utf-8

from log import c

general: str = f'''
{c.BOLD}{c.CYAN}gh-p - GitHub Pull Request Enhanced Tool{c.RESET}

{c.BOLD}Description{c.RESET}
  Enhanced GitHub CLI extension for streamlined Pull Request workflows.
  Provides intelligent PR checkout and push capabilities with automatic
  remote management.

{c.BOLD}Usage{c.RESET}
  {c.WHITE}gh p <command> [pr-number] [flags]{c.RESET}

{c.BOLD}Commands{c.RESET}
  {c.GREEN}checkout (check|chk|co|c){c.RESET}    Checkout PR to local branch with formatted name
  {c.GREEN}push (ps|p){c.RESET}                  Push changes to PR branch with auto remote setup
  {c.YELLOW}[any other gh pr command]{c.RESET}    Pass through to original gh pr

{c.BOLD}Examles{c.RESET}
  {c.WHITE}gh p checkout 123{c.RESET}          # Checkout PR #123 to local branch
  {c.WHITE}gh p push 456{c.RESET}              # Push to PR #456
  {c.WHITE}gh p push{c.RESET}                  # Push to current PR (auto-detected)
  {c.WHITE}gh p list{c.RESET}                  # Pass through to 'gh pr list'

{c.BOLD}Flags{c.RESET}
  {c.WHITE}-h, --help{c.RESET}          Show help (general or command-specific)
  {c.WHITE}-v, --verbose{c.RESET}       Enable verbose output for debugging

{c.BOLD}Configuration{c.RESET}
  Edit config.py to customize:
  • Local branch naming format
  • PR number extraction patterns  
  • Remote URL format (HTTPS/SSH)
  • Command aliases

{c.BOLD}The Open-source repository address for this project{c.RESET}
  {c.WHITE}https://github.com/wyf9/gh-p{c.RESET}
'''[1:-1]

checkout: str = f'''
{c.BOLD}{c.CYAN}gh p checkout - Checkout Pull Request to Local Branch{c.RESET}

{c.BOLD}DESCRIPTION{c.RESET}
  Checkout a GitHub Pull Request to a locally formatted branch name.
  Automatically formats the branch name according to your configuration.

{c.BOLD}USAGE{c.RESET}
  {c.WHITE}gh p checkout <pr-number> [flags]{c.RESET}

{c.BOLD}PARAMETERS{c.RESET}
  {c.GREEN}pr-number{c.RESET}          GitHub Pull Request number (required)

{c.BOLD}EXAMPLES{c.RESET}
  {c.WHITE}gh p checkout 123{c.RESET}           # Checkout PR #123
  {c.WHITE}gh p co 456{c.RESET}                 # Using alias
  {c.WHITE}gh p checkout 789 --verbose{c.RESET} # With verbose output

{c.BOLD}BEHAVIOR{c.RESET}
  1. Fetches PR information from GitHub
  2. Creates local branch with format: {c.YELLOW}gh-pull-{{number}}{c.RESET}
  3. Checks out the branch for development

{c.BOLD}CONFIGURATION{c.RESET}
  • Branch format: {c.WHITE}pr_branch_format{c.RESET} in config.py
  • Default: {c.YELLOW}"gh-pull-{{number}}"{c.RESET}
'''[1:-1]

push: str = f'''
{c.BOLD}{c.CYAN}gh p push - Push Changes to Pull Request Branch{c.RESET}

{c.BOLD}DESCRIPTION{c.RESET}
  Push local changes to a Pull Request branch with automatic remote setup.
  Handles temporary remote configuration and cleanup.

{c.BOLD}USAGE{c.RESET}
  {c.WHITE}gh p push [pr-number] [flags]{c.RESET}

{c.BOLD}PARAMETERS{c.RESET}
  {c.GREEN}pr-number{c.RESET}         GitHub Pull Request number (optional)
                    If omitted, attempts auto-detection from:
                    • Current branch name patterns
                    • GitHub checkout references

{c.BOLD}EXAMPLES{c.RESET}
  {c.WHITE}gh p push 123{c.RESET}              # Push to PR #123
  {c.WHITE}gh p push{c.RESET}                  # Auto-detect PR number
  {c.WHITE}gh p ps 456 --force{c.RESET}        # Using alias with force push

{c.BOLD}BEHAVIOR{c.RESET}
  1. Detects or validates PR number
  2. Fetches PR info (branch, owner, repo)
  3. Configures temporary remote repository
  4. Pushes current HEAD to PR branch
  5. Cleans up temporary remote

{c.BOLD}AUTO-DETECTION{c.RESET}
  PR number is automatically detected from:
  • Branch names matching: {c.YELLOW}gh-pull-*{c.RESET}, {c.YELLOW}gh-*{c.RESET}, etc.
  • GitHub's special pull refs ({c.WHITE}refs/pull/*/head{c.RESET})
  • Configure patterns in {c.WHITE}pr_branch_matches{c.RESET}

{c.BOLD}CONFIGURATION{c.RESET}
  • Remote URL: {c.WHITE}remote_url{c.RESET} in config.py (HTTPS/SSH)
  • Temp remote name: {c.WHITE}temp_remote_name{c.RESET}
  • Branch matching: {c.WHITE}pr_branch_matches{c.RESET}
'''[1:-1]