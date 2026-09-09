from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from graph.state import llm

class RecoveryDecision(BaseModel):
    datasource: Literal[
        "Rag",
        "Github",
        "Google Drive",
        "Mysql",
        "Generate",
    ] = Field(
        description="Choose the best datasource to recover the answer."
    )

llm_with_structured = llm.with_structured_output(RecoveryDecision)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a recovery router for an Agentic RAG system.

The previous answer was not good enough.

Choose the best next action:

- Rag: use the vector database
- Github: retrieve GitHub repository information
- Google Drive: retrieve documents from Google Drive
- Mysql: retrieve notes from MySQL
- Generate: try generating the answer again using the existing context

Choose the datasource that is most likely to provide
information needed to answer the user's question.
"""
    ),
    (
        "human",
        """
Question:
{question}

Current documents:
{documents}

Previous answer:
{generation}

Choose the best recovery action.
"""
    ),
])


recovery_chain = prompt | llm_with_structured