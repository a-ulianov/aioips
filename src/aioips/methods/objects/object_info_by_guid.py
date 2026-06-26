"""Метод получения кратких сведений об объекте по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.objects import QuickObjectInfo


class ObjectInfoByGuidMixin(APIManager):
    """Реализует ``objects/byGuid/{objectGuid}/objectInfo`` (``Objects_GetObjectInfoByGuid``)."""

    async def object_info_by_guid(
        self: "ObjectInfoByGuidMixin",
        object_guid: UUID | str,
    ) -> QuickObjectInfo | None:
        """Возвращает краткие сведения об объекте по GUID объекта (``objectGUID``).

        GUID-аналог :meth:`object_info`: облегчённый заголовок (тип, GUID версии,
        caption) по GUID объекта. Применяйте, когда известен GUID, а полное
        :class:`ObjectDto` не требуется.

        Предусловие по id-пространству: аргумент — это ``objectGUID`` (GUID ОБЪЕКТА,
        общий для всех версий), а НЕ ``guid`` версии.

        Args:
            object_guid: GUID ОБЪЕКТА (``objectGUID``), общий для всех версий. Принимает
                ``uuid.UUID`` или строку канонического вида ``8-4-4-4-12``.

        Returns:
            Краткие сведения по схеме :class:`QuickObjectInfo` или ``None``, если объект
            не найден.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                info = await ips.object_info_by_guid("cad001c5-306c-11d8-b4e9-00304f19f545")

        Notes:
            ``operationId``: ``Objects_GetObjectInfoByGuid``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``QuickObjectInfo | None``.
        """
        data = await self._request("get", f"/core/api/objects/byGuid/{object_guid}/objectInfo")
        entity = data.get("entity") if isinstance(data, dict) else None
        return QuickObjectInfo.model_validate(entity) if entity is not None else None
