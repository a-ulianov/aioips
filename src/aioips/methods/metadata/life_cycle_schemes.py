"""Метод получения списка схем жизненного цикла."""

from ...core import APIManager
from ...schemas.metadata import LifeCycleScheme


class LifeCycleSchemesMixin(APIManager):
    """Реализует метод ``GET /core/api/metadata/lifeCycleSchemes``."""

    async def life_cycle_schemes(self: "LifeCycleSchemesMixin") -> list[LifeCycleScheme]:
        """Возвращает список всех схем жизненного цикла, определённых в метаданных IPS.

        Схема ЖЦ — это именованный набор шагов (состояний) с правилами продвижения,
        на который ссылаются типы объектов; на каждом шаге задан режим правки
        атрибутов (``ObjectModifyModes``). Метод отдаёт полный справочник схем разом.
        Одна из схем может быть помечена как схема по умолчанию (``is_default``).
        Ответ сервера — голый массив ``ImsLifeCycleSchemeDto``, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы получить весь словарь схем ЖЦ (например, построить
        отображение ``id → name`` или найти схему по умолчанию). Для точечного запроса
        по одному id/GUID дешевле :meth:`life_cycle_scheme` /
        :meth:`life_cycle_scheme_by_guid`; шаги конкретной схемы — у
        :meth:`life_cycle_scheme_steps`.

        Returns:
            Список схем ЖЦ по схеме :class:`LifeCycleScheme`. Пустой список означает,
            что в базе не определено ни одной схемы жизненного цикла.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                schemes = await ips.life_cycle_schemes()
                by_name = {s.name: s.id for s in schemes}
                default = next((s for s in schemes if s.is_default), None)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeList``; путь
            ``GET /core/api/metadata/lifeCycleSchemes`` (массив ``ImsLifeCycleSchemeDto``).
            Связанные методы: :meth:`life_cycle_scheme`, :meth:`life_cycle_scheme_steps`.
        """
        data = await self._request("get", "/core/api/metadata/lifeCycleSchemes")
        return [LifeCycleScheme.model_validate(item) for item in data]
