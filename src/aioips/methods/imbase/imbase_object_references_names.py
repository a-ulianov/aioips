"""Резолвер отображаемых имён объектов по ссылкам-строкам IMBASE."""

from ...core import APIManager


class ImBaseObjectReferencesNamesMixin(APIManager):
    """Реализует ``POST .../objectReferencesNames``.

    operationId ``ImBase_GetObjectReferencesNames``.
    """

    async def imbase_object_references_names(
        self: "ImBaseObjectReferencesNamesMixin",
        references: list[str],
    ) -> dict[str, str]:
        """Разрешает отображаемые имена объектов по списку ссылок-строк.

        Резолвер имён: принимает набор ссылок (строковых идентификаторов объектов)
        и возвращает их человекочитаемые названия. Применяют, чтобы массово
        получить подписи для ссылок (например, отрисовать значения атрибутов-ссылок
        без загрузки самих объектов). Это операция ЧТЕНИЯ: несмотря на POST,
        ничего не изменяется.

        Когда применять: когда на руках есть ссылки на ОБЪЕКТЫ (строки) и нужны их
        имена для показа. Парные резолверы: :meth:`imbase_object_by_id_references_names`
        (ссылки на объекты по id версии) и :meth:`imbase_record_references_names`
        (ссылки на записи). Тело запроса — массив строк.

        Args:
            references: Список ссылок-строк на объекты (тело — JSON-массив строк).
                Формат строки задаётся IPS (ссылка на объект).

        Returns:
            Словарь ``{ссылка: отображаемое_имя}`` (``dict[str, str]``). Ссылки, для
            которых имя не разрешилось, в ответе могут отсутствовать. Пустой словарь —
            если сервер вернул не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                names = await ips.imbase_object_references_names(
                    ["@102550", "@102551"]
                )
                print(names)  # {"@102550": "Ребро", ...}

        Notes:
            operationId ``ImBase_GetObjectReferencesNames``; путь
            ``POST /core/api/imbase/objectReferencesNames`` (тело — массив строк,
            ответ — словарь строк).
        """
        data = await self._request(
            "post",
            "/core/api/imbase/objectReferencesNames",
            json=list(references),
        )
        return data if isinstance(data, dict) else {}
