"""Тесты менеджера HTTP-сессии."""

from aioips.core.sessions import SessionManager


async def test_session_is_reused():
    manager = SessionManager()
    first = manager.get_session()
    second = manager.get_session()
    assert first is second
    assert manager.is_open is True
    await manager.close()


async def test_close_is_idempotent():
    manager = SessionManager()
    manager.get_session()
    await manager.close()
    await manager.close()
    assert manager.is_open is False


async def test_get_session_after_close_recreates():
    manager = SessionManager()
    first = manager.get_session()
    await manager.close()
    second = manager.get_session()
    assert first is not second
    await manager.close()
