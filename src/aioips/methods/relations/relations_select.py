"""Метод произвольной выборки связей по типу и условиям."""

from ...schemas.relations import RelationSelectResult, RelationsSelectParameters
from ._extended_select import _ExtendedRelationSelectBase


class RelationsSelectMixin(_ExtendedRelationSelectBase):
    """Реализует ``POST /core/api/relations/select`` (``Relations_GetSelectsRelations``)."""

    async def relations_select(
        self: "RelationsSelectMixin",
        params: RelationsSelectParameters,
    ) -> list[RelationSelectResult]:
        """Произвольная выборка связей по типу, условиям и атрибутам (с пагинацией).

        read-only POST-запрос, без мутаций. В отличие от
        :meth:`relations_consist_from` / :meth:`relations_enters_in` (поиск от конкретного
        ``object_id``), этот метод перечисляет связи заданного типа в целом по базе — без
        привязки к одному объекту, с сортировкой и keyset-пагинацией. Применять для
        массовой фильтрации/выгрузки связей; для состава/вхождений одного объекта берите
        соответствующие методы.

        Пагинация keyset (не offset): продолжение страницы задаётся ``last_key_value`` и
        ``last_order_value`` из предыдущего ответа; ``record_count`` ограничивает размер
        страницы. Для устойчивого порядка фиксируйте ``sort_columns`` / ``orders`` /
        ``sort_sources``.

        id-пространство: результат адресует связи по ``relation_id`` (``RelationID``;
        нестабилен — меняется при ``CheckOut``/``CheckIn`` родителя, не кэшировать). Это
        отдельное id-пространство связей, не совпадающее с id объектов/версий.
        См. объектной модели IPS (раздел «Связи») и граблям.

        Args:
            params: Параметры выборки (см. :class:`RelationsSelectParameters`):
                ``relation_type_id`` (``-1`` — любой), ``attribute_ids_to_select``
                (обязателен, может быть пуст), условия, сортировка и keyset-курсор.

        Returns:
            Список найденных связей по схеме :class:`RelationSelectResult` (id связи +
            значения запрошенных атрибутов). Пустой список — совпадений нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations import RelationsSelectParameters

            async with IPSClient(config=config) as ips:
                results = await ips.relations_select(
                    RelationsSelectParameters(
                        relation_type_id=3,
                        attribute_ids_to_select=[12],
                        record_count=100,
                    )
                )
                for r in results:
                    print(r.relation_id, r.values.get(12))

        Notes:
            operationId ``Relations_GetSelectsRelations``; путь
            ``POST /core/api/relations/select`` (массив ``RelationSelectResultDto``).
            Поиск от объекта — :meth:`relations_consist_from` / :meth:`relations_enters_in`.
        """
        return await self._post_relation_select("/core/api/relations/select", params)
