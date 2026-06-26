"""Метод получения имени схемы жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleSchemeNameMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/{id}/name``."""

    async def life_cycle_scheme_name(
        self: "LifeCycleSchemeNameMixin",
        scheme_id: int,
    ) -> str:
        """Возвращает имя схемы жизненного цикла по её идентификатору.

        Мост «id → имя»: переводит числовой ``id`` схемы ЖЦ в человекочитаемое имя
        из метаданных (для логов, UI, отчётов), не загружая полное метаописание
        (:meth:`life_cycle_scheme`). Ответ сервера — строка (имя), а не объект-обёртка.

        Когда применять: чтобы показать понятное имя по уже известному ``id`` (например,
        из :meth:`life_cycle_schemes`). Аналог по GUID —
        :meth:`life_cycle_scheme_name_by_guid`.

        Args:
            scheme_id: Идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла,
                не ``ObjectTypeID`` и не идентификатор шага ЖЦ).

        Returns:
            Имя схемы ЖЦ как строка. Пустая строка, если сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если схема с таким
                ``id`` не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                name = await ips.life_cycle_scheme_name(100)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeNameById``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/{id}/name``. Связанные методы:
            :meth:`life_cycle_scheme_name_by_guid`, :meth:`life_cycle_scheme`.
        """
        path = f"/core/api/metadata/lifeCycleSchemes/{scheme_id}/name"
        data = await self._request("get", path)
        return "" if data is None else str(data)
