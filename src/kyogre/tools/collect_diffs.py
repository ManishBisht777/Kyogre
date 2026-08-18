import os

import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_commit(repo_full_name, sha):
    response = requests.get(
        f"https://api.github.com/repos/{repo_full_name}/commits/{sha}",
        headers=HEADERS,
    )

    response.raise_for_status()

    return response.json()


def main():
    with open("temp/commits.md") as file:
        content = file.read()

    lines = content.splitlines()

    commits = []

    current_repo = None
    current_sha = None

    for line in lines:
        if line.startswith("## "):
            current_repo = line[3:].strip()

        if line.startswith("**SHA:**"):
            current_sha = (
                line.split("`")[1]
            )

            commits.append({
                "repo": current_repo,
                "sha": current_sha,
            })

    with open("temp/diffs.md", "w") as file:
        file.write("# GitHub Diffs\n\n")

        for commit in commits:
            data = get_commit(
                commit["repo"],
                commit["sha"],
            )

            file.write(
                f"## {commit['repo']}\n\n"
                f"### Commit `{commit['sha']}`\n\n"
            )

            file.write(
                f"**Message:** "
                f"{data['commit']['message']}\n\n"
            )

            for changed_file in data.get("files", []):
                filename = changed_file["filename"]
                patch = changed_file.get(
                    "patch",
                    "Patch unavailable",
                )

                file.write(
                    f"### `{filename}`\n\n"
                    f"```diff\n"
                    f"{patch}\n"
                    f"```\n\n"
                )

            file.write("---\n\n")


if __name__ == "__main__":
    main()