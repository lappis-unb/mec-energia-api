from . import models
from datetime import datetime
from .utils import ContractUtils
import csv
from io import TextIOWrapper
from collections import defaultdict
from mec_energia.error_response_manage import * 
import datetime
import math
from decimal import Decimal

month_translation = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
    'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
    'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
}

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
                row_errors["date"].append(DuplicatedDateError)

            seen_dates.add(str(date))
            energy_bill_row = {
                'consumer_unit': {'value': consumer_unit_id, 'error': False if consumer_unit_id else True},
                'date': {
                    'value': date,
                    'errors': row_errors.get('date')
                },
                'invoice_in_reais': {'value': row.get('invoice_in_reais', ""), 'errors': row_errors.get('invoice_in_reais')},
                'peak_consumption_in_kwh': {'value': row.get('peak_consumption_in_kwh', ""), 'errors': row_errors.get('peak_consumption_in_kwh')},
                'off_peak_consumption_in_kwh': {'value': row.get('off_peak_consumption_in_kwh', ""), 'errors': row_errors.get('off_peak_consumption_in_kwh')},
                'peak_measured_demand_in_kw': {'value': row.get('peak_measured_demand_in_kw', "") ,'errors': row_errors.get('peak_measured_demand_in_kw')},
                'off_peak_measured_demand_in_kw': {'value': row.get('off_peak_measured_demand_in_kw', ""), 'errors': row_errors.get('off_peak_measured_demand_in_kw')}
            }
            energy_bill_data.append(energy_bill_row)
            
        return energy_bill_data

    def error_append(self, field, errors):
        errors[field].append(EnergyBillValueError if field=='invoice_in_reais' else ValueMaxError)

    def check_value(self, value, max_value, row, field, errors):
        try: 
            value = float(value.replace(',', '.'))
            if value > max_value:
                self.error_append(field, errors)
        except: 
            row[field] = value
            if(value != ""):
                self.error_append(field, errors)

    def get_max_values(self):
        return [
            ('invoice_in_reais', 99999999.99),
            ('peak_consumption_in_kwh', 9999999.99),
            ('off_peak_consumption_in_kwh', 9999999.99),
            ('peak_measured_demand_in_kw', 9999999.99),
            ('off_peak_measured_demand_in_kw', 9999999.99),
        ]

    def error_detection(self, row, errors):
        for field, max_value in self.get_max_values():
            value = row.get(field, "")
            if isinstance(value, str):
                self.check_value(value, max_value, row, field, errors)
            
            elif math.isnan(value):
                row[field] = ""

            elif value > max_value:
                row[field] = value
                self.error_append(field, errors)

        if row.get('invoice_in_reais') == '':
            errors['invoice_in_reais'].append(EnergyBillValueError)
            

    def validate_csv_row(self, row, consumer_unit_id):
        errors = defaultdict(list)
        date = ContractUtils().validate_date(row["date"])
        if(not isinstance(date, datetime.date)):
            errors["date"].append(FormatDateError)

        elif models.EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
            errors['date'].append(AlreadyHasEnergyBill)

        else:
            covered, contract_date = models.EnergyBill.check_energy_bill_covered_by_contract(consumer_unit_id, date)
            if not covered:
                month_name = contract_date.strftime("%B")
                month_name_pt = month_translation[month_name]
                contract_date_str = f"{month_name_pt} de {contract_date.year}"
                dynamic_error_message = ErrorMensageParser.parse(DateNotCoverByContractError, (contract_date_str))
                errors["date"].append(dynamic_error_message)

        self.error_detection(row, errors)
        return errors, date

    def process_csv_row(self, row, index, consumer_unit_id):
        row_errors, date = self.validate_csv_row(row, consumer_unit_id)
        return row_errors, date