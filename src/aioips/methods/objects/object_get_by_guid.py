"""Метод получения версии объекта по GUID."""

from typing import Any
from uuid import UUID

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectGetByGuidMixin(APIManager):
    """Реализует ``GET /core/api/objects/byGuid/{objectGuid}`` (``Objects_GetObjectByGuid``)."""

    async def object_get_by_guid(
        self: "ObjectGetByGuidMixin",
        object_guid: UUID | str,
        *,
        throw_not_found: bool = False,
    ) -> ObjectDto | None:
        """Возвращает полное описание объекта по GUID объекта (``objectGUID``).

        GUID-аналог :meth:`object_get`: применяйте, когда известен GUID объекта, а не
        числовой идентификатор. Возвращает то же DTO версии объекта.

        Предусловие по id-пространству (критично): аргумент — это ``objectGUID``
        (GUID ОБЪЕКТА, общий для всех версий), а НЕ ``guid`` версии. По GUID версии
        объект этим методом не достаётся (вернётся ``None``).

        Args:
            object_guid: GUID ОБЪЕКТА (``objectGUID``), общий для всех версий. Принимает
                ``uuid.UUID`` или строку канонического вида ``8-4-4-4-12``.
            throw_not_found: Если ``True``, при отсутствии объекта сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Объект по схеме :class:`ObjectDto` или ``None``, если объект не найден
            (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.object_get_by_guid("cad001c5-306c-11d8-b4e9-00304f19f545")

        Notes:
            ``operationId``: ``Objects_GetObjectByGuid``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``ObjectDto | None``.
            См. [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request("get", f"/core/api/objects/byGuid/{object_guid}", params=params)
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
