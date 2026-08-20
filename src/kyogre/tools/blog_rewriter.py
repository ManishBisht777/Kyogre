#!/usr/bin/env python3
"""
Blog Rewriter: Rewrite blogs that don't meet quality standards.
Uses Claude to improve blogs based on reference standards and feedback.
"""

import json
import subprocess
from pathlib import Path


def rewrite_blog_with_feedback(blog_path: Path, feedback: list[str]) -> str:
    """
    Use Claude to rewrite a blog based on evaluation feedback.
    """
    blog_content = blog_path.read_text()

    feedback_text = "\n".join(f"- {f}" for f in feedback)

    prompt = f"""
You are editing a technical blog post to improve its quality.

CURRENT BLOG:
{blog_content}

FEEDBACK TO ADDRESS:
{feedback_text}

REFERENCE STANDARDS:
- Word count: 1500-3000 words
- Code examples: 2-4 concrete examples with explanation
- Structure: Clear headers organizing: Context → Problem → Solution → Lessons
- Tone: Personal voice, honest about mistakes, conversational
- Clarity: Explain both WHAT and WHY, not just WHAT
- Engagement: Share what you learned, why it matters

TASK:
Rewrite the blog to address the feedback above while:
1. Maintaining the core message and technical accuracy
2. Adding more depth where needed
3. Including code examples if missing
4. Improving structure and clarity
5. Adding personal insights and lessons learned

Output ONLY the improved blog post. Start with the frontmatter (title, description, etc) and continue with the full article.
"""

    # Call Claude
    try:
        result = subprocess.run(
            [
                "claude",
                "--permission-mode",
                "acceptEdits",
                "-p",
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error calling Claude: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_rewritten_blog(original_path: Path, rewritten_content: str) -> Path:
    """Save rewritten blog with _improved suffix."""
    new_name = original_path.stem + "_improved.md"
    new_path = original_path.parent / new_name

    new_path.write_text(rewritten_content)
    print(f"✅ Saved improved blog: {new_path}")

    return new_path


def compare_versions(original_path: Path, improved_path: Path) -> dict:
    """Compare original vs improved blog."""
    original = original_path.read_text()
    improved = improved_path.read_text()

    return {
        "original_length": len(original.split()),
        "improved_length": len(improved.split()),
        "length_change": len(improved.split()) - len(original.split()),
        "original_file": str(original_path),
        "improved_file": str(improved_path),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: blog_rewriter.py <blog_path> [feedback_list]")
        print("\nExample:")
        print('  python blog_rewriter.py drafts/blog.md "Add more code" "Improve structure"')
        sys.exit(1)

    blog_path = Path(sys.argv[1])

    if not blog_path.exists():
        print(f"Error: {blog_path} not found")
        sys.exit(1)

    feedback = sys.argv[2:] if len(sys.argv) > 2 else ["Improve overall quality"]

    print(f"📝 Rewriting: {blog_path}")
    print(f"Feedback: {feedback}\n")

    improved = rewrite_blog_with_feedback(blog_path, feedback)

    if improved:
        new_path = save_rewritten_blog(blog_path, improved)
        comparison = compare_versions(blog_path, new_path)

        print("\n📊 Comparison:")
        print(f"Original: {comparison['original_length']} words")
        print(f"Improved: {comparison['improved_length']} words")
        print(f"Change: +{comparison['length_change']} words")
    else:
        print("❌ Rewriting failed")
        sys.exit(1)
