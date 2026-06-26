"""Метод получения идентификатора шага жизненного цикла по GUID."""

from urllib.parse import quote

from ...core import APIManager


class LifeCycleStepIdByGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/id``."""

    async def life_cycle_step_id_by_guid(
        self: "LifeCycleStepIdByGuidMixin",
        guid: str,
    ) -> int:
        """Возвращает числовой идентификатор шага жизненного цикла по его GUID.

        Мост «переносимый GUID → локальный id»: GUID шага ЖЦ стабилен между базами
        данных, а числовой ``id`` различается между инсталляциями. Метод даёт локальный
        ``id``, нужный для запросов, принимающих идентификатор шага ЖЦ. Ответ сервера —
        целое число (идентификатор), а не объект-обёртка.

        Когда применять: чтобы по известному GUID шага получить его локальный ``id``
        перед вызовами вроде :meth:`life_cycle_step`, :meth:`life_cycle_step_name` или
        :meth:`life_cycle_step_exists`. Обратное преобразование —
        :meth:`life_cycle_step_guid`.

        Args:
            guid: Глобальный идентификатор шага ЖЦ (строка вида
                ``"11111111-2222-3333-4444-555555555555"``). Кодируется в URL.

        Returns:
            Числовой идентификатор шага ЖЦ (id-пространство ШАГОВ жизненного цикла).
            Сервер не возвращает ``None``: при отсутствии GUID — ошибка.

        Raises:
            IPSError: При ошибочном ответе сервера (в том числе если шаг с таким GUID не
                найден).

        Example:
            async with IPSClient(config=config) as ips:
                step_id = await ips.life_cycle_step_id_by_guid(
                    "11111111-2222-3333-4444-555555555555"
                )
                print(step_id)

        Notes:
            operationId ``Metadata_GetLifeCycleStepId``; путь
            ``GET /core/api/metadata/lifeCycleSteps/byGuid/{guid}/id``.
            Связанные методы: :meth:`life_cycle_step`, :meth:`life_cycle_step_guid`.
        """
        encoded_guid = quote(guid, safe="")
        path = f"/core/api/metadata/lifeCycleSteps/byGuid/{encoded_guid}/id"
        data = await self._request("get", path)
        return int(data)
