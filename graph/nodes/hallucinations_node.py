from graph.state import GraphState
from graph.chains.hallucinations_chain import hallucinations_chain,GradeHallucinations
from graph.chains.answer_chain import answer_chain,GradeAnswer


def hallucinations_node(state:GraphState):
    question = state["question"]
    context = state["context"]
    generation=state["generation"]
    retry_count = state.get("retry_count",0)
    print(f"-- Hallucinations Node {retry_count}--")
    if retry_count>3:
        return "useful"

    score:GradeHallucinations=hallucinations_chain.invoke({"documents":context,"generation":generation})
    if score.binary_score is False:
        return "not useful"
    answer_score:GradeAnswer=answer_chain.invoke({"question":question,"generation":generation})
    if answer_score.binary_score:
        return "useful"
    return "not useful"




