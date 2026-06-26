"""Метод получения настроек отображения табличной части справочника IMBASE."""

from typing import Any

from ...core import APIManager


class ImBaseTableDisplaySettingsMixin(APIManager):
    """Реализует ``GET .../displaySettings`` (``ImBase_GetTableDisplaySettings``)."""

    async def imbase_table_display_settings(
        self: "ImBaseTableDisplaySettingsMixin",
        object_version_id: int,
    ) -> dict[str, Any]:
        """Возвращает настройки отображения таблицы справочника IMBASE для версии объекта.

        Настройки отображения задают, как табличная часть показывается пользователю:
        видимость и порядок колонок, ширины, группировки, сортировки и прочие параметры
        представления, привязанные к ВЕРСИИ объекта-справочника.

        Когда применять: чтобы отрисовать таблицу справочника так, как настроено в IPS,
        либо прочитать конфигурацию представления. Сами данные таблицы —
        :meth:`imbase_table_data`, пользовательский фильтр — :meth:`imbase_table_user_filter`.
        Предусловий нет (операция чтения).

        Args:
            object_version_id: Идентификатор ВЕРСИИ объекта-справочника (F_ID / поле ``id``
                DTO, НЕ ``objectID`` объекта).

        Returns:
            Опаковая (нетипизированная) структура настроек как ``dict[str, Any]`` по DTO
            ``TableDisplaySettingsConfigurationDto``. Структура крупная/неоднородная,
            детально не типизируется. Пустой ``dict`` — если сервер вернул не-объект.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.imbase_table_display_settings(7)  # 7 = id ВЕРСИИ
                print(settings.get("columns"))

        Notes:
            operationId ``ImBase_GetTableDisplaySettings``; путь
            ``GET /core/api/imbase/table/{objectVersionId}/displaySettings``
            (``TableDisplaySettingsConfigurationDto``, без result-обёртки). Связанные
            методы: :meth:`imbase_table_data`, :meth:`imbase_table_user_filter`.
        """
        data = await self._request(
            "get",
            f"/core/api/imbase/table/{object_version_id}/displaySettings",
        )
        return data if isinstance(data, dict) else {}
