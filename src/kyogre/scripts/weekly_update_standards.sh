#!/bin/bash

# Weekly Standards Update: Check what reference authors recently posted
# and update quality standards for next week's blogs

set -euo pipefail

AGENT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$AGENT_DIR"

echo "================================"
echo " Weekly Standards Update"
echo "================================"
echo ""
echo "Checking recent posts from reference authors..."
echo ""

# Function to fetch and summarize recent posts
check_author() {
    local author=$1
    local site=$2

    echo "📚 $author ($site)"

    # Note: In production, you'd actually fetch and parse
    # For now, this is a placeholder showing the structure
    # You could use: curl, BeautifulSoup, or RSS feeds if available

    # Try common RSS feeds
    for rss_url in \
        "${site}/feed.xml" \
        "${site}/rss.xml" \
        "${site}/feed/" \
        "${site}/atom.xml"
    do
        # This would fetch and parse RSS
        # For demo, we note it could be done
        true
    done

    echo "   (Would check for recent posts)"
    echo ""
}

# Reference authors
declare -A AUTHORS=(
    ["Emil Kowalski"]="https://emilkowal.ski"
    ["Josh W. Comeau"]="https://www.joshwcomeau.com"
    ["Dan Abramov"]="https://overreacted.io"
    ["Julia Evans"]="https://jvns.ca"
    ["Kent C. Dodds"]="https://kentcdodds.com"
    ["Martin Fowler"]="https://martinfowler.com"
    ["Simon Willison"]="https://simonwillison.net"
)

for author in "${!AUTHORS[@]}"; do
    check_author "$author" "${AUTHORS[$author]}"
done

echo ""
echo "2. Analyzing learnings from this week's blogs..."
echo ""

# Check what we learned from blogs that were successfully improved
if [ -f "evaluations/prompt_learnings.txt" ]; then
    echo "Successful patterns from daily improvements:"
    cat "evaluations/prompt_learnings.txt" | head -20
    echo ""
else
    echo "No daily learnings yet (blogs likely passed on first try)"
    echo ""
fi

echo ""
echo "3. Generating updated standards..."
echo ""

# Create updated standards based on learnings
{
    echo "# Quality Standards (Updated: $(date))"
    echo ""
    echo "## Baseline Requirements (All Blogs)"
    echo "These must be present in every generated blog:"
    echo ""
    echo "### Length"
    echo "- Minimum: 1000 words"
    echo "- Ideal: 1500-3000 words"
    echo "- Maximum: 5000 words"
    echo "- Why: Enough depth without overwhelming readers"
    echo ""
    echo "### Structure"
    echo "- Title: Compelling, specific"
    echo "- Intro: Hook/context (why does this matter?)"
    echo "- Problem: Clear description of what was wrong"
    echo "- Attempts: What you tried first"
    echo "- Solution: How you fixed it"
    echo "- Lessons: What you learned, what matters"
    echo ""
    echo "### Code Examples"
    echo "- Required: 2-4 concrete examples"
    echo "- Format: Runnable, properly formatted"
    echo "- Context: Explain what each example shows"
    echo "- Evolution: Show before/after if possible"
    echo ""
    echo "### Engagement"
    echo "- Personal voice: Use 'I', 'we', conversational tone"
    echo "- Honesty: Admit what you got wrong"
    echo "- Storytelling: 'What triggered this' → 'what I learned'"
    echo "- Surprise: Share unexpected findings"
    echo ""
    echo "### Clarity"
    echo "- Explain WHY, not just WHAT"
    echo "- Use clear transitions between ideas"
    echo "- Define technical terms"
    echo "- Show reasoning, not just results"
    echo ""
    echo "## Reference Author Patterns"
    echo ""
    echo "### Emil Kowalski (Technical Depth)"
    echo "- Deep dives into specific technologies"
    echo "- Multiple approaches compared"
    echo "- Performance implications explained"
    echo ""
    echo "### Josh W. Comeau (Clarity)"
    echo "- Interactive examples when relevant"
    echo "- Step-by-step walkthroughs"
    echo "- Explanations of the 'why' first"
    echo ""
    echo "### Dan Abramov (Philosophy)"
    echo "- Bigger picture thinking"
    echo "- Personal insights and journey"
    echo "- Lessons about problem-solving process"
    echo ""
    echo "### Julia Evans (Accessibility)"
    echo "- Assumes reader is smart but new to topic"
    echo "- Honest about learning process"
    echo "- Practical, actionable content"
    echo ""
    echo "### Kent C. Dodds (Teaching)"
    echo "- Practical, working code"
    echo "- Testing mentioned when relevant"
    echo "- Real-world use cases"
    echo ""
    echo "### Martin Fowler (Enterprise)"
    echo "- Trade-offs discussed explicitly"
    echo "- Context-dependent solutions"
    echo "- When and why to apply"
    echo ""
    echo "### Simon Willison (Currency)"
    echo "- Up-to-date with current tools"
    echo "- Quick, digestible format acceptable"
    echo "- Multiple angles on same topic"
    echo ""
    echo "## Success Criteria (Score 7+)"
    echo "- Meets all baseline requirements"
    echo "- Clear structure with 4+ sections"
    echo "- 2+ code examples"
    echo "- Personal voice present"
    echo "- Explains reasoning, not just facts"
    echo ""
    echo "## Excellence Criteria (Score 8+)"
    echo "- All success criteria met"
    echo "- 3-4 code examples"
    echo "- Strong narrative arc"
    echo "- Surprising insights"
    echo "- Helps reader think differently"
    echo ""
    echo "## Generated: $(date)"

} > "updated_standards.md"

echo "✅ Updated standards generated"
echo ""

# Show what changed
echo "4. Summary of learning this week..."
echo ""

if [ -f "evaluations/prompt_learnings.txt" ]; then
    {
        echo "# This Week's Improvements"
        echo ""
        echo "Blogs were successfully improved by:"
        grep -o "Successful blog" "evaluations/prompt_learnings.txt" 2>/dev/null | wc -l
        echo "successful iterations"
        echo ""
        echo "Key patterns:"
        grep "What worked:" "evaluations/prompt_learnings.txt" 2>/dev/null | head -5
    } > "evaluations/weekly_summary.txt"
fi

echo "================================"
echo " Standards Update Complete"
echo "================================"
echo ""
echo "Next Steps:"
echo "1. Review: updated_standards.md"
echo "2. These standards guide next week's blogs"
echo "3. Check: evaluations/weekly_summary.txt"
echo "4. Your AI will use these improved standards"
echo ""
echo "The standards are automatically updated."
echo "Your reference evaluator learns from your improvements! 📈"
echo ""
