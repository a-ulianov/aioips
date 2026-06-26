"""Методы раздела уведомлений IPS Web API."""

from .send_notification import SendNotificationMixin


class NotifyAPI(SendNotificationMixin):
    """Объединяет методы раздела уведомлений.

    References:
        Эндпоинты ``/core/api/notify/*`` IPS Server Web API.
    """


__all__ = ["NotifyAPI"]
