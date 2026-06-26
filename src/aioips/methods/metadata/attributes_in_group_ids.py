"""Метод получения id типов атрибутов, входящих в группу (по id группы)."""

from ...core import APIManager


class AttributesInGroupIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributesInGroup/{id}/ids``."""

    async def attributes_in_group_ids(
        self: "AttributesInGroupIdsMixin",
        attribute_group_id: int,
    ) -> list[int]:
        """Возвращает id типов атрибутов, входящих в группу (по id группы).

        Раскрывает СОСТАВ группы атрибутов: какие типы атрибутов в неё включены. Метод
        дополняет :meth:`attribute_group` (метаданные самой группы) — вместе они дают
        полную картину «группа + её содержимое». Ответ сервера — плоский массив целых,
        без обёртки ``...NullableResultDto``.

        Когда применять: для перечисления типов атрибутов группы, когда достаточно их
        числовых ``id`` (например, чтобы затем дёрнуть :meth:`attribute_type` по нужным
        ``id``). Перечень GUID — :meth:`attributes_in_group_guids`; адресация группы по
        GUID — :meth:`attributes_in_group_ids_by_guid`.

        Args:
            attribute_group_id: Идентификатор группы атрибутов (id-пространство ГРУПП
                атрибутов; не тип атрибута).

        Returns:
            Список ``id`` типов атрибутов (id-пространство ТИПОВ атрибутов), входящих в
            группу. Пустой список — группа пуста или не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                ids = await ips.attributes_in_group_ids(42)
                print(len(ids))

        Notes:
            operationId ``Metadata_GetAttributesInGroupById``; путь
            ``GET /core/api/metadata/attributesInGroup/{id}/ids`` (ответ — массив ``int``).
            Связанные методы: :meth:`attributes_in_group_guids`, :meth:`attribute_group`.
        """
        path = f"/core/api/metadata/attributesInGroup/{attribute_group_id}/ids"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
