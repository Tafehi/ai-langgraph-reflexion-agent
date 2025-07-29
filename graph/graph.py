from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains.chain import Chain


class Graph:
    def __init__(self, text):
        self._REFLECT = "reflect"
        self._GENERATE = "generate"
        self.chain = Chain()
        self.text = text
        self.graph = None

    def __generation_node(self, state: Sequence[BaseMessage]):
        return self.chain.generation_chain().invoke({"text": state})

    def __reflection_node(self, state: Sequence[BaseMessage]) -> List[BaseMessage]:
        result = self.chain.reflection_chain().invoke({"text": state})
        return [HumanMessage(content=result.content)]

    def __should_continue(self, state: Sequence[BaseMessage]):
        return END if len(state) > 6 else self._REFLECT

    def build_chain(self):
        builder = MessageGraph()
        builder.add_node(self._GENERATE, self.__generation_node)
        builder.add_node(self._REFLECT, self.__reflection_node)
        builder.set_entry_point(self._GENERATE)
        builder.add_conditional_edges(
            self._GENERATE,
            self.__should_continue,
            {END: END, self._REFLECT: self._REFLECT},
        )
        builder.add_edge(self._REFLECT, self._GENERATE)
        self.graph = builder.compile()
        ## uncomment if you dcided to print the text at the terminal
        # print(self.graph.get_graph().draw_mermaid())
        return self.graph


# if __name__ == "__main__":
#     graph_instance = Graph()
#     graph_instance.build_chain()
