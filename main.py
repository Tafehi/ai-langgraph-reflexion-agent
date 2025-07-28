from mcp_server import client
import asyncio

def main(input: str):
    asyncio.run(
        client.agents(
            "llama3.2:latest", "ollama", input
        )
    )

if __name__ == "__main__":
    input_text = "where is Oslo?"
    main(input_text)
