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
""" Default site routes to signin page route """
def index():
    return send_from_directory('static', 'client.html')



### Account management routes ###

@app.route('/signin', methods = ['PUT'])
def signin():
    """ Request route to sign in a user in the welcome interface """
    data = request.get_json()
    
    if not database_helper.check_if_user_in_database(data['email']):
        return json.dumps({"success" : False, "message" : "User doesn't exist!", "data" : {}}), 400
    result = database_helper.sign_in(data['email'], data['password'])
    
    if not result:
        return json.dumps({"success" : False, "message" : "Wrong password!", "data" : {}}), 400
    return json.dumps({"success" : True, "message" : "User logged in!", "data" : {"token" : result}}), 200



@app.route('/signup', methods = ['PUT'])
def signup():
    """ Request route to sign up a user in the welcome interface """
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
    """ Request route to sign out a user from the webpage """
    data = request.get_json()

    if not database_helper.check_if_user_logged_in_token(data['token']):
        return json.dumps({"success" : False, "message" : "User not logged in!", "data" : {}}), 400        
    result = database_helper.sign_out(data['token'])
    return json.dumps({"success" : True, "message" : "Signed out!", "data" : {}}), 200



### User modification functions ###

@app.route('/change_password', methods = ['PUT'])
def change_password():
    """ Request route to change a user's password when the user is logged in """
    data = request.get_json()

    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.change_password(data['token'], data['newPassword'], data['oldPassword'])
        if result:
            return json.dumps({"success" : True, "message" : "Changed password!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Old password does not match!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/forgot_password', methods = ['PUT'])
def forgot_password():
    """ Request route to get send a new password to the user's email """
    data = request.get_json()

    if database_helper.check_if_user_in_database(data['email']): # Check if valid user
        result = database_helper.forgot_password(data['email'])
        if result:
            return json.dumps({"success" : True, "message" : "An email has beren sent to the specified adress with a new password!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Something went wrong!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "No user exists with that email!", "data" : {}}), 400


@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token(token = None):
    """ Request route that returns the sender's data by using the token, used when looking up other users on the webpage. """
    token = request.args.get("token")

    if database_helper.check_if_user_logged_in_token(token):
        result = database_helper.get_user_data_by_token(token)
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/get_user_data_by_email', methods = ['GET'])
def get_user_data_by_email(token = None, email = None):
    """ Request route that returns the user data associated with the email of an account, used when looking up other users on the webpage. """
    token = request.args.get("token")
    email = request.args.get("email")

    if database_helper.check_if_user_logged_in_token(token):
        result = database_helper.get_user_data_by_email(token, email)
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token(token = None):
    """ Request route that returns all messages sent to the sender in exchange for a token """
    token = request.args.get("token")

    if database_helper.check_if_user_logged_in_token(token):
        result = database_helper.get_user_messages_by_token(token)
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_email', methods = ['GET'])
def get_user_messages_by_email(token = None, email=None):
    """ Request route that returns all messages sent to the a certain email """
    token = request.args.get("token")
    email = request.args.get("email")

    if database_helper.check_if_user_logged_in(email):
        result = database_helper.get_user_messages_by_email(token, email)
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/post_message', methods = ['POST'])
def post_message():
    """ Posts a message to a the wall of the target """
    data = request.get_json()

    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.post_message(data['token'], data['message'], data['email'])
        if result:
            return json.dumps({"success" : True, "message" : "Message posted!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Target email invalid!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route("/websocket")
def connect_to_socket(email = None):
    """ Connects a user to a websocket """
    if(request.environ.get("wsgi.websocket")):
        ws = request.environ["wsgi.websocket"]
        global msg
        ws.send("token_req")
        token = ws.receive()
        data = database_helper.get_user_data_by_token(token)
        if (database_helper.check_if_user_logged_in(data["email"]) > 1):
            new_msg = [data["email"], token]
            msg += [new_msg]

        ws_open = True
        while ws_open:
            ws.send("token_req")
            token = ws.receive()
            data = database_helper.get_user_data_by_token(token)
            for mess in msg:
                if(mess[0] == data["email"] and mess[1] != token):
                    msg.remove(mess)
                    result = database_helper.sign_out(token)
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