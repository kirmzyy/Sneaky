# Sneaky GitHub Search

A dependency-free Python terminal tool for searching GitHub with a Sneaky ASCII interface, public-IP location, and local weather status.

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer
- An internet connection

Check that Python is available:

powershell
python --version


## Run it on Windows

1. Open PowerShell.
2. Move into this folder:

   powershell
   cd C:\Users\office\Downloads\github

3. Search GitHub repositories:

   powershell
   python .\github_search.py "public IP"


You will see the Sneaky ASCII header, a status line with your public IP, inferred country, and country weather, then matching repositories with their description, stars, language, and GitHub URL.

## Search examples

powershell
# Popular Python machine-learning repositories
python .\github_search.py "machine learning stars:>50000 language:python" --limit 5

# Search source code
python .\github_search.py "TODO repo:microsoft/vscode" --type code

# Search open issues and pull requests
python .\github_search.py "is:open label:bug" --type issues

# Search GitHub accounts
python .\github_search.py "octocat" --type users


## Optional: increase the GitHub API limit

The tool works without an account, but GitHub limits anonymous API requests. To increase the limit, create a fine-grained GitHub personal access token, then set it for the current PowerShell window:

powershell
$env:GITHUB_TOKEN = "github_pat_your_token_here"
python .\github_search.py "public IP"


The GitHub token is sent only to `api.github.com`. Do not paste a real token into the README or commit it to a repository.

The status line uses `api.ipify.org` to read your public IP, `ipapi.co` to infer its country, and `wttr.in` for weather. These calls are best effort, and GitHub search still runs if they are unavailable. Use `--no-status` to hide the status line.

## Options

text
--type {repositories,code,issues,users}
--limit 1..100
--token TOKEN
--no-banner
--no-status

To view built-in help:

powershell
python .\github_search.py --help
