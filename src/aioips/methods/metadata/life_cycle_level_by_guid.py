"""Метод получения уровня жизненного цикла по GUID."""

from urllib.parse import quote
from uuid import UUID

from ...core import APIManager
from ...schemas.metadata import LifeCycleLevel


class LifeCycleLevelByGuidMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}``."""

    async def life_cycle_level_by_guid(
        self: "LifeCycleLevelByGuidMixin",
        guid: UUID | str,
    ) -> LifeCycleLevel | None:
        """Возвращает описание уровня жизненного цикла по его GUID.

        GUID уровня ЖЦ стабилен между базами данных, поэтому удобен как переносимый
        ключ метаданных. Ответ сервера обёрнут в ``...NullableResultDto``
        (``{entity, isEntityPresent}``); обёртка разворачивается здесь, наружу отдаётся
        либо схема, либо ``None``.

        Когда применять: тот же результат, что у :meth:`life_cycle_level`, но ключ —
        переносимый GUID (когда числовой ``id`` между базами различается). Полезно для
        кода, работающего с несколькими инсталляциями IPS.

        Args:
            guid: Глобальный идентификатор уровня ЖЦ (``UUID`` или строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Уровень ЖЦ по схеме :class:`LifeCycleLevel` либо ``None``, если уровень с
            таким GUID не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                level = await ips.life_cycle_level_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                if level is not None:
                    print(level.id, level.name)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelByGuid``; путь
            ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}``.
            Связанный метод по числовому id — :meth:`life_cycle_level`.
        """
        encoded_guid = quote(str(guid), safe="")
        path = f"/core/api/metadata/lifeCycleLevels/byGuid/{encoded_guid}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleLevel.model_validate(entity) if entity is not None else None
