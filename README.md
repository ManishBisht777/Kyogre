# Kyogre: Automated Technical Blog Generation

Kyogre is an automated system that intelligently discovers blog-worthy technical work from your daily GitHub activity and generates blog drafts, then creates pull requests for publication.

## Overview

Kyogre automates the discovery and documentation of your technical work by:

1. **Collecting commits** from your GitHub activity
2. **Analyzing diffs** to understand what changed
3. **Using Claude AI** to intelligently filter for blog-worthy content
4. **Generating blog drafts** in Markdown format
5. **Creating pull requests** to your portfolio repository for review

Unlike keyword-based filters, Kyogre uses Claude to understand the technical significance of your work and only generates drafts for genuinely interesting engineering problems, architectural decisions, and lessons learned.

## Architecture

```
GitHub Activity (commits)
        ↓
collect_commits.py (GitHub Search API)
        ↓
Commits stored in temp/commits.md
        ↓
collect_diffs.py (GitHub REST API)
        ↓
Diffs stored in temp/diffs.md
        ↓
daily.sh (orchestration)
        ↓
Claude AI (intelligent filtering)
        ↓
drafts/ (generated blog posts)
        ↓
Portfolio Repository (copy + commit + PR)
```

## Features

- **Intelligent Filtering**: Claude analyzes your work and decides if it's blog-worthy
- **Automated Workflow**: Runs daily at 11 PM (configurable)
- **Git Syncing**: Automatically pulls latest code from GitHub before running
- **PR-Based Publishing**: Creates PRs instead of auto-merging for your review
- **Environment Isolated**: Uses `.env` for sensitive configuration
- **Detailed Logging**: Full logs for debugging and monitoring

## Setup

### Prerequisites

- Python 3.12+
- `uv` package manager
- `claude` CLI installed
- Git repository initialized
- GitHub token for API access
- macOS (currently uses launchd for scheduling)

### Installation

1. **Clone the repository**:
```bash
git clone <repo-url>
cd kyogre
```

2. **Create `.env` file** with your credentials:
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=YourUsername
PORTFOLIO_PATH=/path/to/your/portfolio
```

Get your GitHub token from: https://github.com/settings/tokens
- Required scopes: `repo` (for accessing repositories), `public_repo` (for public activity)

3. **Install dependencies**:
```bash
uv sync
```

4. **Create required directories**:
```bash
mkdir -p drafts temp logs
```

## Configuration

### Environment Variables (`.env`)

```env
# Required: Your GitHub personal access token
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Required: Your GitHub username
GITHUB_USERNAME=ManishBisht777

# Required: Path to your portfolio repository
PORTFOLIO_PATH=/Users/yourname/Desktop/portfolio

# Optional: Blog directory in portfolio (default: public/blogs)
BLOG_DIR=$PORTFOLIO_PATH/public/blogs
```

### Scheduling (launchd on macOS)

The automation runs daily via launchd at 11 PM. To change the time:

```bash
nano ~/Library/LaunchAgents/com.manish.kyogre-blog-agent.plist
```

Edit the `StartCalendarInterval` section:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>23</integer>    <!-- Hour: 0-23 (23 = 11 PM) -->
    <key>Minute</key>
    <integer>0</integer>     <!-- Minute: 0-59 -->
</dict>
```

Then reload:
```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.manish.kyogre-blog-agent.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.manish.kyogre-blog-agent.plist
```

## Usage

### Manual Run

Run the blog generation manually:

```bash
./src/kyogre/scripts/daily.sh
```

Or the Python version:

```bash
python src/kyogre/scripts/daily.py
```

### Check Logs

View the last run's output:

```bash
# Full log
cat ~/.kyogre-logs/agent.log

# Errors only
cat ~/.kyogre-logs/agent-error.log

# Real-time monitoring
tail -f ~/.kyogre-logs/agent.log
```

### Check Scheduled Status

View the launchd schedule:

```bash
launchctl print gui/$(id -u)/com.manish.kyogre-blog-agent
```

### View Scheduled Time

```bash
launchctl print gui/$(id -u)/com.manish.kyogre-blog-agent | grep -A 10 "event triggers"
```

### Manually Trigger Run

Test the automation without waiting for 11 PM:

```bash
launchctl kickstart -k gui/$(id -u)/com.manish.kyogre-blog-agent
```

## How It Works

### 1. Collecting Commits (`collect_commits.py`)

- Uses GitHub Search API to find commits by `GITHUB_USERNAME` from today
- Filters to only your commits using advanced search: `author:<username> committer-date:>=YYYY-MM-DD`
- Stores commit messages and metadata in `temp/commits.md`
- Efficient: searches only today's activity instead of reading entire repository

### 2. Collecting Diffs (`collect_diffs.py`)

- For each commit found, fetches the full diff using GitHub REST API
- Stores diffs in `temp/diffs.md`
- Shows what changed in each commit (added lines, removed lines, file changes)

### 3. Claude Analysis (`daily.sh` → Claude)

Claude receives commits and diffs and determines if the work is blog-worthy:

**Ignores:**
- Typo fixes
- README changes
- Dependency updates
- Variable renames
- Trivial refactors
- Simple UI changes

**Prefers:**
- Difficult debugging and root cause analysis
- Architectural decisions and tradeoffs
- Interesting implementations and patterns
- Performance improvements and optimizations
- AI/LLM experiments and integrations
- Failures and what was learned
- Unexpected technical problems solved
- Useful engineering lessons

### 4. Draft Generation

If Claude determines the work is blog-worthy, it generates a Markdown file in `drafts/` with:

1. **Context** - What were you working on and why
2. **Problem** - What challenge did you face
3. **What was tried** - Initial approaches and solutions
4. **What failed** - Why earlier attempts didn't work
5. **Final solution** - What actually worked
6. **Technical reasoning** - Why this solution was chosen
7. **Lessons learned** - Key takeaways and insights

### 5. Portfolio Integration

If a draft was generated:

- Copy the blog post to your portfolio repository
- Create a feature branch: `blog/<slug-name>`
- Commit: `docs: add <blog-title>`
- Push to origin
- Create pull request to `master` branch
- Clean up the draft and temp files

## Directory Structure

```
kyogre/
├── src/kyogre/
│   ├── __init__.py
│   ├── tools/
│   │   ├── collect_commits.py      # Fetch commits from GitHub
│   │   └── collect_diffs.py        # Fetch diffs from GitHub
│   └── scripts/
│       ├── daily.sh                # Shell orchestration script
│       └── daily.py                # Python orchestration script
├── drafts/                         # Generated blog post drafts
├── temp/                          # Temporary files (commits.md, diffs.md)
├── logs/                          # Local logs (when run manually)
├── .env                           # Configuration (not in git)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Workflow Example

**8:00 PM** - You commit interesting architectural changes:
```
commit abc123
Author: You
Message: refactor: implement event-driven architecture for async tasks
```

**10:00 PM** - You push more improvements:
```
commit def456
Author: You
Message: feat: add distributed caching layer with Redis
```

**11:00 PM** - Kyogre runs:

1. Finds 2 commits from today
2. Fetches diffs showing architectural changes
3. Claude analyzes: "This is genuinely blog-worthy architectural work"
4. Generates: `drafts/event-driven-architecture-with-redis.md`
5. Creates PR: `blog/event-driven-architecture-with-redis` → master
6. You review the PR in the morning and merge if satisfied

## Automation Setup

### launchd Agent (macOS)

The automation is configured to run via macOS launchd at 11 PM daily.

**Agent configuration**: `~/Library/LaunchAgents/com.manish.kyogre-blog-agent.plist`

**Entry point**: `~/.kyogre-runner.py` (Python wrapper that syncs Git and runs daily.sh)

**Logs**: `~/.kyogre-logs/`

The wrapper handles:
- Git pull from origin/master (syncs changes from your working directory)
- Environment variable loading from `.env`
- Error handling and logging

### Git Syncing

Before each run, the automation:

1. `git pull origin master` - Gets latest code from GitHub
2. `git checkout HEAD -- .` - Updates working directory with latest files

This ensures your working directory changes (committed and pushed) are always used.

## Troubleshooting

### Issue: "No such file or directory: collect_commits.py"

**Cause**: Relative paths not resolving correctly

**Solution**: Paths are absolute in the wrapper, ensure `~/.kyogre-blog` exists and contains the project

### Issue: "GITHUB_TOKEN: KeyError"

**Cause**: `.env` file not found or not loaded

**Solution**: Ensure `.env` exists with `GITHUB_TOKEN=ghp_...`

### Issue: "No commits found"

**Cause**: No commits authored by you today, or GitHub API rate limited

**Solution**: Check GitHub activity for today, or run manually later

### Issue: "Permission denied" on script

**Cause**: Script not executable

**Solution**: 
```bash
chmod +x src/kyogre/scripts/daily.sh
```

### Issue: launchd says "not running"

**Cause**: Normal - scheduled jobs show "not running" between executions

**Solution**: This is expected. Job runs at 11 PM or when manually triggered with:
```bash
launchctl kickstart -k gui/$(id -u)/com.manish.kyogre-blog-agent
```

### Issue: PR not created

**Cause**: `gh` CLI not installed or not authenticated

**Solution**: 
```bash
# Install gh
brew install gh

# Authenticate
gh auth login

# Check status
gh auth status
```

### Issue: Portfolio repository has uncommitted changes

**Cause**: Stale changes in portfolio repo from previous run

**Solution**: Manually commit or revert changes in portfolio repo before next run

### Issue: "git pull" fails with permission error

**Cause**: launchd can't access SSH keys or credentials

**Solution**: 
1. Ensure GitHub token is in `.env` with full repo access
2. Or configure SSH key for automated access:
```bash
ssh-add ~/.ssh/id_rsa
```

## Logs

All automation activity is logged to `~/.kyogre-logs/`:

- **agent.log**: Standard output (successful runs)
- **agent-error.log**: Errors and debug output

Example log output:

```
================================
 Personal Blog Agent
================================

1. Collecting commits...
Collected 5 commits

2. Collecting diffs...

3. Running Claude...
[Claude analyzes work...]

4. Checking drafts...
Draft found: building-event-driven-systems.md

5. Checking portfolio repository...

6. Copying blog...

7. Creating branch...

8. Checking changes...

9. Committing...

10. Pushing...

11. Creating PR to master...
https://github.com/yourname/portfolio/pull/42

12. Publishing succeeded.
```

## Development

### Running Components Individually

**Collect commits only:**
```bash
uv run python src/kyogre/tools/collect_commits.py
```

**Collect diffs only:**
```bash
uv run python src/kyogre/tools/collect_diffs.py
```

**Run full automation:**
```bash
./src/kyogre/scripts/daily.sh
```

### Testing without Publishing

Edit `daily.sh` to comment out the portfolio copying steps:

```bash
# git add "$BLOG_DIR/$BLOG_FILENAME"
# git commit ...
# git push ...
# gh pr create ...
```

### Debugging Claude's Decision

View the full Claude analysis in the logs:

```bash
cat ~/.kyogre-logs/agent.log | grep -A 50 "Running Claude"
```

## Performance

- **Commit collection**: ~1-2 seconds (GitHub Search API)
- **Diff collection**: ~2-5 seconds (REST API per commit)
- **Claude analysis**: ~10-20 seconds (depends on content size)
- **Git operations**: ~2-3 seconds (push + PR creation)
- **Total run time**: ~20-30 seconds (if blog-worthy)

## Security Considerations

1. **GitHub Token**: Stored in `.env` (not in git, add to `.gitignore`)
2. **API Rate Limits**: GitHub allows 60 requests/hour for search, 5000/hour for REST
3. **Portfolio Access**: Requires write access to portfolio repository
4. **Permission Modes**: Uses Claude's permission mode for safe automation
5. **No Auto-Merge**: PRs created but require manual review before merging

## How to Customize

### Change Blog Filtering Criteria

Edit the Claude prompt in `src/kyogre/scripts/daily.sh`:

```bash
claude --permission-mode acceptEdits -p "
[Your custom prompt here]
"
```

### Change Scheduled Time

Edit the plist file (see Configuration section above)

### Change Portfolio Path

Update `PORTFOLIO_PATH` in `.env`

### Add Multi-Repository Support

Modify `collect_commits.py` to search across multiple repositories

## Contributing

To improve Kyogre:

1. Modify `src/kyogre/tools/` for commit/diff collection
2. Modify `src/kyogre/scripts/daily.sh` for orchestration
3. Adjust Claude's prompt in daily.sh for different filtering criteria
4. Test with manual runs before automated scheduling
5. Create a new commit with your improvements
6. Push to origin

## Support

For issues, check:
1. `.env` configuration (GITHUB_TOKEN, paths)
2. GitHub token permissions and expiration
3. Portfolio repository access and permissions
4. Logs in `~/.kyogre-logs/`
5. `gh` CLI authentication: `gh auth status`
6. Git repository status: `git status`

## Author

Created as an automated blogging system for documenting technical work using Claude AI.

---

**Happy blogging!** Let Kyogre help you share your technical journey. 🐋
