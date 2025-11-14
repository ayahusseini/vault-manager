"""Extract patterns from markdown files."""

import re

REJECT_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'excalidraw', 'csv', 'md', 'mp4', 'mp3'
}

def extract_all_tags(text: str) -> set[str]:
    """Extract all tags from a markdown file."""
    return set(re.findall(r"#(\w+)", text))


def extract_all_headings(text: str) -> set[str]:
    """Extract all headings from a markdown file"""
    return set(re.findall(r"#\s+(\w+)", text))

def is_rejected_extension(filename: str, reject_ext: set = REJECT_EXTENSIONS) -> bool:
    """Check if the filename has a rejected extension."""
    match = re.search(r'\.([a-zA-Z0-9]+)$', filename)
    if match:
        ext = match.group(1).lower()
        if ext in reject_ext:
            return True
    return False

def extract_all_links(text: str) -> set[str]:
    """Extract all markdown links from a file where
    - links to non-markdown files are ignored
    - aliases are stripped
    - headings are stripped
    """
    raw_matches = re.findall(r"\[\[([^\]\|#]+?)(?:\#[^\]]*)?(?:\|[^\]]*)?\]\]", text)
    matches = set()
    for match in raw_matches:
        if match.endswith(".md"):
            match = match[:-3]
        if not is_rejected_extension(match):
            matches.add(match)
    return matches

