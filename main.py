from flask import Flask, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
db = firestore.client()
app = firebase_admin.initialize_app(cred)


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/microservice1': {'origins': '*'}})

@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/microservice1', methods=['GET'])
def ping_pong():
    docs = db.collection("users").stream()
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    return jsonify('pong!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)