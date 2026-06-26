"""Метод проверки, может ли тип объекта входить в какой-либо состав."""

from ...core import APIManager


class CanEntersInMixin(APIManager):
    """Реализует ``GET .../applicabilities/canEntersIn/{partTypeId}``."""

    async def can_enters_in(
        self: "CanEntersInMixin",
        part_type_id: int,
    ) -> bool:
        """Проверяет, может ли объект данного типа входить в чей-либо состав.

        Быстрый булев флаг «снизу вверх»: задана ли хотя бы одна применяемость, в
        которой тип ``part_type_id`` выступает ПОТОМКОМ — то есть может ли объект
        этого типа быть включён в состав какого-либо родителя (по любой связи). Это
        зеркало :meth:`has_applicability`, который смотрит со стороны родителя
        («может ли в тип что-то входить»). Ответ — голое булево значение, без обёртки
        ``...NullableResultDto``.

        Когда применять: как дешёвый предварительный фильтр перед
        :meth:`object_type_parent_applicabilities` (полный список допустимых
        родителей) — чтобы не дёргать тяжёлый метод для типов, которые никуда не
        вкладываются. ``part_type_id`` берётся из :meth:`object_types` или
        :meth:`object_type_id_by_name`.

        Args:
            part_type_id: Идентификатор типа объекта-ПОТОМКА (``ObjectTypeID`` —
                id-пространство ТИПОВ объектов, не ``ObjectID``/``ID``).

        Returns:
            ``True`` — тип может входить хотя бы в один родительский тип; ``False`` —
            применяемостей с этим типом-потомком нет (вложить объект некуда).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                if await ips.can_enters_in(1755):
                    parents = await ips.object_type_parent_applicabilities(1755)

        Notes:
            operationId ``Metadata_CanEntersIn``; путь ``GET /core/api/metadata/``
            ``applicabilities/canEntersIn/{partTypeId}`` (ответ — ``boolean``). См.
            объектной модели IPS (раздел «Связи и состав»). Связанные методы:
            :meth:`object_type_parent_applicabilities`, :meth:`has_applicability`.
        """
        path = f"/core/api/metadata/applicabilities/canEntersIn/{part_type_id}"
        data = await self._request("get", path)
        return bool(data)
