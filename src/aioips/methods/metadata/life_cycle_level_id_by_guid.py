"""Метод получения идентификатора уровня жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleLevelIdByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}/id``."""

    async def life_cycle_level_id_by_guid(
        self: "LifeCycleLevelIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает числовой идентификатор уровня жизненного цикла по его GUID.

        Мост «переносимый GUID → локальный id»: GUID уровня ЖЦ стабилен между базами
        данных, а числовой ``LifeCycleLevelID`` различается между инсталляциями. Метод
        даёт локальный ``id``, нужный для запросов, принимающих id уровня. Ответ
        сервера — целое число (идентификатор), а не объект-обёртка.

        Когда применять: чтобы по известному GUID уровня получить его локальный ``id``
        перед вызовами вроде :meth:`life_cycle_level` или :meth:`life_cycle_level_name`.
        Обратное преобразование — :meth:`life_cycle_level_guid`.

        Args:
            guid: Глобальный идентификатор уровня ЖЦ (строка вида
                ``"cad001c5-306c-11d8-b4e9-00304f19f545"``). Кодируется в URL.

        Returns:
            Числовой идентификатор уровня ЖЦ (``LifeCycleLevelID`` — id-пространство
            УРОВНЕЙ ЖЦ). Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если уровень с таким
                GUID не найден).

        Example:
            async with IPSClient(config=config) as ips:
                level_id = await ips.life_cycle_level_id_by_guid(
                    "cad001c5-306c-11d8-b4e9-00304f19f545"
                )
                print(level_id)

        Notes:
            operationId ``Metadata_GetLifeCycleLevelId``; путь
            ``GET /core/api/metadata/lifeCycleLevels/byGuid/{guid}/id``.
            Обратное преобразование — :meth:`life_cycle_level_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleLevels/byGuid/{encoded_guid}/id"
        data = await self._request("get", path)
        return int(data)
