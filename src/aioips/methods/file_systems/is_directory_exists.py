"""Метод проверки существования каталога в файловой системе сервера IPS."""

from typing import Any

from ...core import APIManager


class IsDirectoryExistsMixin(APIManager):
    """Реализует ``POST /core/api/fileSystems/isDirectoryExists``.

    operationId ``FileSystems_IsDirectoryExists``.
    """

    async def is_directory_exists(
        self: "IsDirectoryExistsMixin", *, path: str | None = None
    ) -> bool:
        """Проверяет существование каталога в файловой системе сервера IPS.

        Сообщает, существует ли каталог по указанному пути на стороне IPS Server.
        Проверяется файловая система именно того хоста, где запущен сервер, а не
        машина клиента. Путь передаётся как query-параметр ``path``; тело запроса
        пустое (``{}``).

        Только чтение (read-only): метод POST ничего не создаёт и не изменяет в
        файловой системе — он лишь проверяет наличие каталога. Вызов идемпотентен.

        Когда применять: перед обращением к серверному каталогу (например, к
        хранилищу vault на диске X:) или как лёгкая проверка доступности пути без
        перечисления его содержимого. Для получения списка подкаталогов используйте
        :meth:`find_directories`.

        Args:
            path: Путь к проверяемому каталогу в терминах файловой системы сервера.
                Передаётся в query, если задан. ``None`` — параметр не отправляется
                (поведение определяется сервером).

        Returns:
            ``True``, если каталог существует; ``False`` — если не существует либо
            сервер не вернул значение.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                exists = await ips.is_directory_exists(path="X:/ips")
                if exists:
                    ...  # каталог доступен на сервере

        Notes:
            operationId ``FileSystems_IsDirectoryExists``; путь
            ``POST /core/api/fileSystems/isDirectoryExists`` (ответ — ``boolean``).
            Связанные методы: :meth:`find_directories`, :meth:`local_drives`.
        """
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        data = await self._request(
            "post", "/core/api/fileSystems/isDirectoryExists", json={}, params=params
        )
        return bool(data) if data is not None else False
