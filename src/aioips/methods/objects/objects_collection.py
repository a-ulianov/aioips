"""Метод пакетного получения версий объектов по списку идентификаторов."""

from typing import Any

from ...core import APIManager
from ...schemas.objects import ObjectDto


class ObjectsCollectionMixin(APIManager):
    """Реализует метод ``POST /core/api/objects/collection`` (``Objects_GetObjects``)."""

    async def objects_collection(
        self: "ObjectsCollectionMixin",
        object_ids: list[int],
        *,
        throw_not_found: bool = False,
    ) -> list[ObjectDto]:
        """Возвращает описания нескольких объектов одним запросом по списку идентификаторов.

        Пакетный аналог :meth:`object_get`: эффективнее последовательных одиночных
        вызовов при работе с группой объектов (один HTTP-запрос вместо N).

        Предусловие по id-пространству (важно): эндпоинт ``POST /objects/collection``
        принимает список идентификаторов ВЕРСИЙ (``id`` / F_ID), в отличие от
        :meth:`object_get`, который принимает ``objectID``. Типичный источник таких
        ``id`` — поля версий из ранее полученных DTO или результатов поиска.

        Args:
            object_ids: Список идентификаторов ВЕРСИЙ объектов (``id`` / F_ID).
                Не идентификаторы объектов (``objectID``).
            throw_not_found: Если ``True``, сервер вернёт ошибку при отсутствии любого из
                запрошенных объектов; если ``False`` (по умолчанию) — отсутствующие
                просто не попадут в результат (порядок и количество могут не совпасть
                со входным списком).

        Returns:
            Список объектов по схеме :class:`ObjectDto` (пустой список, если ничего не
            найдено). Каждый элемент содержит поля идентичности ``object_id`` и ``id``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                objects = await ips.objects_collection([102550, 102551])
                by_object = {o.object_id: o for o in objects}

        Notes:
            ``operationId``: ``Objects_GetObjects``. Тело запроса — голый JSON-массив
            ``list[int]``; ответ — JSON-массив ``ObjectDto`` (не result-обёртка).
            См. граблям и объектной модели IPS.
        """
        params: dict[str, Any] = {"throwNotFoundException": str(throw_not_found).lower()}
        data = await self._request(
            "post", "/core/api/objects/collection", json=object_ids, params=params
        )
        items = data if isinstance(data, list) else []
        return [ObjectDto.model_validate(item) for item in items]
