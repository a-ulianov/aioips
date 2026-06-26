"""Тесты keyset-пагинатора objects_select_iter."""

from typing import Any

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient
SEL = "/core/api/objects/select"


def _obj(oid: int) -> dict[str, Any]:
    return {"objectId": oid, "attributes": []}


async def test_iter_paginates_with_keyset(token_config: IPSConfig, fake_ips: FakeIPS):
    # 3 страницы по page_size=2; последняя короче → стоп
    fake_ips.add("post", SEL, body=[_obj(1), _obj(2)])
    fake_ips.add("post", SEL, body=[_obj(3), _obj(4)])
    fake_ips.add("post", SEL, body=[_obj(5)])
    ids = []
    async with _Client(config=token_config) as ips:
        async for obj in ips.objects_select_iter(1742, page_size=2):
            ids.append(obj.object_id)
    assert ids == [1, 2, 3, 4, 5]
    reqs = [r for r in fake_ips.requests if r.path == SEL]
    assert len(reqs) == 3
    assert "lastKeyValue" not in reqs[0].body  # первая страница без курсора
    assert reqs[1].body["lastKeyValue"] == 2  # курсор = object_id последней записи
    assert reqs[2].body["lastKeyValue"] == 4
    assert all(r.body["recordCount"] == 2 for r in reqs)


async def test_iter_single_short_page_stops(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SEL, body=[_obj(1)])
    async with _Client(config=token_config) as ips:
        ids = [o.object_id async for o in ips.objects_select_iter(1742, page_size=10)]
    assert ids == [1]
    assert len([r for r in fake_ips.requests if r.path == SEL]) == 1


async def test_iter_empty_result(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", SEL, body=[])
    async with _Client(config=token_config) as ips:
        ids = [o.object_id async for o in ips.objects_select_iter(1742, page_size=10)]
    assert ids == []
