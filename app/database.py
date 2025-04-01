from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:password@localhost/fastapi"  
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"  

# syntax: postgresql://username:password@host/database_name
# postgres is the username. 
# password is the password.
# localhost is the host.
# fastapi is the database name.


'''SQLAlchemy (in the synchronous example) uses psycopg2 as a backend driver to communicate with PostgreSQL databases. 
SQLAlchemy itself doesn't handle the actual database connections, but it relies on a database driver to do so. 
For PostgreSQL, psycopg2 is a popular driver that SQLAlchemy uses under the hood.
SQLAlchemy automatically uses the appropriate driver to connect to PostgreSQL. 
Since we specify the postgresql:// prefix in the connection string, SQLAlchemy will look for the PostgreSQL driver. 
If you have psycopg2 installed, it will use that driver to establish the connection.
'''
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
# The Base class is a foundational component in SQLAlchemy that serves as the declarative base for defining database models.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
