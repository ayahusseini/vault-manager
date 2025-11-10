import os
import re

all_links = set()
vault = '/Users/ayahusseini/Documents/husseini4'

if __name__ == "__main__":
    for root, dirs, files in os.walk(vault):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_links.update(set(re.findall(
                        r'\[\[([^\[\]\|]+)(?:\|[^\]]*)?\]\]', content)))
    print(all_links)
