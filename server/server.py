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


if __name__ == '__main__':
    app.run()
