#!/bin/bash

# Enhanced Daily Script with Iterative Blog Improvement
# If blog scores < 7, automatically rewrite until it passes
# Then update the prompt based on successful rewrites

set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/Users/manishbisht/.local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

AGENT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORTFOLIO_REPO="/Users/manishbisht/Desktop/dev/manish/portfolio"
BLOG_DIR="$PORTFOLIO_REPO/public/blogs"
cd "$AGENT_DIR"

echo "================================"
echo " Personal Blog Agent (With Auto-Improvement)"
echo " Run started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================"

echo ""
echo "1. Collecting commits..."
# KYOGRE_DATE overrides the default (today) to backfill missed days,
# e.g. KYOGRE_DATE=2026-08-21..2026-09-04
uv run python tools/collect_commits.py ${KYOGRE_DATE:-}

echo ""
echo "2. Collecting diffs..."
uv run python tools/collect_diffs.py

echo ""
echo "3. Running Claude..."

# Titles already live on the portfolio, so a backfill spanning several days
# does not re-tell a story that has been published (by this agent or by hand).
PUBLISHED_TITLES=$(grep -h "^title:" "$BLOG_DIR"/*.md 2>/dev/null | sed 's/^title: *//' || true)

claude --permission-mode acceptEdits -p "
You are my personal engineering blog agent.

Read:

temp/commits.md
temp/diffs.md

Analyze the GitHub activity in those files. It may span a single day or
several days.

ALREADY PUBLISHED - do not re-tell these stories:
$PUBLISHED_TITLES

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

Create one Markdown file inside drafts/ per distinct technical story.

Usually that is exactly one file. If the activity covers several
genuinely unrelated efforts, write one file per story, at most 3.
Never split a single story across files, and never pad the count -
one strong post beats three thin ones.

The article MUST start with YAML frontmatter:

---
title: [Generate a compelling title]
description: [One-line summary of the technical insight]
date: $(date +%Y-%m-%d)
author: Manish Bisht
tags: [kyogre, ai-generated, <generate 2-5 topic tags based on actual content>]
source: autonomous
reading_time: [estimate 1-2 minutes per 300 words]
---

Then the article should contain:

1. Context
2. Problem
3. What was tried
4. What failed
5. Final solution
6. Technical reasoning
7. Lessons learned

IMPORTANT TAGGING RULES:
- ALWAYS include these fixed tags: 'kyogre', 'ai-generated'
- THEN analyze the blog content and add 2-5 topic tags that match what the article is actually about
- Available topic tags (use ONLY if the content matches):
  * debugging (if article discusses troubleshooting/debugging)
  * architecture (if discusses architectural decisions/design)
  * performance (if discusses performance optimization/improvements)
  * ai-llm (if AI/LLM/ML related work)
  * lessons-learned (if article teaches lessons/insights)
  * implementations (if shows code patterns/techniques)
  * tradeoffs (if discusses design tradeoffs)
  * refactoring (if discusses refactoring work)
  * testing (if testing/test coverage related)
  * security (if security/vulnerability related)
- Use lowercase, hyphenated tags
- Do NOT include tags that don't match the content
- Select only the tags that are truly relevant to this specific blog post

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

echo "Drafts to process: $DRAFT_COUNT"

# Function to evaluate blog and extract score
evaluate_blog() {
    local blog_file="$1"
    local eval_output=$(uv run python tools/reference_analyzer.py evaluate-blog "$blog_file" 2>&1)
    local score=$(echo "$eval_output" | grep "Overall Score:" | awk -F'/' '{print $1}' | awk '{print $NF}')

    echo "$eval_output" >&2
    echo "$score"
}

PUBLISHED_COUNT=0

# Everything below runs once per draft. Body is left unindented so the
# per-draft steps stay diffable against the single-draft version.
for DRAFT in drafts/*.md; do

DRAFT_NAME=$(basename "$DRAFT")

echo ""
echo "5. Evaluating $DRAFT_NAME..."

# Get initial score
SCORE=$(evaluate_blog "$DRAFT")
ITERATION=0
MAX_ITERATIONS=3

echo ""
echo "Initial Score: $SCORE/10"

# Save initial evaluation
mkdir -p evaluations
eval_timestamp=$(date +%Y%m%d_%H%M%S)
echo "$SCORE/10 (iteration 0)" > "evaluations/${DRAFT_NAME%.md}_${eval_timestamp}_scores.txt"

# Iterative improvement loop
while (( $(echo "$SCORE < 7.0" | bc -l) )); do
    ITERATION=$((ITERATION + 1))

    if [ "$ITERATION" -gt "$MAX_ITERATIONS" ]; then
        echo ""
        echo "⚠️  Reached max iterations ($MAX_ITERATIONS). Stopping."
        echo "Blog score: $SCORE/10 (below standard)"
        echo "Saving for manual review..."
        break
    fi

    echo ""
    echo "📝 Iteration $ITERATION: Rewriting blog to improve score..."

    # Get feedback
    eval_output=$(uv run python tools/reference_analyzer.py evaluate-blog "$DRAFT" 2>&1)
    feedback=$(echo "$eval_output" | grep "^  •" | cut -d' ' -f2- | head -3)

    # Rewrite with Claude
    claude --permission-mode acceptEdits -p "
The following blog post scored $SCORE/10. Improve it.

FEEDBACK:
$feedback

BLOG TO IMPROVE:
$(cat "$DRAFT")

INSTRUCTIONS:
1. Keep the same topic and structure
2. Address the feedback above
3. Improve writing quality
4. Keep frontmatter (title, description, etc)
5. Make it more engaging and clear

Output ONLY the improved blog (with frontmatter).
"

    # Re-evaluate
    SCORE=$(evaluate_blog "$DRAFT")
    echo "New Score: $SCORE/10"
    echo "$SCORE/10 (iteration $ITERATION)" >> "evaluations/${DRAFT_NAME%.md}_${eval_timestamp}_scores.txt"
done

echo ""
echo "6. Final evaluation..."

if (( $(echo "$SCORE >= 7.0" | bc -l) )); then
    echo "✅ Blog passes quality standard ($SCORE/10)"

    echo ""
    echo "7. Extracting successful prompt patterns..."

    # Extract what worked from successful rewrites
    {
        echo "# Successful Blog: $DRAFT_NAME"
        echo ""
        echo "Final Score: $SCORE/10"
        echo "Iterations: $ITERATION"
        echo ""
        echo "What worked:"
        uv run python tools/reference_analyzer.py evaluate-blog "$DRAFT" 2>&1 | grep -A 20 "Feedback:"
    } > "evaluations/${DRAFT_NAME%.md}_success.txt"

    echo ""
    echo "8. Updating prompt with successful patterns..."

    # Save successful patterns for prompt update
    {
        echo "# Prompt Improvements from Today's Blog"
        echo ""
        echo "Blog: $DRAFT_NAME (Score: $SCORE/10, Iterations: $ITERATION)"
        echo ""
        echo "Successful techniques that improved the blog:"
        cat "evaluations/${DRAFT_NAME%.md}_success.txt"
    } >> "evaluations/prompt_learnings.txt"

    echo "✅ Patterns saved for weekly prompt update"

else
    echo "⚠️  Blog below standard after $ITERATION iterations ($SCORE/10)"
    echo "Manual review needed"
fi

echo ""
echo "9. Checking portfolio repository..."

cd "$PORTFOLIO_REPO"

if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Portfolio repository has uncommitted changes."
    git status --short
    exit 1
fi

echo ""
echo "10. Copying blog..."

cp "$AGENT_DIR/$DRAFT" "$BLOG_DIR/$DRAFT_NAME"

echo ""
echo "11. Creating branch..."

# Branch from master, not from the branch a previous draft left us on,
# or the second PR would also contain the first blog.
git checkout master

BRANCH_NAME="blog/${DRAFT_NAME%.md}"
git checkout -b "$BRANCH_NAME"

echo ""
echo "12. Checking changes..."

CHANGED_FILE_COUNT=$(git status --short | wc -l | tr -d ' ')

if [ "$CHANGED_FILE_COUNT" -ne 1 ]; then
    echo "ERROR: Unexpected files changed."
    git status --short
    exit 1
fi

echo ""
echo "13. Committing..."

git add "$BLOG_DIR/$DRAFT_NAME"
git commit -m "docs: add ${DRAFT_NAME%.md}"

echo ""
echo "14. Pushing..."

git push -u origin "$BRANCH_NAME"

echo ""
echo "15. Creating PR..."

gh pr create \
    --base master \
    --head "$BRANCH_NAME" \
    --title "docs: add ${DRAFT_NAME%.md}" \
    --body "Auto-generated blog post from commits (${KYOGRE_DATE:-today}).

Quality Score: $SCORE/10
Status: $([ $(echo "$SCORE >= 7.0" | bc -l) -eq 1 ] && echo 'Passed' || echo 'Manual Review')"

echo ""
echo "16. Cleanup..."

cd "$AGENT_DIR"
rm "$DRAFT"

echo ""
echo "================================"
echo " PUBLISHED"
echo "================================"
echo "Blog: $DRAFT_NAME"
echo "Score: $SCORE/10"
if [ "$ITERATION" -gt 0 ]; then
    echo "Iterations: $ITERATION (auto-improved)"
fi
echo "Branch: $BRANCH_NAME"
echo "================================"

PUBLISHED_COUNT=$((PUBLISHED_COUNT + 1))

done
# end per-draft loop

# Leave the portfolio on master so the next run starts from a known branch.
git -C "$PORTFOLIO_REPO" checkout master

rm -f temp/commits.md
rm -f temp/diffs.md

echo ""
echo "================================"
echo " SUCCESS - $PUBLISHED_COUNT blog(s) published"
echo "================================"
