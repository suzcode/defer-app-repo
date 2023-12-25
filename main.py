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

def add_months_as_keys(filter, years):
    months1 = ['id', 'jan', 'feb', 'mar', 'apr', 'may',
               'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    lineNumber = 0
    line_with_months = {}
    resultList = []
    years.append('TOTAL')
    for line in filter:
        print('line*****', line)
        if len(line) != 13 and len(line) != 0:
            line.insert(0, years[lineNumber])
            print(line)
        line_with_months = {k: v for (k, v) in zip(months1, line)}
        print('line dict with months added =', line_with_months)
        resultList.append(line_with_months)
        print('Resultlist', resultList)
        lineNumber += 1
    return resultList

def pullRows(users_data):
    i = 0
    while i < 1:
        value_ret = users_data[i]
        dict_ret = value_ret["data"]
        # values_list = [value for value in dict_ret.values()]
        values_list = [dict_ret[key] for key in sorted(dict_ret.keys())]
        i += 1
    # create a separate customer instance
    customer_instance = Customer(*values_list)
    originalBillList = customer_instance.create_list()
    years = customer_instance.create_yearList(originalBillList)
    bill = customer_instance.create_profile(originalBillList, years)
    final_list = add_months_as_keys(bill, years)
    return users_data

@app.route('/')
def main():
    return render_template("defrr.html")

# retrieve customer info
@app.route('/customers')
def customers():
    subscriber_id = 'Charlie Corp'
    database_ref = db.collection('subscribers')
    query = database_ref.document(subscriber_id).collection('contracts')
    docs = query.stream()
    CUSTOMERS = {}
    customers_data = []
    for doc in docs:
        document_data = doc.to_dict()
        print('document data', document_data)
        cust_name = document_data['customer_name']
        print('customer name', cust_name)
        customers_data.append(cust_name)
        print('cusotomers_data', customers_data)
        CUSTOMERS = customers_data
    return jsonify(CUSTOMERS)

@app.route('/microservice1', methods=['GET', 'POST'])
def user_details():
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
            email_selection = post_data['ageval']
            subscriber_id = 'Charlie Corp'
            database_ref = db.collection('subscribers')
            # field_filter = FieldFilter("email", "==", email_selection)
            # -------------------------------------
            # self_info = ["c1234", "TVNZ Inc", "c1", 2021, 3, 10, 10000, 3, 2027, 10, 23, 18]
            # cont_years = Customer.year_diff(self_info)
            # return jsonify(cont_years)
            # -------------------------------------
            query = database_ref.document(subscriber_id).collection('contracts')  # Your query conditions here
            #query = users_ref
            docs = query.stream()
            users_data = []
            CUSTOMERS = {}
            for doc in docs:
                # users_data.append({"id": doc.id, "fields": doc.to_dict()})
                document_data = {'data': doc.to_dict()}
                users_data.append(document_data)
                users_data1 = pullRows(users_data)
            CUSTOMERS['Billing'] = users_data1
            return jsonify(CUSTOMERS)
    else:
        users_data1 = ["hello there shane"]
        print(users_data1)
    return jsonify(users_data1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)