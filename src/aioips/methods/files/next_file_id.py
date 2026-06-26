"""Метод получения следующего идентификатора файла от сервиса имён файлов IPS."""

from ...core import APIManager


class NextFileIdMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getNextFileID``.

    operationId ``Files_GetNextFileID``.
    """

    async def next_file_id(self: "NextFileIdMixin") -> int:
        """Возвращает следующий свободный идентификатор файла из id-пространства IPS.

        Применяют, когда требуется заранее зарезервировать/узнать числовой
        идентификатор для новой записи файла в сервисе имён файлов IPS — например,
        при низкоуровневом формировании имени или связке файла с объектом до
        фактической загрузки. Возвращаемый id принадлежит ОТДЕЛЬНОМУ
        id-пространству файлов (см. :meth:`file_id_by_name`), а не пространству
        объектов/версий.

        Это операция ЧТЕНИЯ. Несмотря на метод POST, тело и query-параметры не
        используются; IPS требует наличия тела, поэтому отправляется пустой
        объект ``{}``.

        Returns:
            Следующий доступный идентификатор файла (целое, int64). ``0``, если
            сервер вернул пустой ответ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                file_id = await ips.next_file_id()
                # file_id — например, 4521

        Notes:
            operationId ``Files_GetNextFileID``. Часть сервиса имён файлов
            (``fileNamesService``). Связанные методы: :meth:`file_id_by_name`,
            :meth:`file_unique_name`.
        """
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getNextFileID",
            json={},
        )
        return int(data) if data is not None else 0
