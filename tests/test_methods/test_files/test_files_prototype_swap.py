"""Тесты мутаций раздела файлов: swap и назначение прототипов.

Покрывают четыре новых метода: :meth:`swap_object_files`,
:meth:`set_file_attr_prototype`, :meth:`set_prototype` (с ``confirm``-гейтами) и
:meth:`handle_file_attributes_for_object_creation` (подготовка без ``confirm``).
"""

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.files.prototype_info import PrototypeInfo
from aioips.schemas.files.swap_files import SwapFiles

_Client = IPSClient

_OBJECT_WITH_FILE_ATTRS: dict[str, object] = {
    "objectVersionId": 333444,
    "objectType": 17,
    "readOnly": False,
    "attributes": [
        {
            "attributeId": 1031,
            "attributeFieldType": "ftFile",
            "isMultiple": True,
            "fileInfoCollection": None,
            "readOnly": False,
        }
    ],
}


# --- swap_object_files -------------------------------------------------------


async def test_swap_object_files_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    body = SwapFiles(attribute_id=1031, blob_id=778899, old_position=0, change_position=1)
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.swap_object_files(-102550, body)

    # запрос к серверу не делался
    assert fake_ips.requests == []


async def test_swap_object_files_posts_json(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/objects/-102550/files/swap", body=None)
    body = SwapFiles(attribute_id=1031, blob_id=778899, old_position=0, change_position=1)
    async with _Client(config=token_config) as ips:
        result = await ips.swap_object_files(-102550, body, confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/files/objects/-102550/files/swap"
    assert request.body == {
        "oldPosition": 0,
        "attributeId": 1031,
        "blobId": 778899,
        "changePosition": 1,
    }


# --- set_file_attr_prototype -------------------------------------------------


async def test_set_file_attr_prototype_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.set_file_attr_prototype(-102550)

    assert fake_ips.requests == []


async def test_set_file_attr_prototype_posts_empty_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/objects/-102550/setFilePrototype", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.set_file_attr_prototype(-102550, confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/files/objects/-102550/setFilePrototype"
    # no-body POST отправляет {} (а не отсутствие тела)
    assert request.body == {}


# --- set_prototype -----------------------------------------------------------


async def test_set_prototype_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    proto = PrototypeInfo(prototype_id=42, name="Чертёж PDF", attribute_id=1031)
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.set_prototype(-102550, proto)

    assert fake_ips.requests == []


async def test_set_prototype_posts_json_and_returns_bool(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/files/setPrototype/-102550", body=True)
    proto = PrototypeInfo(prototype_id=42, name="Чертёж PDF", attribute_id=1031)
    async with _Client(config=token_config) as ips:
        result = await ips.set_prototype(-102550, proto, confirm=True)

    assert result is True
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/files/setPrototype/-102550"
    assert request.body == {"prototypeId": 42, "name": "Чертёж PDF", "attributeId": 1031}


async def test_set_prototype_excludes_none_attribute(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/setPrototype/-102550", body=False)
    proto = PrototypeInfo(prototype_id=42, name="Без атрибута")
    async with _Client(config=token_config) as ips:
        result = await ips.set_prototype(-102550, proto, confirm=True)

    assert result is False
    # attribute_id (None) исключён из тела
    assert fake_ips.requests[-1].body == {"prototypeId": 42, "name": "Без атрибута"}


# --- handle_file_attributes_for_object_creation (без confirm) ----------------


async def test_handle_file_attributes_for_object_creation_returns_dto(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/files/objectCreation/102550", body=_OBJECT_WITH_FILE_ATTRS)
    proto = PrototypeInfo(prototype_id=42, name="Чертёж PDF", attribute_id=1031)
    async with _Client(config=token_config) as ips:
        result = await ips.handle_file_attributes_for_object_creation(102550, proto)

    assert result.object_version_id == 333444
    assert len(result.attributes) == 1
    attr = result.attributes[0]
    assert attr.attribute_id == 1031
    assert attr.is_multiple is True
    # null fileInfoCollection нормализуется в пустой список
    assert attr.file_info_collection == []
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.path == "/core/api/files/objectCreation/102550"
    assert request.body == {"prototypeId": 42, "name": "Чертёж PDF", "attributeId": 1031}
