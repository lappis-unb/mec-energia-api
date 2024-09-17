import pytest

from django.conf import settings as s


@pytest.mark.order(1)
def test_var_secret_key_is_available():
    assert s.SECRET_KEY is not None


@pytest.mark.order(1)
def test_var_debug_is_available():
    assert s.DEBUG is not None


@pytest.mark.order(1)
def test_var_test_is_available():
    assert s.TEST is not None
    assert s.TEST


@pytest.mark.order(1)
def test_var_environment_is_available():
    assert s.ENVIRONMENT is not None
    assert s.ENVIRONMENT == "test"


@pytest.mark.order(1)
def test_var_mepa_front_url_is_available():
    assert s.MEPA_FRONT_END_URL is not None
