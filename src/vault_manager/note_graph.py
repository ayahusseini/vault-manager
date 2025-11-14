import networkx as nx
from networkx.algorithms import community
from vault_manager import extract_all_links, extract_all_tags
import os
from dotenv import load_dotenv


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
        if name in ["is_topic", "tags", "links"]:
            if not self._content_loaded:
                self.load_content()
            return getattr(self, f"_{name}")
        raise AttributeError(f"Attribute not defined: {name}.")

    def load_content(self):
        """Load content when needed (lazy)"""
        if not self._content_loaded:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self._tags = extract_all_tags(content)
                self._is_topic = "topic" in self._tags

                self._links = [
                    self.normalise_name(l) for l in extract_all_links(content)
                ]
                self._content_loaded = True


class NoteGraph:
    def __init__(self, vault_root):
        self.vault_root = vault_root
        if self.vault_root is None:
            raise ValueError("vault_root not set in .env file")
        self.notes = dict()  # mapping note name : Note object
        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self):
        """Find all markdown files in vault"""
        for root, _, files in os.walk(self.vault_root):
            for file in files:
                if file.endswith(".md"):
                    note = Note.from_filepath(os.path.join(root, file))
                    self.notes[note.name] = note

        for note_name, note in self.notes.items():
            self.graph.add_node(note_name)
            for link in note.links:
                self.graph.add_edge(note_name, link)

    def detect_orphans(self) -> set[str]:
        """Detect notes that are not linked to by any other note"""
        linked_notes = set()
        for node, neighbours in self.graph.adjacency():
            linked_notes.update(neighbours)
        orphans = set(self.graph.nodes) - linked_notes
        return orphans

    def detect_communities(
        self, resolution: float = 0.5, seed: int = 42
    ) -> list[set[str]]:
        """Detect communities of notes using the Louvain Algorithm.
        Higher resolution values lead to more, smaller communities.
        """
        if len(self.graph) == 0:
            return []

        partition = community.louvain_communities(
            self.graph, resolution=resolution, seed=seed
        )

        return partition


if __name__ == "__main__":
    load_dotenv()
    vault_root = os.environ.get("VAULT_PATH")
    n = NoteGraph(vault_root)
    print(f"Loaded {len(n.notes)} notes from vault at {vault_root}")
    p = n.detect_communities()
    o = n.detect_orphans()
    print(f"Detected orphans: \n\n {o}")
