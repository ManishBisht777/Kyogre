# Kyogre: Automated Technical Blog Generation

Intelligent system that discovers blog-worthy work from daily GitHub activity, generates drafts, and creates pull requests to your portfolio.

## Quick Start

### 1. Prerequisites

```bash
# Check Python version (need 3.12+)
python3 --version

# Install required tools
brew install uv gh

# Install Claude CLI
pip install anthropic

# Clone and setup
git clone <this-repo>
cd kyogre
uv sync
```

### 2. Configure Credentials

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=your_github_username
PORTFOLIO_PATH=/path/to/your/portfolio
```

Get GitHub token: https://github.com/settings/tokens (needs `repo` scope)

### 3. Test Locally

```bash
# Test commit collection
uv run python src/kyogre/tools/collect_commits.py

# Test diff collection
uv run python src/kyogre/tools/collect_diffs.py

# Run full workflow
./src/kyogre/scripts/daily.sh
```

### 4. Setup Automation (macOS)

Create launchd agent:

```bash
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.kyogre-blog-agent.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kyogre-blog-agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>~/.kyogre-runner.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>~/.kyogre-logs/agent.log</string>
    <key>StandardErrorPath</key>
    <string>~/.kyogre-logs/agent-error.log</string>
</dict>
</plist>
EOF
```

Create Python runner (`~/.kyogre-runner.py`):

```bash
cat > ~/.kyogre-runner.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

KYOGRE_HOME = Path(os.path.expanduser("~/path/to/kyogre"))  # UPDATE THIS
env_file = KYOGRE_HOME / ".env"

# Sync latest from Git
subprocess.run(["git", "pull", "origin", "master"], cwd=str(KYOGRE_HOME), capture_output=True)
subprocess.run(["git", "checkout", "HEAD", "--", "."], cwd=str(KYOGRE_HOME), capture_output=True)

# Load environment
env = {**os.environ, "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")

result = subprocess.run(["/bin/bash", "src/kyogre/scripts/daily.sh"], cwd=str(KYOGRE_HOME), env=env)
sys.exit(result.returncode)
EOF

chmod +x ~/.kyogre-runner.py
```

Create logs directory:

```bash
mkdir -p ~/.kyogre-logs
```

Load automation:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kyogre-blog-agent.plist
```

### 5. Test & Verify

```bash
# Trigger immediately
launchctl kickstart -k gui/$(id -u)/com.kyogre-blog-agent

# Check logs
tail ~/.kyogre-logs/agent.log
```

## How It Works

1. **Collect commits** - GitHub Search API finds today's commits by author
2. **Fetch diffs** - REST API retrieves changes in each commit  
3. **Claude analysis** - Determines if work is blog-worthy
4. **Generate draft** - Creates markdown in `drafts/` if interesting
5. **Create PR** - Pushes to portfolio repo and opens PR for review

## Configuration

### Change Schedule Time

```bash
nano ~/Library/LaunchAgents/com.kyogre-blog-agent.plist
```

Change `Hour` and `Minute`, then reload:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.kyogre-blog-agent.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kyogre-blog-agent.plist
```

### Change Portfolio Path

Update `.env`:

```env
PORTFOLIO_PATH=/new/path
```

### Customize Filtering

Edit Claude prompt in `src/kyogre/scripts/daily.sh`:

```bash
nano src/kyogre/scripts/daily.sh
```

Find the `You are my personal` section and adjust what Claude considers blog-worthy.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GITHUB_TOKEN: KeyError` | Verify `.env` has `GITHUB_TOKEN=ghp_...` |
| `No commits found` | Check you have commits today with your `GITHUB_USERNAME` |
| `Permission denied` | Run `chmod +x src/kyogre/scripts/daily.sh` |
| `gh: command not found` | Run `brew install gh && gh auth login` |
| `git pull` fails | Verify GitHub token in `.env` has repo access |
| `No PR created` | Check `gh auth status` |
| Portfolio has changes | Manually commit/revert before next run |

View logs:

```bash
cat ~/.kyogre-logs/agent.log
cat ~/.kyogre-logs/agent-error.log
tail -f ~/.kyogre-logs/agent.log  # Real-time
```

## What Gets Published

✅ Architectural decisions | Debugging | Performance improvements | Interesting patterns | Failures & lessons  
❌ Typos | README updates | Dependencies | Trivial refactors

## Commands Reference

```bash
# Manual run
./src/kyogre/scripts/daily.sh

# Check status
launchctl list | grep kyogre

# Trigger now
launchctl kickstart -k gui/$(id -u)/com.kyogre-blog-agent

# View schedule
launchctl print gui/$(id -u)/com.kyogre-blog-agent | grep -A 10 "event triggers"

# Disable automation
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.kyogre-blog-agent.plist

# Re-enable
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kyogre-blog-agent.plist
```

## Development

```bash
# Test individual components
uv run python src/kyogre/tools/collect_commits.py
uv run python src/kyogre/tools/collect_diffs.py

# Full workflow
./src/kyogre/scripts/daily.sh
```

## File Structure

```
kyogre/
├── src/kyogre/tools/
│   ├── collect_commits.py
│   └── collect_diffs.py
├── src/kyogre/scripts/
│   ├── daily.sh
│   └── daily.py
├── drafts/         # Generated posts
├── temp/          # Temp files
├── .env.example
├── .env           # Your config (not in git)
└── README.md
```

## Performance

- Commit collection: ~1-2s
- Diff fetching: ~2-5s  
- Claude analysis: ~10-20s
- Git operations: ~2-3s
- **Total**: ~20-30s per run

## Notes

- GitHub token stored in `.env` (add to `.gitignore`)
- No auto-merge - all PRs need review
- Runs daily at 11 PM (configurable)
- Uses Git syncing for code updates
- Full logs available for debugging

## Next Steps

1. Complete Quick Start sections 1-5 above
2. Check logs: `tail ~/.kyogre-logs/agent.log`
3. Make commits and push to trigger automation
4. Review generated PRs in portfolio repo
5. Customize Claude's prompt if needed

---

Questions? Check the logs: `cat ~/.kyogre-logs/agent-error.log`
