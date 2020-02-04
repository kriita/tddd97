from flask import Flask, request, jsonify

app = Flask(__name__)

app.debug = True


@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()



if __name__ == '__main__':
    app.run()
