"""Метод получения версии объекта по правилу версий (по id объекта)."""

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectByVersionRuleMixin(APIManager):
    """Реализует ``GET /core/api/objects/{objectId}/objectByVersionRule``.

    Соответствует операции ``Objects_GetObjectByVersionRuleById``.
    """

    async def object_by_version_rule(
        self: "ObjectByVersionRuleMixin",
        object_id: int,
    ) -> ObjectDto | None:
        """Возвращает версию объекта, выбранную текущим правилом версий, по id объекта.

        Разрешает, какая версия объекта актуальна в текущем контексте выбора версий
        (``VersionsRule`` сессии/процесса), и возвращает её DTO. В отличие от
        :meth:`object_get` (всегда базовая версия по ``objectID``), результат зависит от
        активного правила версий — это «правильная» версия для текущего контекста.
        Отличается от :meth:`object_by_versions_rule`, которому правило задаётся явным
        ``rule_object_id``: здесь правило берётся из текущего контекста. GUID-аналог —
        :meth:`object_by_version_rule_by_guid`. Только чтение — checkout не требуется.

        Предусловие по id-пространству: ``object_id`` — это ``objectID`` (F_OBJECT_ID),
        общий для всех версий, а НЕ ``id`` версии (F_ID).

        Args:
            object_id: Идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID), для которого
                по правилу версий выбирается конкретная версия. Не идентификатор версии
                (``id`` / F_ID).

        Returns:
            Выбранная версия объекта по схеме :class:`ObjectDto` или ``None``, если
            подходящая версия не найдена. Поля идентичности: ``object_id`` (объект) и
            ``id`` (версия); ``caption`` — заголовок.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.object_by_version_rule(102550)
                if obj is not None:
                    print(obj.object_id, obj.id, obj.caption)

        Notes:
            ``operationId``: ``Objects_GetObjectByVersionRuleById``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``ObjectDto | None``. См.
            :meth:`object_by_version_rule_by_guid` и объектной модели IPS (раздел
            «Идентичность»).
        """
        data = await self._request("get", f"/core/api/objects/{object_id}/objectByVersionRule")
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
