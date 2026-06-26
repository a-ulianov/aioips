"""Метод получения GUID типов атрибутов, входящих в группу (по id группы)."""

from ...core import APIManager


class AttributesInGroupGuidsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/attributesInGroup/{id}/guids``."""

    async def attributes_in_group_guids(
        self: "AttributesInGroupGuidsMixin",
        attribute_group_id: int,
    ) -> list[str]:
        """Возвращает GUID типов атрибутов, входящих в группу (по id группы).

        Версия :meth:`attributes_in_group_ids`, отдающая переносимые GUID типов
        атрибутов состава группы вместо локальных ``id``. GUID стабильны между
        установками IPS, поэтому подходят для сверки конфигурации между средами. Ответ
        сервера — массив строк, без обёртки ``...NullableResultDto``.

        Когда применять: для переносимого перечисления типов атрибутов группы (сравнение
        состава между средами). Перечень числовых id — :meth:`attributes_in_group_ids`;
        адресация группы по GUID — :meth:`attributes_in_group_guids_by_guid`.

        Args:
            attribute_group_id: Идентификатор группы атрибутов (id-пространство ГРУПП
                атрибутов; не тип атрибута).

        Returns:
            Список GUID типов атрибутов (строки в id-пространстве ТИПОВ атрибутов),
            входящих в группу. Пустой список — группа пуста или не существует.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guids = await ips.attributes_in_group_guids(42)
                print(len(guids))

        Notes:
            operationId ``Metadata_GetAttributesInGroupGuidsById``; путь
            ``GET /core/api/metadata/attributesInGroup/{id}/guids`` (ответ — массив строк).
            Связанные методы: :meth:`attributes_in_group_ids`, :meth:`attribute_group`.
        """
        path = f"/core/api/metadata/attributesInGroup/{attribute_group_id}/guids"
        data = await self._request("get", path)
        return [str(item) for item in data] if data is not None else []
