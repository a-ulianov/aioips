"""Тесты методов жизненного цикла объекта (создание/правка/удаление)."""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.objects import Attribute


async def test_object_create_unwraps_result(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects",
        body={
            "result": {"objectID": -123, "id": 5, "isCreationMode": True},
            "modificationsHistory": [],
        },
    )
    async with IPSClient(config=token_config) as ips:
        draft = await ips.object_create(1116, attributes=[Attribute(attribute_id=10, values=["x"])])
    assert draft.object_id == -123
    request = next(r for r in fake_ips.requests if r.path == "/core/api/objects")
    assert request.body["objectType"] == 1116
    assert request.body["attributes"][0]["attributeID"] == 10


async def test_object_commit_creation_returns_new_id(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/-123/commitCreation",
        body={"result": {"objectId": 777, "relatedObjectIds": []}, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        new_id = await ips.object_commit_creation(-123, related_object_ids=[10])
    assert new_id == 777
    req = next(r for r in fake_ips.requests if "commitCreation" in r.path)
    assert req.body["relatedObjectIds"] == [10]
    assert req.body["deleteOnException"] is True


async def test_object_check_out_returns_working_copy(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/777/checkOut",
        body={"result": -777, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        wc = await ips.object_check_out(777)
    assert wc == -777
    req = next(r for r in fake_ips.requests if "checkOut" in r.path)
    assert req.body == {}  # POST требует тело


async def test_object_check_in(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post", "/core/api/objects/-777/checkIn", body={"result": 778, "modificationsHistory": []}
    )
    async with IPSClient(config=token_config) as ips:
        res = await ips.object_check_in(-777)
    assert res == 778


async def test_object_save_changes(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/objects/-777/saveChanges",
        body={"result": None, "modificationsHistory": []},
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_save_changes(-777) is None


async def test_object_delete_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm"):
            await ips.object_delete(777)
    # без confirm запрос НЕ должен уходить
    assert all("delete" not in r.path for r in fake_ips.requests)


async def test_object_delete_with_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post", "/core/api/objects/777/delete", body={"result": 0, "modificationsHistory": []}
    )
    async with IPSClient(config=token_config) as ips:
        assert await ips.object_delete(777, confirm=True) == 0
    req = next(r for r in fake_ips.requests if r.path == "/core/api/objects/777/delete")
    assert req.body == {}
