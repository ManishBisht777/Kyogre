#!/usr/bin/env python3
"""
Reference Analyzer: Fetch articles from reference authors and extract writing patterns.
Builds a quality standard that kyogre blogs are judged against.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Reference authors to analyze
REFERENCE_SOURCES = {
    "Emil Kowalski": {
        "url": "https://emilkowal.ski",
        "type": "blog",
        "focus": ["technical depth", "code examples", "debugging", "performance"],
    },
    "Josh W. Comeau": {
        "url": "https://www.joshwcomeau.com",
        "type": "blog",
        "focus": ["web dev", "React", "interactive examples", "clear explanations"],
    },
    "Dan Abramov": {
        "url": "https://overreacted.io",
        "type": "blog",
        "focus": ["React internals", "storytelling", "personal insights", "philosophy"],
    },
    "Julia Evans": {
        "url": "https://jvns.ca",
        "type": "blog",
        "focus": ["systems", "debugging", "learning process", "honest mistakes"],
    },
    "Kent C. Dodds": {
        "url": "https://kentcdodds.com",
        "type": "blog",
        "focus": ["testing", "React", "teaching", "practical examples"],
    },
    "Martin Fowler": {
        "url": "https://martinfowler.com",
        "type": "blog",
        "focus": ["architecture", "design patterns", "enterprise", "depth"],
    },
    "Simon Willison": {
        "url": "https://simonwillison.net",
        "type": "blog",
        "focus": ["web dev", "AI/LLMs", "tutorials", "quick tips"],
    },
}


class ArticleAnalyzer:
    """Analyze articles to extract writing patterns and quality signals."""

    def __init__(self):
        self.patterns = {}
        self.standards = {}

    def fetch_article(self, url: str) -> dict | None:
        """Fetch and parse an article."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract text
            text = soup.get_text(separator="\n")
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            content = "\n".join(lines)

            # Extract title
            title_tag = soup.find("h1") or soup.find("title")
            title = title_tag.get_text() if title_tag else "Unknown"

            return {
                "url": url,
                "title": title,
                "content": content,
                "length": len(content),
                "word_count": len(content.split()),
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def analyze_writing_patterns(self, article: dict) -> dict:
        """Extract writing patterns from an article."""
        content = article.get("content", "")
        patterns = {
            "word_count": article.get("word_count", 0),
            "has_code_blocks": "```" in content or "<code>" in content,
            "code_block_count": len(re.findall(r"```", content)) // 2,
            "has_headers": bool(re.search(r"^#+", content, re.MULTILINE)),
            "header_count": len(re.findall(r"^#+", content, re.MULTILINE)),
            "has_lists": bool(re.search(r"^[\*\-\+]", content, re.MULTILINE)),
            "list_items_count": len(re.findall(r"^[\*\-\+]", content, re.MULTILINE)),
            "has_quotes": bool(re.search(r"^>", content, re.MULTILINE)),
            "quote_count": len(re.findall(r"^>", content, re.MULTILINE)),
            "has_links": content.count("[") and content.count("]("),
            "link_count": len(re.findall(r"\]\(https?://", content)),
            "paragraphs": len([p for p in content.split("\n\n") if p.strip()]),
            "code_to_text_ratio": (
                article.get("word_count", 1) / max(1, len(re.findall(r"```", content)) // 2)
            ),
        }
        return patterns

    def build_standards(self) -> dict:
        """Build quality standards from reference articles."""
        standards = {}

        for author, config in REFERENCE_SOURCES.items():
            print(f"\n📚 Analyzing {author}...")
            # In a real implementation, would fetch multiple articles
            # For now, create a template standard

            standards[author] = {
                "url": config["url"],
                "focus_areas": config["focus"],
                "characteristics": {
                    "typical_word_count": "1500-3000",
                    "code_examples": "2-4 per article",
                    "structure": "Hook → Problem → Solution → Lessons",
                    "tone": "varies by author",
                    "technical_depth": "high",
                    "storytelling": "present",
                },
                "quality_signals": {
                    "clarity": "explains both WHAT and WHY",
                    "depth": "dives deep into topics",
                    "examples": "concrete, runnable code",
                    "engagement": "personal voice, honest mistakes",
                    "completeness": "covers edge cases and alternatives",
                },
            }

        return standards

    def save_standards(self, output_path: Path):
        """Save standards to file."""
        standards = self.build_standards()
        output_path.write_text(json.dumps(standards, indent=2))
        print(f"✅ Saved standards to {output_path}")
        return standards


class BlogEvaluator:
    """Judge generated blogs against reference standards."""

    def __init__(self, standards: dict):
        self.standards = standards

    def evaluate_blog(self, blog_content: str, blog_title: str = "") -> dict:
        """Score a blog against reference standards."""
        # Basic pattern analysis
        word_count = len(blog_content.split())
        code_blocks = len(re.findall(r"```", blog_content)) // 2
        headers = len(re.findall(r"^#+", blog_content, re.MULTILINE))
        paragraphs = len([p for p in blog_content.split("\n\n") if p.strip()])
        links = len(re.findall(r"\]\(https?://", blog_content))

        # Score components (0-10)
        scores = {
            "length": self._score_length(word_count),
            "code_density": self._score_code_density(code_blocks, word_count),
            "structure": self._score_structure(headers, paragraphs),
            "examples": self._score_examples(code_blocks),
            "engagement": self._score_engagement(blog_content),
            "clarity": self._score_clarity(blog_content),
        }

        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)

        return {
            "title": blog_title,
            "word_count": word_count,
            "code_blocks": code_blocks,
            "headers": headers,
            "paragraphs": paragraphs,
            "links": links,
            "scores": scores,
            "overall_score": round(overall_score, 1),
            "meets_standard": overall_score >= 7.0,
            "feedback": self._generate_feedback(scores, overall_score),
        }

    def _score_length(self, word_count: int) -> float:
        """Score based on word count (ideal: 1500-3000)."""
        if 1500 <= word_count <= 3000:
            return 10
        elif 1000 <= word_count <= 4000:
            return 7
        elif word_count < 500:
            return 3
        else:
            return 5

    def _score_code_density(self, code_blocks: int, word_count: int) -> float:
        """Score based on code examples (ideal: 2-4)."""
        if 2 <= code_blocks <= 4:
            return 10
        elif code_blocks >= 1:
            return 7
        elif code_blocks == 0:
            return 4
        else:
            return 6

    def _score_structure(self, headers: int, paragraphs: int) -> float:
        """Score based on structure (headers and organization)."""
        if headers >= 4 and paragraphs >= 5:
            return 9
        elif headers >= 2 and paragraphs >= 3:
            return 7
        elif headers == 0:
            return 2
        else:
            return 5

    def _score_examples(self, code_blocks: int) -> float:
        """Score based on concrete examples."""
        if code_blocks >= 3:
            return 10
        elif code_blocks >= 2:
            return 8
        elif code_blocks >= 1:
            return 5
        else:
            return 2

    def _score_engagement(self, content: str) -> float:
        """Score based on storytelling and engagement signals."""
        engagement_signals = [
            "I ",
            "we ",
            "learned",
            "discovered",
            "realized",
            "problem was",
            "turns out",
            "surprisingly",
        ]
        signal_count = sum(1 for signal in engagement_signals if signal in content.lower())

        if signal_count >= 5:
            return 9
        elif signal_count >= 3:
            return 7
        elif signal_count >= 1:
            return 5
        else:
            return 3

    def _score_clarity(self, content: str) -> float:
        """Score based on clarity signals."""
        # Check for explanation patterns
        explanations = [
            "why ",
            "because",
            "this means",
            "in other words",
            "for example",
            "here's why",
        ]
        explanation_count = sum(1 for exp in explanations if exp in content.lower())

        if explanation_count >= 5:
            return 9
        elif explanation_count >= 3:
            return 7
        elif explanation_count >= 1:
            return 5
        else:
            return 3

    def _generate_feedback(self, scores: dict, overall: float) -> list[str]:
        """Generate actionable feedback."""
        feedback = []

        if scores["length"] < 7:
            feedback.append("📏 Consider expanding the article (aim for 1500-3000 words)")
        if scores["code_density"] < 7:
            feedback.append("💻 Add more code examples or improve existing ones")
        if scores["structure"] < 7:
            feedback.append("🏗️ Better structure: use more headers, organize sections clearly")
        if scores["examples"] < 7:
            feedback.append("📝 Include concrete, runnable examples")
        if scores["engagement"] < 7:
            feedback.append("💭 Add more personal voice and storytelling")
        if scores["clarity"] < 7:
            feedback.append("🔍 Explain the WHY, not just the WHAT")

        if overall >= 8:
            feedback.append("⭐ Excellent! Meets reference standards.")
        elif overall >= 7:
            feedback.append("✅ Good quality, minor improvements suggested.")
        else:
            feedback.append("⚠️ Below reference standard, consider rewriting.")

        return feedback


class PromptOptimizer:
    """Improve Claude's prompt based on evaluation results."""

    def __init__(self, standards_path: Path):
        self.standards_path = standards_path
        self.learning_log = []

    def extract_improvement_hints(self, evaluation: dict) -> str:
        """Extract hints for improving the prompt."""
        hints = []

        if evaluation["overall_score"] < 7:
            hints.extend(evaluation["feedback"])

        hints_text = "\n".join(f"  • {hint}" for hint in hints)
        return hints_text

    def suggest_prompt_improvements(
        self, blog_evaluation: dict, standards: dict
    ) -> dict:
        """Suggest how to improve the Claude prompt."""
        suggestions = {
            "timestamp": datetime.now().isoformat(),
            "blog_score": blog_evaluation["overall_score"],
            "meets_standard": blog_evaluation["meets_standard"],
            "improvements": blog_evaluation["feedback"],
            "prompt_adjustments": [],
        }

        if not blog_evaluation["meets_standard"]:
            # Extract what's missing
            if blog_evaluation["scores"]["structure"] < 7:
                suggestions["prompt_adjustments"].append(
                    "Add instruction: Use clear headers (4-6 per article), organize in: Context → Problem → Solution → Lessons"
                )
            if blog_evaluation["scores"]["code_density"] < 7:
                suggestions["prompt_adjustments"].append(
                    "Add instruction: Include 2-4 code examples, explain each step"
                )
            if blog_evaluation["scores"]["engagement"] < 7:
                suggestions["prompt_adjustments"].append(
                    "Add instruction: Use personal voice, share what you learned, be honest about mistakes"
                )
            if blog_evaluation["scores"]["clarity"] < 7:
                suggestions["prompt_adjustments"].append(
                    "Add instruction: Always explain WHY, not just WHAT. Include reasoning and tradeoffs"
                )

        return suggestions

    def save_learning(self, learning: dict, output_path: Path):
        """Save learning to version control."""
        self.learning_log.append(learning)

        # Append to learning log file
        log_file = output_path / "learning_log.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(learning) + "\n")

        print(f"✅ Saved learning to {log_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: reference_analyzer.py <command> [args]")
        print("\nCommands:")
        print("  build-standards           - Build quality standards from references")
        print("  evaluate-blog <filepath>  - Evaluate a blog against standards")
        print("  suggest-improvements      - Suggest prompt improvements")
        sys.exit(1)

    command = sys.argv[1]

    if command == "build-standards":
        analyzer = ArticleAnalyzer()
        standards_file = Path("reference_standards.json")
        analyzer.save_standards(standards_file)
        print("\n📊 Reference Standards Built!")
        print(f"Location: {standards_file}")

    elif command == "evaluate-blog":
        if len(sys.argv) < 3:
            print("Error: please specify blog filepath")
            sys.exit(1)

        blog_path = Path(sys.argv[2])
        if not blog_path.exists():
            print(f"Error: file not found {blog_path}")
            sys.exit(1)

        blog_content = blog_path.read_text()
        blog_title = blog_path.stem

        # Load standards
        standards_file = Path("reference_standards.json")
        if standards_file.exists():
            standards = json.loads(standards_file.read_text())
        else:
            standards = {}

        # Evaluate
        evaluator = BlogEvaluator(standards)
        evaluation = evaluator.evaluate_blog(blog_content, blog_title)

        # Print results
        print(f"\n📊 Blog Evaluation: {blog_title}\n")
        print(f"Overall Score: {evaluation['overall_score']}/10")
        print(f"Meets Standard: {'✅ Yes' if evaluation['meets_standard'] else '❌ No'}\n")

        print("Scores:")
        for metric, score in evaluation["scores"].items():
            print(f"  {metric.capitalize()}: {score}/10")

        print("\nStatistics:")
        print(f"  Words: {evaluation['word_count']}")
        print(f"  Code blocks: {evaluation['code_blocks']}")
        print(f"  Headers: {evaluation['headers']}")
        print(f"  Paragraphs: {evaluation['paragraphs']}")

        print("\nFeedback:")
        for feedback in evaluation["feedback"]:
            print(f"  {feedback}")

    elif command == "suggest-improvements":
        # This would be called after evaluation
        print("Use evaluate-blog first, then this will suggest improvements")
