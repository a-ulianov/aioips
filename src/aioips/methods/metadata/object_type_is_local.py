"""Метод проверки локальности типа объекта по идентификатору."""

from ...core import APIManager


class ObjectTypeIsLocalMixin(APIManager):
    """Реализует ``GET /core/api/metadata/objectTypes/{id}/isLocal``."""

    async def object_type_is_local(
        self: "ObjectTypeIsLocalMixin",
        object_type_id: int,
    ) -> bool:
        """Проверяет, является ли тип объекта локальным для текущей базы данных.

        Локальный тип объекта определён только в данной инсталляции IPS (не входит в
        общую/тиражируемую часть метаданных). Флаг важен при переносе данных и работе с
        несколькими базами: локальные типы не гарантированно совпадают между БД. Ответ
        сервера — голое булево значение, без обёртки ``...NullableResultDto``.

        Когда применять: чтобы отличить локальные типы от общесистемных перед переносом
        ссылок между инсталляциями или анализом совместимости метаданных. Аналог по GUID —
        :meth:`object_type_is_local_by_guid`.

        Args:
            object_type_id: Идентификатор типа объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            ``True`` — тип локальный для текущей базы; ``False`` — нет (в том числе если
            сервер вернул ``null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.object_type_is_local(1742):
                    print("Локальный тип — переносить ссылки осторожно")

        Notes:
            operationId ``Metadata_IsLocalObjectTypeById``; путь
            ``GET /core/api/metadata/objectTypes/{id}/isLocal`` (ответ — ``boolean``).
            Аналог по GUID — :meth:`object_type_is_local_by_guid`.
        """
        path = f"/core/api/metadata/objectTypes/{object_type_id}/isLocal"
        data = await self._request("get", path)
        return bool(data) if data is not None else False
