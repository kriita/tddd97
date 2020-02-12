from flask import Flask, request, jsonify
import json;
import database_helper


app = Flask(__name__)

app.debug = True


@app.teardown_request
def after_request(exception):
    database_helper.disconnect_db()


@app.route('/signin', methods = ['PUT'])
def signin():
    data = request.get_json()
    result = database_helper.sign_in(data['email'], data['password'])
    if result:
        return json.dumps({"token" : result})
    else:
    	return json.dumps({"msg" : "email or password wrong!"}), 400


@app.route('/signup', methods = ['PUT'])
def signup():
    data = request.get_json()

    #print(data['email'], data['password'],
    #   data['name'], data['familyName'],
    #   data['gender'], data['city'],
    #   data['country'])

    result = database_helper.save_user(data['email'], data['password'],
                                            data['name'], data['familyName'],
                                            data['gender'], data['city'],
                                            data['country']
                                            )
    if(result == True):
        return json.dumps({"msg" : "User created!"}), 200
    else:
        return json.dumps({"msg" : "failed!", "data" : data}), 400




@app.route('/sign_out', methods = ['POST'])
def sign_out():
    data = request.get_json()
    result = database_helper.sign_out(data['token'])
    if(result):
    	return json.dumps({"msg" : "Signed out!"}), 200
    else:
    	return json.dumps({"msg" : "ERROR NO USER"}), 400

@app.route('/change_password', methods = ['PUT'])
def change_password():
    data = request.get_json()
    result = database_helper.change_password(data['token'], data['newPassword'], data['oldPassword'])
    if result:
    	return json.dumps({"msg" : "changed password!"}), 200
    else:
    	return json.dumps({"msg" : "old password does not match!"}), 400



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
