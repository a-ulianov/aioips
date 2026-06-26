"""Метод получения значений всех атрибутов связи."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import AttributeValues


class RelationAttributesValuesMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttributesValues`` (значения всех атрибутов связи)."""

    async def relation_attributes_values(
        self: "RelationAttributesValuesMixin",
        relation_id: int,
        *,
        extend_by_type: bool = False,
    ) -> list[AttributeValues]:
        """Возвращает значения всех атрибутов СВЯЗИ с расширенными метаданными.

        Самый подробный способ прочитать атрибуты связи: в отличие от
        :meth:`relation_attributes`, для каждого атрибута дополнительно отдаёт GUID,
        псевдоним, режим множественности (``MultiValueModes``) и режим вычисления
        (``ComputeValueModes``), а также извлечённые (разрешённые) значения. Связь —
        атрибутируемая сущность (``IDBAttributable``) со своими характеристиками.
        Отличие от :meth:`object_attributes_values`: тот читает атрибуты ОБЪЕКТА по
        ``objectID``, а здесь — атрибуты СВЯЗИ по ``relationID``. Применяйте, когда нужны
        эти метаданные; иначе достаточно :meth:`relation_attributes`. Только чтение —
        checkout не нужен.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).
            extend_by_type: Если ``True``, дополнить сведениями о типе атрибута
                (``attribute_type_info``). По умолчанию ``False``.

        Returns:
            Список значений атрибутов связи по схеме :class:`AttributeValues` (пустой
            список, если атрибутов нет). У каждого: ``attribute_id``, ``attribute_type``
            (``FieldTypes``), ``values``, ``multiple_valued``, ``compute_mode``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                values = await ips.relation_attributes_values(700123)
                by_id = {v.attribute_id: v.values for v in values}

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributesValues``. IPS может отдавать
            ``null`` вместо ``[]`` для пустых списков (``descriptions`` и др.) — схема это
            нормализует. См. [[gotchas]] и [[ips-object-model]] (разделы «Атрибуты»,
            «Связи и состав»).
        """
        params: dict[str, Any] = {"isNeedToExtendByAttributeType": str(extend_by_type).lower()}
        data = await self._request(
            "get", f"/core/api/relations/{relation_id}/attributesValues", params=params
        )
        items = data if isinstance(data, list) else []
        return [AttributeValues.model_validate(item) for item in items]
