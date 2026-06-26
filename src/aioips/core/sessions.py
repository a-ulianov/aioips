"""Управление HTTP-сессией клиента IPS.

В отличие от API со статичным ключом, IPS использует короткоживущий JWT-токен,
который меняется при обновлении. Поэтому заголовок ``Authorization`` не вшивается
в сессию, а добавляется к каждому запросу. Сессия здесь — это переиспользуемый
пул соединений (``aiohttp.ClientSession``) на один экземпляр клиента.
"""

import ssl

from aiohttp import ClientSession, ClientTimeout, TCPConnector


class SessionManager:
    """Лениво создаёт и хранит единственную ``aiohttp.ClientSession``.

    Сессия создаётся при первом обращении и переиспользуется до закрытия клиента.
    """

    def __init__(
        self,
        timeout: float = 30.0,
        connector_limit: int = 100,
        verify_ssl: bool = True,
    ) -> None:
        """Инициализирует менеджер сессии.

        Args:
            timeout: Общий таймаут запроса в секундах.
            connector_limit: Лимит одновременных соединений.
            verify_ssl: Проверять ли TLS-сертификат сервера.
        """
        self._timeout = ClientTimeout(total=timeout)
        self._connector_limit = connector_limit
        self._verify_ssl = verify_ssl
        self._session: ClientSession | None = None

    def get_session(self) -> ClientSession:
        """Возвращает активную сессию, создавая её при первом вызове.

        Returns:
            Открытая ``aiohttp.ClientSession`` экземпляра клиента.
        """
        if self._session is None or self._session.closed:
            ssl_context: ssl.SSLContext | bool = True if self._verify_ssl else False
            self._session = ClientSession(
                timeout=self._timeout,
                connector=TCPConnector(limit=self._connector_limit, ssl=ssl_context),
            )
        return self._session

    @property
    def is_open(self) -> bool:
        """Возвращает ``True``, если сессия создана и не закрыта."""
        return self._session is not None and not self._session.closed

    async def close(self) -> None:
        """Закрывает сессию, если она была открыта."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None
