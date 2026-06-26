"""Метод создания действия запуска IPS Bridge (мутация)."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.launch_action_info import LaunchActionInfo
from ...schemas.bridge.launch_action_request import CreateLaunchActionDto


class BridgeCreateLaunchActionMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/CreateLaunchAction``.

    ``operationId``: ``Bridge_CreateLaunchAction``.
    """

    async def bridge_create_launch_action(
        self: "BridgeCreateLaunchActionMixin",
        body: CreateLaunchActionDto | dict[str, Any] | None = None,
        *,
        confirm: bool = False,
    ) -> LaunchActionInfo:
        """Создаёт новое действие запуска IPS Bridge (МУТАЦИЯ).

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод регистрирует новое действие (обработчик, XML-настройки, тип
        объекта, режим) и возвращает его сведения. Изменить — позже
        :meth:`bridge_update_launch_action`, удалить —
        :meth:`bridge_remove_launch_action`.

        Обратимость: операция ОБРАТИМА — созданное действие удаляется парным
        :meth:`bridge_remove_launch_action` (по полю ``action_id`` результата).

        Защита: создаёт сущность на сервере, поэтому защищена ``confirm`` — без
        ``confirm=True`` поднимается :class:`ValueError` ещё ДО обращения к
        серверу (запрос не выполняется).

        Args:
            body: Описание действия. Принимает :class:`CreateLaunchActionDto` или
                ``dict`` с ключами ``handlerId`` / ``settingsXml`` / ``objectTypeId``
                / ``userId`` / ``launchType``. ``None`` — пустое тело ``{}`` (но
                ``handlerId`` обязателен на сервере). Модель сериализуется
                ``by_alias`` + ``exclude_none``.
            confirm: Подтверждение операции. Без ``True`` запрос не выполняется.

        Returns:
            Созданное действие по схеме :class:`LaunchActionInfo` с полями
            ``action_id``, ``handler_id`` и ``display_name``.

        Raises:
            ValueError: Если ``confirm`` не равен ``True`` (защитный гейт).
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.launch_action_request import (
                CreateLaunchActionDto, LaunchType,
            )
            async with IPSClient(config=config) as ips:
                action = await ips.bridge_create_launch_action(
                    CreateLaunchActionDto(
                        handler_id="cad001c5-306c-11d8-b4e9-00304f19f545",
                        object_type_id=1, launch_type=LaunchType.EDIT,
                    ),
                    confirm=True,
                )

        Notes:
            ``operationId``: ``Bridge_CreateLaunchAction``; путь
            ``POST /core/api/Bridge/Launch/CreateLaunchAction``. Тело —
            ``CreateLaunchActionDto``.
        """
        if confirm is not True:
            raise ValueError(
                "bridge_create_launch_action создаёт действие на сервере; передайте confirm=True",
            )
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, CreateLaunchActionDto):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request(
            "post", "/core/api/Bridge/Launch/CreateLaunchAction", json=payload
        )
        return LaunchActionInfo.model_validate(data)
