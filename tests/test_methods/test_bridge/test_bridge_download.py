"""Тесты методов загрузки (Download) раздела IPS Bridge.

Бинарные методы проверяют возврат ``bytes``; JSON-методы — путь, query и
распаковку против поддельного сервера :class:`FakeIPS`.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

_Client = IPSClient


async def test_bridge_download_app_returns_bytes(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/App"
    fake_ips.add("get", path, body=b"\x00MZBINARY\xff")
    async with _Client(config=token_config) as ips:
        data = await ips.bridge_download_app("win-x64")

    assert data == b"\x00MZBINARY\xff"
    request = fake_ips.requests[-1]
    assert request.method == "GET"
    assert request.path == path
    assert request.query == {"platformName": "win-x64"}


async def test_bridge_download_library_returns_dict(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/Library"
    fake_ips.add("get", path, body={"fileName": "Intermech.Pdf.dll", "content": "AQID"})
    async with _Client(config=token_config) as ips:
        dto = await ips.bridge_download_library("Intermech.Pdf.dll")

    assert dto == {"fileName": "Intermech.Pdf.dll", "content": "AQID"}
    request = fake_ips.requests[-1]
    assert request.path == path
    assert request.query == {"libraryName": "Intermech.Pdf.dll"}


async def test_bridge_download_library_empty_on_null(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/Library"
    fake_ips.add("get", path, body=None)
    async with _Client(config=token_config) as ips:
        assert await ips.bridge_download_library("X.dll") == {}


async def test_bridge_download_plugin_with_file(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/IntegratedAppPlugin"
    fake_ips.add("get", path, body={"pluginName": "PdfViewer"})
    async with _Client(config=token_config) as ips:
        dto = await ips.bridge_download_integrated_app_plugin("PdfViewer", with_file=True)

    assert dto == {"pluginName": "PdfViewer"}
    request = fake_ips.requests[-1]
    assert request.path == path
    assert request.query == {"pluginName": "PdfViewer", "withFile": "true"}


async def test_bridge_download_plugin_omits_with_file(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/IntegratedAppPlugin"
    fake_ips.add("get", path, body={"pluginName": "PdfViewer"})
    async with _Client(config=token_config) as ips:
        await ips.bridge_download_integrated_app_plugin("PdfViewer")

    request = fake_ips.requests[-1]
    assert request.query == {"pluginName": "PdfViewer"}
