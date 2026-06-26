"""Метод получения состава ОБЪЕКТОВ заданного типа."""

from typing import Any

from ...core import APIManager
from ...schemas.object_types.composition import (
    ObjectsCompositionParams,
    ObjectWithCompositionDto,
)


class ObjectTypeCompositionMixin(APIManager):
    """Реализует метод ``POST /core/api/objectTypes/{objectTypeId}/composition``."""

    async def object_type_composition(
        self: "ObjectTypeCompositionMixin",
        object_type_id: int,
        params: ObjectsCompositionParams | dict[str, Any] | None = None,
    ) -> list[ObjectWithCompositionDto]:
        """Возвращает состав ОБЪЕКТОВ заданного типа (объекты + их под-состав).

        Для каждого объекта указанного ТИПА отдаёт его идентификатор, дополнительно
        запрошенные атрибуты и состав (дочерние объекты со связями). Применяется,
        когда нужно разом получить структуру вложенности (BOM-подобный состав) по всем
        объектам типа, не обходя их по одному.

        POST-verb, но операция ЧТЕНИЯ (идемпотентна, ничего не мутирует): тело несёт
        параметры выборки (набор атрибутов, правило контекста версий).

        Args:
            object_type_id: Идентификатор ТИПА объекта (``ObjectTypeID`` —
                id-пространство ТИПОВ). Уходит в путь ``{objectTypeId}``. В ответе поле
                ``object_id`` каждого элемента — это id ОБЪЕКТА (``objectID``), а НЕ id
                типа: не путать пространства.
            params: Параметры запроса — :class:`ObjectsCompositionParams` или
                эквивалентный словарь, либо ``None`` (пустое тело: состав в контексте
                по умолчанию без дополнительных атрибутов). Словарь сериализуется как
                есть; модель — через ``model_dump(by_alias=True)``.

        Returns:
            Список :class:`ObjectWithCompositionDto` — по одному элементу на объект
            типа. У каждого: ``object_id`` (id объекта), ``attributes`` (запрошенные
            атрибуты), ``object_compositions`` (под-состав как «сырые» словари
            ``{"object": ObjectDto, "relation": RelationDto}``). Пустой список —
            объектов данного типа нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                params = ObjectsCompositionParams(attribute_ids=[55])
                items = await ips.object_type_composition(1742, params)
                for it in items:
                    print(it.object_id, len(it.object_compositions))

        Notes:
            operationId ``Objects_GetObjectsComposition``; путь
            ``POST /core/api/objectTypes/{objectTypeId}/composition``. Тело —
            ``ObjectsCompositionParamsDto``; ответ — массив ``ObjectWithCompositionDto``
            (не result-обёртка). ⚠️ Проверено на проде: ``params.attribute_ids`` должен
            быть НЕПУСТЫМ — при пустом наборе атрибутов сервер отвечает 500
            (``Value cannot be null``). С заданными ``attribute_ids`` возвращает состав
            корректно. См. [[ips-object-model]] (раздел «Состав»).
        """
        if isinstance(params, ObjectsCompositionParams):
            body: dict[str, Any] = params.model_dump(by_alias=True, exclude_none=True)
        else:
            body = params or {}
        path = f"/core/api/objectTypes/{object_type_id}/composition"
        data = await self._request("post", path, json=body)
        items = data if isinstance(data, list) else []
        return [ObjectWithCompositionDto.model_validate(item) for item in items]
