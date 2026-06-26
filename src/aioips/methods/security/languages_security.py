"""Метод чтения прав доступа на коллекцию языков."""

from ...core import APIManager
from ...schemas.security import Security


class LanguagesSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/languages``.

    operationId ``Security_GetLanguageCollectionSecurity``.
    """

    async def languages_security(self: "LanguagesSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ языков (метаданное в целом).

        Read-only снимок безопасности на набор языков системы: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например добавление
        нового языка локализации) могут выполнять над коллекцией языков как метаданным.
        Метод только читает права, не изменяет их.

        Когда применять: проверить, кто вправе администрировать языки (мультиязычные
        атрибуты/локализацию). Для прав на систему в целом используйте
        :meth:`system_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.languages_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetLanguageCollectionSecurity``; путь
            ``GET /core/api/security/languages`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/languages")
        return Security.model_validate(data)
