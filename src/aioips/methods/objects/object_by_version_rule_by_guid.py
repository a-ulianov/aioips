"""Метод получения версии объекта по правилу версий (по GUID объекта)."""

from urllib.parse import quote
from uuid import UUID

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectByVersionRuleByGuidMixin(APIManager):
    """Реализует ``GET /core/api/objects/byGuid/{guid}/objectByVersionRule``.

    Соответствует операции ``Objects_GetObjectByVersionRule``.
    """

    async def object_by_version_rule_by_guid(
        self: "ObjectByVersionRuleByGuidMixin",
        object_guid: UUID | str,
    ) -> ObjectDto | None:
        """Возвращает версию объекта по текущему правилу версий, по GUID объекта.

        GUID-аналог :meth:`object_by_version_rule`: разрешает актуальную в текущем
        контексте версию объекта (``VersionsRule``), когда известен GUID объекта, а не
        числовой идентификатор. Применяйте для получения «правильной» версии по GUID, не
        зная числовой ``objectID``. Только чтение — checkout не требуется.

        Предусловие по id-пространству (критично): аргумент — это ``objectGUID`` (GUID
        ОБЪЕКТА, общий для всех версий), а НЕ ``guid`` версии. По GUID версии объект этим
        методом не разрешается (вернётся ``None``).

        Args:
            object_guid: GUID ОБЪЕКТА (``objectGUID``), общий для всех версий. Принимает
                ``uuid.UUID`` или строку канонического вида ``8-4-4-4-12``; кодируется в
                URL.

        Returns:
            Выбранная версия объекта по схеме :class:`ObjectDto` или ``None``, если
            подходящая версия не найдена. Поля идентичности: ``object_id`` (объект) и
            ``id`` (версия).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                obj = await ips.object_by_version_rule_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )

        Notes:
            ``operationId``: ``Objects_GetObjectByVersionRule``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``ObjectDto | None``. См.
            :meth:`object_by_version_rule` и [[ips-object-model]] (раздел «Идентичность»).
        """
        encoded_guid = quote(str(object_guid), safe="")
        path = f"/core/api/objects/byGuid/{encoded_guid}/objectByVersionRule"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectDto.model_validate(entity) if entity is not None else None
