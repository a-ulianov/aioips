"""Тесты конфигурации клиента IPS."""

import pytest
from pydantic import ValidationError
from tests.conftest import BASE_URL

from aioips import IPSConfig


def test_token_auth_is_valid():
    config = IPSConfig(base_url=BASE_URL, access_token="tok", _env_file=None)
    assert config.uses_token_auth is True
    assert config.base_url == BASE_URL


def test_login_auth_is_valid():
    config = IPSConfig(base_url=BASE_URL, login_name="u", password="p", _env_file=None)
    assert config.uses_token_auth is False


def test_missing_credentials_raises():
    with pytest.raises(ValidationError, match="авторизационные данные"):
        IPSConfig(base_url=BASE_URL, _env_file=None)


def test_login_without_password_is_not_enough():
    with pytest.raises(ValidationError):
        IPSConfig(base_url=BASE_URL, login_name="u", _env_file=None)


def test_base_url_scheme_validated():
    with pytest.raises(ValidationError, match="http"):
        IPSConfig(base_url="ftp://host", access_token="t", _env_file=None)


def test_base_url_trailing_slash_stripped():
    config = IPSConfig(base_url=f"{BASE_URL}/", access_token="t", _env_file=None)
    assert config.base_url == BASE_URL


def test_retry_bounds_validated():
    with pytest.raises(ValidationError, match="retry_max_wait"):
        IPSConfig(
            base_url=BASE_URL,
            access_token="t",
            retry_min_wait=5,
            retry_max_wait=1,
            _env_file=None,
        )


def test_reads_from_environment(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("IPS_BASE_URL", BASE_URL)
    monkeypatch.setenv("IPS_ACCESS_TOKEN", "from-env")
    config = IPSConfig(_env_file=None)
    assert config.access_token == "from-env"
