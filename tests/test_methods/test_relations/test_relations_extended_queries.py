"""Тесты расширенных (параметризованных) поисковых POST-методов раздела связей.

Проверяют тело запроса (сериализация схемы по алиасам с ``exclude_none``), путь эндпоинта
и разбор голого массива ``RelationSelectResultDto`` (включая коэрсинг ``null`` → ``[]``).
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.relations import (
    ObjectRelationsSelectParameters,
    RelationsSelectParameters,
)

_RESULT = [
    {"relationId": 700123, "attributes": [{"attributeId": 12, "value": "5"}]},
    {"relationId": 700124, "attributes": None},
]


async def test_relations_consist_from(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/relations/consistFrom", body=_RESULT)
    async with IPSClient(config=token_config) as ips:
        results = await ips.relations_consist_from(
            ObjectRelationsSelectParameters(
                object_id=102550,
                relation_type_id=-1,
                attributes_to_select=[{"attributeId": 12}],
            )
        )

    # Разбор массива результатов.
    assert [r.relation_id for r in results] == [700123, 700124]
    assert results[0].values == {12: "5"}
    # null вместо [] коэрсится в пустой список.
    assert results[1].attributes == []

    # Тело: путь, alias relationTypeId, exclude_none (object_type_id отсутствует).
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/relations/consistFrom"
    assert req.body == {
        "objectId": 102550,
        "relationTypeId": -1,
        "attributesToSelect": [{"attributeId": 12}],
    }


async def test_relations_enters_in(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/relations/entersIn", body=_RESULT)
    async with IPSClient(config=token_config) as ips:
        results = await ips.relations_enters_in(
            ObjectRelationsSelectParameters(
                object_id=102777,
                relation_type_id=3,
                attributes_to_select=[],
            )
        )

    assert len(results) == 2
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/relations/entersIn"
    assert req.body == {
        "objectId": 102777,
        "relationTypeId": 3,
        "attributesToSelect": [],
    }


async def test_relations_enters_in_version(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/relations/entersInVersion", body=[])
    async with IPSClient(config=token_config) as ips:
        results = await ips.relations_enters_in_version(
            ObjectRelationsSelectParameters(
                object_id=102777,
                relation_type_id=3,
                attributes_to_select=[],
                recursive=True,
            )
        )

    # Пустой массив → пустой список.
    assert results == []
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/relations/entersInVersion"
    assert req.body["recursive"] is True


async def test_relations_select(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/relations/select", body=_RESULT)
    async with IPSClient(config=token_config) as ips:
        results = await ips.relations_select(
            RelationsSelectParameters(
                relation_type_id=3,
                attribute_ids_to_select=[12],
                record_count=100,
            )
        )

    assert results[0].relation_id == 700123
    assert results[0].values.get(12) == "5"
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/relations/select"
    assert req.body == {
        "relationTypeId": 3,
        "attributeIdsToSelect": [12],
        "recordCount": 100,
    }
