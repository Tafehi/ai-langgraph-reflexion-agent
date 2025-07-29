from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import datetime
from dotenv import load_dotenv
from chains.schema import AnswerQuestion, ReviseAnswer


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
                    """You are expert researcher.
                    Current time: {time}

                    1. {first_instruction}
                    2. Reflect and critique your answer. Be severe to maximize improvement.
                    3. Recommend search queries to research information and improve your answer.""",
                ),
                MessagesPlaceholder(variable_name="text"),
                (
                    "system",
                    "Answer the user's question above using the required format.",
                ),
            ]
        ).partial(
            time=lambda: datetime.datetime.now().isoformat(),
        )

    def __first_prompt_template(self):
        return ChatPromptTemplate.from_messages(
            [("system", "Provide a detailed ~250 word answer."), ("human", "{input}")]
        )

    # Generate the first answer
    def first_responder(self):
        llm = ChatOllama(model=self._model)
        return self.__first_prompt_template() | llm.bind_tools(
            tools=[AnswerQuestion], tool_choice="AnswerQuestion"
        )

    def __revised_instruction_template(self):
        return """Reivse your answer using new information\n.
        - You should use the previuos citique to add important information to your answer.\n
        - You must include numerical citation in your revised answer to ensure it can be verified.\n
        - Add a "References" section to the bottom of your answer (which dose not count toward the worl limits in the form of)\n.
            - [1] https://example.com
            - [2] https://example.com
        - You should use the previous critique toi remove superfluous information from your answer and make SURE it is not more than 250 words.
        """

    def revision_response(self):
        llm = ChatOllama(model=self._model)
        return self.__revised_instruction_template | llm.bind_tools(
            tools=[ReviseAnswer], tool_choice="ReviseAnswer"
        )
