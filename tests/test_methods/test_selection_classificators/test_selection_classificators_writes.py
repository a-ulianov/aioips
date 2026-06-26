"""Тесты мутирующих методов раздела классификаторов выбора."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

# Путь classify задаётся через КИРИЛЛИЧЕСКУЮ ``с`` (U+0441) — баг IPS API.
_CLASSIFY_PATH = "/core/api/selectionClassificators/сlassifyObject"


async def test_include_object_in_classificators(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/selectionClassificators/includeObjectInClassificators"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.include_object_in_classificators(102550, [204, 205])

    assert result is None
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == path
    assert captured.body == {"objectId": 102550, "classificatorObjectIds": [204, 205]}


async def test_include_objects_in_classificator(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/selectionClassificators/includeObjectsInClassificator"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.include_objects_in_classificator(204, [102550, 102551])

    assert result is None
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == path
    assert captured.body == {"classificatorId": 204, "objectIds": [102550, 102551]}


async def test_exclude_object_from_classificators(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/selectionClassificators/excludeObjectFromClassificators"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.exclude_object_from_classificators(102550, [204, 205], confirm=True)

    assert result is None
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == path
    assert captured.body == {"objectId": 102550, "classificatorObjectIds": [204, 205]}


async def test_exclude_object_from_classificators_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.exclude_object_from_classificators(102550, [204])

    assert fake_ips.requests == []


async def test_exclude_objects_from_classificator(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/selectionClassificators/excludeObjectsFromClassificator"
    fake_ips.add("post", path, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.exclude_objects_from_classificator(204, [102550, 102551], confirm=True)

    assert result is None
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == path
    assert captured.body == {"classificatorId": 204, "objectIds": [102550, 102551]}


async def test_exclude_objects_from_classificator_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError):
            await ips.exclude_objects_from_classificator(204, [102550])

    assert fake_ips.requests == []


async def test_classify_object_uses_cyrillic_path(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", _CLASSIFY_PATH, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.classify_object(102550, [204, 205])

    assert result is None
    captured = fake_ips.requests[-1]
    assert captured.method == "POST"
    assert captured.path == _CLASSIFY_PATH
    # Проверяем, что сегмент начинается именно с кириллической ``с`` (U+0441).
    assert captured.path.rsplit("/", 1)[-1][0] == "с"
    assert captured.body == {"objectId": 102550, "classificatorObjectIds": [204, 205]}
