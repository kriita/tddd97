from flask import Flask, request, jsonify
import json;
import database_helper


app = Flask(__name__)

app.debug = True


@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()


@app.route('/signin', methods = ['GET'])
def signin(email, password):
	result = database_helper.sign_in(email, password):
    
    if result['success'] == True:
    	return result['token']
    elif result['error'] == "password":
    	return json.dumps({"msg" : "Wrong password!"}), 400
    else:
    	return json.dumps({"msg" : "User not found"}), 400


@app.route('/signup', methods = ['PUT'])
def signup():
	data = request.get_json()

	#print(data['email'], data['password'],
	#	data['name'], data['familyName'],
	#	data['gender'], data['city'],
	#	data['country'])

	result = database_helper.save_user(data['email'], data['password'],
											data['name'], data['familyName'],
											data['gender'], data['city'],
											data['country']
											)
	if(result == True):
		return json.dumps({"msg" : "User created!"}), 200
	else:
		return json.dumps({"msg" : "failed!", "data" : data}), 400




@app.route('/sign_out', methods = ['GET'])
def sign_out(token):
	result = database_helper.sign_out(token)
    return json.dumps({"msg" : "Signed out!"}), 200

@app.route('/change_password', methods = ['PUT'])
def change_password(token):
	data = request.get_json()

	if data['oldPassword'] != data['newPassword']:
		result = database_helper.change_password(token, data['newPassword'])
    	return json.dumps({"msg" : "Password changed!"}), 200
    else:
    	return json.dumps({"msg" : "New password can't be the same as the old password!"}), 400

@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token(token):
	if token is not None:
        result = database_handler.get_user_data_by_token(token)
        return jsonify(result)

@app.route('/get_user_data_by_email', methods = ['GET'])
def get_user_data_by_email(token, email):
    if token and email is not None:
        result = database_handler.get_user_data_by_email(token, email)
        return jsonify(result)

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token(token):
	if token is not None:
        result = database_handler.get_user_messages_by_token(token)
        return jsonify(result)

@app.route('/get_user_messages_by_email', methods = ['GET'])
def get_user_messages_by_email(token, email):
    if token and email is not None:
        result = database_handler.get_user_messages_by_email(token, email)
        return jsonify(result)

@app.route('/post_message', methods = ['POST'])
def post_message(token):
    data = request.get_json()

	result = database_helper.post_message(token, data['msg'], data['email'])
	if(result['success']  == True):
		return json.dumps({"msg" : "Message posted!"}), 200
	else:
		return json.dumps({"msg" : "failed!", "data" : data}), 400


if __name__ == '__main__':
    app.run()
