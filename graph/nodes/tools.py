from langchain_core.documents import Document

from graph.mcp.google_drive_mcp_server import google_drive_mcp_server
from graph.mcp.github_mcp_server import get_github_repo
from graph.mcp.database_mcp_server import fetch_notes
from graph.consts import GOOGLE_DRIVE,GITHUB,MYSQL
from graph.state import GraphState


def get_google_drive_mcp(state:GraphState):
    print(f"--{GOOGLE_DRIVE}--")
    documents=state.get("documents",[])
    sources = state.get("sources",[])
    if GOOGLE_DRIVE not in sources:
        sources.append(GOOGLE_DRIVE)
    doc=google_drive_mcp_server()
    if doc:
        documents.extend(doc)
    return {**state,"documents":documents,"sources":sources}


def get_github_mcp(state:GraphState):
    print(f"--{GITHUB}--")
    documents = state.get("documents", [])
    sources = state.get("sources",[])
    if GITHUB not in sources:
        sources.append(GITHUB)
    doc = get_github_repo()
    if doc:
        documents.append(Document(page_content=str(doc), metadata={"source": "github"}))
    return {**state, "documents": documents,"sources":sources}


def get_mysql_mcp(state:GraphState):
    print(f"--{MYSQL}--")
    sources = state.get("sources", [])
    if MYSQL not in sources:
        sources.append(MYSQL)
    documents = state.get("documents", [])
    doc = fetch_notes()

    documents.extend(doc)
    return {**state, "documents": documents,"sources":sources}