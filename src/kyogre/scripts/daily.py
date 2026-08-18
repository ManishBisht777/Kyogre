#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AGENT_DIR = SCRIPT_DIR.parent
PORTFOLIO_REPO = Path("/Users/manishbisht/Desktop/dev/manish/portfolio")
BLOG_DIR = PORTFOLIO_REPO / "public" / "blogs"

print("=" * 32)
print(" Personal Blog Agent")
print("=" * 32)

print("\n1. Collecting commits...")
subprocess.run(
    ["uv", "run", "python", str(AGENT_DIR / "tools/collect_commits.py")],
    cwd=AGENT_DIR,
    check=True,
)

print("\n2. Collecting diffs...")
subprocess.run(
    ["uv", "run", "python", str(AGENT_DIR / "tools/collect_diffs.py")],
    cwd=AGENT_DIR,
    check=True,
)

print("\n3. Running Claude...")

prompt = """
You are my personal engineering blog agent.

Read these files first:

temp/commits.md
temp/diffs.md

Analyze today's GitHub activity.

Determine whether there is a genuinely valuable
technical story.

Ignore:
- typo fixes
- README changes
- dependency updates
- variable renames
- trivial refactors
- simple UI changes

Prefer:
- difficult debugging
- architectural decisions
- interesting implementations
- performance improvements
- AI/LLM experiments
- failures
- tradeoffs
- unexpected technical problems
- useful engineering lessons

If the work is NOT blog-worthy:

Do not create anything inside drafts/.
Simply report that there is no suitable blog.

If the work IS blog-worthy:

Create exactly one Markdown file inside:

drafts/

Use a descriptive slug, for example:

drafts/building-a-reliable-ai-agent.md

The article must be based ONLY on:
- temp/commits.md
- temp/diffs.md
- the actual repository code when necessary

Do not invent:
- metrics
- users
- production usage
- benchmarks
- technologies
- implementation details

The article should explain:

1. Context
2. Problem
3. What was tried
4. What failed
5. Final solution
6. Technical reasoning
7. Lessons learned

After writing the article, review it for accuracy.

Do NOT publish it.
Do NOT modify the portfolio repository.
Do NOT delete anything.
"""

result = subprocess.run(
    ["claude", "--permission-mode", "acceptEdits", "-p", prompt],
    cwd=AGENT_DIR,
    check=True,
)

print("\n4. Checking generated drafts...")

drafts_dir = AGENT_DIR / "drafts"
draft_files = list(drafts_dir.glob("*.md")) if drafts_dir.exists() else []

if not draft_files:
    print("No blog was generated.")
    (AGENT_DIR / "temp" / "commits.md").unlink(missing_ok=True)
    (AGENT_DIR / "temp" / "diffs.md").unlink(missing_ok=True)
    sys.exit(0)

if len(draft_files) > 1:
    print("ERROR: Claude generated more than one draft.")
    print("Keeping everything for manual inspection.")
    sys.exit(1)

draft = draft_files[0]
draft_filename = draft.name
print(f"Draft found: {draft_filename}")

print("\n5. Checking portfolio repository...")
os.chdir(PORTFOLIO_REPO)

result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if result.stdout.strip():
    print("ERROR: Portfolio repository has uncommitted changes.")
    print(result.stdout)
    sys.exit(1)

print("\n6. Copying blog...")
blog_dest = BLOG_DIR / draft_filename
import shutil
shutil.copy(draft, blog_dest)

print("\n7. Creating branch...")
branch_name = f"blog/{draft_filename[:-3]}"
subprocess.run(["git", "checkout", "-b", branch_name], check=True)

print("\n8. Checking changes...")
result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
if len(changed_files) != 1:
    print("ERROR: Unexpected files changed.")
    print(result.stdout)
    sys.exit(1)

print("\n9. Committing...")
subprocess.run(["git", "add", str(blog_dest)], check=True)
subprocess.run(
    ["git", "commit", "-m", f"docs: add {draft_filename[:-3]}"],
    check=True,
)

print("\n10. Pushing...")
subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

print("\n11. Creating PR to master...")
subprocess.run(
    ["gh", "pr", "create",
     "--base", "master",
     "--head", branch_name,
     "--title", f"docs: add {draft_filename[:-3]}",
     "--body", "Auto-generated blog post from today's commits."],
    check=True,
)

print("\n12. Publishing succeeded.")
os.chdir(AGENT_DIR)

draft.unlink()
(AGENT_DIR / "temp" / "commits.md").unlink(missing_ok=True)
(AGENT_DIR / "temp" / "diffs.md").unlink(missing_ok=True)

print("\n" + "=" * 32)
print(" SUCCESS")
print("=" * 32)
print(f"Blog: {draft_filename}")
print(f"Branch: {branch_name}")
print("Draft removed.")
