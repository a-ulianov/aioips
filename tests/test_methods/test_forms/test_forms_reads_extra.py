"""Тесты дополнительных методов чтения раздела форм (forms).

Проверяют новые read-методы: точные ключи JSON новых DTO, разворачивание
``WidgetDtoNullableResultDto`` в :meth:`form`, корректные пути эндпоинтов и
строковый ответ :meth:`image_for_widget`.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


_GROUP = {"id": 5001, "versionID": 5002, "typeID": 1041, "caption": "Конструкторы"}
_USER = {"id": 7001, "versionID": 7001, "typeID": 1040, "caption": "Иванов И.И."}
_COLOR = {"colorName": "Синий", "colorRGBA": "#0000FFFF", "a": 255, "r": 0, "g": 0, "b": 255}
_COLUMN = {
    "attrInfo": {"id": 1029, "name": "Архив"},
    "uiInfo": {"width": 120, "caption": "Архив"},
    "order": {"index": 0, "ascending": True},
    "scheme": "default",
    "attrType": "ftObjectLink",
    "isCustom": True,
    "isVirtual": False,
}
_SUBJECT_AREA = {
    "guid": "11111111-2222-3333-4444-555555555555",
    "name": "Конструкторская документация",
    "note": "КД",
    "symbol": "KD",
}
_WIDGET = {
    "id": "w-root",
    "name": "MainForm",
    "widgetType": "Form",
    "attributeTypeId": 1029,
    "attributeGuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "attributeName": "Архив",
    "text": "Заголовок",
    "hint": "подсказка",
    "visible": True,
    "disabledInDesign": False,
    "widgets": [{"id": "w-child", "name": "Label"}],
    "columnCollection": [_COLUMN],
}
_QUICK = {
    "id": 9002,
    "objectID": 9001,
    "objectTypeID": 1742,
    "versionGuid": "99999999-8888-7777-6666-555555555555",
    "caption": "Форма карточки",
}


def _config(fake_ips: FakeIPS) -> IPSConfig:
    return IPSConfig(
        base_url=fake_ips.base_url,
        access_token="test-token",
        retry_min_wait=0.01,
        retry_max_wait=0.02,
        _env_file=None,
    )


async def test_find_user_groups_and_users_in_composition(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    path = "/core/api/forms/findUserGroupsAndUsersInComposition"
    fake_ips.add("get", path, body={"userGroups": [_GROUP], "users": [_USER]})
    async with _Client(config=_config(fake_ips)) as ips:
        result = await ips.find_user_groups_and_users_in_composition(102551)

    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].query["versionId"] == "102551"
    assert result.user_groups[0].id == 5001
    assert result.users[0].id == 7001


async def test_user_group_find_roots(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/userGroupFindRoots"
    fake_ips.add("get", path, body=[_GROUP, _GROUP])
    async with _Client(config=_config(fake_ips)) as ips:
        roots = await ips.user_group_find_roots()

    assert fake_ips.requests[-1].path == path
    assert len(roots) == 2
    assert roots[0].caption == "Конструкторы"


async def test_default_columns_for_widget(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getDefaultColumns4Widget"
    fake_ips.add("get", path, body=[_COLUMN])
    async with _Client(config=_config(fake_ips)) as ips:
        columns = await ips.default_columns_for_widget()

    assert fake_ips.requests[-1].path == path
    assert len(columns) == 1
    col = columns[0]
    assert col.attr_info == {"id": 1029, "name": "Архив"}
    assert col.ui_info["width"] == 120
    assert col.order == {"index": 0, "ascending": True}
    assert col.scheme == "default"
    assert col.attr_type == "ftObjectLink"
    assert col.is_custom is True
    assert col.is_virtual is False


async def test_default_widget_colors(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getDefaultWidgetColors"
    fake_ips.add("get", path, body=[_COLOR])
    async with _Client(config=_config(fake_ips)) as ips:
        colors = await ips.default_widget_colors()

    assert fake_ips.requests[-1].path == path
    assert colors[0].color_name == "Синий"
    assert colors[0].b == 255


async def test_image_for_widget_returns_string(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getImage4Widget"
    fake_ips.add("get", path, body="data:image/png;base64,AAAA")
    async with _Client(config=_config(fake_ips)) as ips:
        image = await ips.image_for_widget(102551)

    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].query["versionId"] == "102551"
    assert image == "data:image/png;base64,AAAA"


async def test_image_for_widget_none_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/getImage4Widget"
    fake_ips.add("get", path, body=None)
    async with _Client(config=_config(fake_ips)) as ips:
        image = await ips.image_for_widget(102551)

    assert image == ""


async def test_subject_area_find_collection(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/subjectAreaFindCollection"
    fake_ips.add("get", path, body=[_SUBJECT_AREA])
    async with _Client(config=_config(fake_ips)) as ips:
        areas = await ips.subject_area_find_collection()

    assert fake_ips.requests[-1].path == path
    area = areas[0]
    assert str(area.guid) == "11111111-2222-3333-4444-555555555555"
    assert area.name == "Конструкторская документация"
    assert area.note == "КД"
    assert area.symbol == "KD"


async def test_form_unwraps_present_entity(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/102551"
    fake_ips.add("get", path, body={"entity": _WIDGET, "isEntityPresent": True})
    async with _Client(config=_config(fake_ips)) as ips:
        form = await ips.form(102551)

    assert fake_ips.requests[-1].path == path
    assert form is not None
    assert form.id == "w-root"
    assert form.name == "MainForm"
    assert form.widget_type == "Form"
    assert form.attribute_type_id == 1029
    assert form.attribute_name == "Архив"
    assert form.visible is True
    assert len(form.widgets) == 1
    assert form.widgets[0]["id"] == "w-child"
    assert len(form.column_collection) == 1
    # Полный сырой JSON сохранён в properties (включая нетипизированные поля).
    assert form.properties["widgetType"] == "Form"


async def test_form_returns_none_when_absent(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/777"
    fake_ips.add("get", path, body={"entity": None, "isEntityPresent": False})
    async with _Client(config=_config(fake_ips)) as ips:
        form = await ips.form(777)

    assert form is None


async def test_forms_for_uses_forms_for_path(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/102551/formsFor"
    fake_ips.add("get", path, body=[_QUICK])
    async with _Client(config=_config(fake_ips)) as ips:
        forms = await ips.forms_for(102551, is_create_object=True, is_relation=False)

    assert fake_ips.requests[-1].path == path
    assert fake_ips.requests[-1].query["isCreateObject"] == "true"
    assert fake_ips.requests[-1].query["isRelation"] == "false"
    assert forms[0].id == 9002
    assert forms[0].object_id == 9001
    assert forms[0].caption == "Форма карточки"


async def test_form_related_object_type_guids(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/102551/relatedObjectTypeGuidsForForm"
    fake_ips.add("get", path, body=["guid-a", "guid-b"])
    async with _Client(config=_config(fake_ips)) as ips:
        guids = await ips.form_related_object_type_guids(102551)

    assert fake_ips.requests[-1].path == path
    assert guids == ["guid-a", "guid-b"]


async def test_form_related_relation_type_guids(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/forms/102551/relatedRelationTypeGuidsForForm"
    fake_ips.add("get", path, body=["rel-1"])
    async with _Client(config=_config(fake_ips)) as ips:
        guids = await ips.form_related_relation_type_guids(102551)

    assert fake_ips.requests[-1].path == path
    assert guids == ["rel-1"]
