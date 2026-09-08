from graph.consts import RETRIEVE,GOOGLE_DRIVE,GITHUB,MYSQL,GENERAL
from graph.chains.router_chain import router_chain,RouteQuery
from graph.state import GraphState


def router(state:GraphState):
    question = state["question"]
    query:RouteQuery=router_chain.invoke({"question":question})
    print(f"-- Router {query.datasource.upper()}--")
    if query.datasource=="Rag":
        return RETRIEVE
    if query.datasource=="Google Drive":
        return GOOGLE_DRIVE
    if query.datasource=="Mysql":
        return MYSQL
    if query.datasource=="Github":
        return GITHUB

    if query.datasource == "General":
        return GENERAL

    return RETRIEVE