from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph,END

from graph.state import GraphState
from graph.consts import RETRIEVE,GOOGLE_DRIVE,GITHUB,GENERATE,GRADE_DOCUMENTS,MYSQL,GENERAL
from graph.nodes.retriever_node import retriever_node
from graph.nodes.grade_documents_node import grade_documents_node
from graph.nodes.generation_node import generation_node
from graph.nodes.hallucinations_node import hallucinations_node
from graph.nodes.router_node import router
from graph.nodes.tools import get_google_drive_mcp,get_mysql_mcp,get_github_mcp
from graph.nodes.general_node import general_node
from graph.nodes.decide import decide




workflow=StateGraph(GraphState)
workflow.set_conditional_entry_point(router,{
    RETRIEVE:RETRIEVE,
    MYSQL:MYSQL,
    GOOGLE_DRIVE:GOOGLE_DRIVE,
    GITHUB:GITHUB,
    GENERAL:GENERAL
})
workflow.add_node(GENERAL,general_node)
workflow.add_edge(GENERAL,END)

workflow.add_node(RETRIEVE,retriever_node)
workflow.add_node(GOOGLE_DRIVE,get_google_drive_mcp)
workflow.add_node(GITHUB,get_github_mcp)
workflow.add_node(MYSQL,get_mysql_mcp)

workflow.add_node(GRADE_DOCUMENTS,grade_documents_node)


workflow.add_conditional_edges(RETRIEVE,decide,{
    GRADE_DOCUMENTS:GRADE_DOCUMENTS,
    MYSQL:MYSQL,
    GOOGLE_DRIVE:GOOGLE_DRIVE,
    GITHUB:GITHUB,
})
workflow.add_conditional_edges(MYSQL,decide,{
    GRADE_DOCUMENTS:GRADE_DOCUMENTS,
    GOOGLE_DRIVE:GOOGLE_DRIVE,
    GITHUB:GITHUB,
    RETRIEVE:RETRIEVE,
})
workflow.add_conditional_edges(GOOGLE_DRIVE,decide,{
    GRADE_DOCUMENTS:GRADE_DOCUMENTS,
    MYSQL:MYSQL,
    GITHUB:GITHUB,
    RETRIEVE:RETRIEVE,
})

workflow.add_conditional_edges(GITHUB,decide,{
    GRADE_DOCUMENTS:GRADE_DOCUMENTS,
    MYSQL:MYSQL,
    GOOGLE_DRIVE:GOOGLE_DRIVE,
    RETRIEVE:RETRIEVE,
})



workflow.add_node(GENERATE,generation_node)

workflow.add_edge(GRADE_DOCUMENTS,GENERATE)

workflow.add_conditional_edges(GENERATE,hallucinations_node,{
    "useful":END,
    "not useful":GENERATE,
})

app=workflow.compile()


