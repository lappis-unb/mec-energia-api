import pytest

from utils.user.user_type_util import UserType

from tests.test_utils import dicts_test_utils
from users import models


def test_raise_exeception_for_invalid_user_type():
    # CT1
    invalid_user_type = 'invalid'

    try:
        UserType.is_valid_user_type(invalid_user_type)
        assert False
    except Exception:
        assert True


def test_return_user_type_when_user_type_is_valid():
    # CT2
    user_type = models.CustomUser.all_user_types[0]
    assert user_type == UserType.is_valid_user_type(user_type)


def test_return_user_type_for_university_user_and_valid_university_user_type():
    # CT3
    user_model = models.UniversityUser
    user_type = models.CustomUser.university_user_types[0]
    assert user_type == UserType.is_valid_user_type(user_type, user_model)


def test_raise_expection_for_valid_university_user_and_invalid_university_user_type():
    # CT4
    user_model = models.UniversityUser
    user_type = 'invalid'

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_raise_exeception_for_invalid_university_user_and_valid_university_user_type():
    # CT5
    user_model = 'invalid'
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_return_user_type_for_custom_user_and_use_type_super_user():
    # CT6
    user = models.CustomUser
    user_type = models.CustomUser.super_user_type
    assert user_type == UserType.is_valid_user_type(user_type, user)


def test_raise_expection_for_valid_custom_user_and_not_super_user_type():
    # CT7
    user_model = models.CustomUser
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_raise_exception_for_invalid_custom_user_and_valid_super_user_type():
    # CT8
    user_model = 'invalid'
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True
