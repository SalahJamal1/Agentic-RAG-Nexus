from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.consts import (
    RETRIEVE,
    GOOGLE_DRIVE,
    GITHUB,
    GENERATE,
    GRADE_DOCUMENTS,
    MYSQL,
    GENERAL,
    RECOVERY,
)

from graph.nodes.retriever_node import retriever_node
from graph.nodes.grade_documents_node import grade_documents_node
from graph.nodes.generation_node import generation_node
from graph.nodes.hallucinations_node import hallucinations_node
from graph.nodes.router_node import router
from graph.nodes.tools import (
    get_google_drive_mcp,
    get_mysql_mcp,
    get_github_mcp,
)
from graph.nodes.general_node import general_node
from graph.nodes.recovery_node import recovery_node


workflow = StateGraph(GraphState)


# =========================
# ROUTER
# =========================

workflow.set_conditional_entry_point(router)


# =========================
# SOURCE NODES
# =========================

workflow.add_node(GENERAL, general_node)

workflow.add_node(RETRIEVE, retriever_node)
workflow.add_node(GOOGLE_DRIVE, get_google_drive_mcp)
workflow.add_node(GITHUB, get_github_mcp)
workflow.add_node(MYSQL, get_mysql_mcp)


# =========================
# DOCUMENT GRADING
# =========================

workflow.add_node(
    GRADE_DOCUMENTS,
    grade_documents_node
)

workflow.add_edge(
    RETRIEVE,
    GRADE_DOCUMENTS
)

workflow.add_edge(
    GOOGLE_DRIVE,
    GRADE_DOCUMENTS
)

workflow.add_edge(
    GITHUB,
    GRADE_DOCUMENTS
)

workflow.add_edge(
    MYSQL,
    GRADE_DOCUMENTS
)


# =========================
# GENERATION
# =========================

workflow.add_node(
    GENERATE,
    generation_node
)

workflow.add_edge(
    GRADE_DOCUMENTS,
    GENERATE
)


# =========================
# HALLUCINATION / ANSWER GRADER
# =========================

workflow.add_conditional_edges(
    GENERATE,
    hallucinations_node,
    {
        "useful": END,
        "failed": END,
        "regenerate": GENERATE,
        "recover": RECOVERY,
    }
)


# =========================
# RECOVERY
# =========================

workflow.add_node(
    RECOVERY,
    recovery_node
)

workflow.add_conditional_edges(
    RECOVERY,
    recovery_node,
)


# =========================
# GENERAL CHAT
# =========================

workflow.add_edge(
    GENERAL,
    END
)


# =========================
# COMPILE
# =========================

memory=MemorySaver()

app = workflow.compile(checkpointer=memory)