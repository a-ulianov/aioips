"""Тесты методов чтения раздела поисковых схем (выборок)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.search_schemes import AttributeSourceType

_SCHEME = {
    "personal": True,
    "searchSchemaName": "Документы по архиву",
    "searchDirection": 1,
    "groupByVersions": False,
    "onlyActualVersions": True,
    "selector": 555,
    "versionRule": 2,
    "includeInProductionSeletor": False,
    "searchedObjectTypes": [570, 571],
    "expandCompositionObjectTypes": [570],
    "dontExpandCompositionObjectTypes": [],
    "relationTypes": [10, 11],
    "columns": [
        {"attribute": 1029, "width": 120, "source": "object"},
        {"attribute": 1030, "source": "relation"},
    ],
    "roles": [10, 20],
}


async def test_search_scheme_returns_scheme(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/core/api/searchSchemes/102550/getById", body=_SCHEME)
    async with IPSClient(config=token_config) as ips:
        scheme = await ips.search_scheme(102550)

    assert scheme.search_schema_name == "Документы по архиву"
    assert scheme.personal is True
    assert scheme.search_direction == 1
    assert scheme.only_actual_versions is True
    assert scheme.selector == 555
    assert scheme.version_rule == 2
    assert scheme.searched_object_types == [570, 571]
    assert scheme.expand_composition_object_types == [570]
    assert scheme.relation_types == [10, 11]
    assert scheme.roles == [10, 20]
    assert len(scheme.columns) == 2
    assert scheme.columns[0].attribute == 1029
    assert scheme.columns[0].width == 120
    assert scheme.columns[0].source is AttributeSourceType.OBJECT
    assert scheme.columns[1].width is None
    assert scheme.columns[1].source is AttributeSourceType.RELATION


async def test_search_scheme_coerces_null_lists(token_config: IPSConfig, fake_ips: FakeIPS):
    scheme = {
        **_SCHEME,
        "searchedObjectTypes": None,
        "columns": None,
        "roles": None,
        "relationTypes": None,
    }
    fake_ips.add("get", "/core/api/searchSchemes/1/getById", body=scheme)
    async with IPSClient(config=token_config) as ips:
        result = await ips.search_scheme(1)

    assert result.searched_object_types == []
    assert result.columns == []
    assert result.roles == []
    assert result.relation_types == []


async def test_condition_structure_info_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    body = [
        {"attributeId": 1029, "attributeSourceTypes": "object"},
        {"attributeId": 1030, "attributeSourceTypes": "relation"},
    ]
    fake_ips.add(
        "get",
        "/core/api/searchSchemes/1024/getConditionStructureInfo",
        body=body,
    )
    async with IPSClient(config=token_config) as ips:
        infos = await ips.condition_structure_info(1024)

    assert len(infos) == 2
    assert infos[0].attribute_id == 1029
    assert infos[0].attribute_source_types is AttributeSourceType.OBJECT
    assert infos[1].attribute_id == 1030
    assert infos[1].attribute_source_types is AttributeSourceType.RELATION
