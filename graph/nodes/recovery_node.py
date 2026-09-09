from langgraph.constants import Send
from graph.consts import (
    RETRIEVE,
    GOOGLE_DRIVE,
    GITHUB,
    MYSQL,GENERATE
)

from graph.chains.recovery_chain import recovery_chain
from graph.state import GraphState



def recovery_node(state: GraphState):
    question = state["question"]
    documents = state.get("documents", [])
    generation = state.get("generation", "")

    decision = recovery_chain.invoke({
        "question": question,
        "documents": documents,
        "generation": generation,
    })

    print(f"-- Recovery Router: {decision.datasource} --")

    if decision.datasource == "Rag":
        return Send(
            RETRIEVE,
            {"question": question}
        )

    if decision.datasource == "Github":
        return Send(
            GITHUB,
            {"question": question}
        )

    if decision.datasource == "Google Drive":
        return Send(
            GOOGLE_DRIVE,
            {"question": question}
        )

    if decision.datasource == "Mysql":
        return Send(
            MYSQL,
            {"question": question}
        )

    return GENERATE