"""Метод получения дочерних типов объектов по id родителя и типа связи."""

from ...core import APIManager
from ...schemas.metadata import ObjectType


class ApplicabilityChildObjectTypesMixin(APIManager):
    """Реализует ``GET .../childObjectTypes/byIds/{parentObjectTypeId}/{relationTypeId}``."""

    async def applicability_child_object_types(
        self: "ApplicabilityChildObjectTypesMixin",
        parent_object_type_id: int,
        relation_type_id: int,
    ) -> list[ObjectType] | None:
        """Возвращает полные описания дочерних типов, допустимых в составе по одной связи.

        Свёртка применяемостей до набора дочерних ТИПОВ объектов: какие типы можно
        включить в состав объекта типа ``parent_object_type_id`` по связи
        ``relation_type_id``. В отличие от :meth:`object_type_applicabilities` (правила
        :class:`ObjectTypeApplicability` с ограничениями) и
        :meth:`applicability_child_object_type_ids` (только id) — здесь возвращаются
        полные :class:`ObjectType` (имена, режим версионирования и т.п.). Ответ обёрнут
        в ``...ListNullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь.

        Когда применять: для построения UI/списка кандидатов на добавление в состав,
        когда нужны человекочитаемые имена типов, а не только их id. Если достаточно
        идентификаторов — :meth:`applicability_child_object_type_ids`. Аналог по GUID —
        :meth:`applicability_child_object_types_by_guids`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            relation_type_id: Идентификатор типа связи (``RelationType``), по которой
                ограничивается выбор допустимых потомков.

        Returns:
            Список :class:`ObjectType` либо ``None``, если применяемостей нет
            (``isEntityPresent == false`` / ``entity == null``). Пустой список —
            допустимых потомков по этой связи нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                types = await ips.applicability_child_object_types(1742, 501)
                if types is not None:
                    for object_type in types:
                        print(object_type.id, object_type.object_name)

        Notes:
            operationId ``Metadata_GetApplicabilityChildObjectTypesByIds``; путь
            ``GET /core/api/metadata/applicabilities/childObjectTypes/byIds/``
            ``{parentObjectTypeId}/{relationTypeId}`` (массив ``ImsObjectTypeDto`` в
            обёртке). См. [[ips-object-model]] (раздел «Связи и состав»). Связанные
            методы: :meth:`applicability_child_object_type_ids`,
            :meth:`applicability_child_object_types_by_guids`,
            :meth:`object_type_applicabilities`.
        """
        path = (
            "/core/api/metadata/applicabilities/childObjectTypes/byIds/"
            f"{parent_object_type_id}/{relation_type_id}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        if entity is None:
            return None
        return [ObjectType.model_validate(item) for item in entity]
