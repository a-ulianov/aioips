"""Методы legacy search-контроллера ``Relations`` (состав / вхождение по запросу)."""

from ...core import APIManager
from ...schemas.relations.relation_collection_request import (
    ObjectRelationDTO,
    RelationCollectionRequest,
)


class RelationsConsistFromRequestMixin(APIManager):
    """Реализует ``POST /core/api/Relations/ConsistFromRequest``.

    ``operationId`` ``Relations_ConsistFromRequest``.
    """

    async def relations_consist_from_request(
        self: "RelationsConsistFromRequestMixin",
        request: RelationCollectionRequest,
    ) -> list[ObjectRelationDTO]:
        """Возвращает рёбра состава объекта (из чего состоит) через POST-запрос.

        read-only POST-запрос альтернативного search-контроллера ``Relations`` (путь с
        ЗАГЛАВНОЙ буквы). Ищет связи состава, где переданный объект
        (``request.object_id``) — родитель. В отличие от lowercase-метода
        :meth:`relations_consist_from` (параметризованный поиск с выборкой АТРИБУТОВ
        связи через ``ObjectRelationsSelectParameters``), здесь тело —
        :class:`RelationCollectionRequest` (id объекта + флаги обхода/фильтры по типам),
        а возвращается плоский список рёбер :class:`ObjectRelationDTO` БЕЗ значений
        атрибутов связи. Поддерживает рекурсивный обход (``request.is_recure``).

        Предусловие по id-пространству (критично): ``request.object_id`` — id ОБЪЕКТА
        (F_OBJECT_ID), общий для версий, а НЕ id версии (F_ID). В ответе
        ``parent_object_id``/``object_id`` — id объектов; ``part_id`` — id ВЕРСИИ
        дочернего объекта (≠ ``object_id``). См. [[ips-object-model]].

        Args:
            request: Тело запроса (:class:`RelationCollectionRequest`): ``object_id``
                родителя, ``is_recure`` (рекурсия), ``relation_type_id`` (``-1`` —
                любой), ``object_type_id`` (``-1`` — любой), ``local_types_mode``.

        Returns:
            Список :class:`ObjectRelationDTO` — рёбра состава. Пустой список — объект
            ни из чего не состоит (с учётом фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations.relation_collection_request import (
                RelationCollectionRequest,
            )

            async with IPSClient(config=config) as ips:
                edges = await ips.relations_consist_from_request(
                    RelationCollectionRequest(object_id=102550, is_recure=False)
                )
                child_object_ids = [e.object_id for e in edges]

        Notes:
            ``operationId``: ``Relations_ConsistFromRequest``; путь
            ``POST /core/api/Relations/ConsistFromRequest`` (массив ``ObjectRelationDTO``).
            Зеркальный запрос «куда входит» — :meth:`relations_enters_in_version_request`.
            Параметризованный аналог с атрибутами — :meth:`relations_consist_from`.
        """
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request("post", "/core/api/Relations/ConsistFromRequest", json=payload)
        items = data if isinstance(data, list) else []
        return [ObjectRelationDTO.model_validate(item) for item in items]


class RelationsEntersInVersionRequestMixin(APIManager):
    """Реализует ``POST /core/api/Relations/EntersInVersionRequest``.

    ``operationId`` ``Relations_EntersInVersionRequest``.
    """

    async def relations_enters_in_version_request(
        self: "RelationsEntersInVersionRequestMixin",
        request: RelationCollectionRequest,
    ) -> list[ObjectRelationDTO]:
        """Возвращает рёбра вхождения версии объекта (куда входит) через POST-запрос.

        read-only POST-запрос альтернативного search-контроллера ``Relations`` (путь с
        ЗАГЛАВНОЙ буквы). Ищет связи, где переданный объект (``request.object_id``) —
        дочерний (входит в состав других). В отличие от lowercase-метода
        :meth:`relations_enters_in_version` (параметризованный поиск с выборкой
        АТРИБУТОВ связи), здесь тело — :class:`RelationCollectionRequest`, а
        возвращается плоский список рёбер :class:`ObjectRelationDTO` БЕЗ значений
        атрибутов связи. Поддерживает рекурсивный обход (``request.is_recure``).

        Предусловие по id-пространству (критично): ``request.object_id`` — id ОБЪЕКТА
        (F_OBJECT_ID), а НЕ id версии. В рёбрах ответа ``parent_object_id`` — родитель,
        в который входит объект; ``part_id`` — id ВЕРСИИ дочернего (≠ ``object_id``).
        См. [[ips-object-model]].

        Args:
            request: Тело запроса (:class:`RelationCollectionRequest`): ``object_id``
                дочернего объекта, ``is_recure`` (рекурсия), ``relation_type_id``
                (``-1`` — любой), ``object_type_id`` (``-1`` — любой), ``local_types_mode``.

        Returns:
            Список :class:`ObjectRelationDTO` — рёбра вхождения. Пустой список — объект
            никуда не входит (с учётом фильтров).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.relations.relation_collection_request import (
                RelationCollectionRequest,
            )

            async with IPSClient(config=config) as ips:
                edges = await ips.relations_enters_in_version_request(
                    RelationCollectionRequest(object_id=102550)
                )
                parents = [e.parent_object_id for e in edges]

        Notes:
            ``operationId``: ``Relations_EntersInVersionRequest``; путь
            ``POST /core/api/Relations/EntersInVersionRequest`` (массив ``ObjectRelationDTO``).
            Зеркальный запрос «из чего состоит» — :meth:`relations_consist_from_request`.
            Параметризованный аналог с атрибутами — :meth:`relations_enters_in_version`.
        """
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/Relations/EntersInVersionRequest", json=payload
        )
        items = data if isinstance(data, list) else []
        return [ObjectRelationDTO.model_validate(item) for item in items]
