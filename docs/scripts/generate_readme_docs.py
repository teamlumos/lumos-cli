#!/usr/bin/env python3
"""Generate readme.io documentation with YAML frontmatter.

This script takes the generated Sphinx markdown docs and adds readme.io
specific YAML frontmatter for publishing to developers.lumos.com.

Usage:
    python generate_readme_docs.py [--output-dir DIR]
"""

import argparse
import re
import sys
from pathlib import Path

# Mapping of source files to readme.io configuration
# Each entry contains the frontmatter metadata for readme.io
DOCS_CONFIG = {
    "index.md": {
        "title": "Lumos CLI",
        "slug": "lumos-cli",
        "excerpt": "Command-line interface for the Lumos platform",
        "category": "reference",
        "order": 1,
    },
    "installation.md": {
        "title": "Installation",
        "slug": "lumos-cli-installation",
        "excerpt": "How to install the Lumos CLI on macOS, Linux, and Windows",
        "category": "reference",
        "order": 2,
    },
    "examples.md": {
        "title": "Examples",
        "slug": "lumos-cli-examples",
        "excerpt": "Practical examples for common Lumos CLI workflows",
        "category": "reference",
        "order": 3,
    },
    "cli-reference.md": {
        "title": "CLI Reference",
        "slug": "lumos-cli-reference",
        "excerpt": "Complete reference for all Lumos CLI commands",
        "category": "reference",
        "order": 4,
    },
}


def generate_frontmatter(config: dict) -> str:
    """Generate YAML frontmatter for readme.io."""
    lines = ["---"]
    lines.append(f'title: "{config["title"]}"')
    lines.append(f'slug: "{config["slug"]}"')
    lines.append(f'excerpt: "{config["excerpt"]}"')
    lines.append(f'category: "{config["category"]}"')
    lines.append(f"order: {config['order']}")
    lines.append("hidden: false")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def process_markdown_content(content: str, filename: str) -> str:
    """Process markdown content for readme.io compatibility.

    - Removes Sphinx-specific directives
    - Fixes relative links
    - Adjusts heading levels if needed
    """
    # Remove Sphinx toctree directives
    content = re.sub(
        r"```\{toctree\}.*?```",
        "",
        content,
        flags=re.DOTALL,
    )

    # Remove empty code blocks that might remain
    content = re.sub(r"```\s*```", "", content)

    # Convert internal links to readme.io slugs
    for source_file, config in DOCS_CONFIG.items():
        base_name = source_file.replace(".md", "")
        # Update relative links
        content = content.replace(f"]({base_name})", f"]({config['slug']})")
        content = content.replace(f"]({source_file})", f"]({config['slug']})")

    # Clean up multiple consecutive newlines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    return content


def generate_readme_docs(source_dir: Path, output_dir: Path) -> list[str]:
    """Generate readme.io docs from source markdown files.

    Args:
        source_dir: Directory containing source markdown files
        output_dir: Directory to write readme.io docs

    Returns:
        List of generated file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    for filename, config in DOCS_CONFIG.items():
        source_file = source_dir / filename
        if not source_file.exists():
            print(f"Warning: Source file not found: {source_file}", file=sys.stderr)
            continue

        content = source_file.read_text()
        frontmatter = generate_frontmatter(config)
        processed_content = process_markdown_content(content, filename)

        output_content = frontmatter + processed_content
        output_file = output_dir / filename
        output_file.write_text(output_content)
        generated_files.append(str(output_file))
        print(f"Generated: {output_file}")

    return generated_files


def main():
    parser = argparse.ArgumentParser(description="Generate readme.io documentation with YAML frontmatter")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Source directory containing markdown files (default: docs/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent / "readme.io",
        help="Output directory for readme.io docs (default: docs/readme.io/)",
    )
    args = parser.parse_args()

    generated = generate_readme_docs(args.source_dir, args.output_dir)

    if generated:
        print(f"\nSuccessfully generated {len(generated)} files for readme.io")
    else:
        print("No files were generated", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
