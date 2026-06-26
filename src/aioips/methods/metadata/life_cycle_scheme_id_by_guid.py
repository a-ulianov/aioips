"""Метод получения идентификатора схемы жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleSchemeIdByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/id``."""

    async def life_cycle_scheme_id_by_guid(
        self: "LifeCycleSchemeIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает числовой идентификатор схемы жизненного цикла по её GUID.

        Мост «переносимый GUID → локальный id»: GUID схемы ЖЦ стабилен между базами
        данных, а числовой ``id`` различается между инсталляциями. Метод даёт локальный
        ``id``, нужный для запросов, принимающих идентификатор схемы. Ответ сервера —
        целое число, а не объект-обёртка.

        Когда применять: чтобы по известному GUID схемы получить её локальный ``id``
        перед вызовами вроде :meth:`life_cycle_scheme` или
        :meth:`life_cycle_scheme_steps`.

        Args:
            guid: Глобальный идентификатор схемы ЖЦ (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Числовой идентификатор схемы ЖЦ (id-пространство СХЕМ жизненного цикла).
            Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если схема с таким GUID
                не найдена).

        Example:
            async with IPSClient(config=config) as ips:
                scheme_id = await ips.life_cycle_scheme_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(scheme_id)

        Notes:
            operationId ``Metadata_GetLifeCycleSchemeId``; путь
            ``GET /core/api/metadata/lifeCycleSchemes/byGuid/{guid}/id``.
            Связанные методы: :meth:`life_cycle_scheme`, :meth:`life_cycle_scheme_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSchemes/byGuid/{encoded_guid}/id"
        data = await self._request("get", path)
        return int(data)
