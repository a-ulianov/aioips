"""Метод проверки, является ли заданный тип родительским для типа объекта."""

from typing import Any
from uuid import UUID

from ...core import APIManager


class ObjectIsParentTypeMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/isParentType``.

    Соответствует операции ``Objects_IsParentType``.
    """

    async def object_is_parent_type(
        self: "ObjectIsParentTypeMixin",
        object_id: int,
        object_type_guid: UUID | str,
    ) -> bool:
        """Проверяет, является ли тип с заданным GUID родительским для типа объекта.

        Типы объектов IPS образуют иерархию наследования. Метод отвечает, наследует ли тип
        объекта ``object_id`` (прямо или транзитивно) от типа с GUID ``object_type_guid``,
        то есть «является ли объект экземпляром (подтипом) этого типа». Применяйте для
        проверки принадлежности объекта к категории типов, не зная точный тип объекта
        (например, «является ли объект документом любого вида»). Только чтение.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID). ``object_type_guid`` — это GUID
        ТИПА объекта (из метаданных типов), не GUID объекта.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), чей тип
                проверяется. Не идентификатор версии (``id`` / F_ID).
            object_type_guid: GUID ТИПА-кандидата в родители (из метаданных типов).
                Принимает ``uuid.UUID`` или строку канонического вида ``8-4-4-4-12``;
                передаётся как query-параметр ``objectTypeGuid``.

        Returns:
            ``True``, если тип ``object_type_guid`` является родительским (или совпадает)
            для типа объекта; иначе ``False``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                is_doc = await ips.object_is_parent_type(
                    102550, "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            ``operationId``: ``Objects_IsParentType``. Ответ — голое булево
            (``type: boolean``), не result-обёртка. См. объектной модели IPS
            (раздел «Типы объектов»).
        """
        params: dict[str, Any] = {"objectTypeGuid": str(object_type_guid)}
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/isParentType", params=params
        )
        return bool(data)
