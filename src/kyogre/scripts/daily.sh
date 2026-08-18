#!/bin/bash

set -euo pipefail

AGENT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORTFOLIO_REPO="/Users/manishbisht/Desktop/dev/manish/portfolio"
BLOG_DIR="$PORTFOLIO_REPO/public/blogs"
cd "$AGENT_DIR"

echo "================================"
echo " Personal Blog Agent"
echo "================================"

echo ""
echo "1. Collecting commits..."

uv run python tools/collect_commits.py

echo ""
echo "2. Collecting diffs..."

uv run python tools/collect_diffs.py

echo ""
echo "3. Running Claude..."

claude --permission-mode acceptEdits -p "
You are my personal engineering blog agent.

Read:

temp/commits.md
temp/diffs.md

Analyze today's GitHub activity.

Determine whether there is a genuinely valuable
technical story.

Ignore trivial changes.

Prefer:
- difficult debugging
- architectural decisions
- interesting implementations
- performance improvements
- AI/LLM experiments
- failures
- tradeoffs
- useful engineering lessons

If the work is NOT blog-worthy:

Do not create a draft.

If the work IS blog-worthy:

Create exactly one Markdown file inside:

drafts/

The article should contain:

1. Context
2. Problem
3. What was tried
4. What failed
5. Final solution
6. Technical reasoning
7. Lessons learned

Use only information supported by the GitHub
activity and repository.

Do not invent metrics, users, production usage,
benchmarks, technologies, or implementation details.

Review the article for technical accuracy.

Do NOT publish anything.
Do NOT modify the portfolio repository.
"

echo ""
echo "4. Checking drafts..."

DRAFT_COUNT=$(find drafts -maxdepth 1 -type f -name "*.md" | wc -l | tr -d ' ')

if [ "$DRAFT_COUNT" -eq 0 ]; then
    echo "No blog-worthy work today."

    rm -f temp/commits.md
    rm -f temp/diffs.md

    exit 0
fi

if [ "$DRAFT_COUNT" -gt 1 ]; then
    echo "ERROR: More than one draft generated."
    exit 1
fi

DRAFT=$(find drafts -maxdepth 1 -type f -name "*.md" | head -n 1)

BLOG_FILENAME=$(basename "$DRAFT")

echo ""
echo "Draft:"
echo "$BLOG_FILENAME"

echo ""
echo "5. Checking portfolio repository..."

cd "$PORTFOLIO_REPO"

if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Portfolio repository has uncommitted changes."
    git status --short
    exit 1
fi

echo ""
echo "6. Copying blog..."

cp "$AGENT_DIR/$DRAFT" "$BLOG_DIR/$BLOG_FILENAME"

echo ""
echo "7. Creating branch..."

BRANCH_NAME="blog/${BLOG_FILENAME%.md}"

git checkout -b "$BRANCH_NAME"

echo ""
echo "8. Checking changes..."

CHANGED_FILE_COUNT=$(git status --short | wc -l | tr -d ' ')

if [ "$CHANGED_FILE_COUNT" -ne 1 ]; then
    echo "ERROR: Unexpected files changed."
    git status --short
    exit 1
fi

echo ""
echo "9. Committing..."

git add "$BLOG_DIR/$BLOG_FILENAME"

git commit \
    -m "docs: add ${BLOG_FILENAME%.md}"

echo ""
echo "10. Pushing..."

git push -u origin "$BRANCH_NAME"

echo ""
echo "11. Creating PR to master..."

gh pr create \
    --base master \
    --head "$BRANCH_NAME" \
    --title "docs: add ${BLOG_FILENAME%.md}" \
    --body "Auto-generated blog post from today's commits."

echo ""
echo "12. Publishing succeeded."

cd "$AGENT_DIR"

rm "$DRAFT"
rm -f temp/commits.md
rm -f temp/diffs.md

echo ""
echo "================================"
echo " SUCCESS"
echo "================================"
echo "Blog: $BLOG_FILENAME"
echo "Branch: $BRANCH_NAME"
echo "Draft removed."