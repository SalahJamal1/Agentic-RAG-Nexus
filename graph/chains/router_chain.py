from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from graph.state import llm


class RouteQuery(BaseModel):
    datasource: Literal[
        "Rag",
        "Mysql",
        "Google Drive",
        "Github",
        "General",
    ] = Field(
        description=(
            "Choose exactly one datasource. "
            "Use General for greetings, casual conversation, "
            "simple general questions, or questions that do not "
            "require information from Rag, Mysql, Google Drive, or Github."
        )
    )


llm_with_structured = llm.with_structured_output(RouteQuery)


system = """
You are an expert query router for an AI assistant.

Your job is to choose EXACTLY ONE datasource for the user's question.

Available datasources:

1. Rag
Use Rag when the answer can be found in the application's indexed
knowledge-base documents.

Examples:
- "What is prompt engineering?"
- "Explain adversarial attacks."
- "What is LangGraph?"
- "Explain RAG."
- "What is an AI agent?"

2. Mysql
Use Mysql when the question requires structured application/database
information stored in MySQL.

Examples:
- "Show me my orders."
- "What is the status of order 123?"
- "How many users are registered?"
- "Show me the latest notes."
- "Find the user with email example@email.com."

3. Google Drive
Use Google Drive when the question requires searching or retrieving
files stored in the user's Google Drive.

Examples:
- "Find my CV."
- "Search my Google Drive for my React certificate."
- "Show me the PDF about Java."
- "What does my CV say about my Python experience?"
- "Find documents containing LangGraph."

4. Github
Use Github when the question requires information from GitHub repositories,
code, issues, pull requests, commits, branches, or GitHub projects.
5. General

Use General when the user's message does not require any of the
four specialized datasources.

Examples:
- "Hi"
- "Hello"
- "How are you?"
- "Good morning"
- "Thanks"
- "Tell me a joke"
- "What is your name?"
- "Who is Albert Einstein?"
- "What is the capital of France?"
- "What can you do?"

General should also be used for casual conversation and simple
questions that do not require the application's private data.

IMPORTANT:
If the question requires information from the application's
knowledge base, use Rag.

If the question requires MySQL data, use Mysql.

If the question requires Google Drive files, use Google Drive.

If the question requires GitHub data, use Github.

Otherwise use General.

Examples:
- "Find my GitHub repositories."
- "Search my repository for FastAPI."
- "Find the authentication code in my GitHub project."
- "Show me open issues in my repository."
- "Search GitHub for LangGraph examples."

IMPORTANT RULES:

- Choose EXACTLY ONE datasource.
- Do not choose multiple datasources.
- Do not invent a datasource.
- Choose the datasource that is MOST directly related to the question.

Routing examples:

"What is prompt engineering?"
→ Rag

"Explain adversarial attacks."
→ Rag

"What is LangGraph?"
→ Rag

"What is the status of order 123?"
→ Mysql

"Show me my notes."
→ Mysql

"Find my CV in Google Drive."
→ Google Drive

"Search my Drive for React.pdf."
→ Google Drive

"Find the authentication implementation in my GitHub repository."
→ Github

"Show me my GitHub repositories."
→ Github
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

router_chain = prompt | llm_with_structured