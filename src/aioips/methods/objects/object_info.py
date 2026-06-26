"""Метод получения кратких сведений об объекте по идентификатору."""

from ...core import APIManager
from ...schemas.objects import QuickObjectInfo


class ObjectInfoMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/objectInfo`` (``Objects_GetObjectInfo``)."""

    async def object_info(
        self: "ObjectInfoMixin",
        object_id: int,
    ) -> QuickObjectInfo | None:
        """Возвращает краткие сведения об объекте по идентификатору объекта.

        Облегчённый аналог :meth:`object_get`: отдаёт только заголовок, тип и GUID
        версии. Применяйте, когда полное :class:`ObjectDto` не нужно (например, для
        проверки существования объекта или построения списка/ссылки) — дешевле и быстрее.

        Предусловие по id-пространству: аргумент — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии. По GUID см. :meth:`object_info_by_guid`.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).

        Returns:
            Краткие сведения по схеме :class:`QuickObjectInfo` или ``None``, если объект
            не найден. Поля: ``object_id`` (объект), ``id`` (версия), ``caption``,
            ``object_type_id``, ``version_guid``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_info(102550)
                exists = info is not None

        Notes:
            ``operationId``: ``Objects_GetObjectInfo``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``QuickObjectInfo | None``.
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/objectInfo")
        entity = data.get("entity") if isinstance(data, dict) else None
        return QuickObjectInfo.model_validate(entity) if entity is not None else None
