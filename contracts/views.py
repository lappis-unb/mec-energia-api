import os
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import FileResponse
from datetime import datetime

from . import models
from . import serializers

from universities.models import ConsumerUnit
from users.requests_permissions import RequestsPermissions

from utils.subgroup_util import Subgroup

import csv
from io import TextIOWrapper


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        body_consumer_unit_id = request.data['consumer_unit']

        try:
            consumer_unit = ConsumerUnit.objects.get(id=body_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        contract = self.get_object()

        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(query_serializer=serializers.ContractListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.default_users_permissions

        params_serializer = serializers.ContractListParamsSerializer(
            data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get('consumer_unit_id')

        try:
            consumer_unit = ConsumerUnit.objects.get(
                id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        queryset = models.Contract.objects.filter(
            consumer_unit=consumer_unit.id)
        serializer = serializers.ContractSerializer(
            queryset, many=True, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.default_users_permissions
        contract = self.get_object()

        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(contract)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializers.ListSubgroupsSerializerForDocs(many=True)})
    @action(detail=False, methods=['get'], url_path='list-subgroups')
    def list_subgroups(self, request: Request, pk=None):
        try:
            subgroups = {"subgroups": Subgroup.get_all_subgroups()}
        except Exception as error:
            return Response({'list subgroups error': f'{error}'}, status.HTTP_400_BAD_REQUEST)

        return JsonResponse(subgroups, safe=False)

    @swagger_auto_schema(
        query_serializer=serializers.ContractListParamsSerializer,
        responses={200: serializers.ContractListSerializer})
    @action(detail=False, methods=['get'], url_path='get-current-contract-of-consumer-unit')
    def get_current_contract_of_consumer_unit(self, request: Request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        params_serializer = serializers.ContractListParamsSerializer(
            data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get('consumer_unit_id')

        try:
            consumer_unit = ConsumerUnit.objects.get(
                id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        contract = consumer_unit.current_contract

        serializer = serializers.ContractListSerializer(
            contract, many=False, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)


class EnergyBillViewSet(viewsets.ModelViewSet):
    queryset = models.EnergyBill.objects.all()
    serializer_class = serializers.EnergyBillSerializer

    def create(self, request, *args, **kwargs):
        consumer_unit_id = request.data.get('consumer_unit')
        date_str = request.data.get('date')
        anotacoes = request.data.get('anotacoes', "")
        address = request.data.get('address', "")

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response('Invalid date, try this format: "yyyy-mm-dd".', status=status.HTTP_400_BAD_REQUEST)

        if len(anotacoes) > 1000:  # comprimento máximo
            return Response('Anotacoes is too long.', status=status.HTTP_400_BAD_REQUEST)

        if len(address) > 1000:
            return Response('Endereco is too long.', status=status.HTTP_400_BAD_REQUEST)

        if models.EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
            return Response('There is already an energy bill this month and year for this consumer unit.', status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: serializers.EnergyBillListSerializerForDocs(many=True)},
                         query_serializer=serializers.EnergyBillListParamsSerializer)
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.default_users_permissions

        params_serializer = serializers.EnergyBillListParamsSerializer(
            data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get('consumer_unit_id')

        try:
            consumer_unit = ConsumerUnit.objects.get(
                id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({'error': 'consumer unit does not exist'}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({'detail': f'{error}'}, status.HTTP_401_UNAUTHORIZED)

        energy_bills = consumer_unit.get_all_energy_bills()

        return Response(energy_bills)

    @action(detail=False, methods=['post'], url_path='multiple_create')
    def multiple_create(self, request, *args, **kwargs):
        consumer_unit_id = request.data.get('consumer_unit')
        contract_id = request.data.get('contract')
        energy_bills_data = request.data.get('energy_bills', [])
        response_data = []
        errors = []

        for bill_data in energy_bills_data:
            date_str = bill_data.get('date')

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append(
                    {'error': 'Invalid date format', 'data': bill_data})
                continue

            if models.EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
                errors.append({
                    'error': 'There is already an energy bill this month and year for this consumer unit',
                    'data': bill_data
                })
                continue

            if not models.EnergyBill.check_energy_bill_covered_by_contract(consumer_unit_id, date):
                errors.append({
                    'error': 'No contract covers the date of this energy bill',
                    'data': bill_data
                })
                continue

            bill_data['consumer_unit'] = consumer_unit_id
            bill_data['contract'] = contract_id

            serializer = self.get_serializer(data=bill_data)
            if not serializer.is_valid():
                errors.append({'error': 'Validation error',
                              'data': bill_data, 'details': serializer.errors})

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        for bill_data in energy_bills_data:
            bill_data['consumer_unit'] = consumer_unit_id
            bill_data['contract'] = contract_id

            serializer = self.get_serializer(data=bill_data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)

        return Response({'created': response_data}, status=status.HTTP_201_CREATED)

    # Csv functions

    def validate_csv_row(self, row, consumer_unit_id):
        errors = {}

        try:
            date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            errors['date'] = False
        except ValueError:
            errors['date'] = True

        for field, max_length in [
            ('invoice_in_reais', 10),
            ('peak_consumption_in_kwh', 6),
            ('off_peak_consumption_in_kwh', 6),
            ('peak_measured_demand_in_kw', 6),
            ('off_peak_measured_demand_in_kw', 6),
        ]:
            value = row.get(field, "")
            if len(value) > max_length:
                errors[field] = True
            else:
                errors[field] = False

        if models.EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
            errors['date'] = True

        errors['dateNotCoveredByContract'] = not models.EnergyBill.check_energy_bill_covered_by_contract(
            consumer_unit_id, date)

        return errors, date

    def process_csv_row(self, row, index, consumer_unit_id):
        row_errors, date = self.validate_csv_row(row, consumer_unit_id)
        return row_errors, date

    @swagger_auto_schema(method='post')
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_csv(self, request, *args, **kwargs):
        errors = []
        energy_bill_data = []
        date_list = []
        duplicate_dates = []

        serializer = serializers.CSVFileSerializer(data=request.data)

        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            csv_reader = csv.DictReader(decoded_file)

            consumer_unit_id = request.data.get('consumer_unit_id')

            if not consumer_unit_id:
                return Response({'errorsMsg': {'consumer_unit_id': True}}, status=status.HTTP_400_BAD_REQUEST)

            for row in csv_reader:
                date = row.get('date').strip()
                if date in date_list:
                    if date not in duplicate_dates:
                        duplicate_dates.append(date)

                else:
                    date_list.append(date)

            decoded_file.seek(0)
            csv_reader = csv.DictReader(decoded_file)

            seen_dates = set()

            for index, row in enumerate(csv_reader):
                row_errors, date = self.process_csv_row(
                    row, index, consumer_unit_id)

                is_duplicate_date_csv = str(date) in duplicate_dates

                if str(date) in seen_dates:
                    continue

                seen_dates.add(str(date))

                energy_bill_row = {
                    'consumer_unit': {'value': consumer_unit_id, 'error': False if consumer_unit_id else True},
                    'date': {
                        'value': date,
                        'errorDoubleDateCsv': is_duplicate_date_csv,
                        'errorDoubleDateRegistered': row_errors.get('date', False),
                        'errorDateNotCoveredByContract': row_errors.get('dateNotCoveredByContract', False)
                    },
                    'invoice_in_reais': {'value': row.get('invoice_in_reais', ""), 'error': row_errors.get('invoice_in_reais', False)},
                    'is_atypical': {'value': row.get('is_atypical', ""), 'error': False},
                    'peak_consumption_in_kwh': {'value': row.get('peak_consumption_in_kwh', ""), 'error': row_errors.get('peak_consumption_in_kwh', False)},
                    'off_peak_consumption_in_kwh': {'value': row.get('off_peak_consumption_in_kwh', ""), 'error': row_errors.get('off_peak_consumption_in_kwh', False)},
                    'peak_measured_demand_in_kw': {'value': row.get('peak_measured_demand_in_kw', ""), 'error': row_errors.get('peak_measured_demand_in_kw', False)},
                    'off_peak_measured_demand_in_kw': {'value': row.get('off_peak_measured_demand_in_kw', ""), 'error': row_errors.get('off_peak_measured_demand_in_kw', False)}
                }

                energy_bill_data.append(energy_bill_row)

            return Response({'data': energy_bill_data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download-csv-model')
    def download_csv_model(self, request):
        file_path = os.path.join(
            settings.BASE_DIR, 'docs', 'modelo_importar_tarifas.csv')

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        else:
            return Response("Document does not exist", status=400)
