import asyncio

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from graph.rag.vectorstore import  splitter, index_async


urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

def web_loader() -> list[Document]:
    sub_list = [WebBaseLoader(url).load() for url in urls]
    documents = [item for sublist in sub_list for item in sublist]
    return documents

async def ingestion(documents:list[Document]):
    try:
        print(f"Starting ingestion of {len(documents)} documents...")

        chunks=splitter.split_documents(documents)
        print(
            f"Created {len(chunks)} chunks "
            f"from {len(documents)} documents"
        )

        await index_async(chunks)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(ingestion(web_loader()))
