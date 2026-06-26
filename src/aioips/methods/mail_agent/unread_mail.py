"""Метод получения сведений о непрочитанной почте пользователя IPS."""

from ...core import APIManager
from ...schemas.mail_agent import UnreadMail


class UnreadMailMixin(APIManager):
    """Реализует метод ``GET /core/api/MailAgent/mailbox/unreadMail``.

    operationId ``MailAgent_GetUnrealMailInfo`` (в swagger опечатка ``Unreal``).
    """

    async def unread_mail(self: "UnreadMailMixin") -> UnreadMail:
        """Возвращает сводку по непрочитанным письмам почтового ящика пользователя.

        Отдаёт количество непрочитанных писем, сгруппированных по важности (высокая /
        обычная / низкая), и время последней проверки ящика. Данные относятся к ящику
        текущего авторизованного пользователя. Для настроек самого агента (интервал
        проверки и т.п.) используйте :meth:`mail_agent_settings`.

        Когда применять: для индикации непрочитанной почты (например, бейдж с числом
        новых писем) и оценки актуальности данных по ``last_check_time``. Вызов читающий
        и идемпотентный.

        Returns:
            Сводка по непрочитанной почте по схеме :class:`UnreadMail`: счётчики
            ``high_count`` / ``normal_count`` / ``low_count`` и ``last_check_time``
            (UTC) — время последней проверки ящика.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                mail = await ips.unread_mail()
                total = mail.high_count + mail.normal_count + mail.low_count
                print(total, mail.last_check_time)

        Notes:
            operationId ``MailAgent_GetUnrealMailInfo`` (опечатка ``Unreal`` сохранена как
            в swagger); путь ``GET /core/api/MailAgent/mailbox/unreadMail`` (объект
            ``UnreadMailDTO``).
        """
        data = await self._request("get", "/core/api/MailAgent/mailbox/unreadMail")
        return UnreadMail.model_validate(data)
