"""Тест метода списка типов объектов."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.common.enumerations import ObjectVersionMode


async def test_object_types_parses_list_with_optional_fields(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    # У типа отсутствуют lifetimeReserve и classifyType — реальная особенность IPS.
    fake_ips.add(
        "get",
        "/core/api/metadata/objectTypes",
        body=[
            {
                "id": 1127,
                "guid": "cad001c5-306c-11d8-b4e9-00304f19f545",
                "objectTypeName": "Элемент правила нумерации",
                "objectName": "Элемент правила нумерации",
                "versionsMode": "multiVersion",
                "defaultRelation": 0,
                "schemeId": 1,
                "options": ["none", "localObjectType"],
            }
        ],
    )
    async with IPSClient(config=token_config) as ips:
        types = await ips.object_types()

    assert len(types) == 1
    obj = types[0]
    assert obj.id == 1127
    assert obj.versions_mode == ObjectVersionMode.MULTI_VERSION
    assert obj.lifetime_reserve is None
    assert obj.classify_type is None
    assert obj.options == ["none", "localObjectType"]
