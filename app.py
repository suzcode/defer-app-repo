import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/pong': {'origins': '*'}})

@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/pong', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    from waitress import serve
    app.run(host='0.0.0.0', port=8000)