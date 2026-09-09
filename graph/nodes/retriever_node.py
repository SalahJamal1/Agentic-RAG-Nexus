from graph.consts import RETRIEVE
from graph.state import GraphState
from graph.rag.retriever import retriever

def retriever_node(state:GraphState)->GraphState:
    print("--Retriever--")
    question=state["question"]
    documents=retriever.invoke(question)

    return {"documents":documents}