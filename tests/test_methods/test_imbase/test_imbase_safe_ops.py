"""Тесты безопасных операций IMBASE: конвертеры, резолверы имён, избранное, mix."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


# --- конвертеры (тело — JSON-строка) ---------------------------------------


async def test_rtf_to_plain_text_sends_json_string(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/imbase/object/converter/rtfToPlainText",
        body="Ребро жёсткости",
    )
    async with _Client(config=token_config) as ips:
        text = await ips.imbase_rtf_to_plain_text(r"{\rtf1 Ребро жёсткости}")

    assert text == "Ребро жёсткости"
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/imbase/object/converter/rtfToPlainText"
    # тело должно быть сериализовано как голая JSON-строка, а не объект/массив
    assert req.body == r"{\rtf1 Ребро жёсткости}"
    assert isinstance(req.body, str)


async def test_rtf_to_plain_text_coerces_non_str(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/imbase/object/converter/rtfToPlainText",
        body=123,
    )
    async with _Client(config=token_config) as ips:
        text = await ips.imbase_rtf_to_plain_text("x")

    assert text == "123"


async def test_rtf_to_svg_width_in_path_and_json_string_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/imbase/object/converter/rtfToSvg/240",
        body="PHN2Zz4=",
    )
    async with _Client(config=token_config) as ips:
        svg = await ips.imbase_rtf_to_svg(r"{\rtf1 H2O}", 240)

    assert svg == "PHN2Zz4="
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/imbase/object/converter/rtfToSvg/240"
    assert req.body == r"{\rtf1 H2O}"
    assert isinstance(req.body, str)


# --- резолверы имён (тело — list[str], ответ — dict[str, str]) --------------


async def test_object_references_names_sends_list_and_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    mapping = {"@102550": "Ребро", "@102551": "Полка"}
    fake_ips.add("post", "/core/api/imbase/objectReferencesNames", body=mapping)
    async with _Client(config=token_config) as ips:
        names = await ips.imbase_object_references_names(["@102550", "@102551"])

    assert names == mapping
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.body == ["@102550", "@102551"]


async def test_object_references_names_coerces_non_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/imbase/objectReferencesNames", body=[1, 2])
    async with _Client(config=token_config) as ips:
        names = await ips.imbase_object_references_names(["x"])

    assert names == {}


async def test_object_by_id_references_names_returns_dict(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    mapping = {"#7": "Версия A"}
    fake_ips.add("post", "/core/api/imbase/objectByIdReferencesNames", body=mapping)
    async with _Client(config=token_config) as ips:
        names = await ips.imbase_object_by_id_references_names(["#7"])

    assert names == mapping
    assert fake_ips.requests[-1].body == ["#7"]


async def test_record_references_names_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    mapping = {"r:1001": "Запись 1"}
    fake_ips.add("post", "/core/api/imbase/recordReferencesNames", body=mapping)
    async with _Client(config=token_config) as ips:
        names = await ips.imbase_record_references_names(["r:1001"])

    assert names == mapping
    assert fake_ips.requests[-1].body == ["r:1001"]


# --- favorites: обратимая пара add / remove --------------------------------


async def test_add_to_favorite_folder_path_and_no_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/imbase/favorites/12/add/102550",
        body={"objectId": 102550, "relationId": 9001},
    )
    async with _Client(config=token_config) as ips:
        fav = await ips.imbase_add_to_favorite_folder(12, 102550)

    assert fav.object_id == 102550
    assert fav.relation_id == 9001
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/imbase/favorites/12/add/102550"
    # Параметры в пути; тело — пустой ``{}`` (нужен для Content-Type, иначе 415).
    assert req.body == {}


async def test_add_to_favorite_folder_null_response(token_config: IPSConfig, fake_ips: FakeIPS):
    # Прод отдаёт ``null`` при успехе — метод возвращает None, а не падает.
    fake_ips.add("post", "/core/api/imbase/favorites/12/add/102550", body=None)
    async with _Client(config=token_config) as ips:
        fav = await ips.imbase_add_to_favorite_folder(12, 102550)
    assert fav is None


async def test_remove_from_favorites_returns_none_void(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/imbase/favorites/12/remove/102550", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.imbase_remove_from_favorites(12, 102550)

    assert result is None
    req = fake_ips.requests[-1]
    assert req.path == "/core/api/imbase/favorites/12/remove/102550"
    assert req.body == {}


async def test_favorites_add_remove_are_reversible_pair(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/imbase/favorites/12/add/102550",
        body={"objectId": 102550, "relationId": 9001},
    )
    fake_ips.add("post", "/core/api/imbase/favorites/12/remove/102550", body=None)
    async with _Client(config=token_config) as ips:
        await ips.imbase_add_to_favorite_folder(12, 102550)
        await ips.imbase_remove_from_favorites(12, 102550)

    paths = [r.path for r in fake_ips.requests if r.method == "POST"]
    assert paths == [
        "/core/api/imbase/favorites/12/add/102550",
        "/core/api/imbase/favorites/12/remove/102550",
    ]


# --- tableMix (без тела) ----------------------------------------------------


async def test_table_mix_data_returns_dto(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {
        "receptures": {"1": "Рецептура 1"},
        "components": {"1": [{"keyId": "k1", "title": "Компонент", "displayedValue": "10 кг"}]},
    }
    fake_ips.add("post", "/core/api/imbase/tableMix/102550/data", body=body)
    async with _Client(config=token_config) as ips:
        mix = await ips.imbase_table_mix_data(102550)

    assert mix.receptures == {"1": "Рецептура 1"}
    assert mix.components["1"][0].key_id == "k1"
    assert mix.components["1"][0].displayed_value == "10 кг"
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == "/core/api/imbase/tableMix/102550/data"
    assert req.body == {}


async def test_table_mix_data_handles_null_components(token_config: IPSConfig, fake_ips: FakeIPS):
    body = {"receptures": {}, "components": None}
    fake_ips.add("post", "/core/api/imbase/tableMix/102550/data", body=body)
    async with _Client(config=token_config) as ips:
        mix = await ips.imbase_table_mix_data(102550)

    assert mix.components == {}
