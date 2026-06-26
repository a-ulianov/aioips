"""Метод отправки уведомления пользователю."""

from ...core import APIManager
from ...schemas.notify import NotificationMessage


class SendNotificationMixin(APIManager):
    """Реализует ``Notification_SendNotification`` (отправка уведомления пользователю)."""

    async def send_notification(
        self: "SendNotificationMixin",
        notification: NotificationMessage,
    ) -> None:
        """Отправляет уведомление пользователю IPS (МУТИРУЮЩАЯ операция).

        Доставляет одному пользователю сообщение с заголовком и текстом по выбранному
        каналу: внутренняя почта IPS, внешняя (e-mail) или оба (см.
        ``way_of_notification`` в теле; по умолчанию — оба канала).

        Когда применять: чтобы программно оповестить конкретного пользователя
        (например, по итогам обработки задачи/процесса). Адресат задаётся ``user_id`` —
        идентификатором учётной записи пользователя IPS, а не объекта.

        Args:
            notification: Сообщение :class:`NotificationMessage` — ``user_id``
                получателя, ``title``, ``message`` и способ доставки
                ``way_of_notification``.

        Returns:
            ``None``. Сервер не возвращает содержательного тела (void).

        Raises:
            IPSForbiddenError: При отсутствии прав на отправку уведомлений.
            IPSError: При ином ошибочном ответе сервера.

        Example:
            from aioips.schemas.notify import NotificationMessage, WayOfNotification

            async with IPSClient(config=config) as ips:
                await ips.send_notification(
                    NotificationMessage(
                        user_id=42,
                        title="Готово",
                        message="Документ согласован.",
                        way_of_notification=WayOfNotification.INTERNAL_MAIL,
                    ),
                )

        Notes:
            ``operationId``: ``Notification_SendNotification``; путь
            ``POST /core/api/notify/SendNotification``.
        """
        payload = notification.model_dump(mode="json", by_alias=True, exclude_none=True)
        await self._request("post", "/core/api/notify/SendNotification", json=payload)
        return None
