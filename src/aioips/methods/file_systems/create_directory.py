"""Метод создания каталога на файловой системе сервера IPS (мутация)."""

from typing import Any

from ...core import APIManager


class CreateDirectoryMixin(APIManager):
    """Реализует ``POST /core/api/fileSystems/createDirectory``.

    operationId ``FileSystems_CreateDirectory``.
    """

    async def create_directory(
        self: "CreateDirectoryMixin",
        path: str,
        *,
        confirm: bool = False,
    ) -> None:
        r"""Создаёт каталог по указанному пути на файловой системе СЕРВЕРА IPS (МУТАЦИЯ).

        Создаёт директорию в файловой системе сервера приложений (а не на клиенте).
        Путь интерпретируется сервером в его файловой системе; обычно создаются и
        недостающие промежуточные каталоги. Это операция ЗАПИСИ во внешнюю по отношению
        к базе данных среду — она изменяет состояние диска сервера.

        Когда применять: при подготовке каталога-приёмника перед выгрузкой/сохранением
        файлов на сервере (например, перед :meth:`find_files` / экспортом). Проверить
        существование каталога заранее можно методом :meth:`is_directory_exists`, а
        перечислить подкаталоги — :meth:`find_directories`.

        Обратимость: операция НЕОБРАТИМА средствами этого API — отдельного метода
        удаления каталога в обёртке нет; убрать созданный каталог можно только вручную
        на сервере. Поэтому защищена параметром ``confirm`` и применяется осознанно.

        Args:
            path: Абсолютный путь создаваемого каталога в файловой системе СЕРВЕРА IPS
                (query-параметр ``path``). Формат пути — серверный (Windows-пути с
                ``\\`` либо UNC, в зависимости от ОС сервера).
            confirm: Подтверждение необратимой операции. Без ``True`` запрос НЕ
                выполняется и поднимается :class:`ValueError` ещё до обращения к серверу.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (нет прав, недопустимый путь и т. п.).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.create_directory(r"D:\\export\\batch-42", confirm=True)

        Notes:
            operationId ``FileSystems_CreateDirectory``; путь
            ``POST /core/api/fileSystems/createDirectory``. Query — ``path`` (string);
            тело не требуется. Ответ — void (None).
        """
        if confirm is not True:
            raise ValueError(
                "create_directory создаёт каталог на ФС сервера (необратимо без ручного "
                "удаления); передайте confirm=True",
            )
        params: dict[str, Any] = {"path": path}
        await self._request("post", "/core/api/fileSystems/createDirectory", params=params)
        return None
