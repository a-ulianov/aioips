"""Метод поиска идентификаторов объектов по имени файла (сервис имён файлов IPS)."""

from typing import Any

from ...core import APIManager


class ObjectIdsByFileNameMixin(APIManager):
    """Реализует ``POST /core/api/files/fileNamesService/getObjectIDByFileName``.

    operationId ``Files_GetObjectIDByFileName``.
    """

    async def object_ids_by_file_name(
        self: "ObjectIdsByFileNameMixin",
        *,
        file_name: str | None = None,
    ) -> list[int]:
        """Возвращает идентификаторы объектов, владеющих файлом с заданным именем.

        Применяют, когда нужно найти, к каким объектам прикреплён файл с
        известным именем, — например, чтобы перейти от файла к его объектам
        через :meth:`object_get`. Один файл может быть привязан к нескольким
        объектам, поэтому возвращается список.

        Это операция ЧТЕНИЯ. Несмотря на метод POST, тело не используется —
        имя передаётся в query; IPS требует наличия тела, поэтому отправляется
        пустой объект ``{}``.

        Args:
            file_name: Имя файла (query ``fileName``). ``None`` — параметр не
                передаётся; сервер применит поведение по умолчанию.

        Returns:
            Список идентификаторов ОБЪЕКТОВ (``ObjectID`` / F_OBJECT_ID, int64),
            у которых есть файл с таким именем. Пустой список — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                object_ids = await ips.object_ids_by_file_name(file_name="schema.pdf")
                # object_ids == [102550, 103001]

        Notes:
            operationId ``Files_GetObjectIDByFileName``. Часть сервиса имён файлов
            (``fileNamesService``). Возвращает id ОБЪЕКТОВ (не версий и не id
            файлов). Связанные методы: :meth:`file_id_by_name`,
            :meth:`object_file_by_name`.
        """
        params: dict[str, Any] = {}
        if file_name is not None:
            params["fileName"] = "" if file_name is None else str(file_name)
        data = await self._request(
            "post",
            "/core/api/files/fileNamesService/getObjectIDByFileName",
            json={},
            params=params or None,
        )
        return [int(x) for x in (data or [])]
