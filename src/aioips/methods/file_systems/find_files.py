"""Метод поиска файлов в файловой системе сервера IPS."""

from typing import Any

from ...core import APIManager
from ...schemas.file_systems import FileSystemsSearchParameters


class FindFilesMixin(APIManager):
    """Реализует ``POST /core/api/fileSystems/files``.

    operationId ``FileSystems_FindFiles``.
    """

    async def find_files(self: "FindFilesMixin", params: FileSystemsSearchParameters) -> list[Any]:
        """Ищет файлы в файловой системе сервера IPS по заданным параметрам.

        Перечисляет файлы указанного каталога на стороне IPS Server
        (``Directory.EnumerateFiles``) с учётом шаблона имён и опций перечисления.
        Опрашивается файловая система именно того хоста, где запущен сервер, а не
        машина клиента.

        Только чтение (read-only): метод POST не создаёт, не изменяет и не удаляет
        файлы — он лишь перечисляет существующие. Вызов идемпотентен.

        Когда применять: чтобы найти файлы на сервере по маске (например, ``*.pdf`` в
        каталоге исходников отчётов), проверить наличие ожидаемых файлов или построить
        список для последующей обработки. Для перечисления каталогов используйте
        :meth:`find_directories`.

        Args:
            params: Параметры поиска (:class:`FileSystemsSearchParameters`): корневой
                ``path``, шаблон ``search_pattern`` и ``options``. Пути трактуются в
                терминах файловой системы сервера. ``None``-поля заменяются серверными
                значениями по умолчанию.

        Returns:
            Список путей к найденным файлам (строки в представлении ОС сервера). Пустой
            список означает, что под параметры не подошёл ни один файл.

        Raises:
            IPSError: При ошибочном ответе сервера (в т. ч. 400, если путь некорректен
                или недоступен).

        Example:
            from aioips.schemas.file_systems import FileSystemsSearchParameters

            async with IPSClient(config=config) as ips:
                files = await ips.find_files(
                    FileSystemsSearchParameters(path="X:/ips", search_pattern="*.pdf")
                )
                print(files)  # например, ['X:/ips/report.pdf']

        Notes:
            operationId ``FileSystems_FindFiles``; путь
            ``POST /core/api/fileSystems/files`` (ответ — голый массив строк).
            Связанные методы: :meth:`find_directories`, :meth:`is_directory_exists`.
        """
        payload = params.model_dump(by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/fileSystems/files", json=payload)
        return list(data) if data is not None else []
