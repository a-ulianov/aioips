"""Метод записи настроек просмотра/печати для типа объекта (config-мутация, confirm)."""

from typing import Any

from ...core import APIManager
from ...schemas.settings import ViewObjectTypeSettings


class SetViewPrintSettingsMixin(APIManager):
    """Реализует ``POST /core/api/settings/view/{objectTypeId}/setSettings``.

    operationId ``Settings_SetViewPrintSettings``.
    """

    async def set_view_print_settings(
        self: "SetViewPrintSettingsMixin",
        object_type_id: int,
        settings: ViewObjectTypeSettings | dict[str, Any],
        *,
        confirm: bool = False,
    ) -> None:
        """Записывает настройки внедрения данных при просмотре/печати типа объекта (``confirm``).

        Парная запись к чтению :meth:`view_print_settings`: задаёт, что добавляется в
        результат просмотра/печати документов данного ТИПА (подписи, контрольная сумма
        файла, набор внедряемых атрибутов). Это настройка уровня ТИПА объекта — влияет на
        все объекты типа, поэтому защищена ``confirm``: без ``confirm=True`` поднимается
        :class:`ValueError` ещё до обращения к серверу.

        Обратимость: прочитайте текущие настройки через :meth:`view_print_settings`,
        сохраните, измените нужное и запишите; для отката запишите сохранённый снимок
        обратно. Тристейт-флаги: ``None`` = «наследовать от вышестоящего типа».

        Args:
            object_type_id: Идентификатор ТИПА объекта (``objectTypeId``), а не
                конкретного объекта/версии. Подставляется в путь URL.
            settings: Настройки (:class:`ViewObjectTypeSettings`) или эквивалентный
                словарь (``ViewObjectTypeSettingsDto``). Для точного round-trip
                передавайте снимок, прочитанный :meth:`view_print_settings`.
            confirm: Подтверждение мутирующей операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                cur = await ips.view_print_settings(1742)        # бэкап
                await ips.set_view_print_settings(1742, cur, confirm=True)

        Notes:
            operationId ``Settings_SetViewPrintSettings``; путь
            ``POST /core/api/settings/view/{objectTypeId}/setSettings``; тело —
            ``ViewObjectTypeSettingsDto``. Парный read — :meth:`view_print_settings`.
        """
        if confirm is not True:
            raise ValueError(
                "set_view_print_settings мутирует настройки типа; передайте confirm=True"
            )
        if isinstance(settings, ViewObjectTypeSettings):
            payload: Any = settings.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = settings
        path = f"/core/api/settings/view/{object_type_id}/setSettings"
        await self._request("post", path, json=payload)
        return None
