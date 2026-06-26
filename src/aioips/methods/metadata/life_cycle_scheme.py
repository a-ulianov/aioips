"""Метод получения схемы жизненного цикла по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleScheme


class LifeCycleSchemeMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSchemes/{id}``."""

    async def life_cycle_scheme(
        self: "LifeCycleSchemeMixin",
        scheme_id: int,
    ) -> LifeCycleScheme | None:
        """Возвращает описание схемы жизненного цикла по её идентификатору.

        Схема ЖЦ — именованный набор шагов (состояний) с правилами продвижения; её
        идентификатор задаёт «пространство схем ЖЦ» и служит ключом для запроса шагов
        и проверок. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` схемы получить её метаописание
        (имя, область, признак схемы по умолчанию). ``id`` берётся из
        :meth:`life_cycle_schemes` или :meth:`life_cycle_scheme_id_by_guid`. Аналог по
        GUID — :meth:`life_cycle_scheme_by_guid`; шаги схемы — :meth:`life_cycle_scheme_steps`.

        Args:
            scheme_id: Идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла,
                не ``ObjectTypeID`` и не идентификатор шага ЖЦ).

        Returns:
            Схема ЖЦ по схеме :class:`LifeCycleScheme` либо ``None``, если схема с таким
            идентификатором не найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                scheme = await ips.life_cycle_scheme(100)
                if scheme is not None:
                    print(scheme.name, scheme.is_default)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeById``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/{id}``.
            Связанные методы: :meth:`life_cycle_schemes`, :meth:`life_cycle_scheme_by_guid`,
            :meth:`life_cycle_scheme_steps`.
        """
        data = await self._request("get", f"/core/api/metadata/lifeCycleSchemes/{scheme_id}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleScheme.model_validate(entity) if entity is not None else None
