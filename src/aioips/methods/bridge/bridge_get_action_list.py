"""Метод выборки списка действий запуска IPS Bridge по фильтру."""

from typing import Any

from ...core import APIManager
from ...schemas.bridge.launch_action_info import LaunchActionInfo
from ...schemas.bridge.launch_action_request import LaunchActionDto


class BridgeGetActionListMixin(APIManager):
    """Реализует ``POST /core/api/Bridge/Launch/GetActionList``.

    ``operationId``: ``Bridge_GetActionList``.
    """

    async def bridge_get_action_list(
        self: "BridgeGetActionListMixin",
        body: LaunchActionDto | dict[str, Any] | None = None,
    ) -> list[LaunchActionInfo]:
        """Возвращает список действий запуска IPS Bridge по заданному фильтру.

        IPS Bridge — серверный помощник десктоп-клиента; действие запуска
        (launch action) описывает операцию над объектом на стороне клиента.
        Метод отдаёт действия, подходящие под фильтр (тип объекта, пользователь,
        режим запуска). Это операция ЧТЕНИЯ — подтверждения не требует. Для
        полного списка с типами используйте :meth:`bridge_get_full_action_list`,
        для действий по умолчанию — :meth:`bridge_get_default_actions`.
        Предусловий нет.

        Args:
            body: Фильтр выборки. Принимает :class:`LaunchActionDto` или ``dict``
                с ключами ``objectTypeId`` / ``userId`` / ``launchType``.
                ``None`` (по умолчанию) — отправляется пустое тело ``{}``
                (без фильтра). Модель сериализуется ``by_alias`` + ``exclude_none``.

        Returns:
            Список :class:`LaunchActionInfo`. Пустой список ``[]``, если действий
            нет или сервер вернул ``null``.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            from aioips.schemas.bridge.launch_action_request import (
                LaunchActionDto, LaunchType,
            )
            async with IPSClient(config=config) as ips:
                actions = await ips.bridge_get_action_list(
                    LaunchActionDto(object_type_id=1, launch_type=LaunchType.VIEW),
                )

        Notes:
            ``operationId``: ``Bridge_GetActionList``; путь
            ``POST /core/api/Bridge/Launch/GetActionList``. Тело —
            ``LaunchActionDto``.
        """
        if body is None:
            payload: dict[str, Any] = {}
        elif isinstance(body, LaunchActionDto):
            payload = body.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            payload = body
        data = await self._request("post", "/core/api/Bridge/Launch/GetActionList", json=payload)
        items = data if isinstance(data, list) else []
        return [LaunchActionInfo.model_validate(item) for item in items]
