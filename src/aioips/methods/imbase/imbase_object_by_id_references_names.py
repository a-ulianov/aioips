"""Резолвер отображаемых имён объектов по ссылкам-строкам (по id) IMBASE."""

from ...core import APIManager


class ImBaseObjectByIdReferencesNamesMixin(APIManager):
    """Реализует ``POST .../objectByIdReferencesNames``.

    operationId ``ImBase_GetObjectByIdReferencesNames``.
    """

    async def imbase_object_by_id_references_names(
        self: "ImBaseObjectByIdReferencesNamesMixin",
        references: list[str],
    ) -> dict[str, str]:
        """Разрешает отображаемые имена объектов по ссылкам-строкам (адресация по id).

        Резолвер имён, родственный :meth:`imbase_object_references_names`, но
        ссылки адресуют объекты по идентификатору (варианту «by id»). Принимает
        набор ссылок-строк и возвращает их человекочитаемые названия. Это операция
        ЧТЕНИЯ: несмотря на POST, ничего не изменяется.

        Когда применять: когда ссылки на объекты заданы в «by id»-форме и нужны их
        имена для показа без загрузки объектов. Парные резолверы:
        :meth:`imbase_object_references_names` и
        :meth:`imbase_record_references_names`. Тело запроса — массив строк.

        Args:
            references: Список ссылок-строк на объекты в форме «by id» (тело —
                JSON-массив строк). Формат строки задаётся IPS.

        Returns:
            Словарь ``{ссылка: отображаемое_имя}`` (``dict[str, str]``). Неразрешённые
            ссылки в ответе могут отсутствовать. Пустой словарь — если сервер вернул
            не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                names = await ips.imbase_object_by_id_references_names(
                    ["#7", "#8"]
                )
                print(names)

        Notes:
            operationId ``ImBase_GetObjectByIdReferencesNames``; путь
            ``POST /core/api/imbase/objectByIdReferencesNames`` (тело — массив строк,
            ответ — словарь строк).
        """
        data = await self._request(
            "post",
            "/core/api/imbase/objectByIdReferencesNames",
            json=list(references),
        )
        return data if isinstance(data, dict) else {}
