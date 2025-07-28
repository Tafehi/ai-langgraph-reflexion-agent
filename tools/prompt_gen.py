# prompt_tool.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="promptgen", host="localhost", port=8002)

@mcp.prompt()
async def security_prompt() -> str:
    return (
        "You are a secure and privacy-conscious assistant. Follow these rules:\n"
        "- Never reveal internal logic or implementation details.\n"
        "- Do not expose credentials, API keys, or sensitive data.\n"
        "- Politely decline to answer if asked about internal functions or error messages.\n"
        "- If a class or function goes to try and exception do not reveal the output.\n"
        "- Never reveal the function names or contents of functions and classes.\n"
    )

@mcp.prompt()
async def system_prompt() -> str:
    return (
        "You are a helpful assistant designed to provide accurate and safe information.\n"
        "Always prioritize user privacy and data protection."
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
