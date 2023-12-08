from flask import Flask, jsonify, render_template, json, request
import firebase_admin
from firebase_admin import firestore
from flask_cors import CORS
from google.cloud.firestore_v1.base_query import FieldFilter
import contractcalcs
from contractcalcs import *


app = Flask(__name__)

whitelisted_origins = [
    r'/microservice1',
    'http://34.111.111.147',
    # Add more origins as needed
]

# White list the origins
CORS(app, origins=whitelisted_origins)

app.config.from_object(__name__)

firebase_admin.initialize_app()

db = firestore.client()

@app.route('/')
def main():
    return render_template("defrr.html")

@app.route('/microservice1', methods=['GET', 'POST'])
def user_details():
    users_data = ["beep"]
    if request.method == 'POST':
        print('Request', request)
        if request.data == None or request.data == '':
            print('null or empty string value for data in a file')
        else:
            post_data_raw = request.data
            print('Post data raw', post_data_raw)
            post_data = json.loads(request.data)
            print('Post data is:', post_data)
            # user_age = int(post_data['ageval'])
            customer_selection = post_data['ageval']
            users_ref = db.collection('users')
            field_filter = FieldFilter("customer_name", "==", customer_selection)
            # -------------------------------------
            # self_info = ["c1234", "TVNZ Inc", "c1", 2021, 3, 10, 10000, 3, 2027, 10, 23, 18]
            # cont_years = Customer.year_diff(self_info)
            # return jsonify(cont_years)
            # -------------------------------------

            query = users_ref.where(filter=field_filter)  # Your query conditions here
            #query = users_ref
            docs = query.stream()
            users_data = [customer_selection]
            for doc in docs:
                # users_data.append({"id": doc.id, "fields": doc.to_dict()})
                document_data = {'document_id': doc.id, 'data': doc.to_dict()}
                users_data.append(document_data)
            return jsonify(users_data)
    else:
        users_data = ["hello there shane"]
        print(users_data)
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)