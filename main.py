from fastapi import FastAPI
from fastmcp import FastMCP
import typer
import uvicorn

mcp = FastMCP()


@mcp.tool("add", "Add two numbers")
def add(a: int, b: int) -> int:
    return a + b


app = FastAPI()
app.mount("/", mcp.http_app(transport="streamable-http"))


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    typer.run(main)
