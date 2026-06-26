"""Тесты мутирующих методов справочника IMBASE и поиска с прогресс-стримом.

Проверяют: confirm-гейты (мутации не делают запрос без ``confirm=True``), путь,
тело/query и распаковку ответа (int / dict / void) на поддельном сервере.
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.imbase.table_search_params import ImBaseTableSearchParams

_Client = IPSClient


async def test_imbase_create_object_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.imbase_create_object(204)
    assert fake_ips.requests == []


async def test_imbase_create_object_returns_bare_int(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/imbase/object/byBase/204", body=102550)
    async with _Client(config=token_config) as ips:
        object_id = await ips.imbase_create_object(
            204, record_id=1042, commit_creation=True, need_type=3, confirm=True
        )

    assert object_id == 102550
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/imbase/object/byBase/204"
    assert request.body == {}
    assert request.query == {"recordId": "1042", "commitCreation": "true", "needType": "3"}


async def test_imbase_create_object_non_int_returns_zero(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/imbase/object/byBase/204", body={"unexpected": True})
    async with _Client(config=token_config) as ips:
        object_id = await ips.imbase_create_object(204, confirm=True)

    assert object_id == 0
    assert fake_ips.requests[-1].query == {}


async def test_imbase_add_from_im_base_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.imbase_add_from_im_base({"baseId": 204})
    assert fake_ips.requests == []


async def test_imbase_add_from_im_base_posts_body(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"objectId": 102550, "relationId": 9001}
    fake_ips.add("post", "/core/api/imbase/object/composition", body=body)
    payload = {"projObjectId": 1, "projObjectTypeId": 3, "baseId": 204, "recordId": 1042}
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_add_from_im_base(payload, confirm=True)

    assert result == body
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/imbase/object/composition"
    assert request.body == payload


async def test_imbase_add_from_im_base_non_dict_returns_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/imbase/object/composition", body=[1, 2, 3])
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_add_from_im_base({"baseId": 204}, confirm=True)

    assert result == {}


async def test_imbase_fill_object_attributes_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.imbase_fill_object_attributes(102550)
    assert fake_ips.requests == []


async def test_imbase_fill_object_attributes_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/imbase/object/102550/fillObjectAttributes",
        body=None,
    )
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_fill_object_attributes(
            102550, object_type_id=3, base_id=204, record_id=1042, confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/imbase/object/102550/fillObjectAttributes"
    assert request.body == {}
    assert request.query == {"objectTypeId": "3", "baseId": "204", "recordId": "1042"}


async def test_imbase_find_in_tables_with_progress_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/imbase/find/inTables/withProgress", body=None)
    params = ImBaseTableSearchParams(table_links_lookup={"204": [1, 2, 3]})
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_find_in_tables_with_progress(params, progress_report_step=25)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/imbase/find/inTables/withProgress"
    assert request.body == {"tableLinksLookup": {"204": [1, 2, 3]}, "conditions": []}
    assert request.query == {"progressReportStep": "25"}


async def test_imbase_existing_values_with_progress_void(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    guid = "8f3c2a10-0000-0000-0000-000000000000"
    path = f"/core/api/imbase/attribute/byGuid/{guid}/existingValues/withProgress"
    fake_ips.add("post", path, body=None)
    params = ImBaseTableSearchParams(table_links_lookup={"204": [1, 2]})
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_get_table_search_existing_attribute_values_with_progress(
            guid, params
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.path == path
    assert request.body == {"tableLinksLookup": {"204": [1, 2]}, "conditions": []}
    assert request.query == {}
