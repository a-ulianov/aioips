"""Тесты GET-метода проверки возможности правки атрибутов объекта.

Проверяют путь, HTTP-метод и void-распаковку (успех = ``None``, отсутствие
исключения) для ``object_check_edit``. Внешний HTTP мокируется ``FakeIPS``.

Метод подключён к агрегатору ``ObjectsAPI``, поэтому тест использует штатный
``IPSClient``.
"""

from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig

OBJ = 102550

_Client = IPSClient


async def test_check_edit_returns_none(token_config: IPSConfig, fake_ips: FakeIPS):
    path = f"/core/api/objects/{OBJ}/checkEdit"
    fake_ips.add("get", path, body=None)
    async with _Client(config=token_config) as ips:
        result = await ips.object_check_edit(OBJ)
    assert result is None
    assert any(r.path == path and r.method == "GET" for r in fake_ips.requests)
