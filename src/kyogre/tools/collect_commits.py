import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]


def get_commits_by_user(username: str, token: str = None):
    """Search commits authored by `username` across all repos, committed today (UTC)."""
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    url = "https://api.github.com/search/commits"
    headers = {"Accept": "application/vnd.github.cloak-preview+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    query = f"author:{username} author-date:{today_str}"
    commits = []
    page = 1
    while True:
        params = {
            "q": query,
            "per_page": 100,
            "page": page,
            "sort": "author-date",
            "order": "desc",
        }
        resp = requests.get(url, headers=headers, params=params, timeout=30)

        if resp.status_code != 200:
            print(f"Error {resp.status_code}: {resp.json().get('message', resp.text)}")
            sys.exit(1)

        data = resp.json()
        items = data.get("items", [])
        commits.extend(items)

        if len(items) < 100 or len(commits) >= data.get("total_count", 0):
            break
        page += 1

    return commits


def main():
    commits_data = get_commits_by_user(GITHUB_USERNAME, GITHUB_TOKEN)

    commits = []
    for commit in commits_data:
        commits.append({
            "repository": commit["repository"]["full_name"],
            "sha": commit["sha"],
            "message": commit["commit"]["message"],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"],
        })

    os.makedirs("temp", exist_ok=True)

    with open("temp/commits.md", "w") as file:
        file.write("# GitHub Activity\n\n")

        for commit in commits:
            file.write(
                f"## {commit['repository']}\n\n"
                f"**SHA:** `{commit['sha']}`\n\n"
                f"**Message:** {commit['message']}\n\n"
                f"**Author:** {commit['author']}\n\n"
                f"**Date:** {commit['date']}\n\n"
                f"---\n\n"
            )

    print(f"Collected {len(commits)} commits")


if __name__ == "__main__":
    main()