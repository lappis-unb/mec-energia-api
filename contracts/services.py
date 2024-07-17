from . import models
from datetime import datetime
from .utils import ContractUtils
import csv
from io import TextIOWrapper
from collections import defaultdict
from mec_energia.error_response_manage import * 
import math

class ContractServices:  
    def get_file_errors(self, csv_reader, consumer_unit_id): 
        energy_bill_data = []
        date_list = []
        duplicate_dates = []
        seen_dates = set()

        for index, row in enumerate(csv_reader):
            row_errors, date = self.process_csv_row(
                row, index, consumer_unit_id)

            if str(date) in seen_dates:
                row_errors["date"].append(DuplicatedDate)

            seen_dates.add(str(date))

            energy_bill_row = {
                'consumer_unit': {'value': consumer_unit_id, 'error': False if consumer_unit_id else True},
                'date': {
                    'value': date,
                    'errors': row_errors.get('date')
                },
                'invoice_in_reais': {'value': "" if math.isnan(row.get('invoice_in_reais')) else row.get('invoice_in_reais', ""), 'errors': row_errors.get('invoice_in_reais')},
                'peak_consumption_in_kwh': {'value': row.get('peak_consumption_in_kwh', ""), 'errors': row_errors.get('peak_consumption_in_kwh')},
                'off_peak_consumption_in_kwh': {'value': row.get('off_peak_consumption_in_kwh', ""), 'errors': row_errors.get('off_peak_consumption_in_kwh')},
                'peak_measured_demand_in_kw': {'value': row.get('peak_measured_demand_in_kw', ""), 'errors': row_errors.get('peak_measured_demand_in_kw')},
                'off_peak_measured_demand_in_kw': {'value': row.get('off_peak_measured_demand_in_kw', ""), 'errors': row_errors.get('off_peak_measured_demand_in_kw')}
            }
            energy_bill_data.append(energy_bill_row)
            
        return energy_bill_data


    def validate_csv_row(self, row, consumer_unit_id):
        errors = defaultdict(list)
        date = ContractUtils().validate_date(row["date"])
        if(not date):
            errors["date"].append(FormatDateError)

        elif models.EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
            errors['date'].append(AlreadyHasEnergyBill)

        elif not models.EnergyBill.check_energy_bill_covered_by_contract(
            consumer_unit_id, date):
            errors["date"].append(DateNotCoverByContractError)

        for field, max_length in [
            ('invoice_in_reais', 10),
            ('peak_consumption_in_kwh', 6),
            ('off_peak_consumption_in_kwh', 6),
            ('peak_measured_demand_in_kw', 6),
            ('off_peak_measured_demand_in_kw', 6),
        ]:
            value = row.get(field, "")
            if len(str(value)) > max_length:
                errors[field].append(ValueMaxError)

        if math.isnan(row.get('invoice_in_reais')) or row.get('invoice_in_reais') == '':
            errors['invoice_in_reais'].append(EnergyBillValueError)

        return errors, date

    def process_csv_row(self, row, index, consumer_unit_id):
        row_errors, date = self.validate_csv_row(row, consumer_unit_id)
        return row_errors, date