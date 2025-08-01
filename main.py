import asyncio
from mcp_server import client
from chains.chain import Chain
from graph.graph import Graph
import streamlit as st
from langchain_core.messages import HumanMessage
import json



# async def main(input_text: str):
#     graph_instance = Graph(input_text)
#     compiled_graph = graph_instance.build_chain()

#     # ✅ Use async invocation
#     response = await compiled_graph.ainvoke([HumanMessage(content=input_text)])

#     # print(response[1:])

#     print("\n🔍 Final Answer:\n")
#     print(response)

# if __name__ == "__main__":
#     input_text = "Write about the current USA president and his views, especially on foreign policy."
#     asyncio.run(main(input_text))



# Streamlit page configuration
st.set_page_config(page_title="LLM Chatbot", layout="wide")

# Sidebar: LLM Configuration
st.sidebar.title("LLM Configuration")

provider = st.sidebar.selectbox("Select LLM Provider", ["aws", "ollama"], index=1)

model_options = {
    "ollama": [
        "llama3.2:latest",
        "orionstar/orion14b-q4:latest",
        "prompt/hermes-2-pro",
    ],
    "aws": [
        "anthropic.claude-3-7-sonnet-20250219-v1:0",
        "mistral.mixtral-8x7b-instruct-v0:1",
        "anthropic.claude-3-haiku-20240307-v1:0",
    ],
}

default_model = (
    "llama3.2:latest"
    if provider == "ollama"
    else "anthropic.claude-3-7-sonnet-20250219-v1:0"
)

model = st.sidebar.selectbox(
    "Select Model",
    model_options[provider],
    index=model_options[provider].index(default_model),
)

# Sidebar: Logs
st.sidebar.markdown("### Logs for Agents/Tools from MCP Server")
log_placeholder = (
    "Logs related to the agents and tools generated from MCP server will appear here."
)
st.sidebar.text_area("Logs", log_placeholder, height=150)

# Main UI
st.title("🧠 MCP Server Chatbot with Reflexion & LangGraph")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Async wrapper for MCP agent call
    async def run_agent():
        return await client.agents(
            llm_model=model,
            llm_provider=provider,
            question=prompt,
        )

    # Run the async function
    agent_response = asyncio.run(run_agent())

    # Run the LangChain chain
    chain = Chain()
    chain._model = model  # Override model dynamically
    chain_pipeline = chain.first_response()
    chain_response = chain_pipeline.invoke({"input": prompt})

    # Combine responses (optional: choose one or both)
    final_response = f"**Agent Response:**\n{agent_response}\n"

    # Display assistant response
    st.session_state.messages.append({"role": "assistant", "content": final_response})
    with st.chat_message("assistant"):
        st.markdown(final_response)
