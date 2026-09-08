from fastmcp import FastMCP, Context
from langchain_core.documents import Document

from app.database import Session,engine

from app.models import Notes,Base
from contextlib import asynccontextmanager



mcp=FastMCP(name="Sql Server")

Base.metadata.create_all(engine)



@mcp.tool()
def fetch_notes():
    db = Session()
    try:
        notes = db.query(Notes).all()
        return [Document(metadata={'source':note.id},page_content=f"content:{note.content}") for note in notes]
    finally:
        db.close()





if __name__ == '__main__':
    mcp.run(transport="http",port=8082)