from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# db = SQLAlchemy()


# class ChatHistory(Base):

#     __tablename__ = "ChatHistory"

#     id = Column("id", Integer, primary_key=True, autoincrement=True)
#     author = Column("author", String, nullable=False)
#     chat = Column("chat", String, nullable=False)

#     def __int__(self, author, chat):
#         self.content = author
#         self.content = chat

#     def __repr__(self):
#         return f"({self.id} {self.author} {self.chat})"
    
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
