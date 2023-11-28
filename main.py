from flask import Flask, jsonify, render_template, json, request
import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


app = Flask(__name__)

app.config.from_object(__name__)

firebase_admin.initialize_app()

db = firestore.client()

@app.route('/')
def main():
    return render_template("defrr.html")

@app.after_request
def after_request(response):
    white_origin= [r'/microservice1','http://34.111.111.147']

    # Check if 'Origin' is present in request headers
    if 'Origin' in request.headers:
        if request.headers['Origin'] in white_origin:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin'] 
    return response

@app.route('/microservice1', methods=['GET', 'POST'])
def user_details():
    users_data = []
    if request.method == 'POST':
        print('Request', request)
        if request.data == None or request.data == '':
            print('I got a null or empty string value for data in a file')
        else:
            post_data_raw = request.data
            print('Post data raw', post_data_raw)
            # post_data = json.loads(request.data)
        # print('Post data is:', post_data)
        return post_data_raw
        # user_age = post_data['ageval']
        # users_ref = db.collection('users')
        # field_filter = FieldFilter("age", "==", user_age)
        # query = users_ref.where(filter=field_filter)  # Your query conditions here
        # results = query.stream()
        # users_data = []
        # for result in results:
        #     users_data.append({"id": result.id, "data": result.to_dict()})
        # return jsonify(users_data)
    else:
        users_data = ["hell0"]
        print(users_data)
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)