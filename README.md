# fastmcp-streamable-http-issue

This repository demonstrates a bug when running a FastMCP server in `streamable-http` mode mounted inside a FastAPI server. It is intended as a minimal reproducible example for opening a pull request or issue on the FastMCP project.

## Purpose

The goal of this repository is to show that when you mount a FastMCP app with `streamable-http` mode into a FastAPI application, a runtime error occurs when accessing the MCP endpoint. This can help maintainers reproduce and fix the issue.

## Installation

You need Python 3.13 or higher.

1. Clone this repository:
   ```sh
   git clone <this-repo-url>
   cd fastmcp_stremable_http_issue
   ```
2. Install dependencies (using [uv](https://github.com/astral-sh/uv) or pip):
   ```sh
   uv venv
   source .venv/bin/activate
   uv pip install -r pyproject.toml
   # or, with pip:
   pip install -r pyproject.toml
   ```

## How to Reproduce the Bug

1. Start the server:
   ```sh
   python main.py
   ```
2. In your browser or with curl, access:
   ```
   http://localhost:8080/mcp/
   ```
3. You will see a 500 Internal Server Error, and the following traceback will appear in the logs:

```
RuntimeError: Task group is not initialized. Make sure to use run().

Traceback (most recent call last):
  File "/.../uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
    ...
  File "/.../fastmcp/server/http.py", line 309, in handle_streamable_http
    await session_manager.handle_request(scope, receive, send)
  File "/.../mcp/server/streamable_http_manager.py", line 137, in handle_request
    raise RuntimeError("Task group is not initialized. Make sure to use run().")
RuntimeError: Task group is not initialized. Make sure to use run().
```

## main.py Example

```python
from fastapi import FastAPI
from fastmcp import FastMCP
import typer
import uvicorn

mcp = FastMCP()

@mcp.tool("add", "Add two numbers")
def add(a: int, b: int) -> int:
    return a + b

app = FastAPI()
app.mount("/", mcp.http_app("streamable-http"))

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    typer.run(main)
```

## Notes
- This bug only occurs when using `streamable-http` mode and mounting the MCP app inside FastAPI.
- The same MCP app may work fine in other modes or when run standalone.

---
Feel free to use this repository as a minimal reproduction for your issue or pull request on FastMCP.
