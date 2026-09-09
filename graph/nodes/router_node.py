from langgraph.constants import Send

from graph.consts import (
    RETRIEVE,
    GOOGLE_DRIVE,
    GITHUB,
    MYSQL,
    GENERAL,
)

from graph.chains.router_chain import (
    router_chain,
    RouteQuery,
)

from graph.state import GraphState


def router(state: GraphState):

    question = state["question"]

    query: RouteQuery = router_chain.invoke(
        {"question": question}
    )

    print(f"-- Router: {query.datasources} --")

    routes = []

    for datasource in query.datasources:

        if datasource == "Rag":
            routes.append(
                Send(
                    RETRIEVE,
                    {
                        "question": question,
                    }
                )
            )

        elif datasource == "Google Drive":
            routes.append(
                Send(
                    GOOGLE_DRIVE,
                    {
                        "question": question,
                    }
                )
            )

        elif datasource == "Mysql":
            routes.append(
                Send(
                    MYSQL,
                    {
                        "question": question,
                    }
                )
            )

        elif datasource == "Github":
            routes.append(
                Send(
                    GITHUB,
                    {
                        "question": question,
                    }
                )
            )

        elif datasource == "General":
            routes.append(
                Send(
                    GENERAL,
                    {
                        "question": question,
                    }
                )
            )

    return routes