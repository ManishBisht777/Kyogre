# Kyogre Updates: Tags & Blog Filtering

## What's New

### 1. Blog Post Created
📝 **Building Autonomous Agents: How to Automate Daily Logs and Blog Generation**

Location: `/Users/manishbisht/Desktop/dev/manish/portfolio/public/blogs/building-autonomous-agents-kyogre.md`

This comprehensive guide covers:
- Why autonomous agents matter
- The 6-component agent harness architecture
- 3-stage implementation pipeline
- Design decisions and trade-offs
- How to extend kyogre
- Setting up automation (launchd example)
- Key insights and lessons learned

**Status**: ✅ Added to portfolio blogs folder (not yet committed)

---

## 2. Updated daily.sh Script

**File**: `src/kyogre/scripts/daily.sh`

### Changes
Claude now generates blogs with **YAML frontmatter** including tags:

```yaml
---
title: Blog Title
description: One-line summary
date: 2026-08-19
author: Manish Bisht
tags: [kyogre, ai-generated, debugging, architecture, performance]
source: autonomous
reading_time: 10
---
```

### Tagging System

Generated blogs automatically include:
- **kyogre** - Always included (marks kyogre-generated content)
- **ai-generated** - Always included (marks AI-generated posts)
- **Topic tags** - Selected based on content:
  - `debugging` - If debugging/troubleshooting
  - `architecture` - If architectural decisions
  - `performance` - If performance improvements
  - `ai-llm` - If AI/LLM related
  - `lessons-learned` - Always included
  - `implementations` - If code patterns
  - `tradeoffs` - If discussing trade-offs
  - `refactoring` - If refactoring work
  - `testing` - If testing related
  - `security` - If security related

### How to Use

After running `./src/kyogre/scripts/daily.sh`:

```bash
# New blogs in drafts/ will have proper tags
cat drafts/2026-08-19-*.md

# Example:
# ---
# title: Debugging Async Race Conditions
# tags: [kyogre, ai-generated, debugging, architecture, lessons-learned]
# source: autonomous
# ...
```

---

## 3. New Blog Analyzer Tool

**File**: `src/kyogre/tools/blog_analyzer.py`

A utility to parse, filter, and analyze blogs by tags and source.

### Usage Examples

```bash
# List all blogs
uv run python src/kyogre/tools/blog_analyzer.py list ~/portfolio/public/blogs

# Filter by tag (e.g., show all kyogre-generated blogs)
uv run python src/kyogre/tools/blog_analyzer.py filter-tag kyogre ~/portfolio/public/blogs

# Show only autonomous (AI-generated) blogs
uv run python src/kyogre/tools/blog_analyzer.py filter-tag ai-generated ~/portfolio/public/blogs

# Show only manual blogs
uv run python src/kyogre/tools/blog_analyzer.py filter-source manual ~/portfolio/public/blogs

# Export blog metadata as JSON (for portfolio website)
uv run python src/kyogre/tools/blog_analyzer.py export-json ~/portfolio/public/blogs output.json
```

### Output Examples

```bash
$ uv run python src/kyogre/tools/blog_analyzer.py filter-tag kyogre ~/portfolio/public/blogs

🏷️  Found 1 blogs with tag 'kyogre'

📝 Building Autonomous Agents: How to Automate Daily Logs and Blog Generation
   Date: 2026-08-19 | 15 min read | Source: autonomous
   A complete guide to building self-directed agents...
   Tags: automation, agents, kyogre, ai, llm, devops, productivity
```

---

## 4. Portfolio Website Integration

The `blog_analyzer.py` can export blog metadata as JSON for your portfolio:

```bash
# Generate JSON file
uv run python src/kyogre/tools/blog_analyzer.py export-json \
  ~/portfolio/public/blogs \
  ~/portfolio/public/blogs-metadata.json
```

This creates a file like:

```json
[
  {
    "title": "Building Autonomous Agents...",
    "description": "A complete guide...",
    "date": "2026-08-19",
    "tags": ["kyogre", "ai-generated", "automation"],
    "source": "autonomous",
    "reading_time": 15,
    "filepath": "..."
  }
]
```

Your portfolio website can:
- Filter blogs by tag: `?tag=kyogre` or `?tag=ai-generated`
- Show only human-written: `?source=manual`
- Show AI-generated content: `?source=autonomous`
- Group by tags for navigation

---

## How To: Filter Blogs on Your Portfolio

### Option 1: Client-Side (JavaScript)

```javascript
// Load the JSON
const response = await fetch('/blogs-metadata.json');
const blogs = await response.json();

// Filter by tag
const kyogreBlog = blogs.filter(b => b.tags.includes('kyogre'));

// Filter by source
const aiBlogs = blogs.filter(b => b.source === 'autonomous');

// Filter by multiple tags
const debuggingBlogs = blogs.filter(b => 
  b.tags.includes('debugging') && b.tags.includes('kyogre')
);
```

### Option 2: Server-Side (Python/Node/etc)

The blog analyzer can be called as a library:

```python
from blog_analyzer import scan_blogs_directory, filter_blogs_by_tag

blogs = scan_blogs_directory(Path('public/blogs'))
kyogre_blogs = filter_blogs_by_tag(blogs, 'kyogre')
ai_blogs = filter_blogs_by_tag(blogs, 'ai-generated')
```

### Option 3: Shell Script

```bash
# Show all kyogre blogs
uv run python src/kyogre/tools/blog_analyzer.py filter-tag kyogre ~/portfolio/public/blogs

# Show count
uv run python src/kyogre/tools/blog_analyzer.py filter-tag kyogre ~/portfolio/public/blogs | grep "Found" 
```

---

## Next Steps

1. **Test the workflow**:
   ```bash
   ./src/kyogre/scripts/daily.sh
   ```
   
2. **Check generated draft** (if work is blog-worthy):
   ```bash
   head -20 drafts/2026-08-*.md
   # Should see tags in frontmatter
   ```

3. **Update your portfolio website** to filter blogs:
   - Use the blog_analyzer.py tool
   - Or parse the JSON metadata
   - Show tags as filter buttons
   - Mark AI-generated content with a badge

4. **Customize tags** (if needed):
   - Edit `daily.sh` Claude prompt
   - Add/remove tags from the tag list
   - Adjust Claude's tagging logic

---

## Summary of Changes

| File | Change | Purpose |
|------|--------|---------|
| `src/kyogre/scripts/daily.sh` | Updated Claude prompt | Add tags to generated blogs |
| `src/kyogre/tools/blog_analyzer.py` | NEW | Parse & filter blogs by tags |
| Portfolio `blogs/` | NEW blog post | Comprehensive guide on building agents |

All changes are backward compatible. Existing blogs continue to work.

---

## Files Modified

```
kyogre/
├── src/kyogre/scripts/
│   └── daily.sh                    # ✅ Updated with tags
├── src/kyogre/tools/
│   └── blog_analyzer.py            # ✅ NEW
└── KYOGRE_UPDATES.md               # ✅ This file
```

Portfolio:
```
portfolio/public/blogs/
└── building-autonomous-agents-kyogre.md    # ✅ NEW
```
