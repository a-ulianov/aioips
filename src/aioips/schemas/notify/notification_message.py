"""Схема сообщения-уведомления пользователю.

References:
    ``POST /core/api/notify/SendNotification`` — тело ``NotificationMessageDto``.
"""

from enum import StrEnum

from pydantic import Field

from ..base import IPSModel


class WayOfNotification(StrEnum):
    """Способ доставки уведомления пользователю (``WayOfNotificationEnum``).

    Определяет каналы, по которым пользователь получит уведомление: внутренняя
    почта IPS, внешняя (e-mail) или оба канала.

    Семантика членов:
        INTERNAL_MAIL: ``internalMail`` — только внутренняя почта IPS.
        EXTERNAL_MAIL: ``externalMail`` — только внешняя почта (e-mail).
        INTERNAL_AND_EXTERNAL_MAIL: ``internalAndExternalMail`` — оба канала
            (значение по умолчанию).
    """

    INTERNAL_MAIL = "internalMail"
    EXTERNAL_MAIL = "externalMail"
    INTERNAL_AND_EXTERNAL_MAIL = "internalAndExternalMail"


class NotificationMessage(IPSModel):
    """Сообщение-уведомление, отправляемое пользователю IPS.

    Адресуется одному пользователю по его идентификатору и содержит заголовок,
    текст и способ доставки. ``user_id`` — это идентификатор пользователя IPS
    (учётной записи), а не объекта.

    Attributes:
        user_id: Идентификатор пользователя-получателя уведомления.
        title: Заголовок сообщения (необязателен).
        message: Текст сообщения (необязателен).
        way_of_notification: Способ доставки уведомления; по умолчанию —
            ``internalAndExternalMail`` (внутренняя и внешняя почта).
    """

    user_id: int = Field(description="Идентификатор пользователя-получателя уведомления")
    title: str | None = Field(default=None, description="Заголовок сообщения")
    message: str | None = Field(default=None, description="Текст сообщения")
    way_of_notification: WayOfNotification = Field(
        default=WayOfNotification.INTERNAL_AND_EXTERNAL_MAIL,
        description="Способ доставки уведомления",
    )
