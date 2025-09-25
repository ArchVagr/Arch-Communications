import pydantic
from flask import Flask,request
import sqlite3 as sql
import main
from pydantic import BaseModel,constr

#SERVER


server=Flask(__name__)

class User(BaseModel):
    username:str
    password:constr(min_length=8)

@server.post("/add")
def handle_signup():
    query = User(request.get_json())
    try:
        main.add_user(query.username,query.password)
        return {"status":True,id:main.id_return(query.username,query.password)}
    except sql.IntegrityError:
        return  {"status":False}
    else:
        return {"status": False}

@server.post("/signin")
def signin():
    query=User(request.get_json())
    try:
        check=main.id_return(query.username,query.password)
        return {"status":check}
    except pydantic.ValidationError:
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




