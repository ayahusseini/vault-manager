"""Extract patterns from markdown files."""
import re

def extract_all_tags(text: str) -> set[str]:
    """Extract all tags from a markdown file."""
    return set(re.findall(r'#(\w+)', text))