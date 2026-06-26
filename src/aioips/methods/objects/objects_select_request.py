"""Методы legacy search-контроллера ``Objects`` (выборка атрибутов по списку id)."""

from typing import Any

from ...core import APIManager
from ...schemas.objects.objects_select_request import (
    ObjectSelectByIdDTO,
    ObjectSelectDTO,
    ObjectSelectRequest,
)


class ObjectsSelectRequestMixin(APIManager):
    """Реализует ``POST /core/api/Objects/ObjectsSelect`` (``Objects_ObjectsSelect``)."""

    async def objects_select_request(
        self: "ObjectsSelectRequestMixin",
        request: ObjectSelectRequest,
        *,
        object_type_id: int | None = None,
    ) -> list[ObjectSelectDTO]:
        """Возвращает системные атрибуты заданных объектов (ключи-имена) через POST.

        read-only POST-запрос альтернативного search-контроллера ``Objects`` (путь с
        ЗАГЛАВНОЙ буквы). В отличие от lowercase-метода :meth:`objects_select` (фильтр
        по условиям на значения атрибутов, ``SelectCondition``), здесь объекты уже
        известны по id: тело :class:`ObjectSelectRequest` несёт список id ОБЪЕКТОВ и
        перечень обязательных системных атрибутов, а ответ — наборы значений на объект.
        Ключи словаря атрибутов в ответе — символьные ИМЕНА (``f_OBJECT_NAME`` и т.п.);
        если нужны ключи-id типов атрибутов — используйте :meth:`objects_select_by_id`.

        Предусловие по id-пространству (критично): ``request.object_ids`` — id ОБЪЕКТОВ
        (F_OBJECT_ID), общие для версий, а НЕ id версий (F_ID). В ответе ``object_id``
        тоже id объекта; ``f_ID``/``f_VERSION_ID`` среди атрибутов адресуют версию.
        См. [[ips-object-model]].

        Args:
            request: Тело запроса (:class:`ObjectSelectRequest`): ``object_ids`` (id
                объектов) и ``attributes`` (имена системных атрибутов для выборки).
            object_type_id: Необязательный фильтр/контекст по id типа объектов
                (query-параметр ``objectTypeId``). ``None`` — не передавать.

        Returns:
            Список :class:`ObjectSelectDTO` (по объекту: ``object_id`` и словарь
            ``object_attributes`` вида ``{имя_атрибута: значение}``). Пустой список —
            ничего не найдено.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects.objects_select_request import ObjectSelectRequest

            async with IPSClient(config=config) as ips:
                result = await ips.objects_select_request(
                    ObjectSelectRequest(
                        object_ids=[1311983, 1288391],
                        attributes=["f_OBJECT_NAME", "f_OWNER_CAPTION"],
                    )
                )
                for dto in result:
                    print(dto.object_id, dto.object_attributes.get("f_OBJECT_NAME"))

        Notes:
            ``operationId``: ``Objects_ObjectsSelect``; путь
            ``POST /core/api/Objects/ObjectsSelect`` (массив ``ObjectSelectDTO``).
            Значения ``attributes`` — ТОЛЬКО из перечня ``ObligatoryObjectAttributes``
            (``f_OBJECT_NAME``, ``f_OWNER_CAPTION``, ``f_VERSIONS_COUNT`` и др.);
            произвольное имя сервер отвергает с 400 (проверено на проде).
            Lowercase-аналог поиска по условиям — :meth:`objects_select`. Парный метод
            с ключами-id атрибутов — :meth:`objects_select_by_id`.
        """
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/Objects/ObjectsSelect", params=params, json=payload
        )
        items = data if isinstance(data, list) else []
        return [ObjectSelectDTO.model_validate(item) for item in items]


class ObjectsSelectByIdMixin(APIManager):
    """Реализует ``POST /core/api/Objects/ObjectsSelectById`` (``Objects_ObjectsSelectById``)."""

    async def objects_select_by_id(
        self: "ObjectsSelectByIdMixin",
        request: ObjectSelectRequest,
        *,
        object_type_id: int | None = None,
    ) -> list[ObjectSelectByIdDTO]:
        """Возвращает атрибуты заданных объектов с ключами-id атрибутов через POST.

        read-only POST-запрос альтернативного search-контроллера ``Objects`` (путь с
        ЗАГЛАВНОЙ буквы). Поведение совпадает с :meth:`objects_select_request`, но в
        ответе КЛЮЧИ словаря атрибутов — числовые id ТИПОВ атрибутов (в JSON приходят
        строками), а не их символьные имена. Применяйте, когда удобнее адресовать
        значения по id атрибута. Отличие от lowercase-метода :meth:`objects_select` —
        там фильтр по условиям, а не выборка по списку id объектов.

        Предусловие по id-пространству (критично): ``request.object_ids`` — id ОБЪЕКТОВ
        (F_OBJECT_ID), не версий. В ответе ``object_id`` — id объекта.
        См. [[ips-object-model]].

        Args:
            request: Тело запроса (:class:`ObjectSelectRequest`): ``object_ids`` (id
                объектов) и ``attributes`` (имена системных атрибутов для выборки).
            object_type_id: Необязательный фильтр/контекст по id типа объектов
                (query-параметр ``objectTypeId``). ``None`` — не передавать.

        Returns:
            Список :class:`ObjectSelectByIdDTO` (по объекту: ``object_id`` и словарь
            ``object_attributes`` вида ``{id_атрибута(str): значение}``). Пустой
            список — ничего не найдено.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.objects.objects_select_request import ObjectSelectRequest

            async with IPSClient(config=config) as ips:
                result = await ips.objects_select_by_id(
                    ObjectSelectRequest(
                        object_ids=[1311983], attributes=["f_OWNER_CAPTION"]
                    )
                )
                value = result[0].object_attributes  # ключи — id атрибутов (str)

        Notes:
            ``operationId``: ``Objects_ObjectsSelectById``; путь
            ``POST /core/api/Objects/ObjectsSelectById`` (массив ``ObjectSelectByIdDTO``).
            Значения ``attributes`` — из перечня ``ObligatoryObjectAttributes`` (как у
            :meth:`objects_select_request`). ⚠️ На обследованном билде IPS этот эндпоинт
            отвечает серверным 500 (``Value cannot be null. Parameter 'source'``)
            независимо от входа — серверная особенность ``ObjectsSelectById``, не обёртки;
            при недоступности используйте парный :meth:`objects_select_request` (ключи —
            имена атрибутов).
        """
        params: dict[str, Any] = {}
        if object_type_id is not None:
            params["objectTypeId"] = object_type_id
        payload = request.model_dump(mode="json", by_alias=True, exclude_none=True)
        data = await self._request(
            "post", "/core/api/Objects/ObjectsSelectById", params=params, json=payload
        )
        items = data if isinstance(data, list) else []
        return [ObjectSelectByIdDTO.model_validate(item) for item in items]
