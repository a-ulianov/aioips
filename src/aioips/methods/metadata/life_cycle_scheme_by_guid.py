"""Метод получения схемы жизненного цикла по GUID."""

from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import LifeCycleScheme


class LifeCycleSchemeByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}``."""

    async def life_cycle_scheme_by_guid(
        self: "LifeCycleSchemeByGuidMixin",
        guid: UUID | str,
    ) -> LifeCycleScheme | None:
        """Возвращает описание схемы жизненного цикла по её GUID.

        GUID схемы ЖЦ стабилен между базами данных, поэтому удобен как переносимый
        ключ метаданных (числовой ``id`` между инсталляциями различается). Ответ
        сервера обёрнут в ``...NullableResultDto`` (``{entity, isEntityPresent}``);
        обёртка разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`life_cycle_scheme`, но ключ —
        переносимый GUID. Полезно для кода, работающего с несколькими инсталляциями
        IPS. Числовой ``id`` по GUID даёт :meth:`life_cycle_scheme_id_by_guid`.

        Args:
            guid: Глобальный идентификатор схемы ЖЦ (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Подставляется в URL как есть.

        Returns:
            Схема ЖЦ по схеме :class:`LifeCycleScheme` либо ``None``, если схема с таким
            GUID не найдена (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                scheme = await ips.life_cycle_scheme_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if scheme is not None:
                    print(scheme.id, scheme.name)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeByGuid``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}``.
            Связанный метод по числовому id — :meth:`life_cycle_scheme`.
        """
        data = await self._request("get", f"/core/api/metadata/lifeCycleSchemes/byGuid/{guid}")
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleScheme.model_validate(entity) if entity is not None else None
