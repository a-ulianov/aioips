"""Тесты методов записи/мутаций и чтения-через-POST раздела IPS Bridge.

Категория A — чтения через POST (без confirm): проверяем путь, тело ``{}``,
распаковку результата. Категория B — обратимые/temp-file/мутации: проверяем
гейт ``confirm`` (без него — ``ValueError`` до запроса) и корректный путь/тело
при ``confirm=True``.
"""

from uuid import UUID

import pytest
from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.client import IPSClient

_Client = IPSClient


_ACTION = {
    "actionId": "cad001c5-306c-11d8-b4e9-00304f19f545",
    "handlerId": "cad001c5-306c-11d8-b4e9-00304f19f546",
    "displayName": "Открыть в просмотрщике",
}
_ACTION_WITH_TYPE = {"actionInfo": _ACTION, "launchType": "view"}
_HISTORY_ITEM = {"categoryType": 1, "categoryID": 42, "actionID": "edit"}


# ---------------------------------------------------------------------------
# Категория A: чтения через POST (без confirm)
# ---------------------------------------------------------------------------


async def test_bridge_get_integrators(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Integrators/GetIntegrators", body={"a": {"name": "x"}})
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_get_integrators()

    assert result == {"a": {"name": "x"}}
    request = fake_ips.requests[-1]
    assert request.method == "POST"
    assert request.body == {}


async def test_bridge_get_integrators_null_to_empty(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Integrators/GetIntegrators", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_get_integrators()

    assert result == {}


async def test_bridge_get_action_list_with_body(token_config: IPSConfig, fake_ips: FakeIPS):
    from aioips.schemas.bridge.launch_action_request import LaunchActionDto, LaunchType

    fake_ips.add("post", "/core/api/Bridge/Launch/GetActionList", body=[_ACTION, _ACTION])
    async with _Client(config=token_config) as ips:
        actions = await ips.bridge_get_action_list(
            LaunchActionDto(object_type_id=1, launch_type=LaunchType.VIEW)
        )

    assert len(actions) == 2
    assert actions[0].action_id == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    request = fake_ips.requests[-1]
    assert request.body == {"objectTypeId": 1, "launchType": "view"}


async def test_bridge_get_action_list_default_body(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Launch/GetActionList", body=None)
    async with _Client(config=token_config) as ips:
        actions = await ips.bridge_get_action_list()

    assert actions == []
    assert fake_ips.requests[-1].body == {}


async def test_bridge_get_default_actions(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Launch/GetDefaultActions", body=[_ACTION_WITH_TYPE])
    async with _Client(config=token_config) as ips:
        actions = await ips.bridge_get_default_actions(object_type_id=1, user_id=7)

    assert actions == [_ACTION_WITH_TYPE]
    request = fake_ips.requests[-1]
    assert request.query["objectTypeId"] == "1"
    assert request.query["userId"] == "7"
    assert request.body == {}


async def test_bridge_get_full_action_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Launch/GetFullActionList", body=[_ACTION_WITH_TYPE])
    async with _Client(config=token_config) as ips:
        actions = await ips.bridge_get_full_action_list(object_type_id=1)

    assert actions == [_ACTION_WITH_TYPE]
    request = fake_ips.requests[-1]
    assert request.query["objectTypeId"] == "1"
    assert "userId" not in request.query


async def test_bridge_get_modifications_history_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post", "/core/api/Bridge/Session/GetModificationsHistoryList", body=[_HISTORY_ITEM]
    )
    async with _Client(config=token_config) as ips:
        history = await ips.bridge_get_modifications_history_list()

    assert history == [_HISTORY_ITEM]
    assert fake_ips.requests[-1].body == {}


async def test_bridge_get_modifications_history_list_null(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/Bridge/Session/GetModificationsHistoryList", body=None)
    async with _Client(config=token_config) as ips:
        history = await ips.bridge_get_modifications_history_list()

    assert history == []


# ---------------------------------------------------------------------------
# Категория B: мутации — гейт confirm и корректный вызов
# ---------------------------------------------------------------------------


async def test_bridge_create_temp_directory_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_create_temp_directory()

    assert fake_ips.requests == []


async def test_bridge_create_temp_directory_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Files/CreateTempDirectory", body="/tmp/ips/s1")
    async with _Client(config=token_config) as ips:
        path = await ips.bridge_create_temp_directory(confirm=True)

    assert path == "/tmp/ips/s1"
    assert fake_ips.requests[-1].body == {}


async def test_bridge_create_temp_directory_null_to_empty(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/Bridge/Files/CreateTempDirectory", body=None)
    async with _Client(config=token_config) as ips:
        path = await ips.bridge_create_temp_directory(confirm=True)

    assert path == ""


async def test_bridge_delete_temp_stored_item_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_delete_temp_stored_item(path="/tmp/x")

    assert fake_ips.requests == []


async def test_bridge_delete_temp_stored_item_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/Bridge/Files/DeleteTempStoredItem", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_delete_temp_stored_item(path="/tmp/x", confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.query["path"] == "/tmp/x"


async def test_bridge_download_temp_folder_as_zip_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_download_temp_folder_as_zip(file_path="/tmp/x")

    assert fake_ips.requests == []


async def test_bridge_download_temp_folder_as_zip_confirmed(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/Bridge/Files/DownloadTempFolderAsZip", body="/tmp/x.zip")
    async with _Client(config=token_config) as ips:
        path = await ips.bridge_download_temp_folder_as_zip(file_path="/tmp/x", confirm=True)

    assert path == "/tmp/x.zip"
    request = fake_ips.requests[-1]
    assert request.query["filePath"] == "/tmp/x"
    assert request.body == {}


async def test_bridge_extract_zip_file_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_extract_zip_file(file_path="/tmp/a.zip")

    assert fake_ips.requests == []


async def test_bridge_extract_zip_file_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Files/ExtractZipFile", body="/tmp/out")
    async with _Client(config=token_config) as ips:
        out = await ips.bridge_extract_zip_file(file_path="/tmp/a.zip", confirm=True)

    assert out == "/tmp/out"
    assert fake_ips.requests[-1].query["filePath"] == "/tmp/a.zip"


async def test_bridge_pack_directory_as_zip_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_pack_directory_as_zip(dir_path="/tmp/d")

    assert fake_ips.requests == []


async def test_bridge_pack_directory_as_zip_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add(
        "post",
        "/core/api/Bridge/Files/PackDirectoryAsZip",
        body={"filePath": "/tmp/d.zip", "totalBytes": 2048},
    )
    async with _Client(config=token_config) as ips:
        info = await ips.bridge_pack_directory_as_zip(dir_path="/tmp/d", confirm=True)

    assert info.file_path == "/tmp/d.zip"
    assert info.total_bytes == 2048
    assert fake_ips.requests[-1].query["dirPath"] == "/tmp/d"


async def test_bridge_upload_file_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_upload_file()

    assert fake_ips.requests == []


async def test_bridge_upload_file_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    from aioips.schemas.bridge.file_request import FileRequestDTO

    fake_ips.add("post", "/core/api/Bridge/Files/UploadFile", body="/tmp/a.txt")
    async with _Client(config=token_config) as ips:
        path = await ips.bridge_upload_file(
            FileRequestDTO(data="QUJD", file_name="a.txt"), confirm=True
        )

    assert path == "/tmp/a.txt"
    assert fake_ips.requests[-1].body == {"data": "QUJD", "fileName": "a.txt"}


async def test_bridge_upload_large_file_request_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_upload_large_file_request()

    assert fake_ips.requests == []


async def test_bridge_upload_large_file_request_confirmed(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    from aioips.schemas.bridge.file_request import LargeFileRequestDTO

    fake_ips.add("post", "/core/api/Bridge/Files/UploadLargeFileRequest", body="guid-123")
    async with _Client(config=token_config) as ips:
        guid = await ips.bridge_upload_large_file_request(
            LargeFileRequestDTO(file_name="big.bin", total_bytes=1024, total_chunks=2),
            confirm=True,
        )

    assert guid == "guid-123"
    assert fake_ips.requests[-1].body["fileName"] == "big.bin"


async def test_bridge_upload_large_file_chunk_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_upload_large_file_chunk()

    assert fake_ips.requests == []


async def test_bridge_upload_large_file_chunk_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    from aioips.schemas.bridge.file_request import LargeFileChunkDTO

    fake_ips.add("post", "/core/api/Bridge/Files/UploadLargeFileChunk", body="ok")
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_upload_large_file_chunk(
            LargeFileChunkDTO(
                request_guid="cad001c5-306c-11d8-b4e9-00304f19f545",
                chunk_number=0,
                data="QUJD",
            ),
            confirm=True,
        )

    assert result == "ok"
    assert fake_ips.requests[-1].body["chunkNumber"] == 0


async def test_bridge_upload_large_file_chunk_base64_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_upload_large_file_chunk_base64()

    assert fake_ips.requests == []


async def test_bridge_upload_large_file_chunk_base64_confirmed(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    from aioips.schemas.bridge.file_request import LargeFileChunkDTOBase64

    fake_ips.add("post", "/core/api/Bridge/Files/UploadLargeFileChunkBase64", body="ok")
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_upload_large_file_chunk_base64(
            LargeFileChunkDTOBase64(
                request_guid="cad001c5-306c-11d8-b4e9-00304f19f545",
                chunk_number=1,
                data="QUJD",
            ),
            confirm=True,
        )

    assert result == "ok"
    assert fake_ips.requests[-1].body["chunkNumber"] == 1


async def test_bridge_upload_large_file_cancel_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_upload_large_file_cancel(request_guid="g1")

    assert fake_ips.requests == []


async def test_bridge_upload_large_file_cancel_confirmed(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("delete", "/core/api/Bridge/Files/UploadLargeFileCancel", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_upload_large_file_cancel(request_guid="g1", confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.query["requestGuid"] == "g1"


async def test_bridge_create_launch_action_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_create_launch_action()

    assert fake_ips.requests == []


async def test_bridge_create_launch_action_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    from aioips.schemas.bridge.launch_action_request import (
        CreateLaunchActionDto,
        LaunchType,
    )

    fake_ips.add("post", "/core/api/Bridge/Launch/CreateLaunchAction", body=_ACTION)
    async with _Client(config=token_config) as ips:
        action = await ips.bridge_create_launch_action(
            CreateLaunchActionDto(
                handler_id="cad001c5-306c-11d8-b4e9-00304f19f546",
                object_type_id=1,
                launch_type=LaunchType.EDIT,
            ),
            confirm=True,
        )

    assert action.action_id == UUID("cad001c5-306c-11d8-b4e9-00304f19f545")
    body = fake_ips.requests[-1].body
    assert body["handlerId"] == "cad001c5-306c-11d8-b4e9-00304f19f546"
    assert body["launchType"] == "edit"


async def test_bridge_remove_launch_action_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_remove_launch_action(action_id="a1")

    assert fake_ips.requests == []


async def test_bridge_remove_launch_action_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/Bridge/Launch/RemoveLaunchAction", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_remove_launch_action(action_id="a1", confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.query["actionId"] == "a1"


async def test_bridge_update_launch_action_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_update_launch_action("<x/>", action_id="a1")

    assert fake_ips.requests == []


async def test_bridge_update_launch_action_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Launch/UpdateLaunchAction", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_update_launch_action("<x/>", action_id="a1", confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.query["actionId"] == "a1"
    assert request.body == "<x/>"


async def test_bridge_set_default_action_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_set_default_action(object_type_id=1, action_id="a1")

    assert fake_ips.requests == []


async def test_bridge_set_default_action_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Launch/SetDefaultAction", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_set_default_action(
            object_type_id=1, action_id="a1", user_id=7, confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.query["objectTypeId"] == "1"
    assert request.query["actionId"] == "a1"
    assert request.query["userId"] == "7"
    assert request.body == {}


async def test_bridge_reset_default_action_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_reset_default_action(object_type_id=1, action_id="a1")

    assert fake_ips.requests == []


async def test_bridge_reset_default_action_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/Bridge/Launch/ResetDefaultAction", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_reset_default_action(
            object_type_id=1, action_id="a1", confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.query["objectTypeId"] == "1"


async def test_bridge_add_or_update_settings_xml_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_add_or_update_settings_xml(integrator_guid="g1", xml_data="<x/>")

    assert fake_ips.requests == []


async def test_bridge_add_or_update_settings_xml_confirmed(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    fake_ips.add("post", "/core/api/Bridge/Integrators/AddOrUpdateSettingsXml", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_add_or_update_settings_xml(
            integrator_guid="g1", xml_data="<x/>", confirm=True
        )

    assert result is None
    request = fake_ips.requests[-1]
    assert request.query["integratorGuid"] == "g1"
    assert request.query["xmlData"] == "<x/>"
    assert request.body == {}


async def test_bridge_remove_integrator_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_remove_integrator(integrator_guid="g1")

    assert fake_ips.requests == []


async def test_bridge_remove_integrator_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("delete", "/core/api/Bridge/Integrators/RemoveIntegrator", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_remove_integrator(integrator_guid="g1", confirm=True)

    assert result is None
    request = fake_ips.requests[-1]
    assert request.method == "DELETE"
    assert request.query["integratorGuid"] == "g1"


async def test_bridge_start_log_history_requires_confirm(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_start_log_history()

    assert fake_ips.requests == []


async def test_bridge_start_log_history_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Session/StartLogHistory", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_start_log_history(confirm=True)

    assert result is None
    assert fake_ips.requests[-1].body == {}


async def test_bridge_stop_log_history_requires_confirm(token_config: IPSConfig, fake_ips: FakeIPS):
    async with _Client(config=token_config) as ips:
        with pytest.raises(ValueError, match="confirm=True"):
            await ips.bridge_stop_log_history()

    assert fake_ips.requests == []


async def test_bridge_stop_log_history_confirmed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", "/core/api/Bridge/Session/StopLogHistory", body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.bridge_stop_log_history(confirm=True)

    assert result is None
    assert fake_ips.requests[-1].body == {}
