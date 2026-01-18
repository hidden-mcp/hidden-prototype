Hidden Prototype

Hidden Prototype is a lightweight MCP server for generating and running isolated Python prototypes.
It creates a dedicated workspace per run, executes the code via `uv`, and returns a detailed report
including stdout, stderr, and any artifacts written to the outputs directory.

## Highlights

- Generate isolated, timestamped prototype workspaces
- Execute self-contained Python scripts via `uv` with a 180s timeout
- Capture stdout/stderr plus any generated artifacts
- Local-first storage under your home directory
- Single MCP tool for programmatic access

## Requirements

- Python 3.11+
- `uv` on PATH

## Data Location

Prototypes are stored under `~/.hidden_prototype/` in your home directory.
Each run is placed in a timestamped folder with an `outputs/` subdirectory for artifacts.

Example:

- `~/.hidden_prototype/20260118_235959_demo_run/`
- `~/.hidden_prototype/20260118_235959_demo_run/outputs/`

## MCP Tools

These tools are exposed via MCP:

- `forge_and_run(code, purpose)`

Tool notes:

- `code` must be a complete Python script.
- Use PEP 723 inline metadata to declare dependencies.
- Use the `PROTOTYPE_OUTPUT_DIR` environment variable to write artifacts.

## MCP Client Setup (uvx)

### Claude Desktop

```json
{
    "mcpServers": {
        "hidden-prototype": {
            "command": "uvx",
            "args": ["--from", "hidden-prototype", "hidden-prototype"]
        }
    }
}
```

### Codex (OpenAI)

```toml
[mcp_servers.hidden-prototype]
command = "uvx"
args = ["--from", "hidden-prototype", "hidden-prototype"]
```

### Cursor

```json
{
    "mcpServers": {
        "hidden-prototype": {
            "command": "uvx",
            "args": ["--from", "hidden-prototype", "hidden-prototype"]
        }
    }
}
```
