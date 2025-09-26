import sqlite3

import pydantic
from flask import Flask,request
import sqlite3 as sql
import main
from pydantic import BaseModel,constr
import json

#SERVER


server=Flask(__name__)

class User(BaseModel):
    username:str
    password:str

class Chat(BaseModel):
    participant_1:int
    participant_2:int


@server.post("/add")
def handle_signup():
    received = request.get_json()
    query = User.model_validate(received)
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
    query=User.model_validate(received)
    try:
        check=main.signup_verification(query.username,query.password)
        return {"status":check.id}
    except pydantic.ValidationError or sqlite3.IntegrityError:
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
    chat=Chat.model_validate(data)
    try:
        action=main.add_chat(chat.participant_1,chat.participant_2)
        return {"status": action}
    except pydantic.ValidationError or sqlite3.IntegrityError:
        return {"status": False}



server.run(port=5555)



