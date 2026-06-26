"""Тесты скалярных методов контекста редактирования и замещения раздела metadata.

Проверяют построение пути запроса и преобразование возврата (bool / list[int] /
list[str]) для каждого метода editingContext и substitution. Для byGuid-методов
дополнительно подтверждается, что GUID попадает в путь запроса.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_GUID = "11111111-2222-3333-4444-555555555555"


# --- editingContext: списки -------------------------------------------------


async def test_editing_context_object_type_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/objectTypes/ids", body=[1, 2, 42])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.editing_context_object_type_ids()

    assert ids == [1, 2, 42]
    assert all(isinstance(i, int) for i in ids)


async def test_editing_context_object_type_ids_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/objectTypes/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        ids = await ips.editing_context_object_type_ids()

    assert ids == []


async def test_editing_context_object_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/objectTypes/guids", body=[_GUID, _GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.editing_context_object_type_guids()

    assert guids == [_GUID, _GUID]
    assert all(isinstance(g, str) for g in guids)


async def test_editing_context_top_object_type_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/topObjectTypes/ids", body=[42])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.editing_context_top_object_type_ids()

    assert ids == [42]


async def test_editing_context_top_object_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/topObjectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.editing_context_top_object_type_guids()

    assert guids == [_GUID]


# --- editingContext: булевы -------------------------------------------------


async def test_is_editing_context_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/editingContext/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_editing_context(42)

    assert result is True
    assert fake_ips.requests[-1].path == "/core/api/metadata/editingContext/42/exists"


async def test_is_editing_context_false_when_null(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/editingContext/999/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_editing_context(999)

    assert result is False


async def test_is_editing_context_by_guid_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", f"/core/api/metadata/editingContext/byGuid/{_GUID}/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_editing_context_by_guid(_GUID)

    assert result is True
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/editingContext/byGuid/{_GUID}/exists"
    )


async def test_can_add_object_type_to_editing_context_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/editingContext/canAddObjectType/42", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.can_add_object_type_to_editing_context(42)

    assert result is True


async def test_can_add_object_type_to_editing_context_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/editingContext/canAddObjectType/byGuid/{_GUID}",
        body=False,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.can_add_object_type_to_editing_context_by_guid(_GUID)

    assert result is False
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/editingContext/canAddObjectType/byGuid/{_GUID}"
    )


async def test_is_simple_editing_context_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/editingContext/isSimple/42", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_simple_editing_context(42)

    assert result is True


async def test_must_append_object_version_returns_bool(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/editingContext/mustAppendObjectVersion/42", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.must_append_object_version(42)

    assert result is True


# --- substitution: списки ---------------------------------------------------


async def test_substitute_object_type_ids_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/metadata/substitution/objectTypes/ids", body=[1, 42])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.substitute_object_type_ids()

    assert ids == [1, 42]
    assert all(isinstance(i, int) for i in ids)


async def test_substitute_object_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/objectTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.substitute_object_type_guids()

    assert guids == [_GUID]
    assert all(isinstance(g, str) for g in guids)


async def test_substitute_object_type_ids_empty_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/objectTypes/ids", body=None)
    async with IPSClient(config=token_config) as ips:
        ids = await ips.substitute_object_type_ids()

    assert ids == []


async def test_object_type_has_substitution_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/objectTypes/42/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_has_substitution(42)

    assert result is True


async def test_object_type_has_substitution_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/substitution/objectTypes/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.object_type_has_substitution_by_guid(_GUID)

    assert result is True
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/substitution/objectTypes/byGuid/{_GUID}/exists"
    )


async def test_substitute_relation_type_ids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/relationTypes/ids", body=[7, 8])
    async with IPSClient(config=token_config) as ips:
        ids = await ips.substitute_relation_type_ids()

    assert ids == [7, 8]


async def test_substitute_relation_type_guids_returns_list(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/relationTypes/guids", body=[_GUID])
    async with IPSClient(config=token_config) as ips:
        guids = await ips.substitute_relation_type_guids()

    assert guids == [_GUID]


async def test_relation_type_has_substitutes_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/relationTypes/7/exists", body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_type_has_substitutes(7)

    assert result is True


async def test_relation_type_has_substitutes_false_when_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("get", "/core/api/metadata/substitution/relationTypes/7/exists", body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_type_has_substitutes(7)

    assert result is False


async def test_relation_type_has_substitutes_by_guid_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "get",
        f"/core/api/metadata/substitution/relationTypes/byGuid/{_GUID}/exists",
        body=True,
    )
    async with IPSClient(config=token_config) as ips:
        result = await ips.relation_type_has_substitutes_by_guid(_GUID)

    assert result is True
    assert fake_ips.requests[-1].path == (
        f"/core/api/metadata/substitution/relationTypes/byGuid/{_GUID}/exists"
    )
