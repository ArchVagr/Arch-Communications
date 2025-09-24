import json
import os.path
import sqlite3 as sql



def create_table_accounts():
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)

    cursor=connection.cursor()
    cursor.execute(
        """
        CREATE TABLE Chats (
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_1 TEXT NOT NULL,
        participant_2 TEXT NOT NULL,
        created_at INTEGER NOT NULL
        );
        """,

    )
    cursor.close()

def add_user(username,password):
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)

    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO Accounts (username,password)
    VALUES
    (?,?)""",(username,password))
    connection.commit()
    cursor.close()

def verify_user(username,password):
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)

    cursor=connection.cursor()
    cursor.execute("""
    SELECT * FROM Accounts WHERE username=? and password=?
    """,(username,password))
    response=cursor.fetchall()
    if response:
        return list(response)
    else:
        return None

def user_search(username):
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username,id FROM Accounts WHERE username LIKE ?
        """, (username + "%",))
    response = cursor.fetchall()
    return response if response else False

def id_return(username,password):
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM Accounts WHERE username = ? AND password=?
        """, (username,password))
    response = cursor.fetchone()
    if response:
        for i in response:
            return i
    else:
        return False

def create_chat(participant_1,participant_2):
    PATH = "MessageDatabase.db"

    connection = sql.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Chats(participant_1,participant_2) VALUES(?,?)',
                   (participant_1,participant_2))
    connection.commit()
    cursor.close()




