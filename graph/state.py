from langchain_ollama import ChatOllama
from typing import  NotRequired, TypedDict

llm=ChatOllama(model="qwen3:1.7b",temperature=0)

class GraphState(TypedDict):
    generation:NotRequired[str]
    retry_count:NotRequired[int]
    question:NotRequired[str]
    documents:NotRequired[list[str]]
    context:NotRequired[str]
    sources:NotRequired[list[str]]

