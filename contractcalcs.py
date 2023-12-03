from flask import json
from datetime import date
from dateutil import rrule
from itertools import accumulate
import pandas as pd


class Customer:
    def __init__(self, customer_id, customer_name, contract_id, start_year, start_mth, start_day, start_subs,
                 percent_inc, end_year, end_mth, end_day, term_mths):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.contract_id = contract_id
        self.start_year = start_year
        self.start_mth = start_mth
        self.start_day = start_day
        self.start_subs = start_subs
        self.percent_inc = percent_inc
        self.end_year = end_year
        self.end_mth = end_mth
        self.end_day = end_day
        self.term_mths = term_mths
        return customer_id, customer_name, contract_id, start_year, start_mth, start_day, start_subs, percent_inc, end_year, end_mth, end_day, term_mths

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
        return end_yr - start_yr