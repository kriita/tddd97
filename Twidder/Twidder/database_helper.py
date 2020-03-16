import sqlite3
import uuid
from flask import g
import os
import psycopg2
import random
from string import ascii_lowercase
import json

### Libraries for email ###
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### Library for encryption ###
import hashlib, hmac
import base64

ON_HEROKU = os.environ.get('ON_HEROKU')

if ON_HEROKU:
    DATABASE_URL = os.environ['DATABASE_URL']
else:         
    DATABASE_URI = 'database.db'

### Account management functions ###

def sign_in(email, password):
    # Signs in a user with specified email if the password matches. 
    # Returns false if sign in fails, otherwise returns an authentication token #
    cursor = get_db().cursor()
    cursor.execute("select * from user_data where email like '"+ email + "' and password like '" + encrypt_string(password) + "'")
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return False
    token = generate_token()
    salt = randomString()
    cursor = get_db().cursor()
    cursor.execute("insert into logged_in values('"+ email + "','" + token + "','" + salt + "');")
    get_db().commit()
    return {"token" : token, "salt" : salt}

def save_user(email, password, name, familyName, gender, city, country):
    # Saves a user in the database after signup #
    sql_new_query = "insert into user_data values('"+ email + "','" + encrypt_string(password) + "','" + name + "','" + familyName + "','" + gender + "','" + city + "','" + country + "');"
    get_db().cursor().execute(sql_new_query)
    get_db().commit()
    return True
    
def sign_out(token, salt):
    # Signs a user out of the server #
    cursor = get_db().cursor()
    print(token)
    cursor.execute("delete from logged_in where token like '"+ token + "' and salt like '" + salt + "';")
    get_db().commit()
    cursor.close()
    return True

def change_password(email, newPassword, oldPassword):
    # Changes the password of the user with specified email from oldPassword to newPassword.
    # Returns False if oldPassword doesn't match the previous password in the databse, otherwiser returns true #
    cursor = get_db().cursor()
    cursor.execute("select password from user_data where email like '" + email + "';")
    password = cursor.fetchall()
    cursor.close()
    if password[0][0] == encrypt_string(oldPassword):
        cursor = get_db().cursor()
        cursor.execute("update user_data set password = '" + encrypt_string(newPassword) + "' where email like '" + email + "';")
        get_db().commit()
        cursor.close()
        return True;
    else:
        return False;

def forgot_password(email):
    # Changes the password of the user with specified email to a random 10-character string if the user exists,
    # and sends and email to the user with the new generated password from the support email. #
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

def post_message(email, message, target):
    # Posts a message to the target's wall. Returns False if the target doesn't exist. #
    if get_user_data_by_email(target):
        cursor = get_db().cursor()
        cursor.execute("insert into messages values('" + email+ "','" + message + "','" + target + "');")
        get_db().commit()
        cursor.close()
        return True
    else:
        return False

### Database functions ###

def get_db():
    # Returns the server's SQL database, used for database commands #
    db = getattr(g, 'db', None)
    if db is None:
        if ON_HEROKU:
            db = g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:   
            db = g.db = sqlite3.connect(DATABASE_URI)
    return db

def disconnect_db():
    # Disconnects the server's SQL database #
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

### GET Functions ###

def get_token_by_email(email):
    # Returns the token of the user with specified email if logged in, otherwise returns false #
    cursor = get_db().cursor()
    cursor.execute("select token from logged_in where email like '" + email + "';")
    token = cursor.fetchall()
    cursor.close()
    if(not token):
        return token
    else:
        return token[0][0]

def get_user_data_by_token(token):
    # Returns the user data of the user with specified token #
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '" + token + "';")
    data = cursor.fetchall()
    cursor.close()
    if len(data) == 0:
        return False
    return get_user_data_by_email(token,data[0][0])

def get_user_data_by_email(email):
    # Returns the user data of the user with specified email #
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
    # Returns the messages of the user with specified token #
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '" + token + "';")
    data = cursor.fetchall()
    cursor.close()
    return get_user_messages_by_email(token, data[0][0])

def get_user_messages_by_email(email):
    # Returns the messages of the user with specified email #
    cursor = get_db().cursor()
    cursor.execute("select * from messages where target like '" + email + "';")
    messages = cursor.fetchall()
    cursor.close()
    return {"messages" : messages}

def check_if_user_logged_in(email):
    # Checks if a user currently is logged in #
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where email like '" + email + "';")
    messages = cursor.fetchall()
    cursor.close()
    return len(messages)

def check_if_user_logged_in_token(token):
    # Checks if the user with a specified token is logged in #
    cursor = get_db().cursor()
    cursor.execute("select * from logged_in where token like '"+ token + "';")
    messages = cursor.fetchall()
    cursor.close()
    return len(messages) != 0

def check_if_user_in_database(email):
    # Returns a boolean stating if the user exists in the database #
    cursor = get_db().cursor()
    cursor.execute("select * from user_data where email like '"+ email + "';")
    message = cursor.fetchall()
    cursor.close()
    if(len(message) == 0):
        return False
    else:
        return True

### Help functions ###

def compare_hmac(old_body):
    # Validates an HMAC key, returns true if valid #
    body = old_body
    HMAC = body.pop("HMAC")
    api_key = body["API Key"]
    token = get_token_by_email(api_key)

    new_hash = hash256(body, token, HMAC) if token else ""

    print(old_body)
    print(HMAC)
    print(token)
    print(new_hash)
    print(HMAC == new_hash)
    
    return HMAC == new_hash

def encrypt_string(hash_string):
    # Returns a basic sha256-encryption of the string #
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def hash256(body, token, old_hmac):
    # Outputs a sha256-hashed version of the body using token as a key #
    bodymsg = json.dumps(body, separators=(',', ':'))
    message = bytes(bodymsg, 'utf-8')
    secret = bytes(token, 'utf-8')
    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    if(old_hmac.count("+")):
        return signature.decode("utf-8")
    return signature.decode("utf-8").replace("+", " ")

def generate_token():
    # Returns a random authentication token #
    return str(uuid.uuid4())

def randomString(stringLength=10):
    # Generates a random 10-character string #
    letters = ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

