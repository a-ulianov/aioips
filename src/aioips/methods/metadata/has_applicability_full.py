"""Метод проверки наличия применяемости по полной тройке идентификаторов."""

from ...core import APIManager


class HasApplicabilityFullMixin(APIManager):
    """Реализует ``GET .../applicabilities/hasApplicability/{parent}/{child}/{relation}``."""

    async def has_applicability_full(
        self: "HasApplicabilityFullMixin",
        parent_object_type_id: int,
        child_object_type_id: int,
        relation_type_id: int,
    ) -> bool:
        """Проверяет существование применяемости для конкретной тройки родитель/потомок/связь.

        Быстрый булев флаг: настроено ли правило, разрешающее объекту типа
        ``child_object_type_id`` входить по связи ``relation_type_id`` в состав
        объекта типа ``parent_object_type_id``. В отличие от
        :meth:`has_applicability` (есть ли у родителя хоть какая-то применяемость),
        здесь проверяется именно заданная тройка. Ответ — голое булево значение,
        без обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предикат валидации перед добавлением объекта в
        состав, когда родитель, потомок и тип связи уже известны. Если нужны
        параметры правила (лимит, режим), вместо флага запросите само правило —
        :meth:`applicability`.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ
                (``ObjectTypeID`` — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).
            child_object_type_id: Идентификатор типа объекта-ПОТОМКА (``ObjectTypeID``).
            relation_type_id: Идентификатор типа связи (``RelationType``).

        Returns:
            ``True`` — такая применяемость существует (вхождение допустимо);
            ``False`` — правила для этой тройки нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.has_applicability_full(1742, 1755, 501):
                    rule = await ips.applicability(1742, 1755, 501)

        Notes:
            operationId ``Metadata_HasApplicability``; путь ``GET /core/api/metadata/``
            ``applicabilities/hasApplicability/{parentObjectTypeId}/``
            ``{childObjectTypeId}/{relationTypeId}`` (ответ — ``boolean``). См.
            [[ips-object-model]] (раздел «Связи и состав»). Связанные методы:
            :meth:`applicability`, :meth:`has_applicability`.
        """
        path = (
            f"/core/api/metadata/applicabilities/hasApplicability/{parent_object_type_id}"
            f"/{child_object_type_id}/{relation_type_id}"
        )
        data = await self._request("get", path)
        return bool(data)
