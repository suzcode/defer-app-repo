from flask import json
from datetime import date
from dateutil import rrule
from itertools import accumulate


class Customer:
    def __init__(self, contract_id, customer_id, customer_name, end_day, end_month, end_year, percent_inc, start_day, start_month, start_subs, start_year, term_months):
        self.conti = contract_id
        self.custi = customer_id
        self.custn = customer_name
        self.end_day = end_day
        self.endm = end_month
        self.endy = end_year
        self.perci = percent_inc
        self.start_day = start_day
        self.start_month = start_month
        self.starts = start_subs
        self.starty = start_year
        self.term_months = term_months

    def start(self):
        start_day = self['start_day']
        start_mth = self['start_mth']
        start_yr = self['start_yr']
        start_subs = self['start_subs']
        return start_day, start_mth, start_yr, start_subs

    def end(self):
        end_day = self['end_day']
        end_mth = self['end_mth']
        end_yr = self['end_yr']
        return end_day, end_mth, end_yr

    def calculate_mths(self):
        monthList = list(rrule.rrule(rrule.MONTHLY, dtstart=date(
            start_yr, start_mth, start_day), until=date(end_yr, end_mth, end_day)))
        print(monthList)
        print(monthList[0])
        return len(monthList)
    
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