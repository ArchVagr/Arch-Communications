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
    password:constr(min_length=8)

@server.post("/add")
def handle_signup():
    query = User(json.loads(request.get_json()))
    try:
        attempt=main.add_user(query.username,query.password)
        return {"status":True,'profile':attempt}
    except sql.IntegrityError:
        return  {"status":False}
    else:
        return {"status": False}

@server.post("/signin")
def signin():
    query=User(json.loads(request.get_json()))
    try:
        check=main.signup_verification(query.username,query.password)
        return {"status":check}
    except pydantic.ValidationError or sqlite3.IntegrityError:
        return {"status":False}


@server.post("/search")
def search():
    query=request.get_json()
    results=main.user_search(query['query'])
    final=[]
    if not results:
        return False
    elif results:
        for i in results:
            final.append({i[0]:i[1]})
        return {"results":final}





server.run(port=5555)




