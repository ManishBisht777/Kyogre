#!/usr/bin/env python3
"""
Blog analyzer: Parse, filter, and analyze generated blog posts.
Useful for portfolio websites that want to filter by tags or source.
"""

import re
import sys
from pathlib import Path
from typing import TypedDict
import json


class BlogMetadata(TypedDict):
    title: str
    description: str
    date: str
    author: str
    tags: list[str]
    source: str
    reading_time: int
    filepath: str


def parse_blog_frontmatter(filepath: Path) -> BlogMetadata | None:
    """Extract YAML frontmatter from markdown blog post."""
    try:
        content = filepath.read_text(encoding='utf-8')

        # Match frontmatter between --- markers
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return None

        frontmatter = match.group(1)
        metadata = {}

        for line in frontmatter.split('\n'):
            if ':' not in line:
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Parse different types
            if key == 'tags':
                # Parse YAML list format: [tag1, tag2, tag3]
                tags = re.findall(r'\w+(?:-\w+)*', value)
                metadata[key] = tags
            elif key == 'reading_time':
                metadata[key] = int(value) if value.isdigit() else 0
            else:
                metadata[key] = value

        metadata['filepath'] = str(filepath)
        return metadata
    except Exception as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
        return None


def filter_blogs_by_tag(blogs: list[BlogMetadata], tag: str) -> list[BlogMetadata]:
    """Filter blogs that have the given tag."""
    return [blog for blog in blogs if tag in blog.get('tags', [])]


def filter_blogs_by_source(blogs: list[BlogMetadata], source: str) -> list[BlogMetadata]:
    """Filter blogs by source (autonomous or manual)."""
    return [blog for blog in blogs if blog.get('source') == source]


def scan_blogs_directory(directory: Path) -> list[BlogMetadata]:
    """Scan directory and parse all markdown files."""
    blogs = []

    if not directory.exists():
        return blogs

    for filepath in sorted(directory.glob('*.md'), reverse=True):
        metadata = parse_blog_frontmatter(filepath)
        if metadata:
            blogs.append(metadata)

    return blogs


def print_blog_summary(blog: BlogMetadata) -> None:
    """Print a formatted summary of a blog post."""
    tags_str = ', '.join(blog.get('tags', []))
    source = blog.get('source', 'manual')
    reading_time = blog.get('reading_time', 0)

    print(f"\n📝 {blog['title']}")
    print(f"   Date: {blog['date']} | {reading_time} min read | Source: {source}")
    print(f"   {blog['description']}")
    if tags_str:
        print(f"   Tags: {tags_str}")


def export_blogs_json(blogs: list[BlogMetadata], output_file: Path) -> None:
    """Export blogs metadata as JSON for portfolio website."""
    # Convert to serializable format
    data = []
    for blog in blogs:
        blog_copy = dict(blog)
        blog_copy['tags'] = blog_copy.get('tags', [])
        data.append(blog_copy)

    output_file.write_text(json.dumps(data, indent=2))
    print(f"✅ Exported {len(blogs)} blogs to {output_file}")


if __name__ == '__main__':
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: blog_analyzer.py <command> [args]")
        print("\nCommands:")
        print("  list [directory]           - List all blogs")
        print("  filter-tag <tag> [dir]     - Filter by tag")
        print("  filter-source <src> [dir]  - Filter by source (autonomous/manual)")
        print("  export-json <dir> <output> - Export metadata as JSON")
        print("\nExample:")
        print("  python blog_analyzer.py list ~/portfolio/public/blogs")
        print("  python blog_analyzer.py filter-tag kyogre ~/portfolio/public/blogs")
        print("  python blog_analyzer.py filter-tag ai-generated ~/portfolio/public/blogs")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        directory = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
        blogs = scan_blogs_directory(directory)
        print(f"\n📚 Found {len(blogs)} blogs\n")
        for blog in blogs:
            print_blog_summary(blog)
        print()

    elif command == 'filter-tag':
        tag = sys.argv[2] if len(sys.argv) > 2 else ''
        directory = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd()

        if not tag:
            print("Error: please specify a tag")
            sys.exit(1)

        blogs = scan_blogs_directory(directory)
        filtered = filter_blogs_by_tag(blogs, tag)
        print(f"\n🏷️  Found {len(filtered)} blogs with tag '{tag}'\n")
        for blog in filtered:
            print_blog_summary(blog)
        print()

    elif command == 'filter-source':
        source = sys.argv[2] if len(sys.argv) > 2 else ''
        directory = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd()

        if not source:
            print("Error: please specify a source (autonomous or manual)")
            sys.exit(1)

        blogs = scan_blogs_directory(directory)
        filtered = filter_blogs_by_source(blogs, source)
        print(f"\n🤖 Found {len(filtered)} {source} blogs\n")
        for blog in filtered:
            print_blog_summary(blog)
        print()

    elif command == 'export-json':
        directory = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
        output = Path(sys.argv[3]) if len(sys.argv) > 3 else Path('blogs.json')

        blogs = scan_blogs_directory(directory)
        export_blogs_json(blogs, output)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
