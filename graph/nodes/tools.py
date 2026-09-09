from langchain_core.documents import Document

from graph.mcp.google_drive_mcp_server import google_drive_mcp_server
from graph.mcp.github_mcp_server import get_github_repo
from graph.mcp.database_mcp_server import fetch_notes
from graph.consts import GOOGLE_DRIVE,GITHUB,MYSQL
from graph.state import GraphState


def get_google_drive_mcp(state:GraphState):
    print(f"--{GOOGLE_DRIVE}--")
    doc=google_drive_mcp_server()
    return {"documents":doc or []}


def get_github_mcp(state:GraphState):
    print(f"--{GITHUB}--")

    doc = get_github_repo()
    documents=[Document(page_content=str(doc), metadata={"source": "github"})]
    return { "documents": documents}


def get_mysql_mcp(state:GraphState):
    print(f"--{MYSQL}--")
    doc = fetch_notes()

    return { "documents": doc}