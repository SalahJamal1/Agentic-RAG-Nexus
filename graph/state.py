import operator

from langchain_ollama import ChatOllama
from typing import NotRequired, TypedDict, Annotated
from langgraph.graph.message import add_messages

llm=ChatOllama(model="qwen3:1.7b",temperature=0)

class GraphState(TypedDict):
    generation:NotRequired[str]
    retry_count:NotRequired[int]
    question:NotRequired[str]
    documents:NotRequired[Annotated[list, operator.add]]
    messages:NotRequired[Annotated[list, add_messages]]
    context:NotRequired[str]
    sources:NotRequired[list[str]]

