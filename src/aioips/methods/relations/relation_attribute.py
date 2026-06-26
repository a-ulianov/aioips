"""Метод получения одного атрибута связи по идентификатору типа атрибута."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import Attribute


class RelationAttributeMixin(APIManager):
    """Реализует ``RelationAttributes_GetAttribute`` (атрибут связи по id типа)."""

    async def relation_attribute(
        self: "RelationAttributeMixin",
        relation_id: int,
        attribute_id: int,
        *,
        extend_by_type: bool = False,
        throw_not_found: bool = False,
    ) -> Attribute | None:
        """Возвращает один атрибут СВЯЗИ по идентификатору типа атрибута.

        Связь — атрибутируемая сущность (``IDBAttributable``) со своими характеристиками;
        этот метод точечно читает одну из них по id типа атрибута (дешевле, чем тянуть все
        через :meth:`relation_attributes`). Отличие от :meth:`object_attribute`: тот
        адресует атрибут ОБЪЕКТА по ``objectID``, а здесь — атрибут СВЯЗИ по ``relationID``.
        Только чтение — checkout не нужен. Для одних лишь значений (без метаданных атрибута)
        есть :meth:`relation_attribute_values`.

        Args:
            relation_id: Идентификатор СВЯЗИ (``relationID``, отдельное id-пространство
                связей). ⚠️ ``relationID`` нестабилен: меняется после ``CheckOut``/
                ``CheckIn`` родителя — не кэшируйте его (см. объектной модели IPS).
            attribute_id: Идентификатор ТИПА атрибута (какую характеристику связи читать).
            extend_by_type: Если ``True``, дополнить сведениями о типе атрибута
                (``attribute_type_info``). По умолчанию ``False``.
            throw_not_found: Если ``True``, при отсутствии атрибута сервер вернёт ошибку
                (метод поднимет исключение); иначе метод вернёт ``None``.

        Returns:
            Атрибут связи по схеме :class:`Attribute` или ``None``, если он не найден
            (и ``throw_not_found`` равно ``False``).

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. 404 при ``throw_not_found``).

        Example:
            async with IPSClient(config=config) as ips:
                attr = await ips.relation_attribute(700123, 12)
                if attr is not None:
                    print(attr.as_string)

        Notes:
            ``operationId``: ``RelationAttributes_GetAttribute``. Ответ — result-обёртка
            ``{entity, isEntityPresent}``, разворачивается в ``Attribute | None``.
        """
        params: dict[str, Any] = {
            "isNeedToExtendByAttributeType": str(extend_by_type).lower(),
            "throwNotFoundException": str(throw_not_found).lower(),
        }
        data = await self._request(
            "get",
            f"/core/api/relations/{relation_id}/attributes/{attribute_id}",
            params=params,
        )
        entity = data.get("entity") if isinstance(data, dict) else None
        return Attribute.model_validate(entity) if entity is not None else None
