"""Метод создания связи между информационными объектами (мутирующий)."""

from typing import Any

from ...core import APIManager
from ...schemas.relations import CreateRelation, Relation


class RelationCreateMixin(APIManager):
    """Реализует ``POST /core/api/relations`` (``Relations_CreateRelation``)."""

    async def relation_create(
        self: "RelationCreateMixin",
        relation: CreateRelation,
        *,
        log_history: bool = True,
    ) -> Relation:
        """Создаёт связь «родитель → потомок» в составе изделия (МУТИРУЮЩАЯ операция).

        Связь в IPS направленная: родитель задаётся ``proj_version_id`` (``ObjectID``
        объекта-родителя, общий для всех его версий), потомок — ``part_version_id``
        (``ObjectID`` объекта-потомка; ``0`` — без привязки к конкретной версии). Тип
        связи (``relation_type``) берётся из справочника типов (см. :meth:`relation_types`).
        Применяйте, когда нужно включить объект в состав другого. Для пакетного создания
        нескольких связей за один запрос используйте :meth:`relation_create_collection`.

        ПРЕДУСЛОВИЕ: объект-РОДИТЕЛЬ должен быть в режиме, разрешающем правку на текущем
        шаге ЖЦ (как правило — извлечён на редактирование, checkout). Без этого сервер
        вернёт ошибку. Внимание на id-пространство: оба конца — ``ObjectID`` объектов,
        а НЕ ``ID`` версий (см. [[ips-object-model]]).

        Args:
            relation: Описание создаваемой связи (схема :class:`CreateRelation`): тип,
                родитель (``proj_version_id``), потомок (``part_version_id``) и
                опциональные атрибуты связи. Сериализуется через
                ``model_dump(mode="json", by_alias=True, exclude_none=True)``.
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций (query ``isNeedToLogModificationHistory``); ``False`` — без
                журналирования.

        Returns:
            Созданная связь (схема :class:`Relation`) из поля ``result`` ответа
            ``RelationDtoProcessResultWithLogInfoDto``. Внимание: ``relation_id`` нестабилен
            и не должен кэшироваться.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель не извлечён на
                редактирование или тип связи недопустим для этих объектов).

        Example:
            from aioips.schemas.relations import CreateRelation

            async with IPSClient(config=config) as ips:
                # Предполагается, что родитель уже на checkout.
                rel = await ips.relation_create(
                    CreateRelation(
                        relation_type=1,
                        proj_version_id=102550,  # ObjectID родителя
                        part_version_id=102777,  # ObjectID потомка
                    )
                )

        Notes:
            ``operationId``: ``Relations_CreateRelation``. Связанные:
            :meth:`relation_create_collection`, :meth:`relation_delete`,
            :meth:`relation_set_attributes`. См. [[ips-object-model]] («Связи и состав»).
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        payload = relation.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/relations", json=payload, params=params)
        result = data.get("result") if isinstance(data, dict) else None
        return Relation.model_validate(result)
