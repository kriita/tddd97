import sqlite3
import uuid
from flask import g
import os
import psycopg2
import random
from string import ascii_lowercase

""" Libraries for email """
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

""" Library for encryption """
import hashlib

ON_HEROKU = os.environ.get('ON_HEROKU')

if ON_HEROKU:
    DATABASE_URL = os.environ['DATABASE_URL']
else:         
    DATABASE_URI = 'database.db'

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        if ON_HEROKU:
            db = g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:   
            db = g.db = sqlite3.connect(DATABASE_URI)

    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

def sign_in(email, password):
    cursor = get_db().cursor()
    cursor.execute("select * from user_data where email like '"+ email + "' and password like '" + encrypt_string(password) + "'")
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return False
    token = generate_token()
    cursor = get_db().cursor()
    cursor.execute("insert into logged_in values('"+ email + "','" + encrypt_string(token) + "');")
    get_db().commit()
    return token

def check_if_user_logged_in(email):
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where email like '" + email + "';")
    messages = cursor.fetchall()
    cursor.close()
    return len(messages)

def generate_token():
    return str(uuid.uuid4())

def save_user(email, password, name, familyName, gender, city, country):
    sql_new_query = "insert into user_data values('"+ email + "','" + encrypt_string(password) + "','" + name + "','" + familyName + "','" + gender + "','" + city + "','" + country + "');"
    get_db().cursor().execute(sql_new_query)
    get_db().commit()
    return True


def check_if_user_in_database(email):
    cursor = get_db().cursor()
    cursor.execute("select * from user_data where email like '"+ email + "';")
    message = cursor.fetchall()
    cursor.close()
    
    if(len(message) == 0):
        return False
    else:
        return True
    
def sign_out(token):
    cursor = get_db().cursor()
    cursor.execute("delete from logged_in where token like '"+ encrypt_string(token) + "';")
    cursor.close()
    return True

def check_if_user_logged_in_token(token):
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '"+ encrypt_string(token) + "';")
    messages = cursor.fetchall()
    cursor.close()
    return len(messages) != 0

def change_password(token,newPassword, oldPassword):
    cursor = get_db().cursor()
    cursor.execute("select email from logged_in where token like '" + encrypt_string(token) + "';")
    email = cursor.fetchall()
    cursor.close()

    cursor = get_db().cursor()
    cursor.execute("select password from user_data where email like '" + email[0][0] + "';")
    password = cursor.fetchall()
    cursor.close()

    if password[0][0] == encrypt_string(oldPassword):
        cursor = get_db().cursor()
        cursor.execute("update user_data set password = '" + encrypt_string(newPassword) + "' where email like '" + email[0][0] + "';")
        get_db().commit()
        cursor.close()
        return True;
    else:
        return False;

def forgot_password(email):
    newPassword = randomString()

    supportemail = "twiddersuport1337@gmail.com"
    supportpass = "Twiddersuport11111"


    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New password:" + newPassword
    msg['From'] = supportemail
    msg['To'] = email

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(supportemail, supportpass)

    s.sendmail(supportemail, email, msg.as_string())
    s.quit()

    cursor = get_db().cursor()
    cursor.execute("update user_data set password = '" + encrypt_string(newPassword) + "' where email like '" + email + "';")
    get_db().commit()
    cursor.close()
    return True;

def randomString(stringLength=10):
    letters = ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_user_data_by_token(token):
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '" + encrypt_string(token) + "';")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return False
    return get_user_data_by_email(token,data[0][0])

def get_user_data_by_email(token, email):
    cursor = get_db().cursor()
    cursor.execute("select * from user_data where email like '" + email + "';")
    messages = cursor.fetchall()
    cursor.close()
    if len(messages) > 0:
        messages = messages[0]
        return {"email" : messages[0], "firstname" : messages[2], "familyname" : messages[3], "gender" : messages[4], "city" : messages[5], "country" : messages[6]}
    else:
        return {}

def get_user_messages_by_token(token):
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '" + encrypt_string(token) + "';")
    data = cursor.fetchall()
    cursor.close()
    return get_user_messages_by_email(token, data[0][0])

def get_user_messages_by_email(token, email):
    cursor = get_db().cursor()
    cursor.execute("select * from messages where target like '" + email + "';")
    messages = cursor.fetchall()
    cursor.close()
    return {"messages" : messages}

def post_message(token, message, target):
    user_data = get_user_data_by_token(token)
    if get_user_data_by_email(token, target):
        cursor = get_db().cursor()
        cursor.execute("insert into messages values('" + user_data['email'] + "','" + message + "','" + target + "');")
        get_db().commit()
        cursor.close()
        return True
    else:
        return False