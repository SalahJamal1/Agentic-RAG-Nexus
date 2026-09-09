from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from graph.state import llm


class RouteQuery(BaseModel):
    datasources: list[
        Literal[
            "Rag",
            "Mysql",
            "Google Drive",
            "Github",
            "General",
        ]
    ] = Field(
        description=(
            "Choose one or more datasources required to answer the user's "
            "question. Use multiple datasources when the question requires "
            "combining, comparing, or merging information from multiple sources."
        )
    )


llm_with_structured = llm.with_structured_output(RouteQuery)


system = """
You are an expert query router for an AI assistant.

Your job is to choose the datasource or datasources required to answer
the user's question.

IMPORTANT:
You can choose ONE or MULTIPLE datasources.

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

Examples:
- "Find my GitHub repositories."
- "Search my repository for FastAPI."
- "Find the authentication code in my GitHub project."
- "Show me open issues in my repository."
- "Search GitHub for LangGraph examples."


5. General

Use General when the question does not require information from
the application's specialized datasources.

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


MULTI-SOURCE ROUTING:

If the user's question requires information from multiple datasources,
return ALL required datasources.

Examples:

"Compare my GitHub README with my Google Drive CV."
→ ["Github", "Google Drive"]

"Compare my GitHub project with the notes stored in MySQL."
→ ["Github", "Mysql"]

"Compare my CV from Google Drive with my GitHub projects."
→ ["Google Drive", "Github"]

"Use my GitHub project and my Drive documents to explain my experience."
→ ["Github", "Google Drive"]

"Compare my notes in MySQL with the knowledge base."
→ ["Mysql", "Rag"]

"Find my CV in Google Drive."
→ ["Google Drive"]

"What is the status of order 123?"
→ ["Mysql"]

"What is LangGraph?"
→ ["Rag"]

"Hi"
→ ["General"]


IMPORTANT RULES:

1. Choose at least ONE datasource.

2. Choose MULTIPLE datasources when the question explicitly requires
   combining, comparing, or merging information from multiple sources.

3. Do NOT choose every datasource by default.

4. Choose only the datasources actually required to answer the question.

5. If the question can be answered using one datasource, return only
   that datasource.

6. If the question requires information from two or more datasources,
   return all required datasources.

7. General should normally be used alone.

8. Do not invent a datasource.

9. The order of datasources should represent a reasonable retrieval order.

10. The router only decides WHERE to retrieve information from.
    It does NOT retrieve the information itself.

After routing, the application will:
1. Call the selected datasource tools.
2. Collect the retrieved information.
3. Merge the results into a shared context.
4. Send the combined context to the LLM.
5. Generate the final answer.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)


router_chain = prompt | llm_with_structured