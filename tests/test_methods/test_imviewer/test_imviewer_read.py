"""Тесты методов чтения раздела 3D-просмотрщика (ImViewer)."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_OBJECT_ID = 102550
_BLOB_ID = 778899

_MESH = {
    "metadata": {"name": "Ребро", "units": "mm"},
    "configInfo": {"current": "Default"},
    "bodies": [{"id": 1, "triangles": 128}, {"id": 2, "triangles": 64}],
}

_ASSEMBLY = {
    "metadata": {"name": "Сборка 550", "units": "mm"},
    "configInfo": {"current": "Default", "components": 12},
}


async def test_imviewer_mesh_returns_mesh(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/imviewer/mesh/{_OBJECT_ID}/{_BLOB_ID}"
    fake_ips.add("get", path, body=_MESH)
    async with IPSClient(config=token_config) as ips:
        mesh = await ips.imviewer_mesh(_OBJECT_ID, _BLOB_ID)

    assert mesh.metadata == {"name": "Ребро", "units": "mm"}
    assert mesh.config_info == {"current": "Default"}
    assert len(mesh.bodies) == 2
    assert mesh.bodies[0] == {"id": 1, "triangles": 128}
    # configName не задан -> в query отсутствует
    assert "configName" not in fake_ips.requests[-1].query


async def test_imviewer_mesh_passes_config_name(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/imviewer/mesh/{_OBJECT_ID}/{_BLOB_ID}"
    fake_ips.add("get", path, body=_MESH)
    async with IPSClient(config=token_config) as ips:
        await ips.imviewer_mesh(_OBJECT_ID, _BLOB_ID, config_name="Variant2")

    assert fake_ips.requests[-1].query["configName"] == "Variant2"


async def test_imviewer_assembly_returns_assembly(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/imviewer/assembly/{_OBJECT_ID}/{_BLOB_ID}"
    fake_ips.add("get", path, body=_ASSEMBLY)
    async with IPSClient(config=token_config) as ips:
        asm = await ips.imviewer_assembly(_OBJECT_ID, _BLOB_ID, config_name="Default")

    assert asm.metadata == {"name": "Сборка 550", "units": "mm"}
    assert asm.config_info == {"current": "Default", "components": 12}
    assert fake_ips.requests[-1].query["configName"] == "Default"


async def test_imviewer_object_info_returns_type(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/imviewer/objectInfo/{_OBJECT_ID}/{_BLOB_ID}"
    fake_ips.add("get", path, body={"type": "part"})
    async with IPSClient(config=token_config) as ips:
        info = await ips.imviewer_object_info(_OBJECT_ID, _BLOB_ID)

    assert info.type == "part"


async def test_imviewer_object_info_type_null(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/imviewer/objectInfo/{_OBJECT_ID}/{_BLOB_ID}"
    fake_ips.add("get", path, body={"type": None})
    async with IPSClient(config=token_config) as ips:
        info = await ips.imviewer_object_info(_OBJECT_ID, _BLOB_ID)

    assert info.type is None
