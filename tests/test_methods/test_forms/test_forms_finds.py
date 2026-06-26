"""Тесты форменных поисков (find*) раздела forms — чтение через POST.

Проверяют путь эндпоинта, сериализацию тела запроса (по алиасам camelCase,
голый ``list[int]`` для коллекций по версиям) и распаковку голого массива ответа
в соответствующие DTO. Все методы используют HTTP POST, но являются чтениями.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.forms.find_collection_options import FindCollectionOptions
from aioips.schemas.forms.ids_find_users_request import Ids4FindUsersRequest
from aioips.schemas.forms.version_id_and_columns_request import (
    VersionIdAndColumns4Request,
)

_Client = IPSClient


_FORM_OBJECT = {
    "id": 102551,
    "versionID": 102551,
    "typeID": 1742,
    "caption": "Деталь 550.07.305",
    "versionGuid": "99999999-8888-7777-6666-555555555555",
    "readOnly": False,
    "attributes": [{"attributeID": 1029, "name": "Архив", "asString": "ИОТТ"}],
}
_USER = {"id": 7001, "versionID": 7001, "typeID": 1040, "caption": "Иванов И.И."}
_GROUP = {"id": 5001, "versionID": 5002, "typeID": 1041, "caption": "Конструкторы"}
_RANK = {"id": 8001, "versionID": 8001, "typeID": 1043, "caption": "Утверждающий"}


def _config(fake_ips: FakeIPS) -> IPSConfig:
    return IPSConfig(
        base_url=fake_ips.base_url,
        access_token="test-token",
        retry_min_wait=0.01,
        retry_max_wait=0.02,
        _env_file=None,
    )


async def test_forms_find_applicability(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findApplicability"
    fake_ips.add("post", path, body=[_FORM_OBJECT])
    options = FindCollectionOptions(object_type_id=1742, object_version_id=102551)
    async with _Client(config=_config(fake_ips)) as ips:
        objects = await ips.find_applicability(options)

    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.method == "POST"
    # Тело сериализовано по алиасам camelCase (плюс пустые списки-дефолты).
    assert {"objectTypeID": 1742, "objectVersionID": 102551}.items() <= req.body.items()
    assert len(objects) == 1
    assert objects[0].id == 102551
    assert objects[0].caption == "Деталь 550.07.305"
    assert objects[0].attributes[0]["attributeID"] == 1029


async def test_forms_find_collection(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findCollection"
    fake_ips.add("post", path, body=[_FORM_OBJECT, _FORM_OBJECT])
    options = FindCollectionOptions(object_type_id=1742, page=0, page_size=50)
    async with _Client(config=_config(fake_ips)) as ips:
        objects = await ips.find_collection(options)

    req = fake_ips.requests[-1]
    assert req.path == path
    assert {"objectTypeID": 1742, "page": 0, "pageSize": 50}.items() <= req.body.items()
    assert len(objects) == 2


async def test_forms_find_composition(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findComposition"
    fake_ips.add("post", path, body=[_FORM_OBJECT])
    options = FindCollectionOptions(object_version_id=102551)
    async with _Client(config=_config(fake_ips)) as ips:
        objects = await ips.find_composition(options)

    req = fake_ips.requests[-1]
    assert req.path == path
    assert {"objectVersionID": 102551}.items() <= req.body.items()
    assert objects[0].version_id == 102551


async def test_forms_find_composition_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findComposition"
    fake_ips.add("post", path, body=None)
    async with _Client(config=_config(fake_ips)) as ips:
        objects = await ips.find_composition(FindCollectionOptions())

    assert objects == []


async def test_forms_find_objects_list(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findObjectsList"
    fake_ips.add("post", path, body=[_FORM_OBJECT])
    request = VersionIdAndColumns4Request(object_version_ids=[102550, 102551], use_version_id=True)
    async with _Client(config=_config(fake_ips)) as ips:
        objects = await ips.find_objects_list(request)

    req = fake_ips.requests[-1]
    assert req.path == path
    assert {
        "objectVersionIds": [102550, 102551],
        "useVersionId": True,
    }.items() <= req.body.items()
    assert objects[0].type_id == 1742


async def test_forms_find_users(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/findUsers"
    fake_ips.add("post", path, body=[_USER])
    request = Ids4FindUsersRequest(user_group_version_ids=[5002], rank_version_ids=[8001])
    async with _Client(config=_config(fake_ips)) as ips:
        users = await ips.find_users(request)

    req = fake_ips.requests[-1]
    assert req.path == path
    assert {
        "userGroupVersionIds": [5002],
        "rankVersionIds": [8001],
    }.items() <= req.body.items()
    assert users[0].id == 7001
    assert users[0].caption == "Иванов И.И."


async def test_forms_rank_find_collection(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/rankFindCollection"
    fake_ips.add("post", path, body=[_RANK])
    async with _Client(config=_config(fake_ips)) as ips:
        ranks = await ips.rank_find_collection([8001, 8002])

    req = fake_ips.requests[-1]
    assert req.path == path
    # Тело — голый JSON-массив int.
    assert req.body == [8001, 8002]
    assert ranks[0].id == 8001
    assert ranks[0].caption == "Утверждающий"


async def test_forms_user_find_collection(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/userFindCollection"
    fake_ips.add("post", path, body=[_USER, _USER])
    async with _Client(config=_config(fake_ips)) as ips:
        users = await ips.user_find_collection([7001, 7002])

    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == [7001, 7002]
    assert len(users) == 2
    assert users[0].caption == "Иванов И.И."


async def test_forms_user_group_find_collection(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/userGroupFindCollection"
    fake_ips.add("post", path, body=[_GROUP])
    async with _Client(config=_config(fake_ips)) as ips:
        groups = await ips.user_group_find_collection([5001])

    req = fake_ips.requests[-1]
    assert req.path == path
    assert req.body == [5001]
    assert groups[0].id == 5001
    assert groups[0].caption == "Конструкторы"
