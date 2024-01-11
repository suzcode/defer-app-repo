from flask import json
from datetime import date
from dateutil import rrule
from itertools import accumulate


class Customer:
    def __init__(self, contract_id, customer_id, customer_name, end_day, end_month, end_year, percent_inc, start_day, start_month, start_subs, start_year, term_months):
        self.contract_id = contract_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.end_day = end_day
        self.end_month = end_month
        self.end_year = end_year
        self.percent_inc = percent_inc
        self.start_day = start_day
        self.start_month = start_month
        self.start_subs = start_subs
        self.start_year = start_year
        self.term_months = term_months

    def start(self):
        start_day = self.start_day
        start_month = self.start_month
        start_year = self.start_year
        start_subs = self.start_subs
        return start_day, start_month, start_year, start_subs

    def end(self):
        end_day = self.end_day
        end_month = self.end_month
        end_year = self.end_year
        return end_day, end_month, end_year

    def calculate_mths(self):
        monthList = list(rrule.rrule(rrule.MONTHLY, dtstart=date(
            start_year, start_month, start_day), until=date(end_year, end_month, end_day)))
        print(monthList)
        print(monthList[0])
        return len(monthList)

    # creates a list of anniversary months
    def calc_ann_months(self):
        # Customer.start(self)
        anniversary_month = []
        counter = 0
        factor = self.start_month
        for i in range(int(self.term_months) + 1):
            # loops through the total number of month and if an anniversary month adds to list
            if (counter - factor) % 12 == 0:
                anniversary_month.append(counter)
            counter += 1
        return anniversary_month

    # this function returns a list of all the invoice values for the duration of the contract
    def calc_ann_invoices(self):
        # starts the invoice list with the initial subs value from the contract
        invoice_list = [float(self.start_subs)]
        print(invoice_list)
        # loops through the number of years of the contract (which is the term div by 12)
        for i in range(int((self.term_months + self.start_month) / 12)):
            print(i)
            # applies the increase to the subs value and appends to the invoice list
            inc_factor = (float(1 + (self.percent_inc / 100)))
            new_subs = invoice_list[i] * inc_factor
            new_subs = round(new_subs, 2)
            # new_subs = round(float(new_subs), 2)
            invoice_list.append(new_subs)
        return invoice_list

    # loops through the list of zero values and adds the invoice amount
    def update_inv(self, billList, anniversary_list, invoices):
        for i in range(len(billList)):
            for annmth in anniversary_list:
                # checks if the current month in the loop is an anniversary month
                if annmth == i + 1:
                    bill_year = int(annmth / 12)
                    billList[i] = invoices[bill_year]
        return billList
    
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

    def year_diff(self):
        end_yr = self[8]
        start_yr = self[3]
        return end_yr - start_yr
    
     # creates a list for the term of contract of zero values
    def create_list(self):
        bill_list = []
        additional_months = 0
        if self.term_months % 12 == 0:
            if abs(self.end_day - self.start_day) <= 1:
                # if teh start month is 1 there is no need for a follow on year
                if self.start_month > 1:
                    additional_months = 12
                    print("addition div ==0", additional_months)
        else:
            if self.term_months > 12:
                additional_months = 12 - (self.term_months % 12)
                print("addtional term > 12", additional_months)
            else:
                additional_months = 12 - self.term_months
                print("addtional term < 12", additional_months)
        # creates a list of zero for the term of the contract
        for i in range(int(self.term_months + additional_months)):
            bill_list.append(0)
        print('length of bill list', len(bill_list))
        return bill_list

    def create_yearList(self, billList):
        yearList = [self.start_year]
        i = 1
        while i < (len(billList) / 12):
            yearList.append(self.start_year + i)
            i += 1
        return yearList

    def create_profile(self, profileraw, years):
        profile = []
        NUM_ROWS = len(years)
        NUM_COLS = 12
        for row_num in range(NUM_ROWS):
            new_row = []
            for col_num in range(NUM_COLS):
                new_row.append(profileraw[row_num * NUM_COLS + col_num])
            profile.append(new_row)
        print('CUSTOMER PROFILE:   ', list(profile))
        return profile

    # this combined_profile function creates a combined dictionary
    def combined_profile(self, all_billProfiles, profile, count):
        active_customer = self.customer_name
        active_start_year = self.start_year
        # adds customers key (based on count variable) plus customer name to dictionary
        all_billProfiles['Customer' + str(count)] = active_customer
        # adds start year key (based on count variable) plus start year to dictionary
        all_billProfiles['Start year' + str(count)] = active_start_year
        # adds prfolie key (plus count variable) and 2D profile list value to the dictionary
        all_billProfiles['billProfile' + str(count)] = profile
        print('ALLLL BILLLLL PROFILLLLES = ', all_billProfiles)
        return all_billProfiles

    def profile_accumulate(self, list_to_accumulate):
        return list(accumulate(list_to_accumulate))

# ----------------------------------------------------------------------------------

    def leap_year(self):
        if self.start_year % 400 == 0:
            return True
        if self.start_year % 100 == 0:
            return False
        if self.start_year % 4 == 0:
            return True
        return False

    def days_in_month(self):
        if self.start_month in {1, 3, 5, 7, 8, 10, 12}:
            return 31
        if self.start_month == 2:
            if Customer.leap_year(self):
                return 29
            return 28
        return 30

    def first_mth_amort(self):
        number_days_in_first_mth = Customer.days_in_month(self)
        active_days_first_mth = number_days_in_first_mth - \
            (self.start_day - 1)
        first_mth_ratio = (active_days_first_mth / number_days_in_first_mth)
        print(first_mth_ratio)
        print(type(first_mth_ratio))
        monthly_subs_1 = float(self.start_subs / 12)
        print(monthly_subs_1)
        print(type(monthly_subs_1))
        amort_mth_1 = round((first_mth_ratio * monthly_subs_1), 2)
        print(amort_mth_1)
        return amort_mth_1, monthly_subs_1

    def anniversary_mth_amort(self, ann_mth, ann_yr, anniversary_list, yearList, invoices):
        print('Ann mth', ann_mth)
        print('yearlist ann mth = billing yr', yearList[ann_mth - 1])
        print('Ann Yr', ann_yr)
        number_days_in_ann_mth = Customer.days_in_month(self)
        # start day is considered an active day therefore added back below so that it is included
        active_days_ann_mth = (number_days_in_ann_mth - self.start_day) + 1
        ann_mth_ratio = active_days_ann_mth / number_days_in_ann_mth
        print('ANN MTH RATIO', type(ann_mth_ratio))
        current_bill_yr = yearList[ann_mth - 2]
        print('CURRENNT BILL YR', current_bill_yr)
        next_bill_yr = yearList[ann_mth - 1]
        print('NEXT BILL YR', next_bill_yr)
        current_yr_subs = float(invoices[current_bill_yr - 1])
        print('CUURRENT YR SUBS', current_yr_subs)
        print(type(current_yr_subs))
        next_yr_subs = float(invoices[next_bill_yr - 1])
        print('yearlist next', yearList[ann_mth - 1])
        print('Next yr', next_yr_subs)
        print(type(next_yr_subs))
        print('len anniversary list = ', len(anniversary_list))
        print(ann_mth_ratio)
        amort_ann_mth = round(
            ((((1-ann_mth_ratio) * current_yr_subs) + ((ann_mth_ratio) * next_yr_subs)) / 12), 2)
        print(amort_ann_mth)
        return amort_ann_mth

    def final_mth_amort(self, invoices, anniversary_list):
        number_days_in_final_mth = Customer.days_in_month(self)
        final_mth_ratio = self.end_day / number_days_in_final_mth
        print(final_mth_ratio)
        final_yr_subs = invoices[len(anniversary_list) - 1]
        print('final yr subs', final_yr_subs)
        amort_final_mth = round(((final_mth_ratio * final_yr_subs) / 12), 2)
        print(amort_final_mth)
        return amort_final_mth
