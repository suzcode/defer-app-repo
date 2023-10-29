from flask import Flask, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud import secretmanager
import google.auth.exceptions

# instantiate the app
app = Flask(__name__)

try:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'simple-398521'
    })   
    db = firestore.client()
except google.auth.exceptions.DefaultCredentialsError as e:
    print("Failed to initialise", e)
#app.config.from_object(__name__)

#firebase_admin.initialize_app()

#db = firestore.client()

CORS(app, resources={r'/microservice1': {'origins': '*'}})

@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/microservice1', methods=['GET'])
def ping_pong():
    users_ref = db.collection('users')
    query = users_ref.where('age', '>', 24).limit(5)  # Your query conditions here
    results = query.stream()
    users_data = []
    for result in results:
        users_data.append({"id": result.id, "data": result.to_dict()})
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)