"""Тесты методов чтения раздела электронной подписи (ЭЦП).

Раздел ``signs`` не подключён к публичному ``IPSClient``, поэтому тесты работают
с агрегатором :class:`SignsAPI` напрямую (он наследует ядро ``APIManager`` и
является асинхронным контекстным менеджером).
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.signs import SignsAPI


async def test_sign_graphs_returns_string_key_name(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"id": "graph-1", "displayName": "Маршрут согласования"},
        {"id": "graph-2", "displayName": "Маршрут утверждения"},
    ]
    fake_ips.add("get", "/api/signs/graphs", body=body)
    async with SignsAPI(config=token_config) as ips:
        graphs = await ips.sign_graphs()

    assert len(graphs) == 2
    assert graphs[0].id == "graph-1"
    assert graphs[0].display_name == "Маршрут согласования"


async def test_sign_graphs_handles_missing_fields(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/signs/graphs", body=[{}])
    async with SignsAPI(config=token_config) as ips:
        graphs = await ips.sign_graphs()

    assert graphs[0].id is None
    assert graphs[0].display_name is None


async def test_sign_ranks_returns_int_key_name(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"id": 1, "displayName": "Подписант"},
        {"id": 2, "displayName": "Утверждающий"},
    ]
    fake_ips.add("get", "/api/signs/ranks", body=body)
    async with SignsAPI(config=token_config) as ips:
        ranks = await ips.sign_ranks()

    assert len(ranks) == 2
    assert ranks[0].id == 1
    assert ranks[0].display_name == "Подписант"


async def test_sign_ranks_defaults_id_to_zero(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/signs/ranks", body=[{"displayName": "Без ключа"}])
    async with SignsAPI(config=token_config) as ips:
        ranks = await ips.sign_ranks()

    assert ranks[0].id == 0
    assert ranks[0].display_name == "Без ключа"


async def test_additional_sign_output_params(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [{"id": 10, "displayName": "Дата подписи"}]
    fake_ips.add("get", "/api/signs/AdditionalSignOutputParams", body=body)
    async with SignsAPI(config=token_config) as ips:
        params = await ips.additional_sign_output_params()

    assert len(params) == 1
    assert params[0].id == 10
    assert params[0].display_name == "Дата подписи"


async def test_additional_user_output_params(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [{"id": 20, "displayName": "Должность"}]
    fake_ips.add("get", "/api/signs/AdditionalUserOutputParams", body=body)
    async with SignsAPI(config=token_config) as ips:
        params = await ips.additional_user_output_params()

    assert len(params) == 1
    assert params[0].id == 20
    assert params[0].display_name == "Должность"
