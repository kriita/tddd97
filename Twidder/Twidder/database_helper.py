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

def check_if_user_logged_in(email):
    cursor = get_db().execute("select * from logged_in where email like ?", [email])
    messages = cursor.fetchall()
    cursor.close()
    return len(messages) != 0

def generate_token(email, password):
    return str(uuid.uuid4())

def save_user(email, password, name, familyName, gender, city, country):
    try:
        get_db().execute("insert into user values(?,?,?,?,?,?,?);", [email, password, name, familyName, gender, city, country])
        get_db().commit()
        return True
    except:
        return False

def check_if_user_in_database(email):
    cursor = get_db().execute("select * from user where email like ?", [email])
    messages = cursor.fetchall()
    cursor.close()
    return len(messages) != 0
    
def sign_out(token):
    get_db().execute("delete from logged_in where token like ?;", [token])
    get_db().commit()
    return True

def check_if_user_logged_in_token(token):
    cursor = get_db().execute("select * from logged_in where token like ?", [token])
    messages = cursor.fetchall()
    cursor.close()
    return len(messages) != 0

def change_password(token,newPassword, oldPassword):
    cursor = get_db().execute("select email from logged_in where token like ?", [token])
    email = cursor.fetchall()
    cursor.close()

    cursor = get_db().execute("select password from user where email like ?", [email[0][0]])
    password = cursor.fetchall()
    cursor.close()

    if password[0][0] == oldPassword:
        get_db().execute("update user set password = ? where email like ?", [newPassword, email[0][0]])
        get_db().commit()
        return True;
    else:
        return False;

def get_user_data_by_token(token):
    cursor = get_db().execute("select * from logged_in where token like ?", [token])
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return False
    return get_user_data_by_email(token,data[0][0])

def get_user_data_by_email(token, email):
    cursor = get_db().execute("select * from user where email like ?", [email])
    messages = cursor.fetchall()
    cursor.close()
    if len(messages) > 0:
        messages = messages[0]
        return {"email" : messages[0], "firstname" : messages[2], "familyname" : messages[3], "gender" : messages[4], "city" : messages[5], "country" : messages[6]}
    else:
        return {}

def get_user_messages_by_token(token):
    cursor = get_db().execute("select * from logged_in where token like ?", [token])
    data = cursor.fetchall()
    cursor.close()
    return get_user_messages_by_email(token, data[0][0])

def get_user_messages_by_email(token, email):
    cursor = get_db().execute("select * from messages where target like ?", [email])
    messages = cursor.fetchall()
    cursor.close()
    return {"messages" : messages}

def post_message(token, message, target):
    user_data = get_user_data_by_token(token)
    if get_user_data_by_email(token, target):
        get_db().execute("insert into messages values(?,?,?);", [user_data['email'], message, target])
        get_db().commit()
        return True
    else:
        return False