"""Метод получения настроек почтового агента IPS."""

from ...core import APIManager
from ...schemas.mail_agent import MailAgentSettings


class MailAgentSettingsMixin(APIManager):
    """Реализует метод ``GET /core/api/MailAgent/settings`` (``MailAgent_GetSettings``)."""

    async def mail_agent_settings(self: "MailAgentSettingsMixin") -> MailAgentSettings:
        """Возвращает текущие настройки почтового агента IPS.

        Отдаёт конфигурацию работы почтового агента сервера — в частности параметры
        периодической проверки непрочитанной почты (интервал опроса). Это настройки
        самого агента, а не содержимое почтового ящика; для сводки по непрочитанным
        письмам используйте :meth:`unread_mail`.

        Когда применять: чтобы показать/проверить текущую конфигурацию почтового агента
        (например, как часто опрашивается ящик). Вызов читающий и идемпотентный.

        Returns:
            Настройки почтового агента по схеме :class:`MailAgentSettings`. Поле
            ``unread_mail`` содержит параметры проверки непрочитанной почты
            (``check_interval`` в минутах).

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                settings = await ips.mail_agent_settings()
                print(settings.unread_mail.check_interval)

        Notes:
            operationId ``MailAgent_GetSettings``; путь
            ``GET /core/api/MailAgent/settings`` (объект ``MailAgentSettingsDTO``).
        """
        data = await self._request("get", "/core/api/MailAgent/settings")
        return MailAgentSettings.model_validate(data)
