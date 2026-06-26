"""Метод получения базовой (актуальной) версии объекта."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectBaseVersionMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/baseVersion``.

    Соответствует операции ``Objects_GetObjectBaseVersionByID``.
    """

    async def object_base_version(
        self: "ObjectBaseVersionMixin",
        object_id: int,
        *,
        throw_not_found: bool = False,
    ) -> ObjectDto | None:
        """Возвращает базовую (актуальную) версию объекта по идентификатору объекта.

        У объекта IPS может быть несколько версий; базовая (``is_base_version`` /
        F_BASE_VERSION) — его актуальная. Применяйте, когда нужно гарантированно
        получить актуальную версию, а не ту, что вернётся по контексту версий.
        Сравните с :meth:`object_get`, который тоже возвращает версию по ``objectID``.

        Предусловие по id-пространству: аргумент — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии.

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                ищется базовая версия. Не идентификатор версии (``id`` / F_ID).
            throw_not_found: Если ``True``, при отсутствии объекта сервер вернёт ошибку
                (метод поднимет исключение); если ``False`` (по умолчанию) — метод
                вернёт ``None``.

        Returns:
            Базовая версия объекта по схеме :class:`ObjectDto` или ``None``. ``None``
            отдаётся, если объект не найден ИЛИ если переданный объект сам уже является
            базовой версией / одноверсионный (отдельной «базовой версии базовой версии»
            не существует — сервер возвращает пустой результат).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                base = await ips.object_base_version(102550)
                if base is not None:
                    print(base.is_base_version, base.caption)

        Notes:
            ``operationId``: ``Objects_GetObjectBaseVersionByID``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``ObjectDto | None``.
            См. [[ips-object-model]] (раздел «Идентичность»).
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "get", f"/core/api/objects/{object_id}/baseVersion", params=params
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
