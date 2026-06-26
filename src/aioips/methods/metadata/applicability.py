"""Метод получения одного правила применяемости по тройке идентификаторов."""

from ...core import APIManager
from ...schemas.metadata import ObjectTypeApplicability


class ApplicabilityMixin(APIManager):
    """Реализует ``GET .../applicabilities/{parent}/{child}/{relation}``."""

    async def applicability(
        self: "ApplicabilityMixin",
        parent_object_type_id: int,
        child_object_type_id: int,
        relation_type_id: int,
    ) -> ObjectTypeApplicability | None:
        """Возвращает правило применяемости для конкретной тройки родитель/потомок/связь.

        Применяемость — правило разрешённого состава: какой тип объекта по какой
        связи допустимо включать в состав объекта другого типа. Этот метод адресно
        запрашивает ОДНО правило по полной тройке (тип-родителя, тип-потомка,
        тип-связи) и возвращает его ограничения (``relation_constraint_mode``,
        ``applicability_mode``, ``maximum_links``, ``is_content`` и др.). Ответ
        обёрнут в ``ImsApplicabilityDtoNullableResultDto`` (``{entity,
        isEntityPresent}``); обёртка разворачивается здесь.

        Когда применять: когда обе стороны и тип связи уже известны и нужно проверить
        допустимость вхождения и его параметры (валидация перед добавлением в состав).
        Для перебора всех потомков родителя — :meth:`object_type_applicabilities`;
        для быстрой проверки «существует ли такая тройка» без тела —
        :meth:`has_applicability_full`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            child_object_type_id: Идентификатор типа объекта-ПОТОМКА (``ObjectTypeID``).
            relation_type_id: Идентификатор типа связи (``RelationType``), по которой
                рассматривается вхождение.

        Returns:
            :class:`ObjectTypeApplicability` для заданной тройки либо ``None``, если
            такого правила нет (``isEntityPresent == false`` / ``entity == null``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rule = await ips.applicability(1742, 1755, 501)
                if rule is not None:
                    print(rule.maximum_links, rule.applicability_mode)

        Notes:
            operationId ``Metadata_GetApplicability``; путь ``GET /core/api/metadata/``
            ``applicabilities/{parentObjectTypeId}/{childObjectTypeId}/{relationTypeId}``
            (``ImsApplicabilityDtoNullableResultDto``). См. объектной модели IPS
            (раздел «Связи и состав»). Связанные методы:
            :meth:`has_applicability_full`, :meth:`object_type_applicabilities`.
        """
        path = (
            f"/core/api/metadata/applicabilities/{parent_object_type_id}"
            f"/{child_object_type_id}/{relation_type_id}"
        )
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return ObjectTypeApplicability.model_validate(entity) if entity is not None else None
