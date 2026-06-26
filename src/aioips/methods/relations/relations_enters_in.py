"""Метод расширенного поиска вхождений объекта (куда входит)."""

from ...schemas.relations import ObjectRelationsSelectParameters, RelationSelectResult
from ._extended_select import _ExtendedRelationSelectBase


class RelationsEntersInMixin(_ExtendedRelationSelectBase):
    """Реализует ``POST /core/api/relations/entersIn`` (``Relations_ExtendedEntersIn``)."""

    async def relations_enters_in(
        self: "RelationsEntersInMixin",
        params: ObjectRelationsSelectParameters,
    ) -> list[RelationSelectResult]:
        """Расширенный поиск вхождений объекта — связи к объектам, в которые он входит.

        read-only POST-запрос, без мутаций. Параметризованный запрос «куда входит объект»:
        ищет рёбра состава, где переданный объект (``params.object_id``) — потомок, а
        результат — связи к его родителям. Это вхождение БЕЗ привязки к версии (по объекту);
        версионный вариант — :meth:`relations_enters_in_version`. Зеркальный запрос «из чего
        состоит» — :meth:`relations_consist_from`.

        В отличие от скалярного :meth:`enters_in_version` (быстрый обзор по id версии без
        параметров) здесь поиск управляем: фильтры, произвольные условия (``conditions``),
        отбор атрибутов связи (``attributes_to_select``), контекст версий — и возвращаются
        записи СВЯЗЕЙ с атрибутами, а не объекты-родители.

        Предусловие по id-пространству (критично): ``params.object_id`` — идентификатор
        ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех версий, а НЕ id версии
        (``id`` / F_ID). Результат адресует связи по ``relation_id`` (нестабилен, не
        кэшировать). См. [[ips-object-model]] (раздел «Связи»).

        Args:
            params: Параметры поиска (см. :class:`ObjectRelationsSelectParameters`):
                ``object_id`` потомка, ``relation_type_id`` (``-1`` — любой),
                ``attributes_to_select`` (обязателен, может быть пуст), условия, контекст.

        Returns:
            Список найденных связей по схеме :class:`RelationSelectResult` (id связи +
            значения запрошенных атрибутов). Пустой список — объект никуда не входит
            (с учётом фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations import ObjectRelationsSelectParameters

            async with IPSClient(config=config) as ips:
                results = await ips.relations_enters_in(
                    ObjectRelationsSelectParameters(
                        object_id=102777,
                        relation_type_id=-1,
                        attributes_to_select=[],
                    )
                )
                for r in results:
                    print(r.relation_id)

        Notes:
            operationId ``Relations_ExtendedEntersIn``; путь
            ``POST /core/api/relations/entersIn`` (массив ``RelationSelectResultDto``).
            Версионный вариант — :meth:`relations_enters_in_version`; зеркальный —
            :meth:`relations_consist_from`.
        """
        return await self._post_relation_select("/core/api/relations/entersIn", params)
