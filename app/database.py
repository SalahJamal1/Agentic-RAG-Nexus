from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker,declarative_base

server_url = "mysql+pymysql://root:2025@localhost:3306"
database = "agentic_db"

engine=create_engine(server_url)


with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))

engine=create_engine(f"{server_url}/{database}")

Session=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()