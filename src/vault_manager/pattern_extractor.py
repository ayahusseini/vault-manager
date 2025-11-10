"""Extract patterns from markdown files."""
import re


def extract_all_tags(text: str) -> set[str]:
    """Extract all tags from a markdown file."""
    return set(re.findall(r'#(\w+)', text))


def extract_all_headings(text: str) -> set[str]:
    """Extract all headings from a markdown file"""
    return set(re.findall(r'#\s+(\w+)', text))


def extract_all_links(text: str) -> set[str]:
    """Extract all markdown links from a file"""
    return set(re.findall(r'\[\[((?!.*\.(?!md\b)\w+)[^\[\]\|\#]+)(?:\#[^\]]*)?(?:\|[^\]]*)?\]\]', text))
