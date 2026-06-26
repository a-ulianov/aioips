"""Тесты ядра запросов: авторизация, повторы, обработка ошибок."""

from typing import Any

import pytest
from tests.conftest import FakeIPS

from aioips import IPSClient, IPSConfig
from aioips.core.exceptions import (
    IPSAuthError,
    IPSConnectionError,
    IPSNotFoundError,
    IPSServerError,
)

UINFO = "/core/api/currentUsers/userInfo"
AUTH = "/core/api/Auth/authenticate"
REFRESH = "/core/api/Auth/refreshTokens"

_TOKENS = {
    "accessToken": "access-1",
    "refreshToken": "refresh-1",
    "expireTime": "2099-01-01T00:00:00Z",
}


async def test_token_auth_skips_authenticate(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, body={"ok": True})
    async with IPSClient(config=token_config) as ips:
        await ips._request("get", UINFO)
    assert all(r.path != AUTH for r in fake_ips.requests)


async def test_login_flow_authenticates_once(login_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", AUTH, body=_TOKENS)
    fake_ips.add("get", UINFO, body={"ok": True})
    async with IPSClient(config=login_config) as ips:
        await ips._request("get", UINFO)
        await ips._request("get", UINFO)
    auth_calls = [r for r in fake_ips.requests if r.path == AUTH]
    assert len(auth_calls) == 1


async def test_sends_bearer_authorization_header(login_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", AUTH, body=_TOKENS)
    fake_ips.add("get", UINFO, body={"ok": True})
    async with IPSClient(config=login_config) as ips:
        await ips._request("get", UINFO)
    user_request = next(r for r in fake_ips.requests if r.path == UINFO)
    assert user_request.headers["Authorization"] == "Bearer access-1"


async def test_401_triggers_refresh_then_retry(login_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("post", AUTH, body=_TOKENS)
    fake_ips.add("get", UINFO, status=401, body={"title": "expired"})
    fake_ips.add("post", REFRESH, body={**_TOKENS, "accessToken": "access-2"})
    fake_ips.add("get", UINFO, body={"ok": True})
    async with IPSClient(config=login_config) as ips:
        result = await ips._request("get", UINFO)
    assert result == {"ok": True}
    assert any(r.path == REFRESH for r in fake_ips.requests)


async def test_401_without_refresh_raises_auth_error(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, status=401, body={"title": "expired"})
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(IPSAuthError):
            await ips._request("get", UINFO)


async def test_404_raises_not_found(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, status=404, body={"title": "NotFound"})
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(IPSNotFoundError):
            await ips._request("get", UINFO)


async def test_500_is_retried_then_succeeds(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, status=500, body={"title": "server"})
    fake_ips.add("get", UINFO, body={"ok": True})
    async with IPSClient(config=token_config) as ips:
        result = await ips._request("get", UINFO)
    assert result == {"ok": True}


async def test_500_exhausts_retries_and_raises(token_config: IPSConfig, fake_ips: FakeIPS):
    config = token_config.model_copy(update={"max_retries": 1})
    fake_ips.add("get", UINFO, status=500, body={"title": "server"})
    async with IPSClient(config=config) as ips:
        with pytest.raises(IPSServerError):
            await ips._request("get", UINFO)


async def test_network_error_is_retried(token_config: IPSConfig, monkeypatch: pytest.MonkeyPatch):
    calls = {"n": 0}

    async def flaky(*_args: Any, **_kwargs: Any) -> tuple[int, Any]:
        calls["n"] += 1
        if calls["n"] == 1:
            raise IPSConnectionError(0, "boom")
        return 200, {"ok": True}

    async with IPSClient(config=token_config) as ips:
        monkeypatch.setattr(ips, "_raw_request", flaky)
        result = await ips._request("get", UINFO)
    assert result == {"ok": True}
    assert calls["n"] == 2


async def test_request_on_closed_client_raises(token_config: IPSConfig):
    ips = IPSClient(config=token_config)
    await ips.close()
    with pytest.raises(RuntimeError):
        await ips._request("get", UINFO)


async def test_context_manager_closes_client(token_config: IPSConfig):
    async with IPSClient(config=token_config) as ips:
        assert ips.is_closed is False
    assert ips.is_closed is True


async def test_reentering_closed_client_raises(token_config: IPSConfig):
    ips = IPSClient(config=token_config)
    await ips.close()
    with pytest.raises(RuntimeError):
        async with ips:
            pass


async def test_raw_bytes_returns_binary_body(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/App"
    fake_ips.add("get", path, body=b"\x00\x01BINARY\xff")
    async with IPSClient(config=token_config) as ips:
        data = await ips._request("get", path, raw_bytes=True)
    assert data == b"\x00\x01BINARY\xff"


async def test_raw_bytes_error_still_maps_exception(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/App"
    fake_ips.add("get", path, status=404, body={"title": "NotFound"})
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(IPSNotFoundError):
            await ips._request("get", path, raw_bytes=True)


async def test_metrics_hook_called_on_success(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, body={"ok": True})
    seen: list[Any] = []
    async with IPSClient(config=token_config, metrics_hook=seen.append) as ips:
        await ips._request("get", UINFO)
    assert len(seen) == 1
    m = seen[0]
    assert m.method == "get" and m.path == UINFO
    assert m.status == 200 and m.error is None and m.attempt == 1
    assert m.duration_ms >= 0


async def test_metrics_hook_called_on_error(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, status=404, body={"title": "NotFound"})
    seen: list[Any] = []
    async with IPSClient(config=token_config, metrics_hook=seen.append) as ips:
        with pytest.raises(IPSNotFoundError):
            await ips._request("get", UINFO)
    assert seen and seen[-1].status == 404 and seen[-1].error is not None


async def test_metrics_hook_exceptions_are_swallowed(token_config: IPSConfig, fake_ips: FakeIPS):
    fake_ips.add("get", UINFO, body={"ok": True})

    def boom(_m: Any) -> None:
        raise RuntimeError("hook boom")

    async with IPSClient(config=token_config, metrics_hook=boom) as ips:
        assert await ips._request("get", UINFO) == {"ok": True}  # не падает из-за хука


async def test_stream_yields_body_in_chunks(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/App"
    payload = b"\x00\x01BINARY" * 5000  # > chunk_size, чтобы было несколько чанков
    fake_ips.add("get", path, body=payload)
    received = bytearray()
    async with IPSClient(config=token_config) as ips:
        async with ips.stream(
            "get", path, params={"platformName": "win"}, chunk_size=4096
        ) as chunks:
            async for c in chunks:
                received.extend(c)
    assert bytes(received) == payload


async def test_stream_maps_error_before_yield(token_config: IPSConfig, fake_ips: FakeIPS):
    path = "/core/api/Bridge/Download/App"
    fake_ips.add("get", path, status=404, body={"title": "NotFound"})
    async with IPSClient(config=token_config) as ips:
        with pytest.raises(IPSNotFoundError):
            async with ips.stream("get", path) as chunks:
                async for _c in chunks:
                    pass
