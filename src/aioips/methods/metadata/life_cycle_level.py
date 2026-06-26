"""Метод получения уровня жизненного цикла по идентификатору."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleLevel


class LifeCycleLevelMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleLevels/{id}``."""

    async def life_cycle_level(
        self: "LifeCycleLevelMixin",
        life_cycle_level_id: int,
    ) -> LifeCycleLevel | None:
        """Возвращает описание уровня жизненного цикла по его идентификатору.

        Уровень ЖЦ — слой зрелости объекта (например «Утверждено»); его описание
        содержит имя, литеру документа и идентификатор хранилища версий. Ответ сервера
        обёрнут в ``...NullableResultDto`` (``{entity, isEntityPresent}``); обёртка
        разворачивается здесь, наружу отдаётся либо схема, либо ``None``.

        Когда применять: чтобы по известному ``id`` уровня получить его полное
        метаописание (литера, хранилище, признак уровня по умолчанию). ``id`` берётся
        из :meth:`life_cycle_levels`, :meth:`life_cycle_level_id_by_guid` или из поля
        ``LifeCycleStep.level_id``. Аналог по GUID — :meth:`life_cycle_level_by_guid`.

        Args:
            life_cycle_level_id: Идентификатор уровня ЖЦ (``LifeCycleLevelID`` —
                id-пространство УРОВНЕЙ ЖЦ, не шаг ЖЦ, не ``ObjectTypeID``,
                не ``ObjectID``/``ID`` объекта или его версии).

        Returns:
            Уровень ЖЦ по схеме :class:`LifeCycleLevel` либо ``None``, если уровень с
            таким идентификатором не найден (``isEntityPresent == false``).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                level = await ips.life_cycle_level(3)
                if level is not None:
                    print(level.name, level.litera, level.storage_id)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelById``; путь
            ``GET /core/api/metadata/lifeCycleLevels/{id}``.
            Связанные методы: :meth:`life_cycle_levels`, :meth:`life_cycle_level_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleLevels/{life_cycle_level_id}"
        data = await self._request("get", path)
        entity = data.get("entity") if isinstance(data, dict) else None
        return LifeCycleLevel.model_validate(entity) if entity is not None else None
