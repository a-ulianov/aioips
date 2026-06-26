"""Метод расширенного поиска состава объекта (из чего состоит)."""

from ...schemas.relations import ObjectRelationsSelectParameters, RelationSelectResult
from ._extended_select import _ExtendedRelationSelectBase


class RelationsConsistFromMixin(_ExtendedRelationSelectBase):
    """Реализует ``POST /core/api/relations/consistFrom`` (``Relations_ExtendedConsistFrom``)."""

    async def relations_consist_from(
        self: "RelationsConsistFromMixin",
        params: ObjectRelationsSelectParameters,
    ) -> list[RelationSelectResult]:
        """Расширенный поиск состава объекта — связи к объектам, из которых он состоит.

        read-only POST-запрос, без мутаций. Параметризованный аналог «из чего состоит»:
        ищет рёбра состава, где переданный объект (``params.object_id``) — родитель.
        В отличие от скалярного :meth:`consist_from` (быстрый обзор по id объекта без
        параметров), здесь поиск управляем: фильтры по типам потомков, произвольные
        условия (``conditions``), отбор конкретных атрибутов связи (``attributes_to_select``),
        контекст версий и срез на дату — а возвращаются записи СВЯЗЕЙ с их атрибутами,
        а не объекты-потомки.

        Предусловие по id-пространству (критично): ``params.object_id`` — идентификатор
        ОБЪЕКТА (``objectID`` / F_OBJECT_ID), общий для всех версий, а НЕ идентификатор
        версии (``id`` / F_ID). Результат адресует связи по ``relation_id`` (нестабилен,
        не кэшировать). См. [[ips-object-model]] (раздел «Связи»).

        Args:
            params: Параметры поиска (см. :class:`ObjectRelationsSelectParameters`):
                ``object_id`` родителя, ``relation_type_id`` (``-1`` — любой),
                ``attributes_to_select`` (обязателен, может быть пуст), условия, контекст.

        Returns:
            Список найденных связей по схеме :class:`RelationSelectResult` (id связи +
            значения запрошенных атрибутов). Пустой список — объект ни из чего не состоит
            (с учётом фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations import ObjectRelationsSelectParameters

            async with IPSClient(config=config) as ips:
                results = await ips.relations_consist_from(
                    ObjectRelationsSelectParameters(
                        object_id=102550,
                        relation_type_id=-1,
                        attributes_to_select=[{"attributeId": 12}],
                    )
                )
                for r in results:
                    print(r.relation_id, r.values)

        Notes:
            operationId ``Relations_ExtendedConsistFrom``; путь
            ``POST /core/api/relations/consistFrom`` (массив ``RelationSelectResultDto``).
            Зеркальные запросы «куда входит» — :meth:`relations_enters_in` /
            :meth:`relations_enters_in_version`. Скалярный аналог — :meth:`consist_from`.
        """
        return await self._post_relation_select("/core/api/relations/consistFrom", params)
