from graph.chains.grade_documents_chain import GradeDocuments,grade_documents_chain
from graph.state import GraphState


def grade_documents_node(state:GraphState)->GraphState:
    print("-- Grade Documents Node --")
    question=state["question"]
    documents=state["documents"]
    filter_doc=[]
    for doc in documents:
        score:GradeDocuments=grade_documents_chain.invoke({"question":question,"document":doc})
        if score.binary_score:
            filter_doc.append(doc)
        else:
            continue

    context="\n\n".join(f"Source:{doc.metadata.get('source','')},Content:{doc.page_content}" for doc in filter_doc)

    return {
        **state,
        "context":context,
        "documents":filter_doc,
    }