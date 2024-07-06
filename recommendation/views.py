from pandas import DataFrame
from datetime import date

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from mec_energia.settings import MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION, IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION
from universities.models import ConsumerUnit
from contracts.models import Contract
from tariffs.models import Tariff

from recommendation_commons.static_getters import StaticGetters
from recommendation.calculator import RecommendationCalculator
from recommendation_commons.helpers import fill_with_pending_dates, fill_history_with_pending_dates
from recommendation_commons.response import build_response

class RecommendationViewSet(ViewSet):
    http_method_names = ['get']

    def retrieve(self, request: Request, pk=None):
        '''Recomendação via percentis. Deve ser fornecido o ID da Unidade Consumidora.

        `plotRecommendedDemands`: se a tarifa recomendada é VERDE, os campos
        `plotRecommendedDemands.offPeakDemandInKw` e
        `plotRecommendedDemands.peakDemandInKw`
        possuem o mesmo valor. Você pode plotar os dois ou plotar apenas um
        desses campos como demanda única.

        `table_current_vs_recommended_contract.absolute_difference = current - recommended`
        '''

        consumer_unit_id = pk
        try:
            consumer_unit = ConsumerUnit.objects.get(pk=consumer_unit_id)
        except ConsumerUnit.DoesNotExist:
            return Response({'errors': ['Consumer unit does not exist']}, status=status.HTTP_404_NOT_FOUND)

        if not consumer_unit.is_active:
            return Response({'errors': ['Consumer unit is not active']}, status=status.HTTP_400_BAD_REQUEST)

        contract = consumer_unit.current_contract
        distributor_id = contract.distributor.id

        blue, green = StaticGetters.get_tariffs(contract.subgroup, distributor_id)

        errors = []
        warnings = []

        is_missing_tariff = blue == None or green == None
        if is_missing_tariff:
            errors.append('Lance tarifas para análise')

        consumption_history, pending_bills_dates, atypical_bills_count = StaticGetters.get_consumption_history(consumer_unit, contract)

        consumption_history_length = len(consumption_history)
        pending_num = len(pending_bills_dates) - atypical_bills_count
        has_enough_energy_bills = consumption_history_length >= MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION

        if not has_enough_energy_bills:
            errors.append(f'Lance ao menos {6 + atypical_bills_count} faturas para realizar a análise'
                        f"{'.' + chr(10) + 'Somente faturas marcadas como ?incluir na análise? são consideradas.'.replace('?', chr(34)) if atypical_bills_count > 0 else ''}")
        elif consumption_history_length + atypical_bills_count < IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION:
            warnings.append(
                f'Lance mais {pending_num} {"fatura" if pending_num == 1 else "faturas"} dos últimos 12 meses para aumentar a precisão da análise'
            )

        if blue.end_date or green.end_date > date.today():
            warnings.append('Atualize as tarifas vencidas para aumentar a precisão da análise')

        calculator = None
        if not is_missing_tariff:
            calculator = RecommendationCalculator(
                consumption_history=consumption_history,
                current_tariff_flag=contract.tariff_flag,
                blue_tariff=blue,
                green_tariff=green,
            )

        recommendation = None
        current_contract = calculator.current_contract

        if calculator and has_enough_energy_bills:
            recommendation = calculator.calculate()
            if recommendation:
                fill_with_pending_dates(recommendation, consumption_history, pending_bills_dates)
        else:
            # FIXME: temporário
            fill_history_with_pending_dates(consumption_history, pending_bills_dates)

        return build_response(
            recommendation,
            current_contract,
            consumption_history,
            contract,
            consumer_unit,
            blue,
            green,
            errors,
            warnings,
            consumption_history_length,
        )
