import sqlalchemy.exc

from PATH import PATH
import sqlite3
from sqlalchemy import create_engine,String,Integer,ForeignKey,Column,DateTime,text
from sqlalchemy.orm import sessionmaker,declarative_base,Session,relationship

engine = create_engine(PATH)
Session = sessionmaker(bind=engine)
session=Session()

Base=declarative_base()

class User(Base):
    __tablename__ = "users"

    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

    messages = relationship("Message", back_populates="author")

def add_user(username,password):
    try:
        user=User(username=username,password=password)
        session.add(user)
        session.commit()
        return user.id
    except sqlite3.IntegrityError:
        session.rollback()
        return False
    except sqlalchemy.exc.SQLAlchemyError:
        session.rollback()
        return False

def signup_verification(username,password):
    search=session.query(User).filter_by(username=username,password=password).first()
    return search

def users_search(username):
    entered = f"%{username}%"
    search=session.query(User).filter(User.username.like(entered)).all()
    return search

class Chat(Base):
    __tablename__='chats'

    chat_id=Column(Integer,primary_key=True,autoincrement=True)
    participant_1 = Column(Integer, ForeignKey("users.id"))
    participant_2 = Column(Integer, ForeignKey("users.id"))

    participant1 = relationship("User", foreign_keys=[participant_1])
    participant2 = relationship("User", foreign_keys=[participant_2])

    messages = relationship('Message', back_populates='chat')
def add_chat(participant_1,participant_2):
    if participant_1<participant_2:
        chat=Chat(participant_1=participant_1, participant_2=participant_2)
        session.add(chat)
        session.commit()
    else:
        chat = Chat(participant_1=participant_2, participant_2=participant_1)
        session.add(chat)
        session.commit()
    return chat.chat_id

def search_chat(participant_1,participant_2):
    chat=session.query(Chat).filter_by(participant_1=participant_1,participant_2=participant_2).first()
    return chat

class Message(Base):
    __tablename__='messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id=Column(Integer,ForeignKey('chats.chat_id'),nullable=False)
    author_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    content=Column(String,nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    author=relationship('User',back_populates='messages')
    chat=relationship('Chat',back_populates='messages')
def add_message(chat_id,author_id,content):
    message=Message(chat_id=chat_id,author_id=author_id,content=content)
    session.add(message)
    session.commit()
    return message

def search_messages(chat_id):
    search=session.query(Message).filter_by(chat_id=chat_id).all()
    return search

