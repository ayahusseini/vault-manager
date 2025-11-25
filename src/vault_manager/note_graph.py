import spacy
from vault_manager import extract_all_links, extract_all_tags, is_rejected_extension
import os
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")


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
        if not os.path.exists(vault_root):
            raise ValueError("vault_root doesn't exist")
        self.notes = dict()  # mapping note name : Note object
        # Each note object has a lazy '.links' attribute to fetch links

    @classmethod
    def from_env(cls):
        load_dotenv()
        pth = os.environ.get("VAULT_PATH")
        if pth is None:
            raise ValueError("vault_root not set in .env file")
        return cls(pth)

    def _build_graph(self):
        """Find all markdown files in vault"""
        for root, _, files in os.walk(self.vault_root):
            for file in files:
                if file.endswith(".md") and not file.replace(".md", "").endswith(
                    ".excalidraw"
                ):
                    note = Note.from_filepath(os.path.join(root, file))
                    self.notes[note.name] = note

    def get_topic_graph(self):
        """Return a weighted graph containing just the topic notes
        If two nodes were connected in the original graph, the weight is -1
        Otherwise, if they were a distance of '2' away, the weight is -2, etc."""
        for node in self.graph.nodes:
            pass


if __name__ == "__main__":
    n = NoteGraph.from_env()
