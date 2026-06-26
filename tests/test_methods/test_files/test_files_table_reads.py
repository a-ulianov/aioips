"""Тесты табличных методов-выборок раздела файлов (POST-verb, чтение).

Проверяют путь, тело и распаковку ``DataTableDto`` / дерева
``ObjectFilesTreeNodeDto`` для методов выборки метаданных о файлах vault.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient as _Client
from aioips import IPSConfig
from aioips.schemas.files.files_table_params import (
    ObjectIdsWithColumnsDto,
    ObjectIdsWithColumnsFileNameDto,
    ObjectSnapshotIds,
)

_TABLE = {
    "columns": ["FileName", "BlobId"],
    "rows": [["schema.pdf", 778899], ["draft.pdf", 778900]],
}


async def test_get_file_name_table_path_query_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getFileNameTable", body=_TABLE)
    async with _Client(config=token_config) as ips:
        table = await ips.get_file_name_table(file_name="schema.pdf")

    assert table.columns == ["FileName", "BlobId"]
    assert table.rows[0] == ["schema.pdf", 778899]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFileNameTable"
    assert request.method == "POST"
    assert request.body == {}
    assert request.query == {"fileName": "schema.pdf"}


async def test_get_file_name_table_null_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getFileNameTable",
        body={"columns": None, "rows": None},
    )
    async with _Client(config=token_config) as ips:
        table = await ips.get_file_name_table()

    assert table.columns == []
    assert table.rows == []
    assert fake_ips.requests[-1].query == {}


async def test_get_file_names_table_list_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getFileNamesTable", body=_TABLE)
    async with _Client(config=token_config) as ips:
        table = await ips.get_file_names_table(["schema.pdf", "draft.pdf"])

    assert table.columns == ["FileName", "BlobId"]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFileNamesTable"
    assert request.body == ["schema.pdf", "draft.pdf"]


async def test_get_files_table_list_int_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getFilesTable", body=_TABLE)
    async with _Client(config=token_config) as ips:
        table = await ips.get_files_table([778899, 778900])

    assert len(table.rows) == 2
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFilesTable"
    assert request.body == [778899, 778900]


async def test_get_files_table_non_dict_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/files/fileNamesService/getFilesTable", body=None)
    async with _Client(config=token_config) as ips:
        table = await ips.get_files_table([1])

    assert table.columns == []
    assert table.rows == []


async def test_get_files_table_by_fields_schema_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getFilesTableByFields",
        body=_TABLE,
    )
    async with _Client(config=token_config) as ips:
        table = await ips.get_files_table_by_fields(
            ObjectIdsWithColumnsDto(object_ids=[102550], column_names=["FileName", "BlobId"])
        )

    assert table.columns == ["FileName", "BlobId"]
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFilesTableByFields"
    assert request.body == {
        "objectIds": [102550],
        "columnNames": ["FileName", "BlobId"],
    }


async def test_get_files_table_by_fields_dict_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getFilesTableByFields",
        body=_TABLE,
    )
    async with _Client(config=token_config) as ips:
        await ips.get_files_table_by_fields({"objectIds": [1], "columnNames": []})

    assert fake_ips.requests[-1].body == {"objectIds": [1], "columnNames": []}


async def test_get_files_table_all_attributes_schema_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getFilesTableAllAttributes",
        body=_TABLE,
    )
    async with _Client(config=token_config) as ips:
        await ips.get_files_table_all_attributes(
            ObjectIdsWithColumnsFileNameDto(object_ids=[102550], file_name="schema.pdf")
        )

    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFilesTableAllAttributes"
    assert request.body["fileName"] == "schema.pdf"
    assert request.body["objectIds"] == [102550]


async def test_get_files_table_with_snapshot_ids_schema_body(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add(
        "post",
        "/core/api/files/fileNamesService/getFilesTableWithSnapshotIds",
        body=_TABLE,
    )
    async with _Client(config=token_config) as ips:
        await ips.get_files_table_with_snapshot_ids(
            ObjectSnapshotIds(object_ids=[102550], snapshot_ids=[5])
        )

    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/fileNamesService/getFilesTableWithSnapshotIds"
    assert request.body == {"objectIds": [102550], "snapshotIds": [5]}


async def test_check_unique_file_names_path_and_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/778899/checkUniqueFileNames",
        body=[
            {
                "originalFileName": "schema.pdf",
                "recommendedFileName": "schema(1).pdf",
                "isOriginalFileNameUnique": False,
            }
        ],
    )
    async with _Client(config=token_config) as ips:
        results = await ips.check_unique_file_names(778899, ["schema.pdf"])

    assert results[0]["isOriginalFileNameUnique"] is False
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/778899/checkUniqueFileNames"
    assert request.method == "POST"
    assert request.body == ["schema.pdf"]


async def test_check_unique_file_names_non_list_to_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/files/1/checkUniqueFileNames", body={"x": 1})
    async with _Client(config=token_config) as ips:
        results = await ips.check_unique_file_names(1, [])

    assert results == []


async def test_object_files_with_composition_tree(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/objects/102550/withComposition",
        body={
            "objectId": 102550,
            "caption": "Сборка",
            "fileInfoCollection": [{"blobId": 778899, "fileName": "schema.pdf"}],
            "childNodes": [
                {
                    "objectId": 102551,
                    "caption": "Деталь",
                    "fileInfoCollection": None,
                    "childNodes": None,
                }
            ],
        },
    )
    async with _Client(config=token_config) as ips:
        tree = await ips.object_files_with_composition(102550)

    assert tree.object_id == 102550
    assert tree.caption == "Сборка"
    assert tree.file_info_collection[0]["blobId"] == 778899
    assert tree.child_nodes[0].object_id == 102551
    assert tree.child_nodes[0].file_info_collection == []
    assert tree.child_nodes[0].child_nodes == []
    request = fake_ips.requests[-1]
    assert request.path == "/core/api/files/objects/102550/withComposition"
    assert request.body == {}


async def test_object_files_with_composition_dict_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/files/objects/1/withComposition",
        body={"objectId": 1},
    )
    async with _Client(config=token_config) as ips:
        await ips.object_files_with_composition(1, {"contextRule": {"versionRuleObjectId": 7}})

    assert fake_ips.requests[-1].body == {"contextRule": {"versionRuleObjectId": 7}}
