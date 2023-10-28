from flask import Flask, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from google.cloud import secretmanager
import json

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

firebase_admin.initialize_app()

db = firestore.client()

#project_id = "defrr-398521"
#secret_id = "api-defrr-key"
#client = secretmanager.SecretManagerServiceClient()
#parent = f"projects/{project_id}"

# GET THE SECRET VERSION NAME
#secret_version_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

# Create the parent secret
#secret = client.create_secret(
    #request={
        #"parent": parent,
        #"secret_id": secret_id,
        #"secret": {"replication": {"automatic": {}}},
    #}
#)

# Add the secret version
#version = client.add_secret_version(
    #request={"parent": secret.name, "payload": {"data": b"hello world!"}}
#)

# enable CORS
CORS(app, resources={r'/microservice1': {'origins': '*'}})

#def get_api_key():
    #response = client.access_secret_version(request={"name": secret_version_name})
    #payload = response.payload.data.decode("UTF-8")
    #print(f"Plaintext: {payload}")
    #return payload


@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/microservice1', methods=['GET'])
def ping_pong():
    users_ref = db.collection('users')
    query = users_ref.where('first name', '==', 'John').limit(5)  # Your query conditions here
    results = query.stream()
    users_data = []
    for result in results:
        users_data.append({"id": result.id, "data": result.to_dict()})
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)