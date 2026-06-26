"""Тесты мутирующих методов раздела графических подписей (штампов ЭЦП).

Каждый метод проверяется на двух уровнях: confirm-гейт (``confirm=False`` →
:class:`ValueError`, запрос НЕ выполняется) и фактическая запись (``confirm=True`` →
правильный путь/тело, возврат ``None``).
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.graph_signs import (
    AssignedSignGraph,
    AssignedSignGraphGroup,
    RankGraphSigns,
    RankGraphSignsSettings,
)

_Client = IPSClient

_SIGN_GROUP_DICT = {
    "name": "Утверждение",
    "graphs": [
        {
            "signId": "sign-1",
            "signDescription": "Главный конструктор",
            "isStrongCheck": True,
        }
    ],
}

_RANK_SIGNS_DICT = {
    "objectTypeId": 7,
    "graphs": [
        {
            "graphId": "approve",
            "isBanMultipleSign": True,
            "isAllowSimpleSign": True,
            "isAllowCryptoSign": False,
        }
    ],
}


def _sign_group_model() -> AssignedSignGraphGroup:
    return AssignedSignGraphGroup(
        name="Утверждение",
        graphs=[
            AssignedSignGraph(
                sign_id="sign-1",
                sign_description="Главный конструктор",
                is_strong_check=True,
            )
        ],
    )


def _rank_signs_model() -> RankGraphSigns:
    return RankGraphSigns(
        object_type_id=7,
        graphs=[
            RankGraphSignsSettings(
                graph_id="approve",
                is_ban_multiple_sign=True,
                is_allow_simple_sign=True,
                is_allow_crypto_sign=False,
            )
        ],
    )


# --- update_archive_sign_settings -------------------------------------------------


async def test_update_archive_sign_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_archive_sign_settings(1029, [_sign_group_model()])

    assert fake_ips.requests == []


async def test_update_archive_sign_settings_writes_model(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/api/archives/1029/signs", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_archive_sign_settings(1029, [_sign_group_model()], confirm=True)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/api/archives/1029/signs"
    assert req.body == [_SIGN_GROUP_DICT]


async def test_update_archive_sign_settings_writes_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/api/archives/1029/signs", body=None)
    async with _Client(config=token_config) as ips:
        await ips.update_archive_sign_settings(1029, [_SIGN_GROUP_DICT], confirm=True)

    assert fake_ips.requests[-1].body == [_SIGN_GROUP_DICT]


# --- update_lifecycle_level_sign_settings -----------------------------------------


async def test_update_lifecycle_level_sign_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_lifecycle_level_sign_settings(3, [_sign_group_model()])

    assert fake_ips.requests == []


async def test_update_lifecycle_level_sign_settings_writes(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/api/lifecycleLevels/3/signs", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_lifecycle_level_sign_settings(
            3, [_sign_group_model()], confirm=True
        )

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/api/lifecycleLevels/3/signs"
    assert req.body == [_SIGN_GROUP_DICT]


# --- update_lifecycle_step_sign_settings ------------------------------------------


async def test_update_lifecycle_step_sign_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_lifecycle_step_sign_settings(42, [_sign_group_model()])

    assert fake_ips.requests == []


async def test_update_lifecycle_step_sign_settings_writes(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/api/lifecycleSteps/42/signs", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_lifecycle_step_sign_settings(
            42, [_sign_group_model()], confirm=True
        )

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/api/lifecycleSteps/42/signs"
    assert req.body == [_SIGN_GROUP_DICT]


# --- update_object_type_lifecycle_step_sign_settings ------------------------------


async def test_update_object_type_lifecycle_step_sign_settings_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.update_object_type_lifecycle_step_sign_settings(
                1742, 5, [_sign_group_model()]
            )

    assert fake_ips.requests == []


async def test_update_object_type_lifecycle_step_sign_settings_writes(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/api/objectTypes/1742/lifecycleSteps/5/signs", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.update_object_type_lifecycle_step_sign_settings(
            1742, 5, [_sign_group_model()], confirm=True
        )

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/api/objectTypes/1742/lifecycleSteps/5/signs"
    assert req.body == [_SIGN_GROUP_DICT]


# --- save_rank_graph_signs --------------------------------------------------------


async def test_save_rank_graph_signs_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.save_rank_graph_signs(10, [_rank_signs_model()])

    assert fake_ips.requests == []


async def test_save_rank_graph_signs_writes_model(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/api/ranks/10/graphSigns", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.save_rank_graph_signs(10, [_rank_signs_model()], confirm=True)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/api/ranks/10/graphSigns"
    assert req.body == [_RANK_SIGNS_DICT]


async def test_save_rank_graph_signs_writes_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/api/ranks/10/graphSigns", body=None)
    async with _Client(config=token_config) as ips:
        await ips.save_rank_graph_signs(10, [_RANK_SIGNS_DICT], confirm=True)

    assert fake_ips.requests[-1].body == [_RANK_SIGNS_DICT]
