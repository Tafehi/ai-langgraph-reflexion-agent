import os
from pdb import run
import httpx
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import asyncio
from chains.schema import AnswerQuestion, ReviseAnswer

mcp = FastMCP(name="serpsearch", host="localhost", port=8001)


class SerpApiSearch:
    def __init__(self):
        load_dotenv()
        self._API_KEY = os.getenv("SERP_API")
        self._BASE_URL = os.getenv("SERP_URL")

    @mcp.tool()
    async def search_serpapi(self, query: str):
        """
        Use this tool to search the internet for up-to-date information\n.
        It fetches real-time data using SerpAPI and returns relevant snippets\n.
        Ideal for answering questions about current events, public figures, or factual queries\n.
        Do not respond with 'I can't answer that' and search in the internet\n.
        """

        if not self._BASE_URL or not self._API_KEY:
            raise ValueError("Missing SERP_API or SERP_URL in environment variables.")

        params = {"q": query, "api_key": self._API_KEY}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:  # 10 seconds timeout
                response = await client.get(self._BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.ReadTimeout:
            return {
                "error": "The request to SerpAPI timed out. Please try again later."
            }
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    @staticmethod
    def extract_snippets(data: dict):
        if "error" in data:
            return [data["error"]]
        snippets = []
        for result in data.get("organic_results", []):
            snippet = result.get("snippet")
            if snippet:
                snippets.append(snippet)
        return snippets

    # def execute_serp(self):

    #     # Create two tools for LLM
    #     execute_tools = ToolNode(
    #         [
    #             StructuredTool.from_function(
    #                 asyncio.run(self.search_serpapi()), name=AnswerQuestion.__name__
    #             ),
    #             StructuredTool.from_function(
    #                 asyncio.run(self.search_serpapi()), name=ReviseAnswer.__name__
    #             ),
    #         ]
    #     )


async def main():
    serp = SerpApiSearch()
    search_result = await serp.search_serpapi("who is current usa president?")
    snippets = serp.extract_snippets(search_result)
    print(snippets)


if __name__ == "__main__":
    # asyncio.run(main())
    serp = SerpApiSearch()  # < -- This line is critical
    mcp.run(transport="streamable-http")
