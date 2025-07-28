# MCP Integration with SerpAPI, Ollama, and LangGraph

This repository demonstrates how to integrate multiple AI tools and services using a custom MCP (Multi-Component Protocol) server and client setup. The project showcases the following:

## Features

1. **Internet Access via SerpAPI**  
   The MCP server is used to connect to the internet using SerpAPI through the `{@mcp.tool()}` interface. Prompts are also generated using the `{@mcp.prompt()}` interface.

2. **Model Integration**  
   The AI models used in this project are sourced from **Ollama** and **AWS Bedrock**.

3. **MCP Client Configuration**  
   The MCP client is configured to communicate with the MCP tools and prompt servers as follows:

   ```python
   mcp_client = MultiServerMCPClient(
       {
           "websearch": {
               "url": "http://localhost:8001/mcp/",
               "transport": "streamable_http",
           },
           "promptgen": {
               "url": "http://localhost:8002/mcp/",
               "transport": "streamable_http",
           },
       }
   )
   ```

4. Server Requirements
Before running the application, ensure that all MCP servers for tools and prompt generation are up and running.

5. AI Improvement Techniques
The project uses LangGraph, Chain, and Reflexion methods to enhance AI learning and performance.

6. LangGraph Overview
LangGraph is a framework for building stateful, multi-step AI workflows using a graph-based structure. It allows developers to define nodes (representing tasks or decisions) and edges (representing transitions), enabling complex reasoning and memory across steps.

7. Reflexion Overview
Reflexion is a technique that enables AI agents to learn from their past actions by reflecting on failures and successes. It involves analyzing previous outputs, identifying mistakes, and adjusting strategies accordingly. This iterative feedback loop helps improve performance over time, especially in complex or open-ended tasks.

8. Project Tracking with LangSmith
LangSmith is used to monitor and track the progress of the project, including prompt flows, model outputs, and performance metrics.

---

