from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import END, MessageGraph
from chains.chain import Chain
from chains.chain import Chain
from tools.serpApi import SerpApiSearch


class Graph:
    def __init__(self, text):
        self._REFLECT = "reflect"
        self._GENERATE = "generate"
        self.chain = Chain()
        self.text = text
        self.graph = None
        self.__max_iterations = 2

    # def __first_response_node(self, state: Sequence[BaseMessage]):
    #     Chain.
    #     return self.chain.generation_chain().invoke({"text": state})

    # def __revision_response_node(self, state: Sequence[BaseMessage]) -> List[BaseMessage]:
    #     result = self.chain.reflection_chain().invoke({"text": state})
    #     return [HumanMessage(content=result.content)]

    # def __should_continue(self, state: Sequence[BaseMessage]):
    #     return END if len(state) > 6 else self._REFLECT

    def build_chain(self):
        builder = MessageGraph()
        chains = Chain()
        builder.add_node("draft", chains.first_response())
        serp = SerpApiSearch()
        builder.add_node("serp_tool", serp)
        builder.add_node("revised", chains.revision_response())

        builder.add_edge("draft", "serp_tool")
        builder.add_edge("serp_tool", "revised")

        # Conditon to stop or countinue
        builder.add_conditional_edges(
            "revise", self.__revisory_node(), {END: END, "serp_tool": "__revisory_node"}
        )

        self.graph = builder.compile()
        ## uncomment if you dcided to print the text at the terminal
        print(self.graph.get_graph().draw_mermaid())
        return self.graph

    # This function decides whether to countinue to to stop
    def __revisory_node(self, state: List[BaseMessage]) -> str:
        count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
        num_iteration = count_tool_visits
        if num_iteration > self.__max_iterations:
            return END
        return "serp_tool"


# if __name__ == "__main__":
#     graph_instance = Graph()
#     graph_instance.build_chain()
