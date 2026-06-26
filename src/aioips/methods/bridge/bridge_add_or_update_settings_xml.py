"""Метод записи XML-настроек интегратора IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeAddOrUpdateSettingsXmlMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Integrators/AddOrUpdateSettingsXml``.

    ``operationId``: ``Bridge_AddOrUpdateSettingsXml``.
    """

    async def bridge_add_or_update_settings_xml(
        self: "BridgeAddOrUpdateSettingsXmlMixin",
        *,
        integrator_guid: str | None = None,
        xml_data: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Создаёт или обновляет XML-настройки интегратора IPS Bridge (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; интеграторы — клиентские
        компоненты связи с внешними приложениями, их настройки хранятся в XML.
        Метод записывает (создаёт или перезаписывает) настройки интегратора по
        его GUID. Прочитать текущие — :meth:`bridge_settings_xml`, удалить
        интегратор — :meth:`bridge_remove_integrator`.

        Обратимость: операция ОБРАТИМА по схеме write-same-back — сохраните
        прежний XML через :meth:`bridge_settings_xml` и для отката запишите его
        обратно тем же методом.

        Защита: меняет настройки на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            integrator_guid: GUID интегратора. ``None`` — параметр не передаётся.
            xml_data: XML-настройки (передаются как query-параметр ``xmlData``).
                ``None`` — параметр не передаётся.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_add_or_update_settings_xml(
                    integrator_guid="cad001c5-306c-11d8-b4e9-00304f19f545",
                    xml_data="<settings/>",
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_AddOrUpdateSettingsXml``; путь
            ``POST /core/api/Bridge/Integrators/AddOrUpdateSettingsXml``. Ключи
            query — ``integratorGuid``, ``xmlData``. Тело не передаётся (``{}``
            против 415).
        """
        if confirm is not True:
            raise ValueError(
                "bridge_add_or_update_settings_xml меняет настройки интегратора; "
                "передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if integrator_guid is not None:
            params["integratorGuid"] = integrator_guid
        if xml_data is not None:
            params["xmlData"] = xml_data
        await self._request(
            "post",
            "/core/api/Bridge/Integrators/AddOrUpdateSettingsXml",
            params=params,
            json={},
        )
        return None
