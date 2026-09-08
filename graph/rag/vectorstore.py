import asyncio
import hashlib
import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


path = Path(__file__).resolve().parents[2] / "chroma_db"

embedding=OllamaEmbeddings(model="nomic-embed-text")


vectorstore=Chroma(collection_name="agentic_v1",persist_directory=str(path),embedding_function=embedding)
splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500,chunk_overlap=150)


def document_idx(document:Document):
    source=document.metadata.get("source","")
    page_content=document.page_content
    page=document.metadata.get("page","")
    return hashlib.sha256(f"{source}:{page}:{page_content}".encode()).hexdigest()



async def index_async(documents:list[Document]):
    batches=[documents[i:i+100] for i in range(0,len(documents),100)]
    async def add_batch(batch:list[Document],num_batch):
        try:
            ids=[document_idx(document) for document in batch]
            await vectorstore.aadd_documents(batch,ids=ids)
            return True
        except Exception as e:
            print(f"Error adding batch {num_batch + 1}: {e}")
            return False
    tasks=[add_batch(batch,i) for i,batch in enumerate(batches)]
    results=await asyncio.gather(*tasks, return_exceptions=True)
    successful=sum(1 for r in results if r is True)
    if successful==len(batches):
        print("Successfully indexed")
    else:
        print(
            f"Indexed {successful}/{len(batches)} batches successfully"
        )