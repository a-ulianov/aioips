"""Тесты методов чтения раздела графических подписей (штампов ЭЦП)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_RANK_GRAPH_SIGNS = {
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

_SIGN_GROUP = {
    "name": "Утверждение",
    "graphs": [
        {
            "signId": "sign-1",
            "signDescription": "Главный конструктор",
            "isStrongCheck": True,
        }
    ],
}


async def test_rank_graph_sign_object_types_returns_ints(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/api/ranks/graphSigns/availableObjectTypeIds", body=[7, 12, 30])
    async with IPSClient(config=token_config) as ips:
        result = await ips.rank_graph_sign_object_types()

    assert result == [7, 12, 30]


async def test_rank_graph_signs_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/ranks/10/graphSigns", body=[_RANK_GRAPH_SIGNS])
    async with IPSClient(config=token_config) as ips:
        result = await ips.rank_graph_signs(10)

    assert len(result) == 1
    item = result[0]
    assert item.object_type_id == 7
    assert len(item.graphs) == 1
    graph = item.graphs[0]
    assert graph.graph_id == "approve"
    assert graph.is_ban_multiple_sign is True
    assert graph.is_allow_simple_sign is True
    assert graph.is_allow_crypto_sign is False


async def test_rank_graph_signs_coerces_null_graphs(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [{"objectTypeId": 7, "graphs": None}]
    fake_ips.add("get", "/api/ranks/10/graphSigns", body=body)
    async with IPSClient(config=token_config) as ips:
        result = await ips.rank_graph_signs(10)

    assert result[0].graphs == []


async def test_archive_sign_settings_returns_groups(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/archives/1029/signs", body=[_SIGN_GROUP])
    async with IPSClient(config=token_config) as ips:
        result = await ips.archive_sign_settings(1029)

    assert len(result) == 1
    group = result[0]
    assert group.name == "Утверждение"
    assert len(group.graphs) == 1
    sign = group.graphs[0]
    assert sign.sign_id == "sign-1"
    assert sign.sign_description == "Главный конструктор"
    assert sign.is_strong_check is True


async def test_lifecycle_level_sign_settings_returns_groups(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/api/lifecycleLevels/3/signs", body=[_SIGN_GROUP])
    async with IPSClient(config=token_config) as ips:
        result = await ips.lifecycle_level_sign_settings(3)

    assert result[0].graphs[0].sign_id == "sign-1"


async def test_lifecycle_step_sign_settings_coerces_null_graphs(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/api/lifecycleSteps/42/signs", body=[{"name": None, "graphs": None}])
    async with IPSClient(config=token_config) as ips:
        result = await ips.lifecycle_step_sign_settings(42)

    assert result[0].name is None
    assert result[0].graphs == []
