from flask import Flask, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# instantiate the app
app = Flask(__name__)

app.config.from_object(__name__)

firebase_admin.initialize_app()

db = firestore.client()

CORS(app, resources={r'/microservice1': {'origins': '*'}})

@app.route('/')
def main():
    return render_template("defrr.html")

# sanity check route
@app.route('/microservice1', methods=['GET'])
def ping_pong():
    users_ref = db.collection('users')
    field_filter = FieldFilter("age", "==", 25)
    query = users_ref.where(filter=field_filter)  # Your query conditions here
    results = query.stream()
    users_data = []
    for result in results:
        users_data.append({"id": result.id, "data": result.to_dict()})
    return jsonify(users_ref)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)