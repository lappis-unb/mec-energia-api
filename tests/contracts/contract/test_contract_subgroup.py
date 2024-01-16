import pytest
from rest_framework.test import APIClient

from contracts.models import Contract

from utils.subgroup_util import Subgroup

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

@pytest.mark.django_db
class TestContractSubGroup:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])

        self.consumer_unit_test_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test = create_objects_test_utils.create_test_consumer_unit(self.consumer_unit_test_dict, self.university)

        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_2_dict = dicts_test_utils.contract_dict_2
        self.contract_test_3_dict = dicts_test_utils.contract_dict_3

        self.contract_test_1 = create_objects_test_utils.create_test_contract(self.contract_test_1_dict, self.distributor, self.consumer_unit_test)
        self.contract_test_2 = create_objects_test_utils.create_test_contract(self.contract_test_2_dict, self.distributor, self.consumer_unit_test)
        self.contract_test_3 = create_objects_test_utils.create_test_contract(self.contract_test_3_dict, self.distributor, self.consumer_unit_test)

        self.contract_test_supply_voltage_1 = -1 # CT1
        self.contract_test_supply_voltage_2 = 69 # CT2
        self.contract_test_supply_voltage_3 = 230  # CT3
        self.contract_test_supply_voltage_4 = 70  # CT4


    def test_read_contract_subgroup_A3(self):
        assert self.contract_test_3.supply_voltage == 69
        assert self.contract_test_3.subgroup == 'A3'
    
    def test_read_contract_subgroup_A2(self):
        assert self.contract_test_1.supply_voltage == 100.00
        assert self.contract_test_1.subgroup == 'A2'

    def test_read_contract_subgroup_A1(self):
        assert self.contract_test_2.supply_voltage == 250.00
        assert self.contract_test_2.subgroup == 'A1'

    def test_throws_exception_when_already_have_a_contract_in_this_date(self):
        with pytest.raises(Exception) as e:
            contract_test_6_dict = dicts_test_utils.contract_dict_6
            create_objects_test_utils.create_test_contract(contract_test_6_dict, self.distributor, self.consumer_unit_test)

        assert 'Already have the contract in this date' in str(e.value)

    def test_throws_exception_when_suply_voltage_does_not_match_subgroup_ranges(self):
        with pytest.raises(Exception) as e:
            contract_test_5_dict = dicts_test_utils.contract_dict_5
            create_objects_test_utils.create_test_contract(contract_test_5_dict, self.distributor, self.consumer_unit_test)
        
        assert 'Subgroup not found' in str(e.value)
        assert 3 == Contract.objects.all().count()

    def test_throws_exception_when_suply_voltage_below_minimum(self):
        with pytest.raises(Exception) as e:
            Subgroup.get_subgroup(self.contract_test_supply_voltage_1)
        assert 'Subgroup not found' in str(e.value)

    def test_get_group_minimum_and_maximum_equal(self):
        assert Subgroup.get_subgroup(self.contract_test_supply_voltage_2) == Subgroup.A3

    def test_get_group_without_maximum_voltage(self):
        assert Subgroup.get_subgroup(self.contract_test_supply_voltage_3) == Subgroup.A1

    def test_throws_exception_when_suply_voltage_does_not_match_ranges(self):
        with pytest.raises(Exception) as e:
            Subgroup.get_subgroup(self.contract_test_supply_voltage_4)
        assert 'Subgroup not found' in str(e.value)