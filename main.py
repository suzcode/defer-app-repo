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

def create_year_filters(profile_to_filter, filter_year):
    filter_profile = {}
    customer_list = []
    FILTERED = []
    for i, (k, v) in enumerate(profile_to_filter.items()):
        print(i, k, v)
        print(type(i), type(k), type(v))
        zero_yr = False
        # If key is a string and value is a string then the value is the customer name
        if type(k) == str and type(v) == str:
            # assign the customer key to the cust_key variable
            cust_key = k
            # assign the customer name to a temp variable
            cust_temp = v
        # If the value is an integer then it is the start year and set it as the start_yr variable
        if type(v) == int:
            start_yr = v
            print('start year', start_yr)
            # The year_offset determines how many positions in the list the filter year is from the start_yr
            print('filter year', filter_year)
            year_offset = filter_year - start_yr
            print('year offset', year_offset)
        # If the value is a list then set the end_yr variable as the length of the list minus 1
        if type(k) == str and type(v) == list:
            end_yr = start_yr + (len(v) - 1)
            print('end yr', end_yr)
            # If the filter yr is > end_yr then set the zero_yr varaible to True
            if filter_year > end_yr:
                zero_yr = True
            # Create a key in the dictionary for the customer and assign the customer name
            filter_profile[cust_key] = cust_temp
            # Append the customer name to a customer list which is used in the dataframe as an index
            customer_list.append(cust_temp)
            print(customer_list)
            # Create a key in the dictionary called year and assign it the filter_year the user entered in the form
            filter_profile['year'] = filter_year
            # If year_offset < 0 (i.e. filter year is less than the start year) set the zero_yr varaible to True
            if year_offset < 0:
                zero_yr = True
            if zero_yr:
                FILTERED.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            else:
                # Appends the list for the appropriate year to the 'filtered_list' list
                FILTERED.append(v[year_offset])
            # print(bill_list_filter)
            # print(len(bill_list_filter))
            # print(customer_list)
    return FILTERED, customer_list

def pullRows1(contract_list):
    all_profiles = {}
    anniversaryList = []
    count = 1
    for contract in contract_list:
        values_list = [contract[key] for key in sorted(contract.keys())]
        customer_instance = Customer(*values_list)
        originalList = customer_instance.create_list()
        anniversaryList = customer_instance.calc_ann_months()
        invoices = customer_instance.calc_ann_invoices()
        billing = customer_instance.update_inv(originalList, anniversaryList, invoices)
        years = customer_instance.create_yearList(originalList)
        print('years in pullRows1', years)
        profile = customer_instance.create_profile(billing, years)
        all_profiles = customer_instance.combined_profile(all_profiles, profile, count)
        count += 1
    return all_profiles, years

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
    return final_list

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

# retrieve ALL customer info
@app.route('/contract', methods=['GET', 'POST'])
def contract_details():
    if request.method == 'POST':
        print('Request', request)
        if request.data == None or request.data == '':
            print('null or empty string value for data in a file')
        else:
            request_value = json.loads(request.data)
            # get values from dict
            filter_year_string = request_value['ref']
            # convert the year string to integer
            filter_year = int(filter_year_string)
            print('filter year is', filter_year)
            subscriber_id = 'Charlie Corp'
            database_ref = db.collection('subscribers')
            query = database_ref.document(subscriber_id).collection('contracts')
            docs = query.stream()
            CONTRACTS = {}
            contracts_data = []
            billingList = []
            billingList_months = []
            customer_list = []
            for doc in docs:
                document_data = doc.to_dict()
                print('document data', document_data)
                contracts_data.append(document_data)
                print('cusotomers_data', contracts_data)
                contractData, years = pullRows1(contracts_data)
                print('contract data', contractData)
                print('years from pullRows1', years)
                billingList, customer_list = create_year_filters(contractData, filter_year)
                print('billingList', billingList)
                # add month labels on x axis and customer names on y axis
                billingList_months = add_months_as_keys(billingList, customer_list)
                CONTRACTS = billingList_months
            return jsonify(CONTRACTS)

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