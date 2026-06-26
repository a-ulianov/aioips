"""Метод получения исходных (инициализационных) значений атрибутов связи."""

from ...core import APIManager
from ...schemas.objects import AttributeValues


class RelationAttributesInitValuesMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttributesInitValues`` (исходные значения атрибутов)."""

    async def relation_attributes_init_values(
        self: "RelationAttributesInitValuesMixin",
        relation_id: int,
    ) -> list[AttributeValues]:
        """Возвращает исходные (инициализационные) значения атрибутов СВЯЗИ.

        Init-значения — это значения по умолчанию, которыми атрибуты связи заполняются при
        её создании (заданные конфигурацией типа связи), а НЕ текущие фактические значения.
        Применяйте, чтобы узнать, какими будут атрибуты вновь создаваемой связи, или для
        сравнения текущего состояния с исходным. Текущие значения читаются методом
        :meth:`relation_attributes_values` (та же схема :class:`AttributeValues`). Отличие
        от значений объекта: здесь сущность — СВЯЗЬ (``relationID``), а не объект.
        Только чтение — checkout не нужен.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).

        Returns:
            Список исходных значений атрибутов связи по схеме :class:`AttributeValues`
            (пустой список, если атрибутов нет). У каждого: ``attribute_id``,
            ``attribute_type`` (``FieldTypes``), ``values``, ``multiple_valued``,
            ``compute_mode``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                init = await ips.relation_attributes_init_values(700123)
                defaults = {v.attribute_id: v.values for v in init}

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributesInitValues``; путь
            ``GET /core/api/relations/{relationId}/attributesInitValues``. Ответ — голый
            массив ``AttributeValuesDto`` (без result-обёртки). IPS может отдавать ``null``
            вместо ``[]`` для вложенных списков — схема это нормализует. Навигация по
            составу — раздел ``relation_queries``. См. [[ips-object-model]]
            (раздел «Атрибуты»).
        """
        data = await self._request(
            "get",
            f"/core/api/relations/{relation_id}/attributesInitValues",
        )
        items = data if isinstance(data, list) else []
        return [AttributeValues.model_validate(item) for item in items]
