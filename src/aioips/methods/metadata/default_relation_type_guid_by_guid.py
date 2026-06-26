"""Метод получения GUID типа связи по умолчанию по GUID типа объекта-родителя."""

from uuid import UUID

from ...core import APIManager


class DefaultRelationTypeGuidByGuidMixin(APIManager):
    """Реализует ``GET .../objectTypeDefault/byGuid/{parentObjectTypeGuid}/guid``."""

    async def default_relation_type_guid_by_guid(
        self: "DefaultRelationTypeGuidByGuidMixin",
        parent_object_type_guid: UUID | str,
    ) -> str:
        """Возвращает GUID типа связи по умолчанию по GUID типа объекта-родителя.

        Полностью «переносимый» вариант: и тип объекта-родителя на входе, и тип связи
        по умолчанию на выходе заданы GUID'ами (стабильными между базами). Удобно для
        кода, не привязанного к локальным числовым id. Ответ сервера — голая строка
        (UUID в текстовом виде).

        Когда применять: при построении состава между несколькими инсталляциями IPS,
        когда нужны только переносимые идентификаторы. Вариант с числовым id связи на
        выходе — :meth:`default_relation_type_id_by_guid`.

        Args:
            parent_object_type_guid: Глобальный идентификатор типа объекта-РОДИТЕЛЯ
                (``UUID`` или строка). Это GUID ТИПА объекта, не GUID конкретного
                объекта/версии. Подставляется в URL как есть.

        Returns:
            GUID типа связи по умолчанию в текстовом виде. Пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.default_relation_type_guid_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(guid)

        Notes:
            operationId ``Metadata_GetDefaultRelationTypeGuidByGuid``; путь
            ``GET /core/api/metadata/relationTypes/objectTypeDefault/byGuid/``
            ``{parentObjectTypeGuid}/guid`` (ответ — ``uuid``). Парный метод (id связи) —
            :meth:`default_relation_type_id_by_guid`.
        """
        path = (
            f"/core/api/metadata/relationTypes/objectTypeDefault/byGuid/"
            f"{parent_object_type_guid}/guid"
        )
        data = await self._request("get", path)
        return "" if data is None else str(data)
