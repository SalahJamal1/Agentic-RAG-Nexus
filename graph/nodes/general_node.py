from graph.state import GraphState, llm


def general_node(state: GraphState):
    print("-- General Node --")

    question = state["question"]

    response = llm.invoke(question)

    return {
        **state,
        "generation": response.content,
    }