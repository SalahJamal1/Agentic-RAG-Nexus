from graph.consts import RETRIEVE
from graph.state import GraphState
from graph.rag.retriever import retriever

def retriever_node(state:GraphState)->GraphState:
    print("--Retriever--")
    question=state["question"]
    documents=retriever.invoke(question)
    sources=state.get("sources",[])
    if  RETRIEVE not in sources:
        sources.append(RETRIEVE)
    return {**state,"documents":documents,"sources":sources}