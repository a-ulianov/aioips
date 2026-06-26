"""Метод получения идентификатора файла по его имени (сервис имён файлов IPS)."""

from typing import Any

from ...core import APIManager


class FileIdByNameMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getIDByFileName``.

    operationId ``Files_GetIDByFileName``.
    """

    async def file_id_by_name(
        self: "FileIdByNameMixin",
        *,
        file_name: str | None = None,
    ) -> int:
        """Возвращает идентификатор файла по его имени из сервиса имён файлов IPS.

        Применяют, когда имя файла известно, а его числовой идентификатор в
        id-пространстве файлов — нет (например, чтобы затем найти объекты по
        этому файлу). Парный метод обратного поиска — :meth:`object_ids_by_file_name`
        (он возвращает идентификаторы ОБЪЕКТОВ, владеющих файлом).

        Это операция ЧТЕНИЯ. Несмотря на метод POST, тело не используется —
        имя передаётся в query; IPS требует наличия тела, поэтому отправляется
        пустой объект ``{}``.

        Args:
            file_name: Имя файла (query ``fileName``). ``None`` — параметр не
                передаётся; сервер применит поведение по умолчанию.

        Returns:
            Идентификатор файла (целое, int64) в id-пространстве файлов. ``0``,
            если сервер вернул пустой ответ (имя не найдено).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                file_id = await ips.file_id_by_name(file_name="schema.pdf")

        Notes:
            operationId ``Files_GetIDByFileName``. Часть сервиса имён файлов
            (``fileNamesService``). Возвращаемый id — из пространства файлов, НЕ
            из пространства объектов/версий. Связанные методы:
            :meth:`object_ids_by_file_name`, :meth:`next_file_id`.
        """
        params: dict[str, Any] = {}
        if file_name is not None:
            params["fileName"] = "" if file_name is None else str(file_name)
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getIDByFileName",
            json={},
            params=params or None,
        )
        return int(data) if data is not None else 0
