"""Метод пакетного обновления атрибутов нескольких связей."""

from typing import Any

from ...core import APIManager


class RelationUpdateRelationsAttributesMixin(APIManager):
    """Реализует ``RelationAttributes_UpdateRelationsAttributes`` (пакетное обновление связей)."""

    async def relation_update_relations_attributes(
        self: "RelationUpdateRelationsAttributesMixin",
        body: dict[str, Any],
        *,
        log_history: bool = True,
    ) -> dict[str, Any]:
        """Пакетно обновляет атрибуты сразу нескольких связей одним запросом.

        Применяет к набору связей их новые значения атрибутов за один вызов —
        эффективнее серии :meth:`relation_set_attribute_values` по отдельным связям.
        Применяйте, когда нужно массово изменить характеристики многих связей
        (например, при перестроении состава).

        ПРЕДУСЛОВИЕ (запись связи): объекты-РОДИТЕЛИ затрагиваемых связей должны быть
        извлечены на редактирование (checkout). Метод НЕ делает checkout сам.

        Структура тела (``UpdateRelationsAttributesDto``)::

            {
              "relationsAttributes": [
                {
                  "relationId": 700123,          # id СВЯЗИ (нестабилен!)
                  "attributes": [ ... ]          # UpdateRelationAttributeDto[]
                },
                ...
              ]
            }

        Args:
            body: Тело запроса ``UpdateRelationsAttributesDto`` как словарь (ключ
                ``relationsAttributes`` — список пакетов
                ``UpdateRelationsAttributesPackageDto`` с ``relationId`` и
                ``attributes``). Тело сложное/вложенное, поэтому передаётся «сырым»
                словарём и отправляется как есть.
            log_history: Если ``True`` (по умолчанию), фиксировать операцию в журнале
                истории модификаций (query ``isNeedToLogModificationHistory``).

        Returns:
            Словарь результата ``UpdateRelationsAttributesResultDto`` — поле ``result``
            ответа: ключ ``relationIds`` со списком id реально изменённых связей.
            Пустой словарь, если сервер ничего не вернул.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родители связей не
                извлечены на редактирование).

        Example:
            async with IPSClient(config=config) as ips:
                result = await ips.relation_update_relations_attributes(
                    {
                        "relationsAttributes": [
                            {
                                "relationId": 700123,
                                "attributes": [{"attributeId": 205, "values": ["A1"]}],
                            }
                        ]
                    }
                )
                changed_ids = result.get("relationIds", [])

        Notes:
            ``operationId``: ``RelationAttributes_UpdateRelationsAttributes``. Эндпоинт
            ``POST /core/api/relations/attributes``. Тело —
            ``UpdateRelationsAttributesDto``; ответ —
            ``UpdateRelationsAttributesResultDtoProcessResultWithLogInfoDto`` (поле
            ``result``). ⚠️ ``relationId`` нестабилен (см. [[ips-object-model]]).
            Связанный метод: :meth:`relation_set_attribute_values`.
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        data = await self._request(
            "post",
            "/core/api/relations/attributes",
            json=body,
            params=params,
        )
        result = data.get("result") if isinstance(data, dict) else None
        return result if isinstance(result, dict) else {}
