"""Метод получения id атрибутов-ссылок, целящихся в тип объекта."""

from ...core import APIManager


class ObjectLinkAttributeTypeIdsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/objectLinkAttributeTypeIds/{objectTypeId}``."""

    async def object_link_attribute_type_ids(
        self: "ObjectLinkAttributeTypeIdsMixin",
        object_type_id: int,
    ) -> list[int]:
        """Возвращает id типов атрибутов-ссылок, которые могут указывать на тип объекта.

        Обратное направление к :meth:`attribute_linked_object_type_ids`: по типу объекта
        перечисляет типы атрибутов-ссылок (``ftObjectLink``), способных ссылаться на
        объекты этого типа. Ответ сервера — плоский массив целых, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы понять, через какие атрибуты-ссылки на объекты данного
        типа можно ссылаться (анализ связности модели, поиск «обратных» ссылок). Прямое
        направление — :meth:`attribute_linked_object_type_ids`.

        Args:
            object_type_id: Идентификатор ТИПА объекта (id-пространство типов объектов
                метаданных, не id объекта/версии).

        Returns:
            Список ``id`` типов атрибутов-ссылок (id-пространство ТИПОВ атрибутов),
            способных ссылаться на объекты данного типа. Пустой список — таких нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attr_ids = await ips.object_link_attribute_type_ids(1742)
                print(attr_ids)

        Notes:
            operationId ``Metadata_GetObjectLinkAttributeTypeIds``; путь
            ``GET /core/api/metadata/objectLinkAttributeTypeIds/{objectTypeId}`` (ответ —
            массив ``int``). Связанные методы: :meth:`attribute_linked_object_type_ids`.
        """
        path = f"/core/api/metadata/objectLinkAttributeTypeIds/{object_type_id}"
        data = await self._request("get", path)
        return [int(item) for item in data] if data is not None else []
