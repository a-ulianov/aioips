"""Метод чтения прав доступа на коллекцию предметных областей."""

from ...core import APIManager
from ...schemas.security import Security


class SubjectAreasSecurityMixin(APIManager):
    """Реализует ``GET /core/api/security/subjectAreas``.

    operationId ``Security_GetSubjectAreaCollectionSecurity``.
    """

    async def subject_areas_security(self: "SubjectAreasSecurityMixin") -> Security:
        """Возвращает права доступа на КОЛЛЕКЦИЮ предметных областей (метаданное в целом).

        Read-only снимок безопасности на набор предметных областей: какие субъекты
        (пользователи, группы, роли) и какие действия (``ActionType``, например создание
        новой предметной области) могут выполнять над коллекцией предметных областей как
        метаданным. Метод только читает права, не изменяет их.

        Когда применять: проверить, кто вправе администрировать/создавать предметные
        области. Для прав на систему в целом используйте :meth:`system_security`, для прав
        на типы объектов — :meth:`object_types_security`.

        Returns:
            Снимок прав по схеме :class:`Security`: ``targets`` (субъекты), ``actions``
            (контролируемые действия), ``permissions`` (связки субъект × действие × вид
            доступа), ``durations``, ``conditions``. Пустые списки означают отсутствие
            соответствующих настроек.

        Raises:
            IPSError: При ошибочном ответе сервера.

        Example:
            async with IPSClient(config=config) as ips:
                sec = await ips.subject_areas_security()
                for perm in sec.permissions:
                    print(perm.target_id, perm.action_id, perm.access_type)

        Notes:
            operationId ``Security_GetSubjectAreaCollectionSecurity``; путь
            ``GET /core/api/security/subjectAreas`` (``SecurityDto``).
        """
        data = await self._request("get", "/core/api/security/subjectAreas")
        return Security.model_validate(data)
