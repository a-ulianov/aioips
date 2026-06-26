"""Метод проверки наличия применяемостей у типа объекта-родителя."""

from ...core import APIManager


class HasApplicabilityMixin(APIManager):
    """Реализует ``GET .../applicabilities/hasApplicability/{parentObjectTypeId}``."""

    async def has_applicability(
        self: "HasApplicabilityMixin",
        parent_object_type_id: int,
    ) -> bool:
        """Проверяет, может ли объект данного типа иметь состав (хоть одну применяемость).

        Быстрый булев флаг: задана ли для типа-родителя хотя бы одна применяемость
        (тройка тип-родителя/тип-связи/тип-потомка) — то есть может ли в объекты этого
        типа что-либо входить в состав. Ответ сервера — голое булево значение, без
        обёртки ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед запросом полного
        списка применяемостей (:meth:`object_type_applicabilities`) или построением UI
        состава — чтобы не дёргать тяжёлые методы для типов, у которых состава нет.

        Args:
            parent_object_type_id: Идентификатор типа объекта-РОДИТЕЛЯ (``ObjectTypeID``
                — id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            ``True`` — у типа есть хотя бы одна применяемость (объект может иметь состав);
            ``False`` — применяемостей нет (состав невозможен).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.has_applicability(1742):
                    rules = await ips.object_type_applicabilities(1742)

        Notes:
            operationId ``Metadata_HasApplicabilityByParentId``; путь
            ``GET /core/api/metadata/applicabilities/hasApplicability/{parentObjectTypeId}``
            (ответ — ``boolean``). См. объектной модели IPS (раздел «Связи и состав»).
            Связанный метод: :meth:`object_type_applicabilities`.
        """
        path = f"/core/api/metadata/applicabilities/hasApplicability/{parent_object_type_id}"
        data = await self._request("get", path)
        return bool(data)
