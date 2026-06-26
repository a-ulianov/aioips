"""Метод получения GUID шага жизненного цикла по идентификатору."""

from ...core import APIManager


class LifeCycleStepGuidMixin(APIManager):
    """Реализует ``GET /core/api/metadata/lifeCycleSteps/{id}/guid``."""

    async def life_cycle_step_guid(
        self: "LifeCycleStepGuidMixin",
        life_cycle_step_id: int,
    ) -> str:
        """Возвращает GUID шага жизненного цикла по его числовому идентификатору.

        Мост «локальный id → переносимый GUID»: числовой ``id`` шага ЖЦ различается между
        инсталляциями, а GUID шага стабилен между базами данных и удобен как переносимый
        ключ метаданных. Ответ сервера — голая строка GUID, без обёртки
        ``...NullableResultDto``.

        Когда применять: чтобы по локальному ``id`` шага получить его GUID для хранения
        переносимых ссылок или последующих вызовов ``...ByGuid`` (например
        :meth:`life_cycle_step_by_guid`, :meth:`life_cycle_step_id_by_guid`). Обратное
        преобразование — :meth:`life_cycle_step_id_by_guid`.

        Args:
            life_cycle_step_id: Идентификатор шага ЖЦ (id-пространство ШАГОВ жизненного
                цикла — глобальное, общее для всех схем; не ``ObjectTypeID`` и не
                ``ObjectID``/``ID``).

        Returns:
            GUID шага ЖЦ строкой (например
            ``"11111111-2222-3333-4444-555555555555"``); пустая строка, если сервер
            вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                guid = await ips.life_cycle_step_guid(10)
                print(guid)

        Notes:
            operationId ``Metadata_GetLifeCycleStepGuid``; путь
            ``GET /core/api/metadata/lifeCycleSteps/{id}/guid``.
            Обратное преобразование — :meth:`life_cycle_step_id_by_guid`.
        """
        path = f"/core/api/metadata/lifeCycleSteps/{life_cycle_step_id}/guid"
        data = await self._request("get", path)
        return "" if data is None else str(data)
