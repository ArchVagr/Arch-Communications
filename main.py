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
        return user
    except sqlite3.IntegrityError:
        return False
def signup_verification(username,password):
    search=session.query(User).filter_by(username=username,password=password)
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
    session.add(Chat(participant_1=participant_1,participant_2=participant_2))
    session.commit()

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
    session.add(Message(chat_id=chat_id,author_id=author_id,content=content))
    session.commit()




# def create_table_messages():
#
#     connection = sql.connect(PATH)
#     connection.execute("PRAGMA foreign_keys = ON;")  # включаем поддержку внешних ключей
#     cursor = connection.cursor()
#
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS Accounts (
#             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username INTEGER NOT NULL,
#             password INTEGER NOT NULL
#         );
#         """
#     )
#
#     connection.commit()
#     cursor.close()
#     connection.close()
#
# def add_user(username,password):
#
#
#     connection = sql.connect(PATH)
#
#     cursor = connection.cursor()
#     cursor.execute("""
#     INSERT INTO Accounts (username,password)
#     VALUES
#     (?,?)""",(username,password))
#     connection.commit()
#     cursor.close()
#
# def verify_user(username,password):
#
#
#     connection = sql.connect(PATH)
#
#     cursor=connection.cursor()
#     cursor.execute("""
#     SELECT * FROM Accounts WHERE username=? and password=?
#     """,(username,password))
#     response=cursor.fetchall()
#     if response:
#         return list(response)
#     else:
#         return None
#
# def user_search(username):
#
#
#     connection = sql.connect(PATH)
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT username,id FROM Accounts WHERE username LIKE ?
#         """, (username + "%",))
#     response = cursor.fetchall()
#     return response if response else False
#
# def id_return(username,password):
#
#
#     connection = sql.connect(PATH)
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT id FROM Accounts WHERE username = ? AND password=?
#         """, (username,password))
#     response = cursor.fetchone()
#     if response:
#         for i in response:
#             return i
#     else:
#         return False
#
# def create_chat(participant_1,participant_2):
#
#
#     connection = sql.connect(PATH)
#     cursor = connection.cursor()
#     cursor.execute('INSERT INTO Chats(participant_1,participant_2) VALUES(?,?)',
#                    (participant_1,participant_2))
#     connection.commit()
#     cursor.close()
#
# def create_message(chat_id,sender,text):
#
#     connection = sql.connect(PATH)
#
#     cursor = connection.cursor()
#     cursor.execute('''INSERT INTO Messages(sender_id,chat_id,message_text) VALUES(?,?,?)''',(chat_id,sender,text))
#
#     connection.commit()
#     cursor.close()
#
# create_table_messages()