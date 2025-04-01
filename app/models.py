from app.database import Base   # We are importing the Base class from the database module(file).
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


''''Purpose of Post(Base) in models.py
Table Definition: It defines the schema of the posts table, including columns and their data types.
Database Operations: It is used to perform database operations like adding new posts, querying existing posts, updating posts, and deleting posts.'''

class Post(Base):
    __tablename__="posts"
    
    id = Column(Integer, primary_key=True, nullable=False)    # Due to the primary_key=True, this column is the primary key and will auto increment.
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='true') 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False )

    owner = relationship("User")
'''In social media like platfrom we need to know the information (like username or email...)
when retrieving the posts to know whose post is it. So sqlalchemy using relationship automatically establish a relationship
and fetches some information from the refered class or something.
Keep in mind it doesn't change our posts table or add any key.
It will return the owner property with some information based on the relationship with "User" class.
So in our case it will return a User based on owner_id.
'''


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at =Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))


class Vote(Base):
    __tablename__="votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)