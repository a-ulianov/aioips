"""Метод получения списка локальных дисков сервера IPS."""

from ...core import APIManager


class LocalDrivesMixin(APIManager):
    """Реализует метод ``GET /core/api/fileSystems/localDrives``.

    operationId ``FileSystems_GetLocalDrives``.
    """

    async def local_drives(self: "LocalDrivesMixin") -> list[str]:
        """Возвращает список локальных дисков (имён томов) файловой системы сервера IPS.

        Метод опрашивает файловую систему именно того хоста, на котором запущен IPS
        Server, и отдаёт перечень его локальных дисков (например, буквы дисков Windows
        ``C:``, ``D:``). Список отражает серверное окружение, а не машину клиента.

        Когда применять: при работе с серверными путями — чтобы предложить выбор корневого
        диска в диалогах загрузки/экспорта файлов, проверить доступность ожидаемого тома
        (например, хранилища vault) или построить навигацию по файловой системе сервера.
        Предусловий нет; вызов идемпотентен (только чтение).

        Returns:
            Список имён локальных дисков сервера в строковом представлении. Пустой
            список означает, что сервер не сообщил ни об одном локальном диске.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                drives = await ips.local_drives()
                print(drives)  # например, ['C:', 'D:', 'X:']

        Notes:
            operationId ``FileSystems_GetLocalDrives``; путь
            ``GET /core/api/fileSystems/localDrives`` (голый массив строк).
        """
        data = await self._request("get", "/core/api/fileSystems/localDrives")
        return [str(item) for item in data]
