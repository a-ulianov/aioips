"""Метод получения версии объекта по идентификатору."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectGetMixin(APIManager):
    """Реализует метод ``GET /core/api/objects/{objectId}`` (``Objects_GetObject``)."""

    async def object_get(
        self: "ObjectGetMixin",
        object_id: int,
        *,
        throw_not_found: bool = False,
    ) -> ObjectDto | None:
        """Возвращает полное описание объекта (его базовую версию) по идентификатору объекта.

        Основной способ загрузить один объект целиком, когда известен его числовой
        идентификатор ОБЪЕКТА. Возвращается DTO версии объекта; для пакетного чтения по
        списку используйте :meth:`objects_collection`, для облегчённого заголовка —
        :meth:`object_info`, а для поиска по атрибутам — :meth:`objects_select`.

        Предусловие по id-пространству (критично): аргумент — это ``objectID``
        (F_OBJECT_ID), общий для всех версий объекта, а НЕ ``id`` версии (F_ID). Если
        передать идентификатор версии, сервер вернёт пустой результат и метод отдаст
        ``None`` (проверено на проде: ``object_get(F_OBJECT_ID)`` → объект,
        ``object_get(F_ID)`` → ``None``). Для доступа по GUID объекта см.
        :meth:`object_get_by_guid`.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для
                всех версий. Не идентификатор версии (``id`` / F_ID).
            throw_not_found: Если ``True``, при отсутствии объекта сервер вернёт ошибку
                (метод поднимет исключение); если ``False`` (по умолчанию) — метод
                вернёт ``None``.

        Returns:
            Объект по схеме :class:`ObjectDto` или ``None``, если объект не найден
            (и ``throw_not_found`` равно ``False``). Поля идентичности: ``object_id``
            (объект) и ``id`` (версия); ``caption`` — заголовок, ``object_type`` — тип.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.object_get(102550)  # 102550 = objectID, не версия
                if obj is not None:
                    print(obj.caption, obj.object_type)

        Notes:
            ``operationId``: ``Objects_GetObject``. Ответ сервера — result-обёртка
            ``{entity, isEntityPresent}``, которую метод разворачивает в
            ``ObjectDto | None``. См. [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request("get", f"/core/api/objects/{object_id}", params=params)
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
