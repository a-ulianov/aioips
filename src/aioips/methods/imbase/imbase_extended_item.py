"""Метод получения расширенных настроек типа атрибута, связанного с IMBASE."""

from ...core import APIManager
from ...schemas.imbase import ImBaseExtendedItem


class ImBaseExtendedItemMixin(APIManager):
    """Реализует ``GET /core/api/imbase/extendedItem/{attributeTypeId}``."""

    async def imbase_extended_item(
        self: "ImBaseExtendedItemMixin",
        attribute_type_id: int,
    ) -> ImBaseExtendedItem | None:
        """Возвращает расширенные настройки IMBASE для типа атрибута.

        Отдаёт, из каких каталогов IMBASE и в каком режиме выбора можно задавать
        значения для указанного типа атрибута (атрибута-ссылки на справочник).
        Используется для подготовки UI выбора значения такого атрибута.

        Когда применять: перед построением диалога/списка выбора значения атрибута,
        связанного с IMBASE. ``attribute_type_id`` берётся из метаданных типа атрибута
        (например, :meth:`attribute_type_id_by_name`). Ответ обёрнут в
        ``...NullableResultDto`` и разворачивается здесь.

        Args:
            attribute_type_id: Идентификатор ТИПА атрибута (``AttributeTypeID`` —
                id-пространство типов атрибутов, не id конкретного значения).

        Returns:
            Настройки по схеме :class:`ImBaseExtendedItem` либо ``None``, если для
            типа атрибута нет связи с IMBASE (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                item = await ips.imbase_extended_item(1029)
                if item is not None:
                    print(item.select_mode, item.catalog_ids)

        Notes:
            operationId ``ImBase_GetExtendedItem``; путь
            ``GET /core/api/imbase/extendedItem/{attributeTypeId}``.
            Ответ — ``ImBaseExtendedItemDtoNullableResultDto`` (``{entity,
            isEntityPresent}``). См. [[ips-object-model]].
        """
        data = await self._request("get", f"/core/api/imbase/extendedItem/{attribute_type_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ImBaseExtendedItem.model_validate(entity) if entity is not None else None
