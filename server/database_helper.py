import sqlite3
import uuid
from flask import g

DATABASE_URI = 'database.db'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)
    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

def sign_in(email, password):
    cursor = get_db().execute("select * from user where email like ? and password like ?", [email, password])
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return False
    token = generate_token(email, password)
    get_db().execute("insert into logged_in values(?,?)", [email, token])
    get_db().commit()
    return token

def generate_token(email, password):
    return str(uuid.uuid4())



def save_user(email, password, name, familyName, gender, city, country):
    try:
        get_db().execute("insert into user values(?,?,?,?,?,?,?);", [email, password, name, familyName, gender, city, country])
        get_db().commit()
        return True
    except:
        return False

def sign_out(token):
    try:
        get_db().execute("delete from logged_in where token like ?;", [token])
        get_db().commit()
        return True
    except:
        return False


def get_user_data_by_token(token):
    user_name = signed_in_users(token)

    cursor = get_db().execute('select * from user where name like ?', [user_name])
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_user_data_by_email(token, email):
    cursor = get_db().execute('select * from user where email like ?', [email])
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_user_messages_by_token(token):
    user_name = signed_in_users(token)

    cursor = get_db().execute('select messages from user where name like ?', [user_name])
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_user_messages_by_email(token, email):
    cursor = get_db().execute('select messages from user where email like ?', [email])
    rows = cursor.fetchall()
    cursor.close()
    return rows