"""Метод получения помощника идентификаторов текущего пользователя."""

from ...core import APIManager
from ...schemas.users import IdHelper


class IdHelperMixin(APIManager):
    """Mixin метода «помощник идентификаторов» текущего пользователя IPS Web API.

    Подмешивает в :class:`IPSClient` метод :meth:`id_helper` —
    обёртку над ``GET /core/api/currentUsers/GetIdHelper``: справочник системных
    идентификаторов (типов объектов, системных атрибутов, групп и ролей),
    вычисленных сервером для текущей сессии.

    References:
        Раздел ``/core/api/currentUsers/*``. Домен: разделу авторизации, объектной модели IPS.
    """

    async def id_helper(self: "IdHelperMixin") -> IdHelper:
        """Возвращает справочник системных идентификаторов IPS для текущей сессии.

        Назначение: получить вычисленные сервером id системных сущностей —
        системных атрибутов (``name_id`` «Наименование», ``designation_id``
        «Обозначение» и т.д.), типов объектов (``users_type_id``,
        ``groups_type_id``, ``roles_type_id`` и т.д.), предопределённых
        групп/ролей (``all_users_group_id``, ``admin_role_id``, ``sysdba_id``)
        и служебных констант. Этот «помощник» кэширует id/guid системных
        сущностей сессии на стороне сервера.

        Когда применять: чтобы не зашивать «магические» id системных сущностей в
        клиентском коде/MCP-инструментах, а получать их из API под текущего
        пользователя. Например, ``name_id``/``designation_id`` пригодны при
        чтении и записи системных атрибутов объектов, ``users_type_id`` — при
        выборках по типу «Пользователи». В отличие от :meth:`user_info`
        («кто я»), здесь — справочник идентификаторов окружения, а не данные
        самого пользователя.

        Предусловия: требуется активная авторизованная сессия — клиент должен
        иметь действующий access-токен (получается автоматически при первом
        запросе из логина/пароля конфигурации).

        Returns:
            :class:`IdHelper`. Все поля необязательны (сервер может вернуть не
            весь набор) и по умолчанию ``None``. Значения — системные
            идентификаторы соответствующих сущностей; интерпретировать их как
            ``objectID`` либо id версии нужно по контексту конкретной сущности
            (см. различие версия/объект в объектной модели IPS).

        Raises:
            IPSError: При ошибочном ответе сервера (например, ``401`` — сессия
                недействительна; см. маппинг в ``core/exceptions.py``).

        Example:
            >>> async with IPSClient(config=config) as ips:
            ...     ids = await ips.id_helper()
            ...     print(ids.name_id, ids.designation_id, ids.all_users_group_id)

        Notes:
            ``operationId``: ``CurrentUsers_GetIdHelper``; путь
            ``GET /core/api/currentUsers/GetIdHelper`` (ответ ``IDHelperDTO``).
            Связанные методы: :meth:`user_info`. Домен: разделу авторизации,
            объектной модели IPS.
        """
        data = await self._request("get", "/core/api/currentUsers/GetIdHelper")
        return IdHelper.model_validate(data)
