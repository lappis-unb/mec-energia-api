import pytest
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework.test import APIClient
from universities.recommendation import Recommendation
from tests.test_utils import dicts_test_utils, create_objects_test_utils

@pytest.mark.django_db
class TestRecommendation:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email=self.user_dict['email'],
            password=self.user_dict['password']
        )

        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

        self.consumer_unit_test_1_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test_1 = create_objects_test_utils.create_test_consumer_unit(self.consumer_unit_test_1_dict, self.university)

        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_1 = create_objects_test_utils.create_test_contract(self.contract_test_1_dict, self.distributor, self.consumer_unit_test_1)

        self.energy_bill_test_2_dict = dicts_test_utils.energy_bill_dict_1
        self.energy_bill_test_2 = create_objects_test_utils.create_test_energy_bill(self.energy_bill_test_2_dict, self.contract_test_1, self.consumer_unit_test_1)



    def test_validate_data_recommendation(self):
        response = Recommendation.get_energy_bills_for_recommendation(self.consumer_unit_test_1.id)
        date_for_recommendation = Recommendation.set_date_for_recommendation(self.consumer_unit_test_1.id)

        if response:
            first_energy_bill_object = response[0]

            assert first_energy_bill_object['month'] < date_for_recommendation.month
            assert first_energy_bill_object['year'] == date_for_recommendation.year

    def test_user_date(self):
        user_date = "2024-05-01"
        response = Recommendation.get_energy_bills_for_recommendation(self.consumer_unit_test_1.id, user_data=user_date)
        date_for_recommendation = Recommendation.set_date_for_recommendation(self.consumer_unit_test_1.id, user_date)

        if response:
            response = response[0]
            assert response['month'] < date_for_recommendation.month
            assert response['year'] == date_for_recommendation.year

    def test_non_user_date(self):
        user_date = ""
        response = Recommendation.get_energy_bills_for_recommendation(self.consumer_unit_test_1.id, user_data=user_date)
        date_for_recommendation = Recommendation.set_date_for_recommendation(self.consumer_unit_test_1.id, user_date)

        if response:
            response = response[0]
            assert response['month'] < date_for_recommendation.month
            assert response['year'] == date_for_recommendation.year


    def test_ValueError(self):
        user_date = "alo"
        with pytest.raises(ValueError, match="Data inválida. Por favor, forneça a data no formato YYYY-MM-DD."):
            Recommendation.set_date_for_recommendation(
                self.consumer_unit_test_1.id,
                user_data=user_date
            )

