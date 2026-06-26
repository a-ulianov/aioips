"""Метод удаления интегратора IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager


class BridgeRemoveIntegratorMixin(APIManager):
    """Реализует ``DELETE /core/api/Bridge/Integrators/RemoveIntegrator``.

    ``operationId``: ``Bridge_RemoveIntegrator``.
    """

    async def bridge_remove_integrator(
        self: "BridgeRemoveIntegratorMixin",
        *,
        integrator_guid: str | None = None,
        confirm: bool = False,
    ) -> None:
        """Удаляет интегратор IPS Bridge по его GUID (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; интеграторы — клиентские
        компоненты связи с внешними приложениями. Метод удаляет интегратор и его
        настройки по GUID. Список интеграторов — :meth:`bridge_get_integrators`,
        запись настроек — :meth:`bridge_add_or_update_settings_xml`.

        Обратимость: операция НЕОБРАТИМА — удалённый интегратор и его XML-настройки
        восстановить нельзя (заведите заново через
        :meth:`bridge_add_or_update_settings_xml`).

        Защита: удаление защищено ``confirm`` — без ``confirm=True`` поднимается
        :class:`ValueError` ещё ДО обращения к серверу (запрос не выполняется).

        Args:
            integrator_guid: GUID интегратора. ``None`` — параметр не передаётся.
            confirm: Подтверждение удаления. Без ``True`` запрос не выполняется.

        Returns:
            ``None``. Эндпоинт ничего не возвращает (void): успех = отсутствие
            ошибки.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера (404, если интегратор не найден).

        Example:
            async with IPSClient(config=config) as ips:
                await ips.bridge_remove_integrator(
                    integrator_guid="cad001c5-306c-11d8-b4e9-00304f19f545",
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_RemoveIntegrator``; путь
            ``DELETE /core/api/Bridge/Integrators/RemoveIntegrator``. Ключ query —
            ``integratorGuid``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_remove_integrator удаляет интегратор на сервере; передайте confirm=True",
            )
        params: dict[str, Any] = {}
        if integrator_guid is not None:
            params["integratorGuid"] = integrator_guid
        await self._request(
            "delete", "/core/api/Bridge/Integrators/RemoveIntegrator", params=params
        )
        return None
