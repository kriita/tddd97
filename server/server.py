from flask import Flask, request, jsonify
import json;
import database_helper


app = Flask(__name__)

app.debug = True


@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()


@app.route('/signin', methods = ['GET'])
def signin():
    return json.dumps({"msg" : "Contact saved!"}), 200



@app.route('/signup', methods = ['PUT'])
def signup():
	data = request.get_json()

	print(data['email'], data['password'],
		data['name'], data['familyName'],
		data['gender'], data['city'],
		data['country'])

	result = database_helper.save_user(data['email'], data['password'],
											data['name'], data['familyName'],
											data['gender'], data['city'],
											data['country']
											)
	if(result  == True):
		return json.dumps({"msg" : "Contact saved!"}), 200
	else:
		return json.dumps({"msg" : "failed!", "data" : data}), 400




@app.route('/sign_out', methods = ['GET'])
def sign_out():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/change_password', methods = ['PUT'])
def change_password():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/get_user_data_by_email', methods = ['GET'])
def get_user_data_by_email():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/get_user_messages_by_email', methods = ['GET'])
def get_user_messages_by_email():
    return json.dumps({"msg" : "Contact saved!"}), 200

@app.route('/post_message', methods = ['POST'])
def post_message():
    return json.dumps({"msg" : "Contact saved!"}), 200


if __name__ == '__main__':
    app.run()
