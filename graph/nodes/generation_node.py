from graph.chains.generation_chain import generation_chain
from graph.state import GraphState


def generation_node(state:GraphState)->GraphState:
    print("--Generation Node--")
    question=state["question"]
    context=state["context"]
    retry_count=state.get("retry_count",0)+1
    generation=generation_chain.invoke({"question":question,"context":context})
    return  {**state,"generation":generation,"retry_count":retry_count}