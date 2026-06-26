"""Тесты legacy search-методов раздела объектов (контроллер ``Objects`` с заглавной)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects.objects_select_request import ObjectSelectRequest

_Client = IPSClient

SELECT_URL = "/core/api/Objects/ObjectsSelect"
SELECT_BY_ID_URL = "/core/api/Objects/ObjectsSelectById"


async def test_objects_select_request_parses_and_builds(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        SELECT_URL,
        body=[
            {
                "objectId": 1311983,
                "objectAttributes": {"f_OBJECT_NAME": "Деталь", "caption": "Деталь A"},
            },
            {"objectId": 1288391, "objectAttributes": None},
        ],
    )
    async with _Client(config=token_config) as ips:
        result = await ips.objects_select_request(
            ObjectSelectRequest(
                object_ids=[1311983, 1288391],
                attributes=["f_OBJECT_NAME", "caption"],
            ),
            object_type_id=1742,
        )

    assert [d.object_id for d in result] == [1311983, 1288391]
    assert result[0].object_attributes["f_OBJECT_NAME"] == "Деталь"
    assert result[1].object_attributes == {}  # null -> {}

    request = next(r for r in fake_ips.requests if r.path == SELECT_URL)
    assert request.method == "POST"
    assert request.query["objectTypeId"] == "1742"
    assert request.body["objectIds"] == [1311983, 1288391]
    assert request.body["attributes"] == ["f_OBJECT_NAME", "caption"]


async def test_objects_select_request_without_object_type(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", SELECT_URL, body=[])
    async with _Client(config=token_config) as ips:
        result = await ips.objects_select_request(ObjectSelectRequest(object_ids=[1]))

    request = next(r for r in fake_ips.requests if r.path == SELECT_URL)
    assert "objectTypeId" not in request.query  # опциональный query не передан
    assert request.body["attributes"] == []
    assert result == []


async def test_objects_select_by_id_parses_and_builds(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        SELECT_BY_ID_URL,
        body=[{"objectId": 1311983, "objectAttributes": {"9": "", "10": "Форма.jpg"}}],
    )
    async with _Client(config=token_config) as ips:
        result = await ips.objects_select_by_id(
            ObjectSelectRequest(object_ids=[1311983], attributes=["caption"]),
            object_type_id=1742,
        )

    assert result[0].object_id == 1311983
    assert result[0].object_attributes["10"] == "Форма.jpg"  # ключи — id атрибутов (str)

    request = next(r for r in fake_ips.requests if r.path == SELECT_BY_ID_URL)
    assert request.method == "POST"
    assert request.query["objectTypeId"] == "1742"
    assert request.body["objectIds"] == [1311983]
