from flask import Flask, request, jsonify, send_from_directory
from flask_sockets import Sockets
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import database_helper
import os


### Global constants ###

ON_HEROKU = os.environ.get('ON_HEROKU')

app = Flask(__name__)
sockets = Sockets(app)

app.debug = True

msg = [] # Request buffer

### Default functions ###

@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()



@app.route('/')
# Default site routes to signin page route #
def index():
    return send_from_directory('static', 'client.html')



### Account management routes ###

@app.route('/signin', methods = ['PUT'])
def signin():
    # Request route to sign in a user in the welcome interface #
    data = request.get_json()
    
    if not database_helper.check_if_user_in_database(data['email']):
        return json.dumps({"success" : False, "message" : "User doesn't exist!", "data" : {}}), 400
    result = database_helper.sign_in(data['email'], data['password'])

    if not result:
        return json.dumps({"success" : False, "message" : "Wrong password!", "data" : {}}), 400
    return json.dumps({"success" : True, "message" : "User logged in!", "data" : {"token" : result["token"], "salt" : result["salt"]}}), 200



@app.route('/signup', methods = ['PUT'])
def signup():
    # Request route to sign up a user in the welcome interface #
    data = request.get_json()
    user_data = database_helper.check_if_user_in_database(data['email'])

    if user_data:
        return json.dumps({"success" : False, "message" : "User already exists!", "data" : {}}), 400
    result = database_helper.save_user(data['email'], data['password'],
                                            data['firstname'], data['familyname'],
                                            data['gender'], data['city'],
                                            data['country']
                                            )
    if(result):
        return json.dumps({"success" : True, "message" : "User created!", "data" : {}}), 200
    else:
        return json.dumps({"success" : False, "message" : "Failed!", "data" : {}}), 200



@app.route('/sign_out', methods = ['POST'])
def sign_out():
    # Request route to sign out a user from the webpage #
    raw_data = request.args.get("data")
    data = json.loads(raw_data)
    print("KEY: " + data["API Key"])

    if not database_helper.compare_hmac(data):
        print("Compare failed!")
        return json.dumps({"success" : False, "message" : "Invalid request!", "data" : {}}), 400
    token = database_helper.get_token_by_email(data["API Key"])
    salt = data["salt"]
    print("Salt: " + salt)
    result = database_helper.sign_out(token, salt)
    return json.dumps({"success" : True, "message" : "Signed out!", "data" : {}}), 200



### User modification functions ###

@app.route('/change_password', methods = ['PUT'])
def change_password(data = None):
    # Request route to change a user's password when the user is logged in #
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data_dic):
        result = database_helper.change_password(data_dic["API Key"], data_dic['newPassword'], data_dic['oldPassword'])
        if result:
            return json.dumps({"success" : True, "message" : "Changed password!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Old password does not match!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/forgot_password', methods = ['PUT'])
def forgot_password(data = None):
    # Request route to get send a new password to the user's email #
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data): # Check if valid user
        result = database_helper.forgot_password(data_dic['API Key'])
        if result:
            return json.dumps({"success" : True, "message" : "An email has beren sent to the specified adress with a new password!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Something went wrong!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "No user exists with that email!", "data" : {}}), 400


@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token(data = None):
    # Request route that returns the sender's data by using the token, used when looking up other users on the webpage. #
    
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data_dic):
        result = database_helper.get_user_data_by_email(data_dic["API Key"])
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/get_user_data_by_email', methods = ['GET'])
def get_user_data_by_email(data=None):
    # Request route that returns the user data associated with the email of an account, used when looking up other users on the webpage. #
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data_dic):
        result = database_helper.get_user_data_by_email(data_dic["email"])
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token(data = None):
    # Request route that returns all messages sent to the sender in exchange for a token #
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data_dic):
        result = database_helper.get_user_messages_by_email(data_dic["API Key"])
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_email', methods = ['GET'])
def get_user_messages_by_email(data=None):
    # Request route that returns all messages sent to the a certain email #
    data = request.args.get("data")
    data_dic = json.loads(data)

    if database_helper.compare_hmac(data_dic):
        result = database_helper.get_user_messages_by_email(data_dic["email"])
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/post_message', methods = ['POST'])
def post_message():
    # Posts a message to a the wall of the target #
    data = request.args.get("data")
    data_dic = json.loads(data)
    if database_helper.compare_hmac(data_dic):
        result = database_helper.post_message(data_dic["API Key"], data_dic["message"], data_dic["email"])
        if result:
            return json.dumps({"success" : True, "message" : "Message posted!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Target email invalid!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route("/websocket")
def connect_to_socket(email = None):
    # Connects a user to a websocket #
    if(request.environ.get("wsgi.websocket")):
        ws = request.environ["wsgi.websocket"]
        global msg
        ws.send("email_req")
        email = ws.receive()
        ws.send("salt_req")
        salt = ws.receive()
        if (database_helper.check_if_user_logged_in(email) > 1):
            new_msg = [email, database_helper.get_token_by_email(email), salt]
            msg += [new_msg]
        ws_open = True
        while ws_open:
            ws.send("email_req")
            email = ws.receive()
            token = database_helper.get_token_by_email(email)
            if(not token):
                ws.close()
                ws_open = False
            else:
                ws.send("salt_req")
                salt = ws.receive()
                for mess in msg:
                    if(mess[0] == email and mess[1] != token):
                        msg.remove(mess)
                        result = database_helper.sign_out(token, mess[2])
                        ws.send("logout_req")
                        message = ws.receive()
                        ws.close()
                        ws_open = False
        return json.dumps({"success" : False, "message" : "User logged in elsewhere!", "data" : {}}), 400



if (__name__ == "__main__"):
    if ON_HEROKU:
        # get the heroku port
        port = int(os.environ.get('PORT', 17995))
    else:   
        port = 5000
    http_server = WSGIServer(('', port), app, handler_class=WebSocketHandler)
    http_server.serve_forever()