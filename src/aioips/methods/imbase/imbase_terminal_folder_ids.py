"""Метод получения идентификаторов терминальных папок IMBASE."""

from ...core import APIManager


class ImBaseTerminalFolderIdsMixin(APIManager):
    """Реализует ``GET /core/api/imbase/terminalFolders``."""

    async def imbase_terminal_folder_ids(
        self: "ImBaseTerminalFolderIdsMixin",
    ) -> list[int]:
        """Возвращает идентификаторы терминальных (конечных) папок IMBASE.

        Терминальная папка IMBASE — узел дерева, в который нельзя вкладывать
        подпапки/каталоги (лист иерархии для размещения записей). Метод отдаёт
        идентификаторы всех таких папок справочной системы.

        Когда применять: при построении дерева IMBASE, чтобы отличить конечные папки
        (нельзя углубляться) от обычных каталогов. Те же данные входят в сводный
        снимок :meth:`imbase_client_cache_state` (поле ``terminal_folder_ids``). Ответ
        — голый массив целых, без result-обёртки.

        Returns:
            Список идентификаторов терминальных папок (``list[int]``). Пустой список
            означает отсутствие терминальных папок.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                folder_ids = await ips.imbase_terminal_folder_ids()
                print(folder_ids)

        Notes:
            operationId ``ImBase_GetTerminalFolderIds``; путь
            ``GET /core/api/imbase/terminalFolders`` (массив ``int64``).
        """
        data = await self._request("get", "/core/api/imbase/terminalFolders")
        items = data if isinstance(data, list) else []
        return [int(item) for item in items]
