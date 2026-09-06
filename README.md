# Sneaky GitHub Search

A dependency-free Python terminal tool for searching GitHub with a **Sneaky ASCII interface**, public-IP location, and local weather status.

## Requirements

* Windows, macOS, or Linux
* Python 3.10 or newer
* An internet connection

Check that Python is available:

```powershell
python --version
```

## Run it on Windows

1. Open PowerShell.
2. Move into the project folder:

```powershell
cd C:\Users\office\Downloads\github
```

3. Search GitHub repositories:

```powershell
python .\github_search.py "public IP"
```

You will see the Sneaky ASCII header, a status line with your public IP, inferred country, and country weather, followed by matching repositories with their description, stars, language, and GitHub URL.

## Search Examples

### Popular Python Machine-Learning Repositories

```powershell
python .\github_search.py "machine learning stars:>50000 language:python" --limit 5
```

### Search Source Code

```powershell
python .\github_search.py "TODO repo:microsoft/vscode" --type code
```

### Search Open Issues and Pull Requests

```powershell
python .\github_search.py "is:open label:bug" --type issues
```

### Search GitHub Accounts

```powershell
python .\github_search.py "octocat" --type users
```

## Optional: Increase the GitHub API Limit

The tool works without an account, but GitHub limits anonymous API requests.

To increase the limit, create a **fine-grained GitHub personal access token**, then set it for the current PowerShell window:

```powershell
$env:GITHUB_TOKEN = "github_pat_your_token_here"
python .\github_search.py "public IP"
```

The GitHub token is sent only to `api.github.com`.

**Never paste a real token into the README or commit it to a repository.**

## Public IP, Location, and Weather

The status line uses:

* `api.ipify.org` to determine your public IP address
* `ipapi.co` to infer your country
* `wttr.in` to retrieve weather information

These requests are **best effort**. GitHub search will still work if one or more of these services are unavailable.

To hide the status line:

```powershell
python .\github_search.py "public IP" --no-status
```

## Options

```text
--type {repositories,code,issues,users}
--limit 1..100
--token TOKEN
--no-banner
--no-status
```

### `--type`

Choose what GitHub searches:

```powershell
--type repositories
--type code
--type issues
--type users
```

### `--limit`

Control the number of results:

```powershell
python .\github_search.py "python" --limit 10
```

The allowed range is **1–100**.

### `--token`

Provide a GitHub token directly:

```powershell
python .\github_search.py "python" --token YOUR_TOKEN
```

Using the `GITHUB_TOKEN` environment variable is recommended instead so the token does not appear in your command history.

### `--no-banner`

Hide the Sneaky ASCII banner:

```powershell
python .\github_search.py "python" --no-banner
```

### `--no-status`

Hide the public-IP, location, and weather status:

```powershell
python .\github_search.py "python" --no-status
```

## Built-in Help

To view all available options:

```powershell
python .\github_search.py --help
```

## Features

* 🔎 GitHub repository search
* 💻 Source-code search
* 🐛 Issue and pull-request search
* 👤 GitHub user search
* ⭐ Repository stars
* 🧑‍💻 Primary programming language
* 🌐 Public-IP detection
* 📍 Country detection
* 🌤️ Local weather information
* 🎨 Sneaky ASCII terminal interface
* 📦 No third-party Python dependencies
* 🪟 Windows, macOS, and Linux support

## Privacy

Sneaky uses external services to provide its status information:

* **GitHub API** — GitHub searches
* **ipify** — public IP detection
* **ipapi.co** — approximate country/location information
* **wttr.in** — weather information

The public IP is displayed locally by the application and is used by the location service to infer your country.

GitHub authentication tokens should be kept private and should never be committed to source control.

## License

Add your project's license information here.

