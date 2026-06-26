"""Метод получения всех правил применяемости объектной модели IPS."""

from ...core import APIManager
from ...schemas.metadata import ObjectTypeApplicability


class ApplicabilitiesMixin(APIManager):
    """Реализует ``GET /core/api/metadata/applicabilities``."""

    async def applicabilities(
        self: "ApplicabilitiesMixin",
    ) -> list[ObjectTypeApplicability]:
        """Возвращает ВСЕ настроенные в базе правила применяемости.

        Применяемость — правило разрешённого состава: тройка
        (тип-родителя ``in_object_type_id`` → тип-связи ``relation_type_id`` →
        тип-потомка ``child_object_type_id``), задающая, какой тип объекта по какой
        связи допустимо включать в состав объекта другого типа. Этот метод отдаёт
        полный набор таких правил всей базы — без фильтра по типу. Ответ — голый
        массив ``ImsApplicabilityDto`` (без обёртки ``...NullableResultDto``).

        Когда применять: для разовой выгрузки/анализа всей матрицы применяемостей
        (построение справочника состава, аудит, кэш). Для адресных запросов по
        конкретному типу используйте :meth:`object_type_applicabilities` (потомки
        родителя) или :meth:`object_type_parent_applicabilities` (родители потомка),
        а для одной тройки — :meth:`applicability`. Связь с составом объектов —
        ``relation_queries.consist_from`` (фактический состав конкретного объекта).

        Returns:
            Список :class:`ObjectTypeApplicability` со всеми правилами базы. Пустой
            список — применяемости не настроены. ``None`` метод не возвращает.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                rules = await ips.applicabilities()
                for rule in rules:
                    print(rule.in_object_type_id, rule.child_object_type_id)

        Notes:
            operationId ``Metadata_GetApplicabilities``; путь
            ``GET /core/api/metadata/applicabilities`` (голый массив
            ``ImsApplicabilityDto``). См. [[ips-object-model]] (раздел «Связи и
            состав»). Связанные методы: :meth:`applicability`,
            :meth:`object_type_applicabilities`,
            :meth:`object_type_parent_applicabilities`.
        """
        data = await self._request("get", "/core/api/metadata/applicabilities")
        items = data if isinstance(data, list) else []
        return [ObjectTypeApplicability.model_validate(item) for item in items]
