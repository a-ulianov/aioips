"""Общие фикстуры и утилиты тестов aioips.

Для тестов HTTP-слоя поднимается настоящий локальный aiohttp-сервер
(:class:`FakeIPS`), который отдаёт заранее запрограммированные ответы. Это
проверяет реальный путь запроса (построение URL, заголовки, разбор JSON,
обработку статусов) без зависимости от внешних mock-библиотек.
"""

import json
from collections import defaultdict
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from aiohttp import ContentTypeError, web
from aiohttp.test_utils import TestServer

from aioips import IPSConfig

BASE_URL = "http://ips.test:8080"


class CapturedRequest:
    """Сведения о принятом сервером запросе."""

    def __init__(
        self,
        method: str,
        path: str,
        headers: dict[str, str],
        body: object,
        query: dict[str, str] | None = None,
    ) -> None:
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.query = query if query is not None else {}


class FakeIPS:
    """Локальный поддельный сервер IPS с программируемыми ответами."""

    def __init__(self) -> None:
        self.base_url = ""
        self.requests: list[CapturedRequest] = []
        self._responses: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

    def add(
        self,
        method: str,
        path: str,
        *,
        status: int = 200,
        body: object = None,
    ) -> None:
        """Регистрирует очередной ответ для пары (метод, путь).

        Ответы выдаются по порядку; последний зарегистрированный повторяется.
        """
        self._responses[(method.upper(), path)].append({"status": status, "body": body})

    async def _handle(self, request: web.Request) -> web.Response:
        try:
            payload: object = await request.json()
        except (ContentTypeError, json.JSONDecodeError, UnicodeDecodeError):
            # multipart/бинарное тело (напр. PNG-изображение) не парсится как JSON
            payload = None

        self.requests.append(
            CapturedRequest(
                request.method,
                request.path,
                dict(request.headers),
                payload,
                dict(request.query),
            )
        )

        queue = self._responses.get((request.method, request.path))
        if not queue:
            return web.json_response({"title": "NotFound", "detail": "не задан мок"}, status=404)

        item = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(item["body"], bytes | bytearray):
            return web.Response(
                body=bytes(item["body"]),
                status=int(item["status"]),
                content_type="application/octet-stream",
            )
        return web.json_response(item["body"], status=int(item["status"]))  # type: ignore[arg-type]


@pytest_asyncio.fixture
async def fake_ips() -> AsyncIterator[FakeIPS]:
    """Поднимает локальный поддельный сервер IPS и возвращает его контроллер."""
    fake = FakeIPS()
    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", fake._handle)
    server = TestServer(app)
    await server.start_server()
    fake.base_url = f"http://{server.host}:{server.port}"
    try:
        yield fake
    finally:
        await server.close()


@pytest.fixture
def token_config(fake_ips: FakeIPS) -> IPSConfig:
    """Конфигурация с готовым токеном, направленная на поддельный сервер."""
    return IPSConfig(
        base_url=fake_ips.base_url,
        access_token="test-token",
        retry_min_wait=0.01,
        retry_max_wait=0.02,
        _env_file=None,
    )


@pytest.fixture
def login_config(fake_ips: FakeIPS) -> IPSConfig:
    """Конфигурация с логином/паролем, направленная на поддельный сервер."""
    return IPSConfig(
        base_url=fake_ips.base_url,
        login_name="your-login",
        password="secret",
        role_id=10,
        retry_min_wait=0.01,
        retry_max_wait=0.02,
        _env_file=None,
    )
