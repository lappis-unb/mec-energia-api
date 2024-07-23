import pytest
from utils.user.authentication import (
    generate_random_password,
    create_token_response,
    create_valid_token_response,
    generate_link_to_reset_password,
)
from mec_energia import settings

def test_generate_link_to_reset_password_first_access(monkeypatch):
    token = "dummy_token"
    user_first_name = "John"
    password_status = "first_access"

    monkeypatch.setattr(settings, "MEC_ENERGIA_URL", "http://example.com")
    monkeypatch.setattr(settings, "MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS", "first_access")

    link = generate_link_to_reset_password(token, user_first_name, password_status)
    expected_link = "http://example.com/first_access/?nome=John&token=dummy_token"

    assert link == expected_link

def test_generate_link_to_reset_password_admin_reset(monkeypatch):
    token = "dummy_token"
    user_first_name = "John"
    password_status = "admin_reset"

    monkeypatch.setattr(settings, "MEC_ENERGIA_URL", "http://example.com")
    monkeypatch.setattr(settings, "MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET", "admin_reset")

    link = generate_link_to_reset_password(token, user_first_name, password_status)
    expected_link = "http://example.com/admin_reset/?nome=John&token=dummy_token"

    assert link == expected_link

def test_generate_link_to_reset_password_user_reset(monkeypatch):
    token = "dummy_token"
    user_first_name = "John"
    password_status = "user_reset"

    monkeypatch.setattr(settings, "MEC_ENERGIA_URL", "http://example.com")
    monkeypatch.setattr(settings, "MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET", "user_reset")

    link = generate_link_to_reset_password(token, user_first_name, password_status)
    expected_link = "http://example.com/user_reset/?nome=John&token=dummy_token"

    assert link == expected_link

def test_generate_link_to_reset_password_invalid_status():
    token = "dummy_token"
    user_first_name = "John"
    password_status = "invalid_status"

    with pytest.raises(ValueError, match="Invalid password_status"):
        generate_link_to_reset_password(token, user_first_name, password_status)
