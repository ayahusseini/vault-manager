from vault_manager import extract_all_links, extract_all_tags
from typing import Dict
import os
from dotenv import load_dotenv
import networkx as nx

class Note:
    def __init__(self, filepath, name, all_links: set['Note'], all_tags: set[str], is_topic: bool) -> None:
        self.filepath = filepath # path relative to the project root
        self.name = name
        self.is_topic = is_topic
        self.all_links = all_links # raw name of all links
        self.linked_topics = set([t for t in all_links if t.is_topic])
    

class NoteGraph:
    def __init__(self, vault_root):
        self.vault_root = vault_root
        if self.vault_root is None:
            raise ValueError('vault_root not set in .env file')
        self.notes = self._parse_notes_from_vault()
        self.graph = self._build_graph()
    
    def _parse_notes_from_vault(self) -> Dict[str, Note]:
        notes_by_name = {}
        
        # Recursively walk through all folders and subfolders
        for root, dirs, files in os.walk(self.vault_root):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.vault_root)
                    name = os.path.basename(full_path).lower().replace(".md", "")
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except (IOError, UnicodeDecodeError) as e:
                        print(f"Warning: Could not read {rel_path}: {e}")
                        continue
            
                    raw_links = extract_all_links(content)
                    tags = extract_all_tags(content)
                    is_topic = 'topic' in tags
                    
                    # Create note with empty links (to be resolved later)
                    note = Note(
                        filepath=rel_path,
                        name=name,
                        all_links=set(),
                        all_tags=tags,
                        is_topic=is_topic
                    )
                    
                    
    def _build_graph(self):
        
        G = nx.Graph()
        for note in self.notes.values():
            G.add_node(note.name, note=note)
            for linked_note in note.all_links:
                G.add_node(linked_note.name, note=linked_note)
                G.add_edge(note.name, linked_note.name)
        return G
        
if __name__ == "__main__":
    load_dotenv()
    vault_root = os.environ.get("VAULT_PATH")