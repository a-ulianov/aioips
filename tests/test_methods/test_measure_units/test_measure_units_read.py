"""Тесты методов чтения раздела единиц измерения."""

from uuid import UUID

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_UNIT = {
    "id": 5,
    "guid": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "longName": "миллиметр",
    "shortName": "мм",
    "k": 0.001,
    "physicalQuantityId": 1,
    "physicalQuantityGuid": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "isDefault": False,
    "shortNameIndex": ["мм"],
    "operationList": ["sum"],
}


async def test_measure_units_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/measureUnits", body=[_UNIT, _UNIT])
    async with IPSClient(config=token_config) as ips:
        units = await ips.measure_units()

    assert len(units) == 2
    unit = units[0]
    assert unit.id == 5
    assert unit.guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    assert unit.short_name == "мм"
    assert unit.k == 0.001
    assert unit.physical_quantity_id == 1
    assert unit.physical_quantity_guid == UUID("cad001c5-306c-11d8-b4e9-00304f19f546")
    assert unit.short_name_index == ["мм"]
    assert unit.operation_list == ["sum"]


async def test_measure_units_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    unit = {**_UNIT, "shortNameIndex": None, "operationList": None}
    fake_ips.add("get", "/core/api/measureUnits", body=[unit])
    async with IPSClient(config=token_config) as ips:
        units = await ips.measure_units()

    assert units[0].short_name_index == []
    assert units[0].operation_list == []


async def test_measure_unit_quantity_guids_returns_strings(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    guids = [
        "cad001c5-306c-11d8-b4e9-00304f19f545",
        "cad001c5-306c-11d8-b4e9-00304f19f546",
    ]
    fake_ips.add("get", "/core/api/measureUnits/quantityGuids", body=guids)
    async with IPSClient(config=token_config) as ips:
        result = await ips.measure_unit_quantity_guids()

    assert result == guids
