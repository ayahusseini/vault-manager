from vault_manager import extract_all_links, extract_all_tags
from typing import Dict
import os
from dotenv import load_dotenv
import networkx as nx
import matplotlib as mpl


class Note:
    def __init__(self, filepath, name) -> None:
        self.filepath = filepath
        self.name = name
        self._content_loaded = False

    @classmethod
    def from_filepath(cls, filepath):
        return cls(filepath, cls.normalise_name(filepath))

    @staticmethod
    def normalise_name(notename: str) -> str:
        return os.path.basename(notename).lower().replace(".md", "").strip()

    def __getattr__(self, name):
        """Called when an attribute is not found"""
        if name in ['is_topic', 'tags', 'raw_links']:
            if not self._content_loaded:
                self.load_content()
            return getattr(self, f'_{name}')
        raise AttributeError(f'Attribute not defined: {name}.')

    def load_content(self):
        """Load content when needed (lazy)"""
        if self._content_loaded:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self._tags = extract_all_tags(content)
                self._is_topic = 'topic' in self._tags

                self._raw_links = [self.normalize_name(l) for l in extract_all_links(content)
                                   if not l.endswith('excalidraw')]
                self._content_loaded = True


class NoteGraph:
    def __init__(self, vault_root):
        self.vault_root = vault_root
        if self.vault_root is None:
            raise ValueError('vault_root not set in .env file')
        self.notes = self._parse_notes_from_vault()
        self.graph = self._build_graph()

    def _parse_notes_from_vault(self) -> list[Note]:
        all_notes = dict()

        for root, dirs, files in os.walk(self.vault_root):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    name = self._normalize_name(full_path)

                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    raw_links = extract_all_links(content)
                    tags = extract_all_tags(content)
                    is_topic = 'topic' in tags

                    note = Note(
                        filepath=full_path,
                        name=name,
                        all_tags=tags,
                        is_topic=is_topic
                    )

                    note._raw_links = [self._normalize_name(
                        l) for l in raw_links if not l.endswith('excalidraw')]
                    all_notes.update({name: note})

        return all_notes

    def _build_graph(self) -> nx.Graph:
        G = nx.Graph()

        for notename, note in self.notes.items():
            if notename not in G.nodes:
                G.add_node(notename, note=note)
            for linkname in note._raw_links:
                if linkname in G.nodes:
                    G.add_edge(notename, linkname)
                elif linkname in self.notes:
                    G.add_node(linkname, note=self.notes[linkname])
                    G.add_edge(notename, linkname)
                else:
                    continue
        return G


if __name__ == "__main__":
    load_dotenv()
    vault_root = os.environ.get("VAULT_PATH")
    n = NoteGraph(vault_root)
