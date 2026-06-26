"""Резолвер отображаемых имён записей по ссылкам-строкам IMBASE."""

from ...core import APIManager


class ImBaseRecordReferencesNamesMixin(APIManager):
    """Реализует ``POST .../recordReferencesNames``.

    operationId ``ImBase_GetRecordReferencesNames``.
    """

    async def imbase_record_references_names(
        self: "ImBaseRecordReferencesNamesMixin",
        references: list[str],
    ) -> dict[str, str]:
        """Разрешает отображаемые имена записей по списку ссылок-строк.

        Резолвер имён для ЗАПИСЕЙ табличных частей справочника (в отличие от
        :meth:`imbase_object_references_names`, который разрешает объекты).
        Принимает набор ссылок-строк на записи и возвращает их человекочитаемые
        названия. Это операция ЧТЕНИЯ: несмотря на POST, ничего не изменяется.

        Когда применять: когда есть ссылки на записи таблиц справочника и нужны их
        имена для показа. Парные резолверы:
        :meth:`imbase_object_references_names`,
        :meth:`imbase_object_by_id_references_names`. Тело запроса — массив строк.

        Args:
            references: Список ссылок-строк на записи (тело — JSON-массив строк).
                Формат строки задаётся IPS (ссылка на запись таблицы).

        Returns:
            Словарь ``{ссылка: отображаемое_имя}`` (``dict[str, str]``). Неразрешённые
            ссылки в ответе могут отсутствовать. Пустой словарь — если сервер вернул
            не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                names = await ips.imbase_record_references_names(["r:1001", "r:1002"])
                print(names)

        Notes:
            operationId ``ImBase_GetRecordReferencesNames``; путь
            ``POST /core/api/imbase/recordReferencesNames`` (тело — массив строк,
            ответ — словарь строк).
        """
        data = await self._request(
            "post",
            "/core/api/imbase/recordReferencesNames",
            json=list(references),
        )
        return data if isinstance(data, dict) else {}
