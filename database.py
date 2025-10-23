from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# PostgreSQL connection string format:
# postgresql://username:password@host:port/database_name

POSTGRESQL_DATABASE_URL = "postgresql://saba:Akhvleda8@localhost:5432/fit_instruqtorebi_db"

engine = create_engine(POSTGRESQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
