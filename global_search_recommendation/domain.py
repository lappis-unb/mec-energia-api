from datetime import date

from mec_energia.settings import MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION, IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION
from universities.models import ConsumerUnit
from tariffs.models import Tariff
from recommendation_commons.static_getters import StaticGetters

from rest_framework import status

class Domain:

    def __init__(self, uc_id: int):
        self.uc_id = uc_id
        self.errors = []
        self.warnings = []

    def _exceeded_demand (self, meassured_demand: .0, contracted_demand: .0) -> .0 :
        if meassured_demand <= contracted_demand :
            return 0
        else :
            return  meassured_demand - contracted_demand

    def mount(self):
        try:
            self.consumer_unit = ConsumerUnit.objects.get(pk=self.uc_id)
        except ConsumerUnit.DoesNotExist:
            return ({'errors': ['Consumer unit does not exist']}, status.HTTP_404_NOT_FOUND)

        if not self.consumer_unit.is_active:
            return ({'errors': ['Consumer unit is not active']}, status.HTTP_400_BAD_REQUEST)
        
        self.current_contract = self.consumer_unit.current_contract
        if not self.current_contract:
           self.errors.append('Unidade Consumidora sem Contrato')
           return None

        self.distributor = self.current_contract.distributor

        self.blue, self.green = StaticGetters.get_tariffs(self.current_contract.subgroup, self.distributor.id)

        if self.blue == None or self.green == None:
            self.errors.append('Lance tarifas para análise')
            return None
        
        self.current_tariff = self.green if self.current_contract.tariff_flag == Tariff.GREEN else self.blue
        
        if self.blue.end_date or self.green.end_date > date.today():
            self.warnings.append('Atualize as tarifas vencidas para aumentar a precisão da análise')

        self.consumption_history, self.pending_bills_dates, atypical_bills_count = StaticGetters.get_consumption_history(self.consumer_unit, self.current_contract)

        self.consumption_history_length = len(self.consumption_history)
        pending_num = len(self.pending_bills_dates) - atypical_bills_count
        
        if self.consumption_history_length < MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION:
            self.errors.append(f'Lance ao menos {6 + atypical_bills_count} faturas para realizar a análise'
                        f"{'.' + chr(10) + 'Somente faturas marcadas como ?incluir na análise? são consideradas.'.replace('?', chr(34)) if atypical_bills_count > 0 else ''}")
            return None
        elif self.consumption_history_length + atypical_bills_count < IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION:
            self.warnings.append(
                f'Lance mais {pending_num} {"fatura" if pending_num == 1 else "faturas"} dos últimos 12 meses para aumentar a precisão da análise'
            )

        self.base_consumption_history = self.consumption_history[['peak_consumption_in_kwh','off_peak_consumption_in_kwh',
                             'peak_measured_demand_in_kw','off_peak_measured_demand_in_kw',
                             'contract_peak_demand_in_kw', 'contract_off_peak_demand_in_kw']].values.astype(float)

        self.consumption_cost_on_blue = StaticGetters.get_comsuption_cost(self.consumption_history, self.blue).sum()
        self.consumption_cost_on_green = StaticGetters.get_comsuption_cost(self.consumption_history, self.green).sum()
        return None

    def green_objective_func(self, demands) -> .0 :
        demand_value = 0
        for bill in self.base_consumption_history:
            demand_value += demands[0] + 3 * (self._exceeded_demand(bill[2], demands[0]) + \
                                 self._exceeded_demand(bill[3], demands[0]))

        return float(self.green.na_tusd_in_reais_per_kw) * demand_value + self.consumption_cost_on_green

    def blue_objective_func(self, demands) -> .0 :
        peak_demand_value = 0
        off_peak_demand_value = 0
        for bill in self.base_consumption_history:
            peak_demand_value += demands[0] + 3 * self._exceeded_demand(bill[2], demands[0])
            off_peak_demand_value += demands[1] + 3 * self._exceeded_demand(bill[3], demands[1])

        return (float(self.blue.peak_tusd_in_reais_per_kw) * peak_demand_value) + \
               (float(self.blue.off_peak_tusd_in_reais_per_kw) * off_peak_demand_value) + self.consumption_cost_on_blue