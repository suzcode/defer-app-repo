from flask import Flask, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from google.cloud import secretmanager
import json


firebase_admin.initialize_app()

db = firestore.client()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/microservice1': {'origins': '*'}})

def get_api_key():
    secret_name = "projects/507089454572/secrets/api-defrr-key/versions/2"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")


@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/microservice1', methods=['GET'])
def ping_pong():
    api_key = get_api_key()
    credentials = firebase_admin.credentials.Certificate(json.loads(api_key))
    firebase_admin.initialize_app(credentials=credentials)
    data = []
    docs = db.collection("users").stream()
    for doc in docs:
        data.append({
            "id": doc.id,
            "data": doc.to_dict()
        })
    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)