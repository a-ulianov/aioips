"""Метод пакетного создания связей одним запросом (мутирующий)."""

from typing import Any

from ...core import APIManager
from ...schemas.relations import CreateRelation, Relation


class RelationCreateCollectionMixin(APIManager):
    """Реализует ``POST /core/api/relations/collection`` (``Relations_CreateRelations``)."""

    async def relation_create_collection(
        self: "RelationCreateCollectionMixin",
        relations: list[CreateRelation],
        *,
        log_history: bool = True,
    ) -> list[Relation]:
        """Создаёт сразу несколько связей «родитель → потомок» одним запросом (МУТИРУЮЩАЯ).

        Пакетный аналог :meth:`relation_create`: принимает список описаний связей и
        возвращает список созданных связей. Применяйте, когда нужно включить в состав
        несколько объектов за один вызов (меньше round-trip'ов). Каждый элемент задаёт
        тип связи, родителя (``proj_version_id`` = ``ObjectID`` родителя) и потомка
        (``part_version_id`` = ``ObjectID`` потомка; ``0`` — без привязки к версии).

        ПРЕДУСЛОВИЕ: объекты-РОДИТЕЛИ должны быть в режиме, разрешающем правку на текущем
        шаге ЖЦ (как правило — извлечены на редактирование, checkout). Внимание на
        id-пространство: концы связей — ``ObjectID`` объектов, а НЕ ``ID`` версий
        (см. [[ips-object-model]]).

        Args:
            relations: Список описаний создаваемых связей (схема :class:`CreateRelation`).
                Тело запроса — голый JSON-массив ``CreateRelationDto``; каждый элемент
                сериализуется через ``model_dump(mode="json", by_alias=True,
                exclude_none=True)``.
            log_history: Если ``True`` (по умолчанию), сервер логирует историю
                модификаций (query ``isNeedToLogModificationHistory``); ``False`` — без
                журналирования.

        Returns:
            Список созданных связей (схема :class:`Relation`) из поля ``result`` ответа
            ``RelationDtoListProcessResultWithLogInfoDto``. Пустой список, если сервер не
            вернул ``result``. Внимание: ``relation_id`` нестабилен, не кэшируйте.

        Raises:
            IPSError: При ошибочном ответе сервера (в т.ч. если родитель не извлечён на
                редактирование или тип связи недопустим для пары объектов).

        Example:
            from aioips.schemas.relations import CreateRelation

            async with IPSClient(config=config) as ips:
                rels = await ips.relation_create_collection(
                    [
                        CreateRelation(relation_type=1, proj_version_id=102550,
                                       part_version_id=102777),
                        CreateRelation(relation_type=1, proj_version_id=102550,
                                       part_version_id=102888),
                    ]
                )

        Notes:
            ``operationId``: ``Relations_CreateRelations``. Связанные:
            :meth:`relation_create`, :meth:`relation_delete`. См. [[ips-object-model]]
            («Связи и состав»).
        """
        params: dict[str, Any] = {"isNeedToLogModificationHistory": str(log_history).lower()}
        payload = [r.model_dump(mode="json", by_alias=True, exclude_none=True) for r in relations]
        data = await self._request(
            "post", "/core/api/relations/collection", json=payload, params=params
        )
        result = data.get("result") if isinstance(data, dict) else None
        items = result if isinstance(result, list) else []
        return [Relation.model_validate(item) for item in items]
