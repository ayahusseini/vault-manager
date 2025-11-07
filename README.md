# Vault Manager

A small repository built for organising and parsing through markdown notes (primarily aimed at those written using [Obsidian](https://obsidian.md/))


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
