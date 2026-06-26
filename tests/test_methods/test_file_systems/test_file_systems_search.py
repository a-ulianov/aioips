"""Тесты read-only методов поиска по файловой системе сервера IPS."""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.schemas.file_systems import FileSystemsSearchParameters

DIRECTORIES_URL = "/core/api/fileSystems/directories"
FILES_URL = "/core/api/fileSystems/files"
EXISTS_URL = "/core/api/fileSystems/isDirectoryExists"


async def test_find_directories_parses_and_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", DIRECTORIES_URL, body=["X:\\ips", "X:\\ips-backup"])
    async with IPSClient(config=token_config) as ips:
        result = await ips.find_directories(
            FileSystemsSearchParameters(path="X:\\", search_pattern="ips*")
        )

    assert result == ["X:\\ips", "X:\\ips-backup"]
    request = next(r for r in fake_ips.requests if r.path == DIRECTORIES_URL)
    assert request.method == "POST"
    assert request.body == {"path": "X:\\", "searchPattern": "ips*"}


async def test_find_directories_null_response(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", DIRECTORIES_URL, body=None)
    async with IPSClient(config=token_config) as ips:
        result = await ips.find_directories(FileSystemsSearchParameters())

    assert result == []


async def test_find_files_parses_and_builds_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", FILES_URL, body=["X:\\ips\\report.pdf"])
    async with IPSClient(config=token_config) as ips:
        result = await ips.find_files(
            FileSystemsSearchParameters(path="X:\\ips", search_pattern="*.pdf")
        )

    assert result == ["X:\\ips\\report.pdf"]
    request = next(r for r in fake_ips.requests if r.path == FILES_URL)
    assert request.body == {"path": "X:\\ips", "searchPattern": "*.pdf"}


async def test_is_directory_exists_true_passes_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", EXISTS_URL, body=True)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_directory_exists(path="X:\\ips")

    assert result is True
    request = next(r for r in fake_ips.requests if r.path == EXISTS_URL)
    assert request.method == "POST"
    assert request.query == {"path": "X:\\ips"}
    assert request.body == {}


async def test_is_directory_exists_false_and_no_query(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", EXISTS_URL, body=False)
    async with IPSClient(config=token_config) as ips:
        result = await ips.is_directory_exists()

    assert result is False
    request = next(r for r in fake_ips.requests if r.path == EXISTS_URL)
    assert request.query == {}
