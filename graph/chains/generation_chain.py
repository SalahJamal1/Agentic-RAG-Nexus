from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from graph.state import llm


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful AI assistant.

Answer the user's question using the provided context.

Use the conversation history when it helps understand
references to previous messages.

If the context does not contain enough information,
say that you don't have enough information.
"""
    ),

    MessagesPlaceholder(variable_name="messages"),

    (
        "human",
        """Context:

{context}

Current question:

{question}
"""
    ),
])

generation_chain = prompt | llm | StrOutputParser()