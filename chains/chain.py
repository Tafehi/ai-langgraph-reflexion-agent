from pyclbr import Class
from socket import timeout
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv


# from models.ollama_model import OllamaLLM
class Chain:
    def __init__(self):
        load_dotenv()
        self._model = os.getenv("OLLAMA_LLM")

    def __reflection_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are a professional text editor and content strategist. Your task is to receive a piece of text and perform the following:
                Critique the text:
                Evaluate clarity, coherence, grammar, and tone.
                Identify weaknesses in structure, engagement, and message delivery.
                Highlight any inconsistencies or areas lacking impact.
                finally improve the text.

                """,
                ),  # your full prompt here
                MessagesPlaceholder(variable_name="text"),
            ]
        )

    def __generation_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
            you are a text editor assisstant tasked with writting excellent texts.
            Generate the best text possible for the user's.
            If the user provide critique, respond with a revised version of your previous attemps
            Offer tips for future writing in similar contexts.
            """,
                ),  # your full prompt here
                MessagesPlaceholder(variable_name="text"),
            ]
        )

    def generation_chain(self):
        llm = ChatOllama(model=self._model)
        return self.__generation_prompt() | llm

    def reflection_chain(self):
        llm = ChatOllama(model=self._model)
        return self.__reflection_prompt() | llm
