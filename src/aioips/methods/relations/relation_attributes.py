"""Метод получения всех атрибутов связи."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class RelationAttributesMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttributes`` (все атрибуты связи)."""

    async def relation_attributes(
        self: "RelationAttributesMixin",
        relation_id: int,
        *,
        extend_by_type: bool = False,
    ) -> list[Attribute]:
        """Возвращает все атрибуты СВЯЗИ вместе с их значениями.

        Связь в IPS — это атрибутируемая сущность (``IDBAttributable``): помимо объектов,
        собственные характеристики несёт и сама связь (например, позиционное обозначение
        или количество в составе изделия). Этот метод читает атрибуты именно связи, а не
        её объектов-концов. Отличие от :meth:`object_attributes`: тот работает с
        идентификатором ОБЪЕКТА (``objectID``), а здесь — с идентификатором СВЯЗИ
        (``relationID``). Только чтение — режим редактирования (checkout) не требуется.

        Для одного атрибута связи используйте :meth:`relation_attribute`; для расширенных
        метаданных (GUID, псевдоним, режимы множественности/вычисления) —
        :meth:`relation_attributes_values`.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. [[ips-object-model]]).
            extend_by_type: Если ``True``, дополнить каждый атрибут сведениями о типе
                (поле ``attribute_type_info``). По умолчанию ``False``.

        Returns:
            Список атрибутов связи по схеме :class:`Attribute` (пустой список, если их
            нет). У каждого: ``attribute_id`` (тип атрибута), ``name``, ``as_string``,
            ``values`` (типы зависят от ``data_type`` — см. ``FieldTypes``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                attributes = await ips.relation_attributes(700123)
                values = {a.name: a.as_string for a in attributes}

        Notes:
            ``operationId``: ``RelationAttributes_GetAttributes``. Видимость и права
            доступа влияют на состав возвращаемых атрибутов. См. [[ips-object-model]]
            (разделы «Атрибуты», «Связи и состав»).
        """
        params: dict[str, Any] = {"isNeedToExtendByAttributeType": str(extend_by_type).lower()}
        data = await self._request(
            "get", f"/core/api/relations/{relation_id}/attributes", params=params
        )
        items = data if isinstance(data, list) else []
        return [Attribute.model_validate(item) for item in items]
