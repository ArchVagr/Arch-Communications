import sqlite3

import pydantic
from flask import Flask,request
import sqlite3 as sql
import main
from pydantic import BaseModel,constr
import json

#SERVER


server=Flask(__name__)

class UserVer(BaseModel):
    username:str
    password:str

class Chat(BaseModel):
    participant_1:int
    participant_2:int

class MessageRequest(BaseModel):
    chat_id:int

class Message(BaseModel):
    chat_id:int
    user_id:int
    content:str

def message_to_dict(m):
    return {
        "id": m.id,
        "chat_id": m.chat_id,
        "author_id": m.author_id,
        "content": m.content,
        "created_at": m.created_at.isoformat() if m.created_at else None,
    }



@server.post("/add")
def handle_signup():
    received = request.get_json()
    query = UserVer.model_validate(received)
    try:
        attempt=main.add_user(query.username,query.password)
        return {"status":attempt}
    except sql.IntegrityError:
        return  {"status":False}
    else:
        return {"status": False}

@server.post("/signin")
def signin():
    received=request.get_json()
    query=UserVer.model_validate(received)
    try:
        check=main.signup_verification(query.username,query.password)
        if check:
            return {"status":check.id}
        else:
            return {"status":False}
    except (pydantic.ValidationError, sqlite3.IntegrityError):
        return {"status":False}


@server.post("/search")
def search():
    query=request.get_json()
    results=main.users_search(query['query'])
    final=[]
    if not results:
        return False
    elif results:
        for i in results:
            final.append({i.username:i.id})
        return {"results":final}

@server.post("/add_chat")
def add_chat():
    data=request.get_json()
    print(data)
    chat=Chat.model_validate(data)
    res=main.search_chat(chat.participant_1, chat.participant_2)
    if res:
        return  {"status": res.chat_id}
    elif res is None:
        action=main.add_chat(chat.participant_1,chat.participant_2)
        return {"status": action}
    else:
        return {"status": False}

@server.post("/search_message")
def search_message():
    data=request.get_json()
    id=MessageRequest.model_validate(data)
    print(id.chat_id)
    try:
        action=main.search_messages(id.chat_id)
        print(action)
        return {"result":[message_to_dict(i) for i in action]}
    except (pydantic.ValidationError, sqlite3.IntegrityError):
        return {"result":False}

@server.post("/add_message")
def add_message():
    data=request.get_json()
    data=Message.model_validate(data)
    message=main.add_message(data.chat_id,data.user_id,data.content)
    return {"id":message.id}


server.run(port=5555)



