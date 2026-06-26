"""Тесты метода разрешения сборочного состава в imv-данные (POST-чтение)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.imviewer.assembly_composition import (
    SourceAssemblyCompositionTreeNode,
)

_Client = IPSClient

_PATH = "/core/api/imviewer/assemblyComposition"

_RESPONSE = {
    "sourceObjectId": 102550,
    "sourceObjectCaption": "Сборка 550",
    "objectStatus": "actual",
    "objectId": 900001,
    "blobId": 778899,
    "fileName": "asm_550.imv",
    "childNodes": [
        {
            "sourceObjectId": 102551,
            "sourceObjectCaption": "Ребро",
            "objectStatus": "outdated",
            "objectId": 900002,
            "blobId": 778900,
            "fileName": "part_rib.imv",
            "childNodes": None,
        }
    ],
}


async def test_assembly_composition_posts_tree_and_unpacks(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", _PATH, body=_RESPONSE)
    root = SourceAssemblyCompositionTreeNode(
        object_id=102550,
        caption="Сборка 550",
        child_nodes=[
            SourceAssemblyCompositionTreeNode(object_id=102551, caption="Ребро"),
        ],
    )

    async with _Client(config=token_config) as ips:
        tree = await ips.imviewer_assembly_composition(root)

    # распаковка ответа (рекурсивно)
    assert tree.source_object_id == 102550
    assert tree.object_status == "actual"
    assert tree.blob_id == 778899
    assert tree.file_name == "asm_550.imv"
    assert len(tree.child_nodes) == 1
    child = tree.child_nodes[0]
    assert child.source_object_caption == "Ребро"
    assert child.object_status == "outdated"
    # childNodes=None нормализуется в пустой список
    assert child.child_nodes == []

    # тело запроса: путь, метод, рекурсивная сериализация с camelCase
    req = fake_ips.requests[-1]
    assert req.method == "POST"
    assert req.path == _PATH
    assert req.body == {
        "objectId": 102550,
        "caption": "Сборка 550",
        "childNodes": [
            {"objectId": 102551, "caption": "Ребро", "childNodes": []},
        ],
    }


async def test_assembly_composition_non_dict_response(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", _PATH, body=None)
    root = SourceAssemblyCompositionTreeNode(object_id=1, caption="root")

    async with _Client(config=token_config) as ips:
        tree = await ips.imviewer_assembly_composition(root)

    assert tree.source_object_id == 0
    assert tree.child_nodes == []
