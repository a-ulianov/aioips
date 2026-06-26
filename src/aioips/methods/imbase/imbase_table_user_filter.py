"""Метод получения пользовательского фильтра табличной части справочника IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseTableUserFilterMixin(APIManager):
    """Реализует ``GET .../table/{objectVersionId}/userFilter`` (``ImBase_GetTableUserFilter``)."""

    async def imbase_table_user_filter(
        self: "ImBaseTableUserFilterMixin",
        object_version_id: int,
    ) -> dict[str, Any]:
        """Возвращает пользовательский фильтр таблицы справочника IMBASE для версии объекта.

        Пользовательский фильтр — это сохранённые пользователем условия отбора строк
        табличной части справочника (значения колонок, операторы сравнения и т.п.),
        привязанные к ВЕРСИИ объекта-справочника.

        Когда применять: чтобы прочитать активный фильтр таблицы перед её показом либо
        воспроизвести отбор на стороне клиента. Данные таблицы — :meth:`imbase_table_data`,
        настройки отображения — :meth:`imbase_table_display_settings`. Предусловий нет
        (операция чтения).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта-справочника (F_ID / поле ``id``
                DTO, НЕ ``objectID`` объекта).

        Returns:
            Опаковая (нетипизированная) структура фильтра как ``dict[str, Any]`` по DTO
            ``TableUserFilterDto``. Структура крупная/неоднородная, детально не
            типизируется. Пустой ``dict`` — если сервер вернул не-объект (в т.ч. когда
            фильтр не задан).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                user_filter = await ips.imbase_table_user_filter(7)  # 7 = id ВЕРСИИ
                print(user_filter.get("conditions"))

        Notes:
            operationId ``ImBase_GetTableUserFilter``; путь
            ``GET /core/api/imbase/table/{objectVersionId}/userFilter``
            (``TableUserFilterDto``, без result-обёртки). Связанные методы:
            :meth:`imbase_table_data`, :meth:`imbase_table_display_settings`.
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/table/{object_version_id}/userFilter",
        )
        return data if isinstance(data, dict) else {}
