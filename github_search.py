#!/usr/bin/env python3
"""Sneaky GitHub terminal search with an ASCII status interface."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# GitHub names, titles, and descriptions may contain any Unicode character. On
# legacy Windows terminals, escaping unsupported characters preserves a usable
# ASCII result instead of raising UnicodeEncodeError.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(errors="backslashreplace")

API = "https://api.github.com/search/{kind}?q={query}&per_page={limit}"
STATUS_TIMEOUT_SECONDS = 4

BANNER = r"""
   ____  _   _ _____    _    _  ______   __
  / ___|| \ | | ____|  / \  | |/ /\ \ \ / /
  \___ \|  \| |  _|   / _ \ | ' /  \ \ V /
   ___) | |\  | |___ / ___ \| . \   | || |
  |____/|_| \_|_____/_/   \_\_|\_\  |_|\_|
"""


def visible(value: Any) -> str:
    """Render untrusted API text as printable ASCII, avoiding terminal controls."""
    return "".join(char if char == "\n" or 32 <= ord(char) < 127 else f"\\u{ord(char):04x}" for char in str(value or ""))


def color(text: str, code: str) -> str:
    text = visible(text)
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def line(char: str = "-") -> str:
    return char * min(shutil.get_terminal_size((100, 24)).columns, 100)


def fetch_text(url: str) -> str:
    headers = {"User-Agent": "sneaky-github-search"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=STATUS_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8", errors="replace").strip()


def status_line() -> str:
    """Return best-effort public network and weather status without blocking search."""
    try:
        public_ip = fetch_text("https://api.ipify.org")
        location_text = fetch_text(f"https://ipapi.co/{urllib.parse.quote(public_ip)}/json/")
        location = json.loads(location_text)
        country = location.get("country_name") or location.get("country") or "Unknown"
        weather_text = fetch_text(f"https://wttr.in/{urllib.parse.quote(country)}?format=%C+%t")
        weather = weather_text or "Unavailable"
        return f"  STATUS  |  PUBLIC IP: {public_ip}  |  COUNTRY: {country}  |  WEATHER: {weather}"
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return "  STATUS  |  PUBLIC IP / COUNTRY / WEATHER: unavailable"


def request(kind: str, query: str, limit: int, token: str | None) -> dict[str, Any]:
    url = API.format(kind=kind, query=urllib.parse.quote(query), limit=limit)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-search-cli",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        try:
            message = json.loads(details).get("message", details)
        except json.JSONDecodeError:
            message = details
        raise RuntimeError(f"GitHub returned HTTP {error.code}: {message}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not reach GitHub: {error.reason}") from error


def clip(value: Any, width: int = 90) -> str:
    text = " ".join(str(value or "").split())
    return textwrap.shorten(visible(text), width=width, placeholder=" ...") or "No description provided."


def print_repo(item: dict[str, Any], index: int) -> None:
    stars = item.get("stargazers_count", 0)
    lang = item.get("language") or "Unknown"
    print(color(f"[{index:02d}] ", "36") + color(item["full_name"], "1;97") + color(f"  * {stars:,}  {lang}", "33"))
    print(f"     {clip(item.get('description'))}")
    print(color(f"     {item['html_url']}", "2"))


def print_code(item: dict[str, Any], index: int) -> None:
    repo = item.get("repository", {}).get("full_name", "unknown repository")
    print(color(f"[{index:02d}] ", "36") + color(item.get("name", "untitled"), "1;97") + color(f"  in {repo}", "33"))
    print(color(f"     {item.get('html_url', '')}", "2"))


def print_issue(item: dict[str, Any], index: int) -> None:
    kind = "PR" if "pull_request" in item else "Issue"
    print(color(f"[{index:02d}] ", "36") + color(item.get("title", "Untitled"), "1;97") + color(f"  {kind} #{item.get('number')}", "33"))
    print(f"     {clip(item.get('body'))}")
    print(color(f"     {item.get('html_url', '')}", "2"))


def print_user(item: dict[str, Any], index: int) -> None:
    print(color(f"[{index:02d}] ", "36") + color(item.get("login", "unknown"), "1;97") + color(f"  {item.get('type', 'User')}", "33"))
    print(color(f"     {item.get('html_url', '')}", "2"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Search GitHub from the Sneaky terminal UI.")
    parser.add_argument("query", nargs="*", help="GitHub search query, including qualifiers")
    parser.add_argument("--type", choices=("repositories", "code", "issues", "users"), default="repositories", dest="kind")
    parser.add_argument("--limit", type=int, default=10, help="Results to show, from 1 to 100 (default: 10)")
    parser.add_argument("--token", help="GitHub token. Defaults to GITHUB_TOKEN.")
    parser.add_argument("--no-banner", action="store_true", help="Hide the ASCII banner")
    parser.add_argument("--no-status", action="store_true", help="Hide public IP, country, and weather status")
    args = parser.parse_args()

    if not args.query:
        parser.error("provide a search query, for example: github_search.py 'public IP'")
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")

    query = " ".join(args.query)
    if not args.no_banner:
        print(color(BANNER, "35"))
    print(color(line(), "35"))
    print(color("  SNEAKY GITHUB SEARCH", "1;35") + f"  |  {args.kind.upper()}  |  {visible(query)}")
    if not args.no_status:
        print(color(status_line(), "2"))
    print(color(line(), "35"))

    try:
        payload = request(args.kind, query, args.limit, args.token or os.getenv("GITHUB_TOKEN"))
    except RuntimeError as error:
        print(color(f"Error: {error}", "31"), file=sys.stderr)
        return 1

    total = payload.get("total_count", 0)
    items = payload.get("items", [])
    print(color(f"  Found {total:,} result{'s' if total != 1 else ''}. Showing {len(items)}.", "2"))
    print()
    renderers = {"repositories": print_repo, "code": print_code, "issues": print_issue, "users": print_user}
    for index, item in enumerate(items, 1):
        renderers[args.kind](item, index)
        print()
    if not items:
        print("No matching results.")
    print(color(line(), "35"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
