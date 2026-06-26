"""Метод проверки наличия применяемостей у типа-родителя по GUID."""

from ...core import APIManager


class HasApplicabilityByGuidMixin(APIManager):
    """Реализует ``GET .../applicabilities/hasApplicability/byGuid/{parentObjectTypeGuid}``."""

    async def has_applicability_by_guid(
        self: "HasApplicabilityByGuidMixin",
        parent_object_type_guid: str,
    ) -> bool:
        """Проверяет, есть ли у типа-родителя (по GUID) хоть одна применяемость.

        То же, что :meth:`has_applicability`, но тип-родитель адресуется переносимым
        между базами GUID типа объекта, а не числовым ``ObjectTypeID``. Флаг отвечает
        на вопрос: задана ли для этого типа хотя бы одна применяемость (тройка
        родитель/связь/потомок) — то есть может ли в объекты данного типа что-либо
        входить в состав. Ответ — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр, когда на руках GUID типа
        (переносимый конфиг/интеграция), перед запросом полного списка
        (:meth:`object_type_applicabilities_by_guid`). GUID берётся из поля ``guid``
        :class:`ObjectType` (id-пространство ТИПОВ; не ``guid`` версии/``objectGUID``).

        Args:
            parent_object_type_guid: GUID типа объекта-РОДИТЕЛЯ (``ObjectType.guid`` —
                переносим между базами; id-пространство ТИПОВ объектов).

        Returns:
            ``True`` — у типа есть хотя бы одна применяемость (объект может иметь
            состав); ``False`` — применяемостей нет.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = "cad001c5-306c-11d8-b4e9-00304f19f545"
                if await ips.has_applicability_by_guid(guid):
                    rules = await ips.object_type_applicabilities_by_guid(guid)

        Notes:
            operationId ``Metadata_HasApplicabilityByParentGuid``; путь
            ``GET /core/api/metadata/applicabilities/hasApplicability/byGuid/``
            ``{parentObjectTypeGuid}`` (ответ — ``boolean``). См. [[ips-object-model]]
            (раздел «Связи и состав»). Связанные методы: :meth:`has_applicability`,
            :meth:`object_type_applicabilities_by_guid`.
        """
        path = (
            f"/core/api/metadata/applicabilities/hasApplicability/byGuid/{parent_object_type_guid}"
        )
        data = await self._request("get", path)
        return bool(data)
