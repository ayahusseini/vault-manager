# Vault Manager

A small repository built for organising and parsing through markdown notes (primarily aimed at those written using [Obsidian](https://obsidian.md/))

## How does it work?

- A `#tag` labels the 'type' of note (e.g. `#topic`, `#tool`, `#atom` (for atomic concepts) etc.)
- Notes have links to one another using `[[ref]]` notation. Most notes will have a linked group of topics

```
#tag1 #tag2 #tag3

# Some Title
---
This is a test note.

# Content 
It has some content and references to [[ref1]] and [[ref2]].

## Other headings 

---
Topics:
- [[topic1]]
- [[topic2]]
```

First, all markdown notes are parsed and 'category indicating' text is extracted:
- The list of tags. These are considered to be categorical features and are one-hot encoded 
- Links between notes. These can be used to build a directed graph. Graph embedding methods are used to get a vector to each node.

Then:
- Build the graph of notes based on links. We assume these are undirected. 
- A community detection (Louvain) algorithm is used to find communities (top-level folders) based on the graph structure 
- The community *name* is based on the most frequently cited topic in the community



## Setup 

1. Create an `.env` file with the path to your vault 

```
VAULT_PATH='path/to/vault'
```

2. Verify that uv is installed 

```
uv --version
```

If not installed, download UV using:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install the project and dependencies 

```
uv sync
```

4. To run any python files, use 

```
uv run python <filename>
```

## Running tests 

Run tests using `uv` 

```
uv run pytest
```

Or, for more detailed output, use the verbose flag:

```
uv run pytest -v
```
