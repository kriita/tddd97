from flask import Flask, request, jsonify, send_from_directory
import json;
import Twidder.database_helper

app = Flask(__name__)

app.debug = True

@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()

@app.route('/')
def index():
    return send_from_directory('static', 'client.html')


@app.route('/signin', methods = ['PUT'])
def signin():
    data = request.get_json()
    if not database_helper.check_if_user_in_database(data['email']):
        return json.dumps({"success" : False, "message" : "User doesn't exist!", "data" : {}}), 400
    if database_helper.check_if_user_logged_in(data['email']):
        return json.dumps({"success" : False, "message" : "User already logged in!", "data" : {}}), 400
    result = database_helper.sign_in(data['email'], data['password'])
    if not result:
        return json.dumps({"success" : False, "message" : "Wrong password!", "data" : {}}), 400
    return json.dumps({"success" : True, "message" : "User logged in!", "data" : {"token" : result}}), 200

@app.route('/signup', methods = ['PUT'])
def signup():
    data = request.get_json()

    user_data = database_helper.check_if_user_in_database(data['email'])

    if user_data:
        return json.dumps({"success" : False, "message" : "User already exists!", "data" : {}}), 400

    result = database_helper.save_user(data['email'], data['password'],
                                            data['firstname'], data['familyname'],
                                            data['gender'], data['city'],
                                            data['country']
                                            )
    return json.dumps({"success" : True, "message" : "User created!", "data" : {}}), 200



@app.route('/sign_out', methods = ['POST'])
def sign_out():
    data = request.get_json()

    if not database_helper.check_if_user_logged_in_token(data['token']):
        return json.dumps({"success" : False, "message" : "User not logged in!", "data" : {}}), 400        
    result = database_helper.sign_out(data['token'])
    return json.dumps({"success" : True, "message" : "Signed out!", "data" : {}}), 200




@app.route('/change_password', methods = ['PUT'])
def change_password():
    data = request.get_json()

    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.change_password(data['token'], data['newPassword'], data['oldPassword'])
        if result:
        	return json.dumps({"success" : True, "message" : "Changed password!", "data" : {}}), 200
        else:
        	return json.dumps({"success" : False, "message" : "Old password does not match!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token():
    data = request.get_json()
    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.get_user_data_by_token(data['token'])
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



@app.route('/get_user_data_by_email', methods = ['GET'])
def get_user_data_by_email():
    data = request.get_json()
    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.get_user_data_by_email(data['token'], data['email'])
        return json.dumps({"success" : True, "message" : "User data received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token():
    data = request.get_json()

    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.get_user_messages_by_token(data['token'])
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/get_user_messages_by_email', methods = ['GET'])
def get_user_messages_by_email():
    data = request.get_json()

    if database_helper.check_if_user_logged_in(data['email']):
        result = database_helper.get_user_messages_by_email(data['token'], data['email'])
        return json.dumps({"success" : True, "message" : "User messages received!", "data" : result}), 200
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400

@app.route('/post_message', methods = ['POST'])
def post_message():
    data = request.get_json()

    if database_helper.check_if_user_logged_in_token(data['token']):
        result = database_helper.post_message(data['token'], data['message'], data['email'])
        if result:
            return json.dumps({"success" : True, "message" : "Message posted!", "data" : {}}), 200
        else:
            return json.dumps({"success" : False, "message" : "Target email invalid!", "data" : {}}), 400
    else:
        return json.dumps({"success" : False, "message" : "Invalid token!", "data" : {}}), 400



if __name__ == '__main__':
    app.run()
