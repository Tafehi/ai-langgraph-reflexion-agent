import os
import httpx
from mcp.server.fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
from starlette.routing import Host



mcp = FastMCP(name="websearch", host="localhost", port=8001)

class SerpApiSearch:
    def __init__(self):
        load_dotenv()
        self._API_KEY = os.getenv("SERP_API")
        self._BASE_URL = os.getenv("SERP_URL")

    @mcp.tool()
    async def search_serpapi(self, query: str):

        " you are a websearch tool. you search the web and bring the results back from ineternet"

        if not self._BASE_URL or not self._API_KEY:
            raise ValueError("Missing SERP_API or SERP_URL in environment variables.")
        params = {
            "q": query,
            "api_key": self._API_KEY
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self._BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

    def extract_snippets(self, data: dict):
        snippets = []
        for result in data.get('organic_results', []):
            snippet = result.get('snippet')
            if snippet:
                snippets.append(snippet)
        return snippets

# async def main():
#     serp = SerpApiSearch()
#     search_result = await serp.search_serpapi("where is iran?")
#     snippets = serp.extract_snippets(search_result)
#     print(snippets)
    

if __name__ == "__main__":
    # asyncio.run(main())
    mcp.run(transport="streamable-http")
