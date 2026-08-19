# Dynamic Tag Examples

## How Tags Are Generated

**Fixed tags (always present):**
- `kyogre` - Always (identifies kyogre-generated content)
- `ai-generated` - Always (identifies AI-generated posts)

**Dynamic tags (selected based on content):**
- Only relevant tags are added based on what the blog is actually about
- 2-5 additional tags per blog

---

## Example 1: Debugging Bug

**Content**: Blog about tracking down a race condition in async code

**Tags Generated**:
```yaml
tags: [kyogre, ai-generated, debugging, architecture]
```

Why?
- ✅ `debugging` - Article is about troubleshooting
- ✅ `architecture` - Discusses async architecture
- ❌ NOT `performance` - Blog doesn't focus on optimization
- ❌ NOT `testing` - Blog doesn't focus on testing

---

## Example 2: Performance Optimization

**Content**: Blog about optimizing database queries and caching strategy

**Tags Generated**:
```yaml
tags: [kyogre, ai-generated, performance, implementations, lessons-learned]
```

Why?
- ✅ `performance` - Article is about optimization
- ✅ `implementations` - Shows caching patterns
- ✅ `lessons-learned` - Shares insights learned
- ❌ NOT `debugging` - Not about troubleshooting
- ❌ NOT `security` - Not about security

---

## Example 3: Architecture Decision

**Content**: Blog about refactoring monolith to microservices and tradeoffs

**Tags Generated**:
```yaml
tags: [kyogre, ai-generated, architecture, tradeoffs, implementations]
```

Why?
- ✅ `architecture` - Core topic
- ✅ `tradeoffs` - Discusses pros/cons
- ✅ `implementations` - Shows code changes
- ✅ `refactoring` - Discusses refactoring work
- ❌ NOT `performance` - Unless it's performance-focused
- ❌ NOT `testing` - Unless testing is a major focus

---

## Example 4: AI/LLM Experiment

**Content**: Blog about integrating Claude API into your app and lessons learned

**Tags Generated**:
```yaml
tags: [kyogre, ai-generated, ai-llm, implementations, lessons-learned]
```

Why?
- ✅ `ai-llm` - AI/LLM integration work
- ✅ `implementations` - Shows integration patterns
- ✅ `lessons-learned` - Shares what was learned
- ❌ NOT `debugging` - Unless you debugged AI issues
- ❌ NOT `security` - Unless security was a focus

---

## Example 5: Multiple Aspects

**Content**: Blog about debugging a performance issue in production and what you learned

**Tags Generated**:
```yaml
tags: [kyogre, ai-generated, debugging, performance, lessons-learned]
```

Why?
- ✅ `debugging` - Troubleshooting involved
- ✅ `performance` - Performance was the issue
- ✅ `lessons-learned` - Shares insights
- ❌ NOT `security` - Not security-focused
- ❌ NOT `testing` - Not testing-focused

---

## Key Rules

1. **Always include**: `kyogre`, `ai-generated`
2. **Never hardcode**: Tags vary per blog
3. **Match content**: Only add tags that match what the blog is about
4. **2-5 extras**: Aim for 2-5 dynamic tags on top of the 2 fixed ones
5. **Be accurate**: Claude reads the blog and picks the right tags

---

## How Claude Decides

Claude will:
1. Write the blog content
2. Review what it wrote
3. Think: "What's this blog actually about?"
4. Pick tags that match
5. Add them to frontmatter

Example thought process:
```
Blog content: "How I fixed a deadlock bug..."
Claude thinks: "This is debugging, involves threading/architecture"
Tags: [kyogre, ai-generated, debugging, architecture]

Blog content: "Optimizing N+1 queries with caching..."
Claude thinks: "This is about performance and implementation patterns"
Tags: [kyogre, ai-generated, performance, implementations]
```

---

## Result

Each blog gets **unique tags that match its actual content**, not a generic list repeated every time. ✅
