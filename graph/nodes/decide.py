from graph.state import GraphState
from graph.consts import RETRIEVE, GOOGLE_DRIVE, GITHUB, MYSQL, GRADE_DOCUMENTS

FALLBACK_ORDER = [MYSQL, GOOGLE_DRIVE, GITHUB, RETRIEVE]


def decide(state: GraphState):
    print("-- Decide --")
    documents = state.get("documents", [])
    if documents:
        return GRADE_DOCUMENTS

    sources = state.get("sources", [])
    for source in FALLBACK_ORDER:
        if source not in sources:
            return source

    return GRADE_DOCUMENTS
