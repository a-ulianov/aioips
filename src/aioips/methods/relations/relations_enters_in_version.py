"""Метод расширенного поиска вхождений версии объекта (куда входит версия)."""

from ...schemas.relations import ObjectRelationsSelectParameters, RelationSelectResult
from ._extended_select import _ExtendedRelationSelectBase


class RelationsEntersInVersionMixin(_ExtendedRelationSelectBase):
    """Реализует ``POST /core/api/relations/entersInVersion``.

    operationId ``Relations_ExtendedEntersInVersion``.
    """

    async def relations_enters_in_version(
        self: "RelationsEntersInVersionMixin",
        params: ObjectRelationsSelectParameters,
    ) -> list[RelationSelectResult]:
        """Расширенный поиск вхождений ВЕРСИИ объекта — связи к её родителям.

        read-only POST-запрос, без мутаций. Параметризованный запрос «куда входит данная
        версия объекта»: как :meth:`relations_enters_in`, но вхождение рассматривается с
        привязкой к конкретной версии потомка (а не к объекту в целом). Зеркальный запрос
        «из чего состоит» — :meth:`relations_consist_from`.

        В отличие от скалярного :meth:`enters_in_version` (быстрый обзор по id версии без
        параметров) здесь поиск управляем: фильтры по типам, произвольные условия
        (``conditions``), отбор атрибутов связи (``attributes_to_select``), контекст версий
        и срез на дату — и возвращаются записи СВЯЗЕЙ с атрибутами, а не объекты-родители.

        Предусловие по id-пространству (критично): ``params.object_id`` всё равно
        идентификатор ОБЪЕКТА (``objectID`` / F_OBJECT_ID); версионный срез обеспечивает
        сам эндпоинт и контекст версий (``context_rule`` / ``actual_date_time``), а не
        замена ``object_id`` на id версии. Результат адресует связи по ``relation_id``
        (нестабилен, не кэшировать). См. объектной модели IPS (раздел «Связи»).

        Args:
            params: Параметры поиска (см. :class:`ObjectRelationsSelectParameters`):
                ``object_id`` потомка, ``relation_type_id`` (``-1`` — любой),
                ``attributes_to_select`` (обязателен, может быть пуст), условия, контекст
                версий (``context_rule`` / ``actual_date_time``).

        Returns:
            Список найденных связей по схеме :class:`RelationSelectResult` (id связи +
            значения запрошенных атрибутов). Пустой список — версия никуда не входит
            (с учётом фильтров и контекста версий).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations import ObjectRelationsSelectParameters

            async with IPSClient(config=config) as ips:
                results = await ips.relations_enters_in_version(
                    ObjectRelationsSelectParameters(
                        object_id=102777,
                        relation_type_id=3,
                        attributes_to_select=[],
                    )
                )
                parents = [r.relation_id for r in results]

        Notes:
            operationId ``Relations_ExtendedEntersInVersion``; путь
            ``POST /core/api/relations/entersInVersion`` (массив ``RelationSelectResultDto``).
            Невёрсионный вариант — :meth:`relations_enters_in`; зеркальный —
            :meth:`relations_consist_from`; скалярный аналог — :meth:`enters_in_version`.
        """
        return await self._post_relation_select("/core/api/relations/entersInVersion", params)
