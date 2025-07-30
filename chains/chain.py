from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import datetime
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from chains.schema import AnswerQuestion, ReviseAnswer
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class Chain:
    def __init__(self):
        load_dotenv()
        self._model = "llama3.2:latest"  # OllamaLLM.get_llm()['llm_model']
        self._jsn_parser = JsonOutputParser(return_id=True)
        self._str_parser = StrOutputParser(tools=[AnswerQuestion])

    def _actor_prompt_template(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert researcher.
                        Current time: {time}

                        Follow these steps:
                        1. Provide a ~250 word detailed answer to the user's question.
                        2. Reflect and critique your answer. Be specific and severe to maximize improvement.
                        3. Recommend 1-3 search queries to improve your answer.

                        Return your response in the following JSON format:
                        ```json
                        {
                        "answer": "...",
                        "reflection": {
                            "missing": "...",
                            "superfluous": "..."
                        },
                        "search_queries": ["...", "..."]
                        }
                        ```""",
                ),
                MessagesPlaceholder(variable_name="text"),
                (
                    "system",
                    "Answer the user's question above using the required format.",
                ),
            ]
        )

    def __first_prompt_template(self):
        return ChatPromptTemplate.from_messages(
            [("system", "Provide a detailed ~250 word answer."), ("human", "{input}")]
        )

    




    def __revised_instruction_template(self):
        return ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="text"),
            ("system", """Revise your answer using new information:
    - Use the previous critique to add important information.
    - Include numerical citations in your revised answer.
    - Add a "References" section at the bottom (not part of the word limit), e.g.:
    - [1] https://example.com
    - [2] https://example.com
    - Remove superfluous information and keep the answer under 250 words.""")
        ])



    # Langgraph chain/Node
    def revision_response(self):
        llm = ChatOllama(model=self._model)
        return self.__revised_instruction_template() | llm.bind_tools(
            tools=[ReviseAnswer], tool_choice="ReviseAnswer"
        )

    # Generate the first answer
    def first_response(self):
        llm = ChatOllama(model=self._model)
        return self.__first_prompt_template() | llm.bind_tools(
            tools=[AnswerQuestion], tool_choice="AnswerQuestion"
        )
