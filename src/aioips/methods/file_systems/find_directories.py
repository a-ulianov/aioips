"""Метод поиска каталогов в файловой системе сервера IPS."""

from typing import Any

from ...core import APIManager
from ...schemas.file_systems import FileSystemsSearchParameters


class FindDirectoriesMixin(APIManager):
    """Реализует ``POST /core/api/fileSystems/directories``.

    operationId ``FileSystems_FindDirectories``.
    """

    async def find_directories(
        self: "FindDirectoriesMixin", params: FileSystemsSearchParameters
    ) -> list[Any]:
        """Ищет каталоги в файловой системе сервера IPS по заданным параметрам.

        Перечисляет подкаталоги указанного каталога на стороне IPS Server
        (``Directory.EnumerateDirectories``) с учётом шаблона имён и опций
        перечисления. Опрашивается файловая система именно того хоста, где запущен
        сервер, а не машина клиента.

        Только чтение (read-only): метод POST не создаёт, не перемещает и не удаляет
        каталоги — он лишь перечисляет существующие. Вызов идемпотентен.

        Когда применять: чтобы построить навигацию по каталогам сервера, проверить
        наличие ожидаемой структуры папок (например, в хранилище vault на диске X:)
        или предложить выбор каталога в диалогах экспорта/импорта. Для перечисления
        файлов используйте :meth:`find_files`, для проверки одного каталога —
        :meth:`is_directory_exists`.

        Args:
            params: Параметры поиска (:class:`FileSystemsSearchParameters`): корневой
                ``path``, шаблон ``search_pattern`` и ``options``. Пути трактуются в
                терминах файловой системы сервера. ``None``-поля заменяются серверными
                значениями по умолчанию.

        Returns:
            Список путей к найденным каталогам (строки в представлении ОС сервера).
            Пустой список означает, что под параметры не подошёл ни один каталог.

        Raises:
            IPSError: При ошибочном ответе сервера (в т. ч. 400, если путь некорректен
                или недоступен).

        Example:
            from aioips.schemas.file_systems import FileSystemsSearchParameters

            async with IPSClient(config=config) as ips:
                dirs = await ips.find_directories(
                    FileSystemsSearchParameters(path="X:/", search_pattern="ips*")
                )
                print(dirs)  # например, ['X:/ips', 'X:/ips-backup']

        Notes:
            operationId ``FileSystems_FindDirectories``; путь
            ``POST /core/api/fileSystems/directories`` (ответ — голый массив строк).
            Связанные методы: :meth:`find_files`, :meth:`is_directory_exists`,
            :meth:`local_drives`.
        """
        payload = params.model_dump(by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/fileSystems/directories", json=payload)
        return list(data) if data is not None else []
