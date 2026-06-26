"""Тесты методов чтения раздела настроек видимости.

Раздел ``visibilities`` пока не подключён к :class:`IPSClient`, поэтому тесты
используют его агрегатор :class:`VisibilitiesAPI` как самостоятельный клиент
(он наследует ядро ``APIManager`` и работает как асинхронный контекстный менеджер).
"""

from tests.conftest import FakeIPS

from aioips import IPSConfig
from aioips.methods.visibilities import VisibilitiesAPI

_SETTING = {
    "objectId": 1029,
    "objectType": 3,
    "objectName": "Архив",
    "isVisible": True,
    "isHidden": False,
    "icon": "archive.png",
}


async def test_default_visibility_settings_returns_list(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", "/api/visibilities/getDefault", body=[_SETTING, _SETTING])
    async with VisibilitiesAPI(config=token_config) as ips:
        settings = await ips.default_visibility_settings()

    assert len(settings) == 2
    item = settings[0]
    assert item.object_id == 1029
    assert item.object_type == 3
    assert item.object_name == "Архив"
    assert item.is_visible is True
    assert item.is_hidden is False
    assert item.icon == "archive.png"


async def test_default_visibility_settings_optional_fields(
    token_config: IPSConfig, fake_ips: FakeIPS
):
    minimal = {"objectType": 5, "objectName": "Узел"}
    fake_ips.add("get", "/api/visibilities/getDefault", body=[minimal])
    async with VisibilitiesAPI(config=token_config) as ips:
        settings = await ips.default_visibility_settings()

    item = settings[0]
    assert item.object_type == 5
    assert item.object_name == "Узел"
    assert item.object_id == 0
    assert item.is_visible is False
    assert item.is_hidden is False
    assert item.icon is None
