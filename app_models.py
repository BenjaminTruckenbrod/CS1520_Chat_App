from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ChatHistory(Base):

    __tablename__ = "ChatHistory"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    author = Column("author", String, nullable=False)
    message = Column("message", String, nullable=False)
    # timestamp = Column(DateTime, default=func.now())

    def __int__(self, author, message):
        self.content = author
        self.content = message

    def __repr__(self):
        return f"({self.id} {self.author} {self.message})"
    
class RegisteredUser(Base):
    __tablename__ = "RegisteredUsers"

    id = Column("id", Integer,  autoincrement=True)
    username = Column("username", String, primary_key=True, nullable=False)
    password = Column("password", String, nullable=False)

    def __int__(self, username, password):
        self.content = username
        self.content = password

    def __repr__(self):
        return f"({self.id} {self.username} {self.password})"
