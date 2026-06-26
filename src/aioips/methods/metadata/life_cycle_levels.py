"""Метод получения списка уровней жизненного цикла."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleLevel


class LifeCycleLevelsMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleLevels``."""

    async def life_cycle_levels(self: "LifeCycleLevelsMixin") -> list[LifeCycleLevel]:
        """Возвращает список всех уровней жизненного цикла, определённых в IPS.

        Уровень ЖЦ — горизонтальный «слой зрелости» объекта (например «В разработке»,
        «Утверждено», «Архив»), общий для разных типов объектов; ему соответствует
        литера документа и физическое хранилище версий. Полный перечень уровней —
        справочник для перевода ``id``/``guid`` уровня в имя/литеру/хранилище и для
        связи с шагами ЖЦ типа объекта (``LifeCycleStep.level_id``).

        Когда применять: чтобы получить весь словарь уровней разом (например, построить
        отображение ``id → name`` или найти уровень по умолчанию через
        ``is_default``). Для точечного запроса по одному id/guid дешевле
        :meth:`life_cycle_level` / :meth:`life_cycle_level_by_guid`.

        Returns:
            Список уровней ЖЦ по схеме :class:`LifeCycleLevel`. Пустой список означает,
            что в базе не определено ни одного уровня ЖЦ.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                levels = await ips.life_cycle_levels()
                default = next((lvl for lvl in levels if lvl.is_default), None)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelList``; путь
            ``GET /core/api/metadata/lifeCycleLevels`` (массив ``ImsLifeCycleLevelDto``).
            Связанные методы: :meth:`life_cycle_level`, :meth:`life_cycle_level_by_guid`.
        """
        data = await self._request("get", "/core/api/metadata/lifeCycleLevels")
        return [LifeCycleLevel.model_validate(item) for item in data]
