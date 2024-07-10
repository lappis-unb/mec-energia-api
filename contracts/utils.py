from datetime import datetime
import re
import locale
from decimal import Decimal
from pathlib import Path 
import arrow

class ContractUtils: 
    def validate_date(self, energy_bill_date): 
        #dd/mm/aaaa, mmm/aaaa, mm/aaaa
        if isinstance(energy_bill_date, datetime): 
            return energy_bill_date.date()

        try: 
            date_obj = arrow.get(energy_bill_date, [
                "MMM/YYYY",         
                "MM/YYYY",           
                "MMM/YY",           
                "YYYY/MM/DD"            
            ], locale='pt_br')
        except: 
            return False

        return date_obj.date()


    def check_file_extension(self, file_name): 
        return Path(file_name).suffix[1:].lower()

